from fastapi import APIRouter, HTTPException
from app.models.rental import RentalCreate, RentalResponse, GetRentalResponse
from app.utils.supabase_client import supabase

router = APIRouter(prefix="/rentals", tags=["rentals"])

@router.post("/", response_model=RentalResponse)
def create_rental(rental: RentalCreate):
    exists = supabase.table("customer").select("id").eq("id", rental.customer_id).execute()
    if not exists.data:
        raise HTTPException(status_code=400, detail="Customer does not exist")
    return {"message": "Rental creation is currently disabled."}
    # result = supabase.table("rentals").insert(rental.model_dump()).execute()
    #
    # if not result.data:
    #     raise HTTPException(status_code=400, detail="Failed to create rental")
    #
    # return result.data[0]

@router.get("/{rental_id}", response_model=GetRentalResponse)
def get_rental(rental_id: str):
    result = supabase.table("rental").select("*").eq("id", rental_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Rental not found")

    return result.data[0]