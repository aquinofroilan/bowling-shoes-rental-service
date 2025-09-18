# Bowling Shoes Rental Service

A FastAPI-based backend for managing bowling shoe rentals and customer data, with Supabase as the backend database and an AI-powered discount engine.

---

## Table of Contents

- [Project Description](#project-description)
- [Setup & Installation](#setup--installation)
- [API Endpoints](#api-endpoints)
  - [Root Endpoints](#root-endpoints)
  - [Customer Endpoints](#customer-endpoints)
  - [Rental Endpoints](#rental-endpoints)
- [Error Responses](#error-responses)
- [Discount Engine](#discount-engine)
- [Data Models](#data-models)
- [Environment Variables](#environment-variables)
- [Running the Service](#running-the-service)
- [Testing](#testing)
- [Contributing](#contributing)

---

## Project Description

This service provides endpoints to manage customers and their bowling shoe rentals. It features:
- Customer creation and retrieval
- Rental creation and retrieval
- Automatic discount calculation based on age, disability, and medical conditions (using a generative AI model)
- Supabase as the backend database

---

## Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd bowling-shoes-rental-service
   ```

2. **Install dependencies:**
   - Using pipenv:
     ```sh
     pipenv install
     ```
   - Or with Docker:
     ```sh
     docker-compose up --build
     ```

3. **Environment Variables:**
   - Create a `.env` file in the project root with your Supabase credentials and any other required secrets.

---

## API Endpoints

### Root Endpoints

#### `GET /`
**Description:** Health check endpoint that returns a welcome message.

**Parameters:** None

**Response:**
```json
{
  "message": "Hello World"
}
```

**Status Codes:**
- `200 OK` - Success

---

#### `GET /hello/{name}`
**Description:** Returns a personalized greeting message.

**Parameters:**
- `name` (path parameter, required): `string` - The name to greet

**Example Request:**
```
GET /hello/John
```

**Response:**
```json
{
  "message": "Hello John"
}
```

**Status Codes:**
- `200 OK` - Success

---

### Customer Endpoints

#### `POST /customers/`
**Description:** Create a new customer in the system.

**Request Body:** `CustomerCreate`
```json
{
  "name": "John Doe",
  "age": 30,
  "contact_info": "john.doe@email.com",
  "is_disabled": false,
  "medical_conditions": "Diabetes, Hypertension"
}
```

**Request Body Parameters:**
- `name` (required): `string` - Full name of the customer
- `age` (required): `integer` - Age of the customer (≥ 0)
- `contact_info` (required): `string` - Email address or contact information
- `is_disabled` (optional): `boolean` - Whether the customer has a disability (default: false)
- `medical_conditions` (optional): `string` - Any medical conditions the customer has

**Response:** `CustomerResponse`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "age": 30,
  "contact_info": "john.doe@email.com",
  "is_disabled": false,
  "medical_conditions": "Diabetes, Hypertension"
}
```

**Status Codes:**
- `200 OK` - Customer created successfully
- `400 Bad Request` - Failed to create customer or validation error

---

#### `GET /customers/{customer_id}`
**Description:** Retrieve a specific customer by their ID.

**Parameters:**
- `customer_id` (path parameter, required): `string` - UUID of the customer

**Example Request:**
```
GET /customers/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `CustomerResponse`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "age": 30,
  "contact_info": "john.doe@email.com",
  "is_disabled": false,
  "medical_conditions": "Diabetes, Hypertension"
}
```

**Status Codes:**
- `200 OK` - Customer found and returned
- `404 Not Found` - Customer not found

---

#### `GET /customers/rentals/{customer_id}`
**Description:** Get all rental records for a specific customer.

**Parameters:**
- `customer_id` (path parameter, required): `string` - UUID of the customer

**Example Request:**
```
GET /customers/rentals/550e8400-e29b-41d4-a716-446655440000
```

**Response:** `GetRentalsResponse`
```json
{
  "rentals": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "customer_id": "550e8400-e29b-41d4-a716-446655440000",
      "rental_date": "2025-09-18",
      "shoe_size": 42.0,
      "rental_fee": 10.0,
      "discount": 15.0,
      "total_fee": 8.5
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "customer_id": "550e8400-e29b-41d4-a716-446655440000",
      "rental_date": "2025-09-15",
      "shoe_size": 41.5,
      "rental_fee": 12.0,
      "discount": 15.0,
      "total_fee": 10.2
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Rentals found and returned
- `404 Not Found` - No rentals found for this customer

---

### Rental Endpoints

#### `POST /rentals/`
**Description:** Create a new rental for an existing customer. Automatically calculates discounts based on customer profile.

**Request Body:** `RentalCreateParameters`
```json
{
  "customer_id": "550e8400-e29b-41d4-a716-446655440000",
  "rental_date": "2025-09-18",
  "shoe_size": 42.0,
  "rental_fee": 10.0
}
```

**Request Body Parameters:**
- `customer_id` (required): `string` - UUID of the existing customer
- `rental_date` (required): `string` - Date of rental in YYYY-MM-DD format
- `shoe_size` (required): `number` - Shoe size (≥ 0)
- `rental_fee` (required): `number` - Base rental fee before discount (≥ 0)

**Response:** `RentalResponse`
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "customer_id": "550e8400-e29b-41d4-a716-446655440000",
  "rental_date": "2025-09-18",
  "shoe_size": 42.0,
  "rental_fee": 10.0,
  "discount": 15.0,
  "total_fee": 8.5
}
```

**Status Codes:**
- `200 OK` - Rental created successfully
- `400 Bad Request` - Customer does not exist or validation error

---

#### `GET /rentals/{rental_id}`
**Description:** Retrieve a specific rental by its ID.

**Parameters:**
- `rental_id` (path parameter, required): `string` - UUID of the rental

**Example Request:**
```
GET /rentals/660e8400-e29b-41d4-a716-446655440001
```

**Response:** `GetRentalResponse`
```json
{
  "rental": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "customer_id": "550e8400-e29b-41d4-a716-446655440000",
    "rental_date": "2025-09-18T00:00:00Z",
    "shoe_size": 42.0,
    "rental_fee": 10.0,
    "discount": 15.0,
    "total_fee": 8.5
  }
}
```

**Status Codes:**
- `200 OK` - Rental found and returned
- `404 Not Found` - Rental not found

---

## Error Responses

All endpoints may return the following error format:

```json
{
  "detail": "Error message description"
}
```

**Common Status Codes:**
- `400 Bad Request` - Invalid input data or business logic violation
- `404 Not Found` - Requested resource does not exist
- `422 Unprocessable Entity` - Validation error in request body
- `500 Internal Server Error` - Server-side error

---

## Discount Engine

Discounts are automatically applied when creating a rental, based on:
- **Age Groups:**
  - 0-12 years: 20% discount
  - 13-18 years: 10% discount
  - 65+ years: 15% discount
- **Disability:** 25% discount
- **Medical Conditions:** 10% discount each for:
  - Diabetes
  - Hypertension
  - Chronic Condition

**Important:** Only the highest applicable discount is used. The discount calculation is powered by Google's Gemini AI model.

---

## Data Models

### Customer

```json
{
  "id": "string (UUID)",
  "name": "string",
  "age": "integer (≥ 0)",
  "contact_info": "string",
  "is_disabled": "boolean",
  "medical_conditions": "string | null"
}
```

### Rental

```json
{
  "id": "string (UUID)",
  "customer_id": "string (UUID)",
  "rental_date": "string (ISO date) | datetime",
  "shoe_size": "number (≥ 0)",
  "rental_fee": "number (≥ 0)",
  "discount": "number (≥ 0)",
  "total_fee": "number (≥ 0)"
}
```

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GOOGLE_API_KEY=your_google_api_key
```

---

## Running the Service

### Locally
```sh
pipenv install
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### With Docker
```sh
docker-compose up --build
```

The API will be available at `http://localhost:8000`

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Testing

### Using the HTTP file
Use the included `test_main.http` file with your IDE's HTTP client.

### Manual Testing Examples

**Create a customer:**
```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "age": 12,
    "contact_info": "alice@example.com",
    "is_disabled": false,
    "medical_conditions": null
  }'
```

**Create a rental:**
```bash
curl -X POST "http://localhost:8000/rentals/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "your-customer-id-here",
    "rental_date": "2025-09-18",
    "shoe_size": 38.5,
    "rental_fee": 15.0
  }'
```

---

## Contributing

- Follow standard Python and FastAPI best practices
- Use type hints and Pydantic models for data validation
- Write tests for new endpoints and features
- Update this documentation when adding new endpoints
- Follow conventional commit messages

**Code Style:**
- Use `black` for code formatting
- Use `isort` for import sorting
- Follow PEP 8 guidelines

---
