# Shopper Intent API

[![tests](https://github.com/Alikhalili56/shopper-intent-api/actions/workflows/tests.yml/badge.svg)](https://github.com/Alikhalili56/shopper-intent-api/actions/workflows/tests.yml)

This project predicts whether an online shopping session ends in a purchase or not, using 12k sessions from a UCI dataset. The score decides whether to show a discount offer: hesitant visitors get it, likely buyers don't, because they would buy anyway. A gradient boosting model reaches a test PR-AUC of 0.741, compared with 0.156 for a dummy baseline that always predicts "no purchase". Most of this performance comes from one feature, `PageValues`, a Google Analytics metric calculated from purchases made on the site, which may include the session's own outcome. Without it, test PR-AUC drops from 0.741 to 0.370, so both results are reported.

## Data
[Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468) (UCI, CC BY 4.0): 12,330 sessions from one retailer over one year, 17 features, target `Revenue`. 15.6% of sessions end in a purchase. 125 duplicate rows removed. Fetched with `scripts/download_data.py`; raw data is not committed.

## Method
- **Models:** dummy (no-skill baseline), logistic regression (linear baseline), and `HistGradientBoostingClassifier` (non-linear). All share one scikit-learn pipeline: scaling for numeric features, one-hot encoding for categorical ones.
- **Metric:** PR-AUC (average precision). With 15.6% buyers, accuracy is misleading: the dummy reaches 84% while finding no buyers. PR-AUC measures how well buyers are ranked above non-buyers, independent of any threshold. No-skill level: 0.156.
- **Validation:** stratified 80/20 train/test split. Models compared with stratified 5-fold CV on the training set. The decision threshold was fixed on out-of-fold training predictions before the test set was used, once.
- **Tuning:** a small grid search gave 0.757 vs 0.742 for default settings, within the fold-to-fold spread, so defaults were kept.

## Results
| Model | CV PR-AUC | Test PR-AUC |
|---|---|---|
| Dummy | 0.156 ± 0.000 | |
| Logistic regression | 0.636 ± 0.022 | |
| Gradient boosting | 0.742 ± 0.022 | 0.741 |
| Gradient boosting, no `PageValues` | 0.365 ± 0.016 | 0.370 |

Test scores match CV. Dropping `PageValues` halves PR-AUC: a strong dependence, consistent with leakage but not proof of it.

**Decision threshold: 0.684**, the lowest score with precision ≥ 0.8 on out-of-fold training predictions. On the test set: precision 0.790, recall 0.463. Without `PageValues`, precision 0.8 is reached only at recall 0.002, so that model is not usable for this rule.

## Use case
Score ≥ 0.684: likely buyer, no offer. Below: show the offer. Precision comes first because wrongly withholding an offer can lose a sale, while an unneeded offer only costs margin.

## How to run
```bash
pip install -r requirements-dev.txt
uvicorn src.api:app --reload          # http://127.0.0.1:8000/docs
python -m pytest
```
Docker:
```bash
docker build -t shopper-intent-api .
docker run -p 8000:8000 shopper-intent-api
```

## API
- `GET /health`
- `POST /predict`: one session (17 fields, validated; invalid input returns 422) →
  `{"score": 0.002, "likely_buyer": false, "show_offer": true}`

Months use three-letter names (`Jan` … `Dec`). Full schema on `/docs`.

## Limitations
- `PageValues` may include the session's own purchase; in live use it may not be available during a session.
- Scores rank sessions; they are not calibrated probabilities.
- The model predicts who buys, not who responds to an offer; that needs an A/B test.
- January and April are absent from training; those months are scored without month information.
- Validation checks each field alone, not consistency between fields.

## Status
v1.0: model, API, tests, CI, Docker. Next: training script in CI, PostgreSQL for sessions and predictions.
