import streamlit as st

from forecast import forecast, sample_daily_usage

st.set_page_config(page_title="Home Energy Forecast", page_icon="⚡")
st.title("Home Energy Forecast")
st.caption("Explore a simple forecast using locally generated sample readings.")
days = st.slider("Sample history (days)", 30, 180, 90)
horizon = st.slider("Forecast horizon (days)", 1, 14, 7)
window = st.slider("Moving-average window", 2, 21, 7)

history = sample_daily_usage(days)
projected = forecast(history, horizon, window)
st.subheader("Daily usage (illustrative kWh)")
st.line_chart(
    {
        "Sample history": history + [None] * len(projected),
        "Forecast": [None] * len(history) + projected,
    }
)
st.metric("Average forecast", f"{sum(projected) / len(projected):.1f} kWh/day")
st.info(
    "This is a basic moving-average baseline on synthetic data, not a smart-meter "
    "prediction. Real usage depends on weather, occupancy, tariffs, and appliances."
)
