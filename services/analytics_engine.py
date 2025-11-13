class AnalyticsEngine:
    """
    Performs analysis on telemetry data including
    regression, average temperature, and battery life estimation.
    """

    def clean_data(self, telemetry_list):
        """Remove telemetry records with invalid temperatures or voltages."""
        return [
            r for r in telemetry_list
            if r.temperature_c > -40 and r.temperature_c < 150
            and r.voltage_v > 0
        ]

    def average_temperature(self, telemetry_list):
        """Return average temperature from telemetry records."""
        if not telemetry_list:
            return 0
        temps = [r.temperature_c for r in telemetry_list]
        return sum(temps) / len(temps)

    def run_regression(self, x_values, y_values):
      """
      Pure Python linear regression
      Returns slope and intercept.
      """
      n = len(x_values)
      if n < 2:
          return 0, 0

      sum_x = sum(x_values)
      sum_y = sum(y_values)
      sum_xy = sum(x*y for x, y in zip(x_values, y_values))
      sum_x2 = sum(x*x for x in x_values)

      denominator = (n * sum_x2 - sum_x**2)
      if denominator == 0:
          return 0, 0

      slope = (n * sum_xy - sum_x * sum_y) / denominator
      intercept = (sum_y - slope * sum_x) / n

      return slope, intercept


    def predict_capacity_fade(self, telemetry_list):
        """
        Fake example: Predict capacity fade from voltage trend.
        (Just enough for a class project.)
        """
        if len(telemetry_list) < 2:
            return 0

        timestamps = [i for i in range(len(telemetry_list))]
        voltages = [r.voltage_v for r in telemetry_list]

        slope, _ = self.run_regression(timestamps, voltages)

        return abs(slope)

    def predict_remaining_life(self, telemetry_list):
        """
        Example model:
        Battery starts at 100 "health points".
        High temperatures reduce it.
        A simple calculation for demonstration.
        """
        if not telemetry_list:
            return 100

        avg_temp = self.average_temperature(telemetry_list)

        loss = max(0, avg_temp - 25)

        remaining = max(0, 100 - loss)
        return remaining
