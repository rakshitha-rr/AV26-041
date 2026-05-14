"""
Synthetic dataset generator for Karnataka crop yield data.
Creates realistic agricultural data for training the yield prediction model.
"""

import os
import numpy as np
import pandas as pd


def generate_karnataka_crop_data(n_samples: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic crop data with realistic correlations
    mimicking Karnataka agricultural conditions.
    """
    np.random.seed(seed)

    # ─── Feature Generation ──────────────────────────────────────
    # Rainfall (mm/season): Karnataka ranges 500-3000mm annually
    rainfall = np.random.normal(800, 250, n_samples).clip(100, 2000)

    # Temperature (°C): Karnataka ranges 15-40°C
    temperature = np.random.normal(28, 5, n_samples).clip(12, 45)

    # Soil pH: Typical agricultural range
    soil_ph = np.random.normal(6.5, 0.8, n_samples).clip(4.0, 9.5)

    # Soil Moisture (%): 10-80%
    soil_moisture = np.random.normal(45, 15, n_samples).clip(5, 90)

    # Fertilizer Usage (kg/hectare): 0-300
    fertilizer_usage = np.random.exponential(80, n_samples).clip(0, 350)

    # Irrigation Level (%): 0-100
    irrigation_level = np.random.beta(2, 2, n_samples) * 100

    # ─── Yield Calculation (tons/hectare) ────────────────────────
    # Realistic yield formula with domain knowledge
    yield_base = 2.0

    # Rainfall contribution (optimal around 800mm)
    rainfall_factor = -0.000003 * (rainfall - 800) ** 2 + 1.0

    # Temperature contribution (optimal around 25°C)
    temp_factor = -0.005 * (temperature - 25) ** 2 + 1.0

    # Soil pH contribution (optimal around 6.5)
    ph_factor = -0.15 * (soil_ph - 6.5) ** 2 + 1.0

    # Soil moisture contribution (optimal around 50%)
    moisture_factor = -0.0003 * (soil_moisture - 50) ** 2 + 1.0

    # Fertilizer contribution (diminishing returns)
    fertilizer_factor = 0.5 * (1 - np.exp(-fertilizer_usage / 100))

    # Irrigation contribution
    irrigation_factor = 0.3 * (irrigation_level / 100)

    # Combined yield with noise
    crop_yield = (
        yield_base
        + 1.5 * rainfall_factor
        + 0.8 * temp_factor
        + 0.5 * ph_factor
        + 0.6 * moisture_factor
        + fertilizer_factor
        + irrigation_factor
        + np.random.normal(0, 0.3, n_samples)  # Random noise
    )

    # Clip to realistic range (0.5 - 8.0 tons/hectare)
    crop_yield = crop_yield.clip(0.5, 8.0)

    # ─── Create DataFrame ────────────────────────────────────────
    df = pd.DataFrame({
        "rainfall_mm": np.round(rainfall, 1),
        "temperature_c": np.round(temperature, 1),
        "soil_ph": np.round(soil_ph, 2),
        "soil_moisture_pct": np.round(soil_moisture, 1),
        "fertilizer_kg_per_hectare": np.round(fertilizer_usage, 1),
        "irrigation_level_pct": np.round(irrigation_level, 1),
        "yield_tons_per_hectare": np.round(crop_yield, 2),
    })

    return df


def save_dataset(df: pd.DataFrame, path: str) -> str:
    """Save dataset to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__))
    output_path = os.path.join(data_dir, "karnataka_crop_data.csv")
    df = generate_karnataka_crop_data()
    save_dataset(df, output_path)
    print(f" Generated {len(df)} samples -> {output_path}")
    print(f"\n Dataset Statistics:\n{df.describe().round(2)}")
