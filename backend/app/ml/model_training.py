"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
FINAL CGPA REGRESSION TRAINING
FEATURE SET B+ | RF + GRADIENT BOOSTING + OOF ENSEMBLE
======================================================================

Final raw features:
    Existing Feature Set B
    + Current Semester
    + Average attendance
    + Completed Credits

Model strategy:
    1. 5-fold CV comparison
    2. Mean baseline
    3. Random Forest tuning
    4. Gradient Boosting tuning
    5. Out-of-fold optimized RF/GB blend
    6. Independent untouched test evaluation
    7. Final model selected by training-only CV/OOF MAE
    8. Save final model + metadata

Important:
    - No manual prediction adjustment.
    - Test set is not used to fit the final model.
    - The selected winner is determined from training-only CV/OOF results.
======================================================================
"""

from pathlib import Path
import json
import joblib
import numpy as np

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)
from sklearn.dummy import DummyRegressor
from sklearn.model_selection import (
    KFold,
    cross_validate,
    RandomizedSearchCV,
    cross_val_predict,
)
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from app.ml.preprocessing import prepare_data
from app.ml.ensemble import WeightedRegressionEnsemble


# ======================================================================
# CONFIGURATION
# ======================================================================

TARGET = "What is your current CGPA?"
RANDOM_STATE = 42
CV_FOLDS = 5

FEATURE_SET_NAME = (
    "B_Plus_Demographic_Academic_Behavior_Context"
)


# ======================================================================
# PATHS
# ======================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = (
    BASE_DIR / "saved_models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_PATH = (
    MODEL_DIR / "cgpa_regression_model.pkl"
)

METADATA_PATH = (
    MODEL_DIR / "cgpa_model_metadata.json"
)


# ======================================================================
# METRICS
# ======================================================================

def calculate_rmse(y_true, y_pred):
    return float(
        np.sqrt(
            mean_squared_error(
                y_true,
                y_pred
            )
        )
    )


def regression_metrics(y_true, y_pred):
    return {
        "mae": float(
            mean_absolute_error(
                y_true,
                y_pred
            )
        ),
        "rmse": calculate_rmse(
            y_true,
            y_pred
        ),
        "r2": float(
            r2_score(
                y_true,
                y_pred
            )
        ),
    }


# ======================================================================
# LOAD PREPROCESSED DATA
# ======================================================================

def load_preprocessed_data():

    print()
    print("=" * 70)
    print("LOADING FINAL FEATURE SET B+")
    print("=" * 70)

    result = prepare_data()

    if not isinstance(result, tuple):
        raise ValueError(
            "prepare_data() must return a tuple."
        )

    if len(result) != 7:
        raise ValueError(
            "Unexpected preprocessing output. "
            "Expected 7 objects."
        )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        X_train_raw,
        X_test_raw,
    ) = result

    print()
    print(f"X_train : {X_train.shape}")
    print(f"X_test  : {X_test.shape}")
    print(f"y_train : {y_train.shape}")
    print(f"y_test  : {y_test.shape}")

    return (
        X_train,
        X_test,
        np.asarray(y_train, dtype=float),
        np.asarray(y_test, dtype=float),
        preprocessor,
        X_train_raw,
        X_test_raw,
    )


# ======================================================================
# VALIDATE DATA
# ======================================================================

def validate_data(
    X_train,
    X_test,
    y_train,
    y_test
):

    print()
    print("=" * 70)
    print("FINAL TRAINING DATA VALIDATION")
    print("=" * 70)

    if len(X_train) != len(y_train):
        raise ValueError(
            "X_train/y_train size mismatch."
        )

    if len(X_test) != len(y_test):
        raise ValueError(
            "X_test/y_test size mismatch."
        )

    if not np.isfinite(X_train).all():
        raise ValueError(
            "X_train contains NaN/infinite values."
        )

    if not np.isfinite(X_test).all():
        raise ValueError(
            "X_test contains NaN/infinite values."
        )

    if not np.isfinite(y_train).all():
        raise ValueError(
            "y_train contains NaN/infinite values."
        )

    if not np.isfinite(y_test).all():
        raise ValueError(
            "y_test contains NaN/infinite values."
        )

    if y_train.min() < 0 or y_train.max() > 4:
        raise ValueError(
            "Training target contains CGPA outside 0-4."
        )

    if y_test.min() < 0 or y_test.max() > 4:
        raise ValueError(
            "Testing target contains CGPA outside 0-4."
        )

    print(
        f"Training samples   : {len(y_train)}"
    )
    print(
        f"Testing samples    : {len(y_test)}"
    )
    print(
        f"Processed features : {X_train.shape[1]}"
    )
    print(
        f"Training CGPA mean : {y_train.mean():.3f}"
    )
    print(
        f"Training CGPA min  : {y_train.min():.3f}"
    )
    print(
        f"Training CGPA max  : {y_train.max():.3f}"
    )
    print("✓ Training data validation passed.")


# ======================================================================
# MODELS
# ======================================================================

def get_baseline_models():

    return {
        "Random Forest": RandomForestRegressor(
            n_estimators=500,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),

        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=250,
            learning_rate=0.05,
            max_depth=3,
            min_samples_leaf=4,
            random_state=RANDOM_STATE,
        ),
    }


# ======================================================================
# CROSS VALIDATION
# ======================================================================

def run_cross_validation(
    X_train,
    y_train
):

    print()
    print("=" * 70)
    print("5-FOLD CROSS VALIDATION")
    print("=" * 70)

    models = get_baseline_models()

    cv = KFold(
        n_splits=CV_FOLDS,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    results = {}

    for name, model in models.items():

        print()
        print(
            f"Evaluating: {name}"
        )

        scores = cross_validate(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring={
                "mae":
                    "neg_mean_absolute_error",
                "rmse":
                    "neg_root_mean_squared_error",
                "r2":
                    "r2",
            },
            n_jobs=-1,
            return_train_score=False,
        )

        cv_mae = float(
            -scores[
                "test_mae"
            ].mean()
        )

        cv_rmse = float(
            -scores[
                "test_rmse"
            ].mean()
        )

        cv_r2 = float(
            scores[
                "test_r2"
            ].mean()
        )

        results[name] = {
            "model": model,
            "cv_mae": cv_mae,
            "cv_rmse": cv_rmse,
            "cv_r2": cv_r2,
        }

        print(
            f"CV MAE  : {cv_mae:.4f}"
        )
        print(
            f"CV RMSE : {cv_rmse:.4f}"
        )
        print(
            f"CV R²   : {cv_r2:.4f}"
        )

    return results, cv


# ======================================================================
# BASELINE
# ======================================================================

def run_mean_baseline(
    X_train,
    X_test,
    y_train,
    y_test
):

    baseline = DummyRegressor(
        strategy="mean"
    )

    baseline.fit(
        X_train,
        y_train
    )

    predictions = baseline.predict(
        X_test
    )

    metrics = regression_metrics(
        y_test,
        predictions
    )

    print()
    print("=" * 70)
    print("MEAN BASELINE")
    print("=" * 70)
    print(
        f"Baseline MAE  : {metrics['mae']:.4f}"
    )
    print(
        f"Baseline RMSE : {metrics['rmse']:.4f}"
    )
    print(
        f"Baseline R²   : {metrics['r2']:.4f}"
    )

    return baseline, metrics


# ======================================================================
# RANDOM FOREST TUNING
# ======================================================================

def tune_random_forest(
    X_train,
    y_train,
    cv
):

    print()
    print("=" * 70)
    print("RANDOM FOREST HYPERPARAMETER TUNING")
    print("=" * 70)

    model = RandomForestRegressor(
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    parameter_distributions = {
        "n_estimators": [
            300,
            500,
            700,
            900,
        ],
        "max_depth": [
            None,
            6,
            8,
            10,
            12,
            16,
            20,
        ],
        "min_samples_split": [
            2,
            5,
            10,
        ],
        "min_samples_leaf": [
            1,
            2,
            4,
            6,
            8,
        ],
        "max_features": [
            0.3,
            0.4,
            0.5,
            0.7,
            1.0,
            "sqrt",
        ],
    }

    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=parameter_distributions,
        n_iter=30,
        scoring="neg_mean_absolute_error",
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
        refit=True,
    )

    search.fit(
        X_train,
        y_train
    )

    best_model = (
        search.best_estimator_
    )

    best_cv_mae = float(
        -search.best_score_
    )

    print()
    print("BEST RANDOM FOREST PARAMETERS")
    print("-" * 70)

    for key, value in (
        search.best_params_.items()
    ):
        print(
            f"{key}: {value}"
        )

    print()
    print(
        f"Best RF CV MAE: "
        f"{best_cv_mae:.4f}"
    )

    return (
        best_model,
        best_cv_mae,
        search.best_params_,
    )


# ======================================================================
# GRADIENT BOOSTING TUNING
# ======================================================================

def tune_gradient_boosting(
    X_train,
    y_train,
    cv
):

    print()
    print("=" * 70)
    print("GRADIENT BOOSTING HYPERPARAMETER TUNING")
    print("=" * 70)

    model = GradientBoostingRegressor(
        random_state=RANDOM_STATE
    )

    parameter_distributions = {
        "n_estimators": [
            100,
            150,
            200,
            250,
            350,
            500,
        ],
        "learning_rate": [
            0.01,
            0.02,
            0.03,
            0.05,
            0.07,
            0.10,
        ],
        "max_depth": [
            2,
            3,
            4,
            5,
        ],
        "min_samples_split": [
            2,
            5,
            10,
            15,
        ],
        "min_samples_leaf": [
            1,
            2,
            4,
            6,
            8,
        ],
        "subsample": [
            0.7,
            0.8,
            0.9,
            1.0,
        ],
        "max_features": [
            None,
            "sqrt",
            "log2",
        ],
    }

    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=parameter_distributions,
        n_iter=30,
        scoring="neg_mean_absolute_error",
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
        refit=True,
    )

    search.fit(
        X_train,
        y_train
    )

    best_model = (
        search.best_estimator_
    )

    best_cv_mae = float(
        -search.best_score_
    )

    print()
    print(
        "BEST GRADIENT BOOSTING PARAMETERS"
    )
    print("-" * 70)

    for key, value in (
        search.best_params_.items()
    ):
        print(
            f"{key}: {value}"
        )

    print()
    print(
        f"Best GB CV MAE: "
        f"{best_cv_mae:.4f}"
    )

    return (
        best_model,
        best_cv_mae,
        search.best_params_,
    )


# ======================================================================
# OOF ENSEMBLE
# ======================================================================

def optimize_oof_ensemble(
    rf_model,
    gb_model,
    X_train,
    y_train,
    cv
):

    print()
    print("=" * 70)
    print("OUT-OF-FOLD RF + GB ENSEMBLE")
    print("=" * 70)

    rf_oof = cross_val_predict(
        rf_model,
        X_train,
        y_train,
        cv=cv,
        n_jobs=-1,
        method="predict",
    )

    gb_oof = cross_val_predict(
        gb_model,
        X_train,
        y_train,
        cv=cv,
        n_jobs=-1,
        method="predict",
    )

    best_weight = 0.5
    best_mae = float("inf")
    best_rmse = float("inf")

    for weight in np.linspace(
        0.0,
        1.0,
        101
    ):

        blended = (
            weight * rf_oof
            +
            (1.0 - weight)
            * gb_oof
        )

        mae = mean_absolute_error(
            y_train,
            blended
        )

        if mae < best_mae:

            best_mae = float(mae)

            best_weight = float(
                weight
            )

            best_rmse = calculate_rmse(
                y_train,
                blended
            )

    final_weight = best_weight

    print(
        f"Best RF weight : "
        f"{final_weight:.2f}"
    )

    print(
        f"Best GB weight : "
        f"{1.0 - final_weight:.2f}"
    )

    print(
        f"OOF MAE        : "
        f"{best_mae:.4f}"
    )

    print(
        f"OOF RMSE       : "
        f"{best_rmse:.4f}"
    )

    return {
        "rf_weight":
            final_weight,
        "gb_weight":
            1.0 - final_weight,
        "oof_mae":
            best_mae,
        "oof_rmse":
            best_rmse,
    }


# ======================================================================
# FINAL TEST EVALUATION
# ======================================================================

def evaluate_test_models(
    rf_model,
    gb_model,
    ensemble_info,
    X_test,
    y_test,
):

    print()
    print("=" * 70)
    print("INDEPENDENT TEST SET EVALUATION")
    print("=" * 70)

    rf_predictions = (
        rf_model.predict(X_test)
    )

    gb_predictions = (
        gb_model.predict(X_test)
    )

    ensemble_predictions = (
        ensemble_info["rf_weight"]
        * rf_predictions
        +
        ensemble_info["gb_weight"]
        * gb_predictions
    )

    results = {
        "Random Forest":
            regression_metrics(
                y_test,
                rf_predictions
            ),

        "Gradient Boosting":
            regression_metrics(
                y_test,
                gb_predictions
            ),

        "RF + GB Ensemble":
            regression_metrics(
                y_test,
                ensemble_predictions
            ),
    }

    for name, metrics in results.items():

        print()
        print(name)
        print(
            f"MAE  : {metrics['mae']:.4f}"
        )
        print(
            f"RMSE : {metrics['rmse']:.4f}"
        )
        print(
            f"R²   : {metrics['r2']:.4f}"
        )

    return {
        "results": results,
        "predictions": {
            "Random Forest":
                rf_predictions,
            "Gradient Boosting":
                gb_predictions,
            "RF + GB Ensemble":
                ensemble_predictions,
        },
    }


# ======================================================================
# ERROR ANALYSIS
# ======================================================================

def error_analysis(
    y_test,
    predictions
):

    errors = (
        predictions - y_test
    )

    absolute_errors = np.abs(
        errors
    )

    result = {
        "within_025_percent":
            float(
                (
                    absolute_errors <= 0.25
                ).mean() * 100
            ),

        "within_050_percent":
            float(
                (
                    absolute_errors <= 0.50
                ).mean() * 100
            ),

        "within_075_percent":
            float(
                (
                    absolute_errors <= 0.75
                ).mean() * 100
            ),

        "within_100_percent":
            float(
                (
                    absolute_errors <= 1.00
                ).mean() * 100
            ),

        "median_absolute_error":
            float(
                np.median(
                    absolute_errors
                )
            ),

        "maximum_absolute_error":
            float(
                absolute_errors.max()
            ),
    }

    print()
    print("=" * 70)
    print("FINAL ERROR ANALYSIS")
    print("=" * 70)

    print(
        f"Within ±0.25 GPA : "
        f"{result['within_025_percent']:.2f}%"
    )

    print(
        f"Within ±0.50 GPA : "
        f"{result['within_050_percent']:.2f}%"
    )

    print(
        f"Within ±0.75 GPA : "
        f"{result['within_075_percent']:.2f}%"
    )

    print(
        f"Within ±1.00 GPA : "
        f"{result['within_100_percent']:.2f}%"
    )

    print(
        f"Median error     : "
        f"{result['median_absolute_error']:.4f}"
    )

    print(
        f"Maximum error    : "
        f"{result['maximum_absolute_error']:.4f}"
    )

    return result


# ======================================================================
# SAVE MODEL
# ======================================================================

def save_model(model):

    joblib.dump(
        model,
        MODEL_PATH
    )

    print()
    print(
        "✓ FINAL MODEL SAVED"
    )
    print(
        MODEL_PATH
    )


# ======================================================================
# SAVE METADATA
# ======================================================================

def save_metadata(
    metadata
):

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    print()
    print(
        "✓ MODEL METADATA SAVED"
    )
    print(
        METADATA_PATH
    )


# ======================================================================
# MAIN
# ======================================================================

# ======================================================================

def main():

    print()
    print("=" * 70)
    print(
        "AI STUDENT ANALYTICS DASHBOARD"
    )
    print(
        "FINAL CGPA REGRESSION TRAINING"
    )
    print(
        "FEATURE SET B+"
    )
    print("=" * 70)

    # --------------------------------------------------------------
    # 1. LOAD DATA
    # --------------------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
        preprocessor,
        X_train_raw,
        X_test_raw,
    ) = load_preprocessed_data()

    validate_data(
        X_train,
        X_test,
        y_train,
        y_test
    )

    # --------------------------------------------------------------
    # 2. CV COMPARISON
    # --------------------------------------------------------------

    cv_results, cv = (
        run_cross_validation(
            X_train,
            y_train
        )
    )

    # --------------------------------------------------------------
    # 3. BASELINE
    # --------------------------------------------------------------

    baseline_model, baseline_metrics = (
        run_mean_baseline(
            X_train,
            X_test,
            y_train,
            y_test
        )
    )

    # --------------------------------------------------------------
    # 4. RF TUNING
    # --------------------------------------------------------------

    (
        tuned_rf,
        rf_cv_mae,
        rf_params,
    ) = tune_random_forest(
        X_train,
        y_train,
        cv
    )

    # --------------------------------------------------------------
    # 5. GB TUNING
    # --------------------------------------------------------------

    (
        tuned_gb,
        gb_cv_mae,
        gb_params,
    ) = tune_gradient_boosting(
        X_train,
        y_train,
        cv
    )

    # --------------------------------------------------------------
    # 6. OOF ENSEMBLE
    # --------------------------------------------------------------

    ensemble_info = (
        optimize_oof_ensemble(
            tuned_rf,
            tuned_gb,
            X_train,
            y_train,
            cv
        )
    )

    # --------------------------------------------------------------
    # 7. TEST EVALUATION
    # --------------------------------------------------------------

    test_evaluation = (
        evaluate_test_models(
            tuned_rf,
            tuned_gb,
            ensemble_info,
            X_test,
            y_test,
        )
    )

    test_results = (
        test_evaluation["results"]
    )

    test_predictions = (
        test_evaluation["predictions"]
    )

    # --------------------------------------------------------------
    # 8. TRAINING-ONLY MODEL SELECTION
    # --------------------------------------------------------------
    #
    # Select using CV/OOF, NOT test performance.
    # This preserves the independent test set as a final report.
    # --------------------------------------------------------------

    candidates = {
        "Random Forest": {
            "cv_mae":
                rf_cv_mae,
            "type":
                "single",
        },

        "Gradient Boosting": {
            "cv_mae":
                gb_cv_mae,
            "type":
                "single",
        },

        "RF + GB Ensemble": {
            "cv_mae":
                ensemble_info[
                    "oof_mae"
                ],
            "type":
                "ensemble",
        },
    }

    selected_name = min(
        candidates,
        key=lambda name:
            candidates[name]["cv_mae"]
    )

    print()
    print("=" * 70)
    print("FINAL MODEL SELECTION")
    print("=" * 70)

    print(
        f"Selected by training-only CV/OOF: "
        f"{selected_name}"
    )

    if selected_name == (
        "Random Forest"
    ):

        final_model = (
            tuned_rf
        )

    elif selected_name == (
        "Gradient Boosting"
    ):

        final_model = (
            tuned_gb
        )

    else:

        final_model = (
            WeightedRegressionEnsemble(
                rf_model=tuned_rf,
                gb_model=tuned_gb,
                rf_weight=
                    ensemble_info[
                        "rf_weight"
                    ],
                gb_weight=
                    ensemble_info[
                        "gb_weight"
                    ],
            )
        )

    # --------------------------------------------------------------
    # 9. FINAL SELECTED MODEL TEST METRICS
    # --------------------------------------------------------------

    selected_test = test_results[
        selected_name
    ]

    selected_predictions = (
        test_predictions[
            selected_name
        ]
    )

    error_results = (
        error_analysis(
            y_test,
            selected_predictions
        )
    )

    improvement = (
        baseline_metrics["mae"]
        -
        selected_test["mae"]
    )

    improvement_percentage = (
        (
            improvement
            /
            baseline_metrics["mae"]
        ) * 100
        if baseline_metrics["mae"] != 0
        else 0.0
    )

    decision = (
        "MODEL OUTPERFORMS BASELINE"
        if selected_test["mae"]
        <
        baseline_metrics["mae"]
        else
        "MODEL REQUIRES REVIEW"
    )

    print()
    print("=" * 70)
    print("FINAL MODEL VS BASELINE")
    print("=" * 70)

    print(
        f"Baseline MAE : "
        f"{baseline_metrics['mae']:.4f}"
    )

    print(
        f"Model MAE    : "
        f"{selected_test['mae']:.4f}"
    )

    print(
        f"Improvement  : "
        f"{improvement:.4f}"
    )

    print(
        f"Improvement %: "
        f"{improvement_percentage:.2f}%"
    )

    print()
    print(
        f"Decision: {decision}"
    )

    # --------------------------------------------------------------
    # 10. SAVE FINAL MODEL
    # --------------------------------------------------------------

    save_model(
        final_model
    )

    # --------------------------------------------------------------
    # 11. METADATA
    # --------------------------------------------------------------

    metadata = {

        "model_name":
            selected_name,

        "model_type":
            type(final_model).__name__,

        "feature_set":
            FEATURE_SET_NAME,

        "target":
            TARGET,

        "dataset":
            "IUBAT_CGPA_Training_Cleaned.csv",

        "raw_features":
            int(
                X_train_raw.shape[1]
            ),

        "processed_features":
            int(
                X_train.shape[1]
            ),

        "training_samples":
            int(
                len(y_train)
            ),

        "testing_samples":
            int(
                len(y_test)
            ),

        "cross_validation_folds":
            CV_FOLDS,

        "rf_cv_mae":
            float(
                rf_cv_mae
            ),

        "gb_cv_mae":
            float(
                gb_cv_mae
            ),

        "ensemble_oof_mae":
            float(
                ensemble_info[
                    "oof_mae"
                ]
            ),

        "ensemble_rf_weight":
            float(
                ensemble_info[
                    "rf_weight"
                ]
            ),

        "ensemble_gb_weight":
            float(
                ensemble_info[
                    "gb_weight"
                ]
            ),

        "selected_test_mae":
            float(
                selected_test["mae"]
            ),

        "selected_test_rmse":
            float(
                selected_test["rmse"]
            ),

        "selected_test_r2":
            float(
                selected_test["r2"]
            ),

        "expected_gpa_error":
            (
                f"±"
                f"{selected_test['mae']:.2f}"
                f" GPA"
            ),

        "baseline_mae":
            float(
                baseline_metrics["mae"]
            ),

        "baseline_rmse":
            float(
                baseline_metrics["rmse"]
            ),

        "baseline_r2":
            float(
                baseline_metrics["r2"]
            ),

        "improvement":
            float(
                improvement
            ),

        "improvement_percentage":
            float(
                improvement_percentage
            ),

        "within_025_percent":
            float(
                error_results[
                    "within_025_percent"
                ]
            ),

        "within_050_percent":
            float(
                error_results[
                    "within_050_percent"
                ]
            ),

        "within_075_percent":
            float(
                error_results[
                    "within_075_percent"
                ]
            ),

        "within_100_percent":
            float(
                error_results[
                    "within_100_percent"
                ]
            ),

        "median_absolute_error":
            float(
                error_results[
                    "median_absolute_error"
                ]
            ),

        "maximum_absolute_error":
            float(
                error_results[
                    "maximum_absolute_error"
                ]
            ),

        "random_forest_parameters":
            rf_params,

        "gradient_boosting_parameters":
            gb_params,

        "hyperparameter_tuning":
            True,

        "leakage_protected":
            True,

        "random_state":
            RANDOM_STATE,

        "decision":
            decision,
    }

    save_metadata(
        metadata
    )

    # --------------------------------------------------------------
    # 12. FINAL SUMMARY
    # --------------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL B+ TRAINING SUMMARY")
    print("=" * 70)

    print()
    print(
        f"Final model         : "
        f"{selected_name}"
    )

    print(
        f"Training samples    : "
        f"{len(y_train)}"
    )

    print(
        f"Testing samples     : "
        f"{len(y_test)}"
    )

    print(
        f"Raw features        : "
        f"{X_train_raw.shape[1]}"
    )

    print(
        f"Processed features  : "
        f"{X_train.shape[1]}"
    )

    print(
        f"Test MAE            : "
        f"{selected_test['mae']:.4f}"
    )

    print(
        f"Test RMSE           : "
        f"{selected_test['rmse']:.4f}"
    )

    print(
        f"Test R²             : "
        f"{selected_test['r2']:.4f}"
    )

    print(
        f"Expected GPA Error  : "
        f"±{selected_test['mae']:.2f} GPA"
    )

    print(
        f"Decision            : "
        f"{decision}"
    )

    if selected_test["r2"] <= 0:
        print()
        print(
            "⚠ R² is non-positive."
        )
    elif selected_test["r2"] < 0.20:
        print()
        print(
            "⚠ R² is positive but weak."
        )
        print(
            "Treat the model as decision-support."
        )
    else:
        print()
        print(
            "✓ Model shows meaningful positive R²."
        )

    print()
    print(
        "Saved model:"
    )
    print(
        MODEL_PATH
    )

    print()
    print(
        "Saved metadata:"
    )
    print(
        METADATA_PATH
    )

    print()
    print("=" * 70)
    print(
        "FINAL MODEL TRAINING COMPLETE"
    )
    print("=" * 70)


# ======================================================================
# ENTRY POINT
# ======================================================================

if __name__ == "__main__":
    main()