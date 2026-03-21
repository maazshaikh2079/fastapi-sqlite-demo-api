from pydantic import BaseModel, ConfigDict
from typing import Optional


# Pydantic Schemas (Data Transfer Objects) :-

# Base Logic (Shared fields)
class OrderBase(BaseModel):
    """Base schema for an order, used for shared properties."""

    name: str
    description: str
    quantity: int
    price: float


# For Creating (No ID needed, DB handles it)
class OrderCreate(OrderBase):
    """Schema for creating a new order. Inherits from OrderBase."""

    pass


# For Updating (All fields optional, NO ID allowed in body)
class OrderUpdate(OrderBase):
    """Schema for updating an existing order. All fields are optional."""

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


# For Returning Data (Includes the ID)
class OrderOut(OrderBase):
    """Schema for returning an order, includes the database ID."""

    id: int

    # Pydantic V2 config to allow ORM model mapping
    model_config = ConfigDict(from_attributes=True)
