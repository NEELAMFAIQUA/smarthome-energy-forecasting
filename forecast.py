"""Deterministic sample data and a transparent moving-average baseline."""

import math


def sample_daily_usage(days=90):
    if days < 1:
        raise ValueError("days must be positive")
    return [
        round(
            12.0 + 2.4 * math.sin(2 * math.pi * day / 7)
            + 1.2 * math.sin(2 * math.pi * day / 30)
            + 0.02 * day,
            2,
        )
        for day in range(days)
    ]


def forecast(values, horizon=7, window=7):
    if not values or horizon < 1 or window < 1:
        raise ValueError("values, horizon, and window must be positive")
    history = list(values)
    predictions = []
    for _ in range(horizon):
        prediction = sum(history[-window:]) / min(window, len(history))
        predictions.append(round(prediction, 2))
        history.append(prediction)
    return predictions


def mean_absolute_error(actual, predicted):
    if len(actual) != len(predicted) or not actual:
        raise ValueError("actual and predicted must have the same non-zero length")
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


def lstm_forecast(values, horizon=7, lookback=14, epochs=15):
    """Train a small one-feature LSTM; tensorflow is installed by the app requirements."""
    if len(values) <= lookback + 2 or horizon < 1 or epochs < 1:
        raise ValueError("Provide enough history and positive horizon/epochs")

    import numpy as np
    from sklearn.preprocessing import MinMaxScaler
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense, Input, LSTM

    series = np.asarray(values, dtype="float32").reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(series)
    x_values, y_values = [], []
    for index in range(lookback, len(scaled)):
        x_values.append(scaled[index - lookback:index, 0])
        y_values.append(scaled[index, 0])
    x_train = np.asarray(x_values, dtype="float32").reshape(-1, lookback, 1)
    y_train = np.asarray(y_values, dtype="float32")

    np.random.seed(7)
    model = Sequential(
        [Input(shape=(lookback, 1)), LSTM(16), Dense(1)]
    )
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(x_train, y_train, epochs=epochs, batch_size=16, verbose=0)

    window = scaled[-lookback:].reshape(1, lookback, 1)
    forecasts = []
    for _ in range(horizon):
        prediction = float(model.predict(window, verbose=0)[0, 0])
        forecasts.append(prediction)
        window = np.concatenate(
            [window[:, 1:, :], np.asarray([[[prediction]]], dtype="float32")],
            axis=1,
        )
    return scaler.inverse_transform(np.asarray(forecasts).reshape(-1, 1)).ravel().tolist()
