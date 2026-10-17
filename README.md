# Smart Home Energy Forecast

An energy-use forecasting teaching demo. Use deterministic illustrative daily
usage or upload a CSV with numeric daily readings. Compare an LSTM forecaster
with a moving-average baseline.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Synthetic results are not household measurements, utility forecasts, or billing
estimates. The LSTM trains on the supplied series; no remote service is used.
On Windows, the requirements install the moving-average baseline; use Linux or
WSL2 to install TensorFlow and enable LSTM forecasting. Run tests with
`python -m unittest discover -s tests -v`.
