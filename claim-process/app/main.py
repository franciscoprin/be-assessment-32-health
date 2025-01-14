from fastapi import FastAPI, HTTPException
from app.app_types import ClaimPayload

# Create an instance of the FastAPI class
app = FastAPI()

# Endpoint to process and store the claim
@app.post("/claims/")
async def process_claim(payload: ClaimPayload):
    try:
        # Calculate the net fee
        net_fee = (
            payload.provider_fees + payload.member_coinsurance + payload.member_copay - payload.allowed_fees
        )
        
        # Prepare the response with the data including net_fee
        return {
            "service_date": payload.service_date,
            "submitted_procedure": payload.submitted_procedure,
            "quadrant": payload.quadrant,
            "plan_group": payload.plan_group,
            "subscriber": payload.subscriber,
            "provider_npi": payload.provider_npi,
            "provider_fees": payload.provider_fees,
            "allowed_fees": payload.allowed_fees,
            "member_coinsurance": payload.member_coinsurance,
            "member_copay": payload.member_copay,
            "net_fee": net_fee
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
