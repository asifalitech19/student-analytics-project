"""Final regression ensemble class for joblib-safe serialization."""

import numpy as np


class WeightedRegressionEnsemble:
    """Weighted Random Forest + Gradient Boosting ensemble."""

    def __init__(self, rf_model, gb_model, rf_weight, gb_weight):
        self.rf_model = rf_model
        self.gb_model = gb_model
        self.rf_weight = float(rf_weight)
        self.gb_weight = float(gb_weight)

    def predict(self, X):
        rf_prediction = self.rf_model.predict(X)
        gb_prediction = self.gb_model.predict(X)
        prediction = (
            self.rf_weight * rf_prediction
            + self.gb_weight * gb_prediction
        )
        return np.clip(prediction, 0.0, 4.0)    