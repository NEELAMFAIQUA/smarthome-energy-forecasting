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
