# Coffee Shop API Usage Examples

## Problem Solved

The original error "Did not attempt to load JSON data because the request Content-Type was not 'application/json'" has been fixed. The API now properly handles both JSON and form data requests.

## API Endpoints

### 1. Add a New Cafe - POST /api/v1/cafes/add

**Using JSON (Content-Type: application/json):**

```bash
curl -X POST http://localhost:5000/api/v1/cafes/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My New Cafe",
    "location": "Downtown",
    "map_url": "https://maps.google.com/...",
    "img_url": "https://example.com/cafe.jpg",
    "has_sockets": true,
    "has_toilet": true,
    "has_wifi": true,
    "can_take_calls": false,
    "seats": "20-30",
    "coffee_price": "$4.50"
  }'
```

**Using Form Data:**

```bash
curl -X POST http://localhost:5000/api/v1/cafes/add \
  -F "name=My New Cafe" \
  -F "location=Downtown" \
  -F "map_url=https://maps.google.com/..." \
  -F "img_url=https://example.com/cafe.jpg" \
  -F "has_sockets=True" \
  -F "has_toilet=True" \
  -F "has_wifi=True" \
  -F "can_take_calls=False" \
  -F "seats=20-30" \
  -F "coffee_price=$4.50"
```

### 2. Get All Cafes - GET /all

```bash
curl http://localhost:5000/all
```

### 3. Get Specific Cafe - GET /api/v1/cafes/{id}

```bash
curl http://localhost:5000/api/v1/cafes/1
```

### 4. Update Cafe - PATCH /api/v1/cafes/{id}

```bash
curl -X PATCH http://localhost:5000/api/v1/cafes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "coffee_price": "$5.00",
    "seats": "25-35"
  }'
```

### 5. Delete Cafe - DELETE /api/v1/cafes/{id}

```bash
curl -X DELETE http://localhost:5000/api/v1/cafes/1?api-key=TopSecretAPIKey
```

### 6. Search Cafes by Location - GET /search

```bash
curl "http://localhost:5000/search?loc=London"
```

### 7. Get Random Cafe - GET /random

```bash
curl http://localhost:5000/random
```

## Key Improvements Made

1. **Fixed JSON Content-Type Issue**: The API now properly detects and handles JSON requests using `request.is_json`
2. **Dual Format Support**: Endpoints accept both JSON and form data
3. **Proper Boolean Handling**: String boolean values from forms are correctly converted
4. **Error Handling**: Added comprehensive error handling with proper HTTP status codes
5. **Input Validation**: Required field validation with meaningful error messages
6. **CRUD Operations**: Full Create, Read, Update, Delete functionality
7. **Database Transaction Safety**: Proper rollback on errors

## Response Formats

**Success Response:**

```json
{
  "response": {
    "success": "Successfully added the new cafe."
  }
}
```

**Error Response:**

```json
{
  "error": "Missing required fields: name and location are required"
}
```

**Cafe Data Response:**

```json
{
  "cafe": {
    "id": 1,
    "name": "Science Gallery London",
    "location": "London",
    "map_url": "https://maps.google.com/...",
    "img_url": "https://example.com/cafe.jpg",
    "has_sockets": true,
    "has_toilet": true,
    "has_wifi": true,
    "can_take_calls": false,
    "seats": "20-30",
    "coffee_price": "$4.50"
  }
}
```
