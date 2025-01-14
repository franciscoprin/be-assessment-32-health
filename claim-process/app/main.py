from fastapi import FastAPI, HTTPException, Depends
from app.app_types import ClaimPayload
from app.database import get_session, init_db
from app.models import Claim
from sqlmodel import Session
from contextlib import asynccontextmanager

# Create an instance of the FastAPI class
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database (create tables) on startup
    init_db()
    yield
    # Optionally add shutdown logic here (if needed)

# Register the lifespan event handler
app.lifespan = lifespan

# Endpoint to process and store the claim
@app.post("/claims/")
async def process_claim(payload: ClaimPayload, session: Session = Depends(get_session)):
    try:
        # Calculate the net fee
        net_fee = (
            payload.provider_fees + payload.member_coinsurance + payload.member_copay - payload.allowed_fees
        )

        # Create the claim object to store in the database
        claim = Claim(
            service_date=payload.service_date,
            submitted_procedure=payload.submitted_procedure,
            quadrant=payload.quadrant,
            plan_group=payload.plan_group,
            subscriber=payload.subscriber,
            provider_npi=payload.provider_npi,
            provider_fees=payload.provider_fees,
            allowed_fees=payload.allowed_fees,
            member_coinsurance=payload.member_coinsurance,
            member_copay=payload.member_copay,
            net_fee=net_fee
        )

        # Add the claim to the session
        session.add(claim)

        # Commit the transaction
        session.commit()

        # Refresh the claim object to get the auto-generated id
        session.refresh(claim)

        # Prepare the response with the data including net_fee
        return {
            "id": str(claim.id),  # Return the ID as a string
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
