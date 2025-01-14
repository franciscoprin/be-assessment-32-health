from pydantic import BaseModel, Field, field_validator
import re

# Define the Pydantic model for the incoming JSON payload
class ClaimPayload(BaseModel):
    service_date: str = Field(..., description="The date the service was provided")
    submitted_procedure: str = Field(..., description="The procedure code submitted, must begin with 'D'")
    # quadrant is not a required field.
    quadrant: str | None = Field(None, description="The quadrant where the procedure was performed")
    plan_group: str = Field(..., description="The plan or group number associated with the claim")
    subscriber: str = Field(..., description="The subscriber's identification number")
    provider_npi: str = Field(..., description="The 10-digit National Provider Identifier (NPI) of the provider")
    provider_fees: float = Field(..., description="The provider's fees for the service")
    allowed_fees: float = Field(..., description="The allowed fees for the procedure")
    member_coinsurance: float = Field(..., description="The member's coinsurance amount")
    member_copay: float = Field(..., description="The member's copay amount")

    # Replace @validator with @field_validator
    @field_validator('submitted_procedure')
    def validate_submitted_procedure(cls, value):
        if not value.startswith('D'):
            raise ValueError('Submitted procedure must start with "D"')
        return value

    @field_validator('provider_npi')
    def validate_provider_npi(cls, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError('Provider NPI must be a 10-digit number')
        return value
