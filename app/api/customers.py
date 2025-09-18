from fastapi import APIRouter, HTTPException
from app.models.customer import CustomerCreate, CustomerResponse
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