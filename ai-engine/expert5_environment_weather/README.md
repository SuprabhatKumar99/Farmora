# STEP 12 — Expert 5: Environment & Weather

Additive implementation preserving the established expert structure.

## Structure
`app/experts/expert5_environment_weather/{api,schemas,services,preprocessing,inference,postprocessing,models,storage}`

Dataset: `data/crop_health_dataset/12_expert5_environment_weather/`
Models: `models/expert5_environment_weather/{production,staging,archived}/`

## Responsibility
Environment/weather evidence only. No invented disease thresholds, causal claims, treatment, or final decisions.

## Input
CSV, Parquet, or JSON with a valid `timestamp` column. The example schema uses temperature, humidity, rainfall, wind, pressure and soil moisture fields; actual fields must follow the real dataset/model contract.

## Supplied model testing
No trained model is fabricated. For a TorchScript model:
```bash
python scripts/test_expert5.py models/expert5_environment_weather/production/model.pt path/to/environment.csv
```
The concrete adapter must match the supplied model's feature order, units, missing-value handling, window length, normalization, forecast horizon, target and output format. These are intentionally not guessed.

## Model candidates
Tabular: Gradient Boosting, Random Forest, XGBoost, LightGBM. Time series: LSTM, GRU, TCN, Transformer-based time-series models. Choose using the actual dataset and deployment task; for temporal data use chronological validation to avoid leakage.

## Metrics
Classification: precision, recall, F1. Regression/forecasting: MAE, RMSE, and R² where applicable. Also evaluate latency and memory.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
- `POST /api/v1/experts/expert5/environment-weather/analyze`
- `GET /api/v1/experts/expert5/environment-weather/model`
- `GET /health`
- `GET /ready`

Expert 5 output is structured evidence for later fusion with Experts 1–4 and 6–7, followed by Expert 8.
