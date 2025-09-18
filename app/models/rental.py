import datetime

from pydantic import BaseModel, Field, NaiveDatetime, AwareDatetime


class Rental(BaseModel):
    id: str = Field(..., description="The unique identifier for the customer")
    customer_id: str = Field(..., description="The customer ID")
    rental_date: AwareDatetime = Field(..., description="The date when the rental was made")
    shoe_size: float = Field(..., ge=0, description="The shoe size of the customer, must be non-negative")
    rental_fee: float = Field(..., ge=0, description="The rental fee, must be non-negative")
    discount: float = Field(0, ge=0, description="The discount applied to the rental fee, must be non-negative")
    total_fee: float = Field(..., ge=0, description="The total fee after discount, must be non-negative")


class RentalCreateParameters(BaseModel):
    customer_id: str
    rental_date: datetime.date
    shoe_size: float
    rental_fee: float

class RentalCreate(RentalCreateParameters):
    discount: float
    total_fee: float

class RentalResponse(RentalCreate):
    id: str
    
class GetRentalsResponse(BaseModel):
    rentals: list[RentalResponse]
    
class GetRentalResponse(BaseModel):
    rental: Rental