# Shopper Intent API

[![tests](https://github.com/Alikhalili56/shopper-intent-api/actions/workflows/tests.yml/badge.svg)](https://github.com/Alikhalili56/shopper-intent-api/actions/workflows/tests.yml)

This project predicts whether an online shopping session ends in a purchase, based on browsing behaviour recorded during the session, and serves the model through a small API. The score is used for one decision: show a discount offer to hesitant visitors, but not to visitors who are likely to buy anyway. The main finding is that most of the predictive power comes from one feature, `PageValues`, which may leak information about the outcome.

## Data

[Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468) from the UCI Machine Learning Repository (Sakar and Kastro, 2018): 12,330 browsing sessions from one online retailer over one year. 17 features, target `Revenue` (purchase or not). About 15.6% of sessions end in a purchase. Licence: CC BY 4.0. The data is downloaded by `scripts/download_data.py` and is not stored in this repo. 125 duplicate rows were removed before modelling.

## Method

- **Models:** a dummy baseline (always "no purchase"), logistic regression, and gradient boosting (scikit-learn `HistGradientBoostingClassifier`). All use the same preprocessing (scaling for numeric columns, one-hot encoding for categorical ones) inside one pipeline.
- **Metric:** PR-AUC (average precision). Only 15.6% of sessions are buyers, so accuracy is misleading: the dummy model reaches 84% accuracy while finding no buyers at all. PR-AUC measures how well the model ranks buyers above non-buyers. The no-skill level is 0.156.
- **Protocol:** stratified 80/20 train/test split. Model comparison with 5-fold stratified cross-validation on the training set only. The decision threshold was chosen on out-of-fold training predictions and committed before the test set was opened. The test set was used once.
- **Tuning:** a small grid search on gradient boosting gave 0.757 against 0.742 for the defaults, a gain within the fold-to-fold spread, so the defaults were kept.

## Results

| Model | CV PR-AUC (mean ± std) | Test PR-AUC |
|---|---|---|
| Dummy | 0.156 ± 0.000 | |
| Logistic regression | 0.636 ± 0.022 | |
| Gradient boosting | 0.742 ± 0.022 | 0.741 |
| Gradient boosting without `PageValues` | 0.365 ± 0.016 | 0.370 |

Test scores match the cross-validation estimates. Removing `PageValues` cuts PR-AUC by about half. This shows a strong dependence on that feature, which is consistent with leakage but does not prove it.

**Decision threshold.** The threshold is the lowest score where precision on "buyer" reaches 0.8 on training predictions: **0.684**. On the test set this gives precision 0.790 and recall 0.463 (177 buyers correctly flagged, 47 non-buyers wrongly flagged, 205 buyers missed). Without `PageValues`, a precision of 0.8 is only reached at a recall of 0.002, so that model is not usable for this rule.

## Use case

- Score at or above 0.684: likely buyer, no offer.
- Score below 0.684: show the offer.

Precision comes first because wrongly withholding an offer from a hesitant visitor can cost a whole sale, while an unneeded offer to a buyer only costs some margin.

## How to run

**Locally** (Python 3.14):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn src.api:app --reload
```
Then open http://127.0.0.1:8000/docs.

**With Docker:**
```bash
docker build -t shopper-intent-api .
docker run -p 8000:8000 shopper-intent-api
```

**Tests:**
```bash
python -m pytest
```
The same tests run on every push with GitHub Actions.

## API

- `GET /health` returns `{"message": "ok"}`.
- `POST /predict` takes one session with all 17 features and returns a score and the decision. Invalid input (wrong type, out of range, unknown category) returns a 422 error.

Example response:
```json
{"score": 0.002, "likely_buyer": false, "show_offer": true}
```

Months use three-letter names (`Jan` to `Dec`). The full input schema is shown on the `/docs` page.

## Limitations

- `PageValues` is computed by Google Analytics from completed purchases. If it includes the session's own outcome, the scores are inflated, and in live use the value may not be available during a session.
- The score ranks sessions; it is not a calibrated probability.
- The model predicts who buys, not who changes their mind because of an offer. Measuring the effect of an offer would need an A/B test.
- January and April do not appear in the training data; for these months the model scores without month information.
- Input validation checks each field on its own, not whether fields make sense together.

## Status

v1.0: model, API, tests, CI and Docker image. Possible next steps: a training script that runs in CI, and storing sessions and predictions in PostgreSQL.