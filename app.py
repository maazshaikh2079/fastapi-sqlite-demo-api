from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Integer, String, Float
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, Mapped, mapped_column
from pydantic import BaseModel, ConfigDict
from typing import List


# Database Configuration :-

# DATABASE_URL = "sqlite:///:memory:"  # DB is stored only in RAM (process memory).
DATABASE_URL = "sqlite:///./orders.db"  # Persistent file-based data (DB) storage

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # `connect_args` is for SQLite only to allow multithreaded access.
    poolclass=StaticPool,  # `StaticPool` is used for in-memory DB to ensure the same connection is used.
)

# Create a sessionmaker to generate new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# SQLAlchemy ORM / DB Model :-

class DBOrder(Base):
    """SQLAlchemy model for the 'orders' table."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    price: Mapped[float] = mapped_column(Float,  nullable=False)


# Create all tables in the database based on the Base metadata
Base.metadata.create_all(bind=engine)


# Pydantic Schemas (Data Transfer Objects) :-

class OrderBase(BaseModel):
    """Base schema for an order, used for shared properties."""

    item_name: str
    quantity: int
    price: float


class OrderCreate(OrderBase):
    """Schema for creating a new order. Inherits from OrderBase."""

    pass


class OrderOut(OrderBase):
    """Schema for returning an order, includes the database ID."""

    id: int

    # Pydantic V2 config to allow ORM model mapping
    model_config = ConfigDict(from_attributes=True)


# FastAPI Application
app = FastAPI(
    title="Order Management API",
    description="A simple CRUD API for managing orders with FastAPI and SQLite.",
    version="1.0.0",
)


# Database Dependency
def get_db():
    """
    Dependency to get a database session for a request.
    Ensures the session is closed after the request is finished.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API Endpoints :-

@app.get("/api/orders", response_model=List[OrderOut], tags=["Orders"])
def get_orders(db: Session = Depends(get_db)):
    """Retrieve all orders from the database."""

    orders = db.query(DBOrder).all()

    return orders


@app.get("/api/orders/{order_id}", response_model=OrderOut, tags=["Orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order by its ID."""

    # db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    db_order = db.get(DBOrder, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.post("/api/orders", response_model=OrderOut, status_code=201, tags=["Orders"])
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order and store it in the database."""

    db_order = DBOrder(**order_in.model_dump())
    db.add(db_order)

    db.commit()
    db.refresh(db_order)

    return db_order


@app.put("/api/orders/{order_id}", response_model=OrderOut, tags=["Orders"])
def update_order(order_id: int, order_in: OrderCreate, db: Session = Depends(get_db)):
    """Update an existing order by its ID."""

    db_order = db.get(DBOrder, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order w/ ID {order_id} not found")

    # Update model fields from the input schema
    update_data = order_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


@app.delete("/api/orders/{order_id}", status_code=204, tags=["Orders"])
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order from the database by its ID."""

    db_order = db.get(DBOrder, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order w/ ID {order_id} not found")

    db.delete(db_order)
    db.commit()

    # No content to return on successful deletion
    return None
