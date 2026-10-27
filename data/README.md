# Data: red wine quality

The source dataset is not included in this repository. This directory is retained for documentation, directory placeholders, and explicitly identified synthetic examples or reproducibility metadata. Raw data and processed source records remain local.

The source is the red-wine file in [UCI Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality), attributed to Cortez, Cerdeira, Almeida, Matos and Reis (2009), [DOI 10.24432/C56S3T](https://doi.org/10.24432/C56S3T). UCI lists CC BY 4.0. The source and derived results retain this attribution; no project-code license is implied.

Download the red component `winequality-red.csv` from UCI. The original UCI file uses semicolons; the local `data/wine-quality-red.csv` uses commas. To match the local schema, parse with `sep=';'` and export `to_csv(..., index=False)` under the local filename. Preserve all 1,599 records and column names; do not deduplicate before reproducing the historical source-row split. Eleven physicochemical features precede integer `quality` labels 3–8. Verify content against `holdout_lock.json` and the recorded provenance; a format conversion need not produce the historical byte hash.

The source CSV is excluded from Git. `example_wines.csv` contains two handwritten unlabeled examples and is tracked. `split_manifest.json` and `holdout_lock.json` retain historical split/hash evidence, not raw measurements. Access journals remain local. Source-feature extracts in tables are also excluded; OOF label/prediction records remain attributed evaluation evidence, not new independent observations.

Inference and the active report do not require the raw CSV. The report uses retained saved tables, including repeated OOF predictions. The complete historical development archive is missing; duplicate executed snapshots and a 53.9 MiB historical trace remain local. Replaying the report does not reconstruct the original nested search. New `train.py` runs require newly supplied comma-delimited labeled data and use a separate fixed-recipe split.
