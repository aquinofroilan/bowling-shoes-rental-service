from fastapi import APIRouter, HTTPException
from app.models.customer import CustomerCreate, CustomerResponse
from app.models.rental import  GetRentalsResponse
from app.utils.supabase_client import supabase

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate):
    result = supabase.table("customers").insert(customer.model_dump()).execute()

    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create customer")

    return result.data[0]

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str):
    result = supabase.table("customers").select("*").eq("id", customer_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Customer not found")

    return result.data[0]

@router.get("rentals/{customer_id}", response_model=GetRentalsResponse)
def get_customer_rentals(customer_id: str, page: int = 1, size: int = 10):
    offset = (page - 1) * size
    result = supabase.table("rentals").select("*").eq("customer_id", customer_id).range(offset, offset + size - 1).execute()
    total_result = supabase.table("rentals").select("id", count="exact").eq("customer_id", customer_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="No rentals found for this customer")

    return {
        "rentals": result.data,
        "total": total_result.count,
        "page": page,
        "size": size
    }