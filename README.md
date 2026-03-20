# FastAPI SQLiteDB Demo API Project: Order Management API

This project is a simple CRUD API for managing orders using:

- FastAPI
- SQLAlchemy ORM
- SQLite database

## Project Structure

- app.py: FastAPI app, SQLAlchemy model, and CRUD endpoints
- requirements.txt: Python dependencies
- orders.db: SQLite database file (created automatically)

## Requirements

- Python 3.8+

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the development server:

```bash
uvicorn app:app --reload
```

API base URL:

```text
http://127.0.0.1:8000
```

## API Endpoints

Base path: `/api/orders`

1. `GET /api/orders`
Returns all orders.

2. `POST /api/orders`
Creates a new order.

Request body example:

```json
{
  "item_name": "Notebook",
  "quantity": 3,
  "price": 129.99
}
```

3. `PUT /api/orders/{order_id}`
Updates an existing order by ID.

Request body example:

```json
{
  "item_name": "Notebook Pro",
  "quantity": 4,
  "price": 149.99
}
```

4. `DELETE /api/orders/{order_id}`
Deletes an order by ID.

If an order does not exist for update/delete, the API returns `404 Order not found`.

## Interactive Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Database Notes

Current setting (persistent on disk):

```python
DATABASE_URL = "sqlite:///./orders.db"
```

Data is saved in the `orders.db` file in the project directory.

Optional setting (temporary in RAM):

```python
DATABASE_URL = "sqlite:///:memory:"
```

Use this if you want process-memory storage only. Data is cleared when the server restarts.
