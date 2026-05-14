"""
Government Schemes Route — Lists schemes and checks eligibility.
GET /schemes, POST /check-eligibility
"""

from fastapi import APIRouter
from models.schemas import SchemeEligibilityRequest, SchemeResponse, SchemeInfo
import config

router = APIRouter(tags=["🏛️ Government Schemes"])


@router.get("/schemes", response_model=SchemeResponse)
async def list_schemes():
    """List all available government schemes for farmers."""
    schemes = []
    for s in config.GOVERNMENT_SCHEMES:
        schemes.append(SchemeInfo(
            id=s["id"], name=s["name"], full_name=s["full_name"],
            description=s["description"], benefit=s["benefit"],
            eligible=True, reason="Eligibility not checked yet. Use /check-eligibility.",
            documents_required=s["documents_required"], website=s["website"],
        ))
    return SchemeResponse(total_schemes=len(schemes), eligible_count=len(schemes), schemes=schemes)


@router.post("/check-eligibility", response_model=SchemeResponse)
async def check_eligibility(req: SchemeEligibilityRequest):
    """Check farmer's eligibility for all government schemes."""
    schemes = []
    eligible_count = 0

    for s in config.GOVERNMENT_SCHEMES:
        eligible = True
        reasons = []
        elig = s["eligibility"]

        if elig.get("must_be_farmer") and not req.is_farmer:
            eligible = False
            reasons.append("Must be a registered farmer")
        if elig.get("min_age") and req.age < elig["min_age"]:
            eligible = False
            reasons.append(f"Minimum age: {elig['min_age']}")
        if elig.get("land_holding_max_hectares") and req.land_holding_hectares > elig["land_holding_max_hectares"]:
            eligible = False
            reasons.append(f"Land holding must be ≤ {elig['land_holding_max_hectares']} hectares")
        if elig.get("state") and req.state.lower() != elig["state"].lower():
            eligible = False
            reasons.append(f"Available only in {elig['state']}")
        if elig.get("must_have_crop") and not req.has_crop:
            eligible = False
            reasons.append("Must have an active crop")

        if eligible:
            eligible_count += 1
            reason = "✅ You are eligible for this scheme!"
        else:
            reason = "❌ Not eligible: " + "; ".join(reasons)

        schemes.append(SchemeInfo(
            id=s["id"], name=s["name"], full_name=s["full_name"],
            description=s["description"], benefit=s["benefit"],
            eligible=eligible, reason=reason,
            documents_required=s["documents_required"], website=s["website"],
        ))

    return SchemeResponse(total_schemes=len(schemes), eligible_count=eligible_count, schemes=schemes)
