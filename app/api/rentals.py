from fastapi import APIRouter, HTTPException
from app.models.rental import RentalCreateParameters, RentalCreate, RentalResponse, GetRentalResponse
from app.utils.supabase_client import supabase
from app.utils.discount_service import get_discount

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("/", response_model=RentalResponse)
def create_rental(rental: RentalCreateParameters):
    # check customer exists
    user = supabase.table("customer").select("*").eq("id", rental.customer_id).execute()
    if not user.data:
        raise HTTPException(status_code=400, detail="Customer does not exist")

    customer = user.data[0]

    discount_percentage = get_discount(
        age=customer.get("age", 0),
        is_disabled=customer.get("is_disabled", False),
        conditions=customer.get("medical_conditions", []),
    )
    rental_new = RentalCreate(
        **rental.model_dump(),
        discount=discount_percentage,
        total_fee=rental.rental_fee * (1 - discount_percentage / 100)
    )
    
    payload = rental_new.model_dump(mode="json")
    
    result = supabase.table("rental").insert(payload).execute()
    return result.data[0]



@router.get("/{rental_id}", response_model=GetRentalResponse)
def get_rental(rental_id: str):
    result = supabase.table("rental").select("*").eq("id", rental_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Rental not found")

    return {"rental": result.data[0]}