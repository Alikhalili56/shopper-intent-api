# Shopper Intent API

This project predicts whether an online shopping session ends in a purchase, based on browsing behaviour recorded during the session. It also measures how much performance depends on `PageValues`, an analytics feature that may leak information about the outcome.

## Data

[Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468) from the UCI Machine Learning Repository: 12,330 browsing sessions from one online retailer over one year, each from a different user. About 15% of sessions end in a purchase. Licence: CC BY 4.0. The data is downloaded by a script and is not stored in this repo.

## Status

Work in progress. Planned: a scikit-learn pipeline compared against simple baselines, served through a FastAPI endpoint, with unit tests, a Docker image and a GitHub Actions CI workflow.

## Limitations

The model finds correlations in browsing behaviour, not causes or intent. It scores completed sessions, not live visits, because some features are only known once a session ends.