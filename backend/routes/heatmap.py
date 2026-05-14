"""
Zone-Based Yield Heatmap Route — Generates zone-wise yield data for Karnataka.
GET /yield-heatmap
"""

from datetime import datetime
from fastapi import APIRouter
from models.schemas import HeatmapResponse, ZoneYieldData
from models.yield_model import predict_yield
import config

router = APIRouter(tags=["🗺️ Heatmap"])

# Default conditions per zone (simulating regional variation)
ZONE_CONDITIONS = {
    "KA-01": {"rainfall": 850, "temp": 27, "ph": 6.5, "moisture": 50, "fert": 100, "irr": 65},
    "KA-02": {"rainfall": 780, "temp": 26, "ph": 6.3, "moisture": 48, "fert": 90, "irr": 60},
    "KA-03": {"rainfall": 700, "temp": 28, "ph": 6.8, "moisture": 52, "fert": 110, "irr": 70},
    "KA-04": {"rainfall": 900, "temp": 25, "ph": 6.2, "moisture": 55, "fert": 85, "irr": 55},
    "KA-05": {"rainfall": 650, "temp": 29, "ph": 7.0, "moisture": 40, "fert": 75, "irr": 50},
    "KA-06": {"rainfall": 550, "temp": 31, "ph": 7.2, "moisture": 35, "fert": 60, "irr": 40},
    "KA-07": {"rainfall": 620, "temp": 30, "ph": 6.9, "moisture": 42, "fert": 80, "irr": 48},
    "KA-08": {"rainfall": 1200, "temp": 26, "ph": 5.8, "moisture": 60, "fert": 70, "irr": 45},
    "KA-09": {"rainfall": 700, "temp": 28, "ph": 7.1, "moisture": 38, "fert": 95, "irr": 52},
    "KA-10": {"rainfall": 750, "temp": 27, "ph": 6.7, "moisture": 45, "fert": 105, "irr": 58},
    "KA-11": {"rainfall": 500, "temp": 33, "ph": 7.5, "moisture": 28, "fert": 55, "irr": 35},
    "KA-12": {"rainfall": 480, "temp": 34, "ph": 7.8, "moisture": 25, "fert": 50, "irr": 30},
    "KA-13": {"rainfall": 600, "temp": 32, "ph": 7.3, "moisture": 32, "fert": 65, "irr": 38},
    "KA-14": {"rainfall": 700, "temp": 30, "ph": 7.0, "moisture": 36, "fert": 70, "irr": 42},
    "KA-15": {"rainfall": 2500, "temp": 22, "ph": 5.5, "moisture": 70, "fert": 60, "irr": 30},
    "KA-16": {"rainfall": 3000, "temp": 27, "ph": 5.8, "moisture": 65, "fert": 55, "irr": 25},
    "KA-17": {"rainfall": 3200, "temp": 28, "ph": 5.6, "moisture": 68, "fert": 50, "irr": 20},
    "KA-18": {"rainfall": 650, "temp": 29, "ph": 6.8, "moisture": 40, "fert": 85, "irr": 50},
    "KA-19": {"rainfall": 550, "temp": 30, "ph": 7.2, "moisture": 33, "fert": 70, "irr": 42},
    "KA-20": {"rainfall": 500, "temp": 32, "ph": 7.4, "moisture": 30, "fert": 60, "irr": 38},
}


@router.get("/yield-heatmap", response_model=HeatmapResponse)
async def get_yield_heatmap():
    """Generate zone-based yield data for all Karnataka zones."""
    zones = []
    high_count = medium_count = low_count = 0

    for zone in config.KARNATAKA_ZONES:
        cond = ZONE_CONDITIONS.get(zone["zone_id"], {
            "rainfall": 700, "temp": 28, "ph": 6.5, "moisture": 45, "fert": 80, "irr": 50
        })

        result = predict_yield(
            rainfall_mm=cond["rainfall"],
            temperature_c=cond["temp"],
            soil_ph=cond["ph"],
            soil_moisture_pct=cond["moisture"],
            fertilizer_kg_per_hectare=cond["fert"],
            irrigation_level_pct=cond["irr"],
        )

        y = result["predicted_yield"]
        if y >= 4.0:
            label, color = "High Yield", "#22c55e"
            high_count += 1
        elif y >= 2.5:
            label, color = "Medium Yield", "#eab308"
            medium_count += 1
        else:
            label, color = "Low Yield", "#ef4444"
            low_count += 1

        zones.append(ZoneYieldData(
            zone_id=zone["zone_id"],
            zone_name=zone["name"],
            latitude=zone["lat"],
            longitude=zone["lng"],
            predicted_yield=y,
            yield_label=label,
            color_code=color,
        ))

    return HeatmapResponse(
        total_zones=len(zones),
        zones=zones,
        generated_at=datetime.now().isoformat(),
        summary={"high_yield_zones": high_count, "medium_yield_zones": medium_count, "low_yield_zones": low_count},
    )
