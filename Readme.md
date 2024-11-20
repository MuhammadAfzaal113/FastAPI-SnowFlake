# FastAPI Client Management API

## Requirements

- Python 3.8+
- Snowflake database

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Configure Snowflake credentials in `db_credentials.py`
2. Create the `clients` table:
                                                 
   ```sql
   CREATE TABLE clients (
    id INTEGER AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
                     
### Run FastAPI

```bash
uvicorn main:app --reload
```

## Usage

1. Create a new client:
   - Endpoint: `/clients`
   - Method: `POST`
   - Body: JSON with client details (`name` and `email`)

2. List all clients:
   - Endpoint: `/clients`
   - Method: `GET`

3. Get a specific client:
   - Endpoint: `/clients/{client_id}`
   - Method: `GET`

4. Update a client:
   - Endpoint: `/clients/{client_id}`
   - Method: `PUT`
   - Body: JSON with updated client details (`name` and `email`)

5. Delete a client:
   - Endpoint: `/clients/{client_id}`
   - Method: `DELETE`