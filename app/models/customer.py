from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Customer(BaseModel):
    id: str = Field(..., description="The unique identifier for the customer")
    name: str = Field(..., description="The full name of the customer")
    age: int = Field(..., ge=0, description="The age of the customer, must be non-negative")
    contact_info: EmailStr = Field(..., description="The email address of the customer")
    is_disabled: bool = Field(False, description="Indicates if the customer is disabled")
    medical_conditions: Optional[str] = Field(None, description="Any medical conditions the customer has")