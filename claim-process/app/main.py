from fastapi import FastAPI, HTTPException, Depends
try:
    from app.app_types import ClaimPayload
    from app.database import get_session, init_db
    from app.models import Claim
except ModuleNotFoundError:
    from app_types import ClaimPayload
    from database import get_session, init_db
    from models import Claim
from sqlalchemy import func
from sqlmodel import Session
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create an instance of the FastAPI class
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database (create tables) on startup
    init_db()
    yield
    # Optionally add shutdown logic here (if needed)

# Register the lifespan event handler
app.lifespan = lifespan

# Define the endpoint to get the top 10 provider NPIs by net fees
@app.get("/top-providers/")
@limiter.limit("10/minute")  # Rate limit: 10 requests per minute
async def get_top_providers(request: Request, session: Session = Depends(get_session)):
    try:
        # Query to calculate the sum of net_fee for each provider_npi
        results = (
            session.query(Claim.provider_npi, func.sum(Claim.net_fee).label("total_net_fee"))
            .group_by(Claim.provider_npi)
            .order_by(func.sum(Claim.net_fee).desc())
            .limit(10)
            .all()
        )

        # Prepare the response as a list of dictionaries
        top_providers = [
            {"provider_npi": provider_npi, "total_net_fee": total_net_fee}
            for provider_npi, total_net_fee in results
        ]

        return {"top_providers": top_providers}

    except RateLimitExceeded:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
