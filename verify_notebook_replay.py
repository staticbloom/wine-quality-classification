"""Execute the closed-development submission report in a fresh guarded kernel.

Run from any directory with this project's Python:
    python verify_notebook_replay.py --cwd notebook --write
    python verify_notebook_replay.py --cwd root

This is an execution harness only; project/report logic stays in the notebook.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from importlib.metadata import version
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from time import perf_counter

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT/'notebook/Wine-Quality-Classification.ipynb'
OUTPUT = ROOT/'tables/submission'

GUARDS = r'''
import importlib.abc
import sys
from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

class RejectRetiredPackage(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'src','wine_quality'}:
            raise AssertionError('Retired project-package import attempted: '+fullname)
sys.meta_path.insert(0,RejectRetiredPackage())
_guard_counts = dict(fit_attempts=0,predict_rows=0,probability_rows=0,model_loads=0,raw_data_parses=0)

def no_fit(*args,**kwargs):
    _guard_counts['fit_attempts']+=1
    raise AssertionError('Model development is closed: fitting/searching is forbidden')
for cls in (Pipeline,StandardScaler,LinearDiscriminantAnalysis,GridSearchCV,RandomizedSearchCV):
    cls.fit=no_fit
_raw_csv = pd.read_csv

def report_csv(path,*args,**kwargs):
    location=Path(path).resolve()
    if _audit_root/'tables' not in location.parents:
        _guard_counts['raw_data_parses']+=1
        raise AssertionError('Only saved result tables may be parsed')
    return _raw_csv(path,*args,**kwargs)
pd.read_csv=report_csv

_expected_example=pd.DataFrame({
 'fixed acidity':[7.6,9.1], 'volatile acidity':[.51,.34], 'citric acid':[.18,.43],
 'residual sugar':[2.3,2.1], 'chlorides':[.076,.080], 'free sulfur dioxide':[17.,13.],
 'total sulfur dioxide':[48.,39.], 'density':[.9964,.9971], 'pH':[3.30,3.19],
 'sulphates':[.67,.74], 'alcohol':[10.6,11.4]},index=pd.Index(['illustrative_A','illustrative_B'],name='Wine'))
def allowed_examples(frame):
    assert isinstance(frame,pd.DataFrame)
    pd.testing.assert_frame_equal(frame,_expected_example,check_exact=True)
_original_predict=Pipeline.predict
_original_probability=Pipeline.predict_proba
_original_load=joblib.load

def report_predict(self,frame,*args,**kwargs):
    allowed_examples(frame);_guard_counts['predict_rows']+=len(frame)
    return _original_predict(self,frame,*args,**kwargs)
def report_probability(self,frame,*args,**kwargs):
    allowed_examples(frame);_guard_counts['probability_rows']+=len(frame)
    return _original_probability(self,frame,*args,**kwargs)
def report_load(path,*args,**kwargs):
    assert Path(path).resolve()==_audit_root/'models/final/wine_quality_classifier_v2.joblib'
    _guard_counts['model_loads']+=1
    return _original_load(path,*args,**kwargs)
Pipeline.predict=report_predict;Pipeline.predict_proba=report_probability;joblib.load=report_load

def guard_file_access(event,args):
    if event not in {'open','os.listdir','os.scandir'} or not args or not isinstance(args[0],(str,bytes)):
        return
    path=Path(args[0].decode() if isinstance(args[0],bytes) else args[0]).resolve()
    retired=_audit_root/'src'
    if path==retired or retired in path.parents:
        raise AssertionError('Retired source-directory access attempted')
    if path==_audit_root/'data/wine-quality-red.csv':
        frame=sys._getframe(1)
        while frame:
            if frame.f_code.co_name=='digest':return  # Integrity hash only, no parsed wine rows.
            frame=frame.f_back
        raise AssertionError('Raw wine data may only be hashed for integrity')
sys.addaudithook(guard_file_access)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    files={}
    for directory in ('data','models','tables','visuals'):
        for path in (ROOT/directory).rglob('*'):
            if not path.is_file() or path.name in {'.DS_Store','.gitkeep'}:
                continue
            relative=path.relative_to(ROOT)
            if relative.parts[:2] in {('tables','submission'),('visuals','submission')} or relative==Path('tables/final_leaderboard.csv'):
                continue
            files[str(relative)]=sha(path)
    archive=ROOT/'notebook/archive/Wine-Quality-Development-2026-10-16.ipynb'
    if archive.is_file():
        files[str(archive.relative_to(ROOT))] = sha(archive)
    return files


def verify_frozen_evidence():
    """Check the recorded release and serialization versions before model loading."""
    lock = json.loads((ROOT / "models/final/version2_freeze_lock.json").read_text())
    for relative, expected_hash in lock["files"].items():
        if sha(ROOT / relative) != expected_hash:
            raise ValueError(f"Frozen evidence checksum mismatch: {relative}")
    metadata = json.loads((ROOT / "models/final/wine_quality_classifier_v2.metadata.json").read_text())
    for package, expected_version in metadata["environment"]["versions"].items():
        if version(package) != expected_version:
            raise ValueError(f"{package}: expected {expected_version}, found {version(package)}")


def refresh_generated_manifest(execution_path):
    """Record the verified report sources and execution; retain historical entries."""
    path = OUTPUT / "submission_manifest.json"
    manifest = json.loads(path.read_text())
    verified = [NOTEBOOK, execution_path, Path(__file__).resolve(),
                ROOT / "README.md", ROOT / "requirements.txt", ROOT / "predict.py",
                ROOT / "train.py", ROOT / "data/example_wines.csv"]
    for artifact in verified:
        manifest["files"][str(artifact.relative_to(ROOT))] = sha(artifact)
    path.write_text(json.dumps(manifest, indent=2) + "\n")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cwd',choices=('root','notebook'),default='notebook')
    parser.add_argument('--write',action='store_true',help='Save successful execution outputs into the main notebook.')
    args=parser.parse_args()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    verify_frozen_evidence()
    before = snapshot()
    book = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(book)
    for cell in book.cells:
        if cell.cell_type=='code':cell.outputs=[];cell.execution_count=None
    work=deepcopy(book)
    # Keep harness imports out of the notebook namespace: otherwise a missing
    # notebook import could accidentally pass this clean-kernel check.
    guard_setup = f"_execution_guard_namespace = {{'_audit_root': __import__('pathlib').Path({str(ROOT)!r})}}\n"
    guard_setup += f'exec({GUARDS!r}, _execution_guard_namespace)'
    work.cells.insert(0,nbformat.v4.new_code_cell(guard_setup,id='execution-guards'))
    work.cells.append(nbformat.v4.new_code_cell('''assert _execution_guard_namespace['_guard_counts'] == {'fit_attempts':0,'predict_rows':2,'probability_rows':2,'model_loads':1,'raw_data_parses':0}
assert len(selected_oof) == 10870
assert selected_oof['source_row_index'].nunique() == 1087
assert example_predictions.shape == (2, 7)
np.testing.assert_allclose(per_class['Mean F1'].mean(), selected_result['Macro F1'], rtol=0, atol=1e-12)
np.testing.assert_allclose(pooled_macro_f1, per_class['Pooled OOF F1'].mean(), rtol=0, atol=1e-12)
assert not any(n.split('.')[0] in {'src','wine_quality'} for n in _execution_guard_namespace['sys'].modules)
print('GUARDED_EXECUTION='+json.dumps(_execution_guard_namespace['_guard_counts']))
''',id='execution-assertions'))
    started=perf_counter();cwd=ROOT if args.cwd=='root' else ROOT/'notebook'
    with tempfile.TemporaryDirectory(prefix='wine-submission-kernel-') as folder:
        temporary=Path(folder);environment=dict(os.environ,MPLBACKEND='Agg',PYTHONHASHSEED='42')
        for key in ('IPYTHONDIR','JUPYTER_CONFIG_DIR','JUPYTER_RUNTIME_DIR','MPLCONFIGDIR'):
            directory=temporary/key.lower();directory.mkdir();environment[key]=str(directory)
        kernel='wine-submission';spec=temporary/'kernels'/kernel;spec.mkdir(parents=True)
        (spec/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
            'display_name':'Wine submission verification','language':'python'}))
        client=NotebookClient(work,timeout=300,kernel_name=kernel,resources={'metadata':{'path':str(cwd)}})
        client.create_kernel_manager();client.km.kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(temporary/'kernels')])
        try:client.execute(env=environment)
        except Exception:
            nbformat.write(work,Path(tempfile.gettempdir())/'wine-submission-failed.ipynb')
            raise
    assert before==snapshot(),'Immutable study/model evidence changed during report execution'
    output=''.join(o.get('text','') for o in work.cells[-1].outputs)
    guard_record=json.loads(next(line.split('=',1)[1] for line in output.splitlines() if line.startswith('GUARDED_EXECUTION=')))
    book.cells=[c for c in work.cells if c.id not in {'execution-guards','execution-assertions'}]
    for count,cell in enumerate((c for c in book.cells if c.cell_type=='code'),1):
        cell.execution_count=count
        for out in cell.outputs:
            if out.output_type=='execute_result':out.execution_count=count
            assert out.output_type!='error'
    nbformat.validate(book)
    check=dict(status='READY',completed_utc=datetime.now(timezone.utc).isoformat(),fresh_kernel=True,
        sequential=True,working_directory=args.cwd,python=platform_version(),
        code_cells=sum(c.cell_type=='code' for c in book.cells),
        embedded_figures=sum('image/png' in o.get('data',{}) for c in book.cells for o in c.get('outputs',[])),
        guards=guard_record,retired_package_and_directory_blocked=True,all_frozen_evidence_unchanged=len(before),
        clean_dependency_download_tested=False,wall_seconds=perf_counter()-started,
        historical_archive_present=(ROOT / 'notebook/archive/Wine-Quality-Development-2026-10-16.ipynb').is_file(),
        no_new_model_tuning=True,notebook_source_sha256=hashlib.sha256('\n'.join(c.source for c in book.cells).encode()).hexdigest())
    assert check['embedded_figures']==6, 'All six report figures must be embedded'
    if args.write:
        book.metadata['submission_execution']=check
        nbformat.write(book,NOTEBOOK)
    execution_path = OUTPUT/f'execution_{args.cwd}.json'
    execution_path.write_text(json.dumps(check,indent=2)+'\n')
    refresh_generated_manifest(execution_path)
    print(json.dumps(check,indent=2))


def platform_version():
    return sys.version.split()[0]


if __name__=='__main__':main()
