"""
What-If Simulation Route — Dynamically compare yield under modified conditions.
POST /simulate-yield
"""

from fastapi import APIRouter, HTTPException
from models.schemas import SimulationRequest, SimulationResponse
from models.yield_model import predict_yield
from utils.interpreter import interpret_yield, interpret_simulation_comparison

router = APIRouter(tags=["🔬 Simulation"])


@router.post("/simulate-yield", response_model=SimulationResponse)
async def simulate_yield(req: SimulationRequest):
    """
    Simulate yield with modified conditions and compare with original.
    Returns both yields, percentage change, and farmer-friendly comparison.
    """
    try:
        # Original prediction
        orig = req.original
        original_result = predict_yield(
            rainfall_mm=orig.rainfall_mm,
            temperature_c=orig.temperature_c,
            soil_ph=orig.soil_ph,
            soil_moisture_pct=orig.soil_moisture_pct,
            fertilizer_kg_per_hectare=orig.fertilizer_kg_per_hectare,
            irrigation_level_pct=orig.irrigation_level_pct,
        )

        # Build simulated inputs (use original value if simulated not provided)
        sim_rainfall = req.simulated_rainfall_mm if req.simulated_rainfall_mm is not None else orig.rainfall_mm
        sim_temp = req.simulated_temperature_c if req.simulated_temperature_c is not None else orig.temperature_c
        sim_ph = req.simulated_soil_ph if req.simulated_soil_ph is not None else orig.soil_ph
        sim_moisture = req.simulated_soil_moisture_pct if req.simulated_soil_moisture_pct is not None else orig.soil_moisture_pct
        sim_fert = req.simulated_fertilizer_kg_per_hectare if req.simulated_fertilizer_kg_per_hectare is not None else orig.fertilizer_kg_per_hectare
        sim_irr = req.simulated_irrigation_level_pct if req.simulated_irrigation_level_pct is not None else orig.irrigation_level_pct

        simulated_result = predict_yield(
            rainfall_mm=sim_rainfall,
            temperature_c=sim_temp,
            soil_ph=sim_ph,
            soil_moisture_pct=sim_moisture,
            fertilizer_kg_per_hectare=sim_fert,
            irrigation_level_pct=sim_irr,
        )

        # Calculate change
        orig_yield = original_result["predicted_yield"]
        sim_yield = simulated_result["predicted_yield"]
        change_tons = round(sim_yield - orig_yield, 2)
        change_pct = round((change_tons / orig_yield) * 100, 1) if orig_yield > 0 else 0.0

        # Track what was modified
        modifications = {}
        if req.simulated_rainfall_mm is not None:
            modifications["rainfall_mm"] = {"original": orig.rainfall_mm, "simulated": sim_rainfall}
        if req.simulated_temperature_c is not None:
            modifications["temperature_c"] = {"original": orig.temperature_c, "simulated": sim_temp}
        if req.simulated_soil_ph is not None:
            modifications["soil_ph"] = {"original": orig.soil_ph, "simulated": sim_ph}
        if req.simulated_soil_moisture_pct is not None:
            modifications["soil_moisture_pct"] = {"original": orig.soil_moisture_pct, "simulated": sim_moisture}
        if req.simulated_fertilizer_kg_per_hectare is not None:
            modifications["fertilizer_kg_per_hectare"] = {"original": orig.fertilizer_kg_per_hectare, "simulated": sim_fert}
        if req.simulated_irrigation_level_pct is not None:
            modifications["irrigation_level_pct"] = {"original": orig.irrigation_level_pct, "simulated": sim_irr}

        lang = req.language.value
        orig_interp = interpret_yield(orig_yield, original_result["category"], lang)
        sim_interp = interpret_yield(sim_yield, simulated_result["category"], lang)
        comparison = interpret_simulation_comparison(orig_yield, sim_yield, change_pct, lang)

        return SimulationResponse(
            original_yield=orig_yield,
            simulated_yield=sim_yield,
            yield_change_tons=change_tons,
            yield_change_pct=change_pct,
            original_interpretation=orig_interp,
            simulated_interpretation=sim_interp,
            comparison_summary=comparison,
            modifications_applied=modifications,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")
