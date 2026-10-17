import unittest

from forecast import forecast, mean_absolute_error, sample_daily_usage


class ForecastTests(unittest.TestCase):
    def test_sample_data_is_deterministic(self):
        self.assertEqual(sample_daily_usage(10), sample_daily_usage(10))

    def test_forecast_has_requested_length(self):
        self.assertEqual(len(forecast([1, 2, 3], 4, 2)), 4)

    def test_mae(self):
        self.assertEqual(mean_absolute_error([1, 3], [2, 1]), 1.5)

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            forecast([], 7)
        with self.assertRaises(ValueError):
            sample_daily_usage(0)


if __name__ == "__main__":
    unittest.main()
