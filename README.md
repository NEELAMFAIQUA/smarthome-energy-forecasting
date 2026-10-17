# Smart Home Energy Forecast

An original, offline energy-use teaching demo. It generates deterministic
illustrative daily usage and projects a short horizon with a moving-average
baseline—no model downloads, meter data, or API keys.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Synthetic results are not household measurements, utility forecasts, or billing
estimates. Run tests with `python -m unittest discover -s tests -v`.
