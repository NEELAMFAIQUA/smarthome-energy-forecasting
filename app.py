import streamlit as st
import pandas as pd

from forecast import forecast, lstm_forecast, sample_daily_usage

st.set_page_config(page_title="Home Energy Forecast", page_icon="⚡")
st.title("Home Energy Forecast")
st.caption("Forecast energy use from a CSV or locally generated sample.")
uploaded = st.file_uploader("Upload CSV with one numeric daily-usage column", type=["csv"])
if uploaded:
    try:
        frame = pd.read_csv(uploaded)
    except (UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
        st.error(f"Unable to read CSV: {error}")
        st.stop()
    numeric_columns = list(frame.select_dtypes(include="number").columns)
    if not numeric_columns:
        st.error("CSV needs at least one numeric usage column.")
        st.stop()
    usage_column = st.selectbox("Daily usage column", numeric_columns)
    history = frame[usage_column].dropna().astype(float).tolist()
    unit = "CSV units"
else:
    days = st.slider("Sample history (days)", 30, 180, 90)
    history = sample_daily_usage(days)
    unit = "illustrative kWh"

horizon = st.slider("Forecast horizon (days)", 1, 14, 7)
method = st.selectbox("Forecast model", ["LSTM neural network", "Moving-average baseline"])
if len(history) < 20:
    st.error("At least 20 daily readings are needed for forecasting.")
    st.stop()

if method == "LSTM neural network":
    epochs = st.slider("Training epochs", 5, 40, 15)
    try:
        projected = lstm_forecast(history, horizon=horizon, lookback=min(14, len(history) // 3), epochs=epochs)
    except ImportError:
        st.error("Install dependencies from requirements.txt to enable LSTM forecasting.")
        st.stop()
else:
    window = st.slider("Moving-average window", 2, min(21, len(history)), min(7, len(history)))
    projected = forecast(history, horizon, window)

st.subheader(f"Daily usage ({unit})")
st.line_chart(
    {
        "Sample history": history + [None] * len(projected),
        "Forecast": [None] * len(history) + projected,
    }
)
st.metric("Average forecast", f"{sum(projected) / len(projected):.1f} kWh/day")
st.info(
    "Forecasts are experimental and depend on the uploaded series. LSTM needs "
    "enough history and is not a utility billing or smart-meter guarantee. "
    "Sample mode uses synthetic readings."
)
