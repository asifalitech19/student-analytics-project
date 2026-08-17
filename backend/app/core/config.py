from pathlib import Path

# =====================================================
# PROJECT ROOT DIRECTORY
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[2]

# =====================================================
# DATASET
# =====================================================

DATASET_DIR = BASE_DIR / "dataset"
DATASET_PATH = DATASET_DIR / "dataset.csv"

# =====================================================
# SAVED MODELS
# =====================================================

MODEL_DIR = BASE_DIR / "saved_models"

MODEL_PATH = MODEL_DIR / "cgpa_model.pkl"

FEATURE_ENCODER_PATH = MODEL_DIR / "feature_encoders.pkl"

TARGET_ENCODER_PATH = MODEL_DIR / "target_encoder.pkl"

# =====================================================
# VECTOR DATABASE
# =====================================================

VECTOR_DB_DIR = BASE_DIR / "vector_db"

# =====================================================
# CREATE DIRECTORIES IF THEY DON'T EXIST
# =====================================================

MODEL_DIR.mkdir(exist_ok=True)

VECTOR_DB_DIR.mkdir(exist_ok=True)