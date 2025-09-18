from fastapi import APIRouter, HTTPException
from app.models.rental import RentalCreate, RentalResponse
from app.utils.supabase_client import supabase

