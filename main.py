from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

# Import the specific Pydantic schemas we created
from schemas import OrderCreate, OrderUpdate, OrderOut
from db_config import SessionLocal, engine
from db_models import Base, Order as DBOrder
# from db_models import Order as DBOrder

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Standardized dummy data for initialization
# Note: Using models.OrderCreate fields (no ID) because DB will generate it
initial_orders = [
    {"name": "Laptop", "description": "A new laptop", "price": 1200.00, "quantity": 1},
    {"name": "Book", "description": "A fiction book", "price": 25.50, "quantity": 2},
    {"name": "Coffee", "description": "A bag of coffee beans", "price": 15.00, "quantity": 1},
    {"name": "Desk Chair", "description": "An ergonomic desk chair", "price": 250.00, "quantity": 1},
]

def init_db():
    """Initializes the database with sample data if the table is empty."""

    db = SessionLocal()

    try:
        existing_count = db.query(DBOrder).count()
        if existing_count == 0:
            for order in initial_orders:
                db.add(DBOrder(**order))
            db.commit()
            print("Database initialized with sample orders.")

    finally:
        db.close()

init_db()


def get_db():
    """Dependency to provide a database session per request."""

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


app = FastAPI(title="Order Management API")


@app.get("/", tags=["Health"])
def health_status():

    return {"status": "Healthy"}


@app.get("/orders/", response_model=List[OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    """Fetches all orders from the database."""

    return db.query(DBOrder).all()


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    """Fetches a single order by its unique ID."""

    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )

    return db_order


@app.post("/orders/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """Creates a new order record."""

    new_order = DBOrder(**order_in.model_dump())
    db.add(new_order)

    db.commit()
    db.refresh(new_order)

    return new_order


@app.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_in: OrderUpdate, db: Session = Depends(get_db)):
    """Updates an existing order using a dynamic loop."""

    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )

    # Convert Pydantic model to dict, ignoring fields not provided by user
    update_data = order_in.model_dump(exclude_unset=True)

    # Update only the attributes present in the dictionary
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Deletes a order record."""

    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()

    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )

    db.delete(db_order)
    db.commit()
    return None # 204 status code requires no content
