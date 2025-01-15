from sqlmodel import Field, SQLModel
import uuid

class Claim(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    service_date: str
    submitted_procedure: str
    quadrant: str | None = None
    plan_group: str
    subscriber: str
    provider_npi: str = Field(index=True) 
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float
    net_fee: float = Field(index=True)
