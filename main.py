from fastapi import FastAPI, HTTPException

from db_connector import get_connection
from models import ClientCreate, ClientUpdate

app = FastAPI()


@app.post("/clients", status_code=201)
def create_client(client: ClientCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO clients (name, email, created_at)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            RETURNING id, name, email, created_at
            """,
            (client.name, client.email)
        )
        result = cursor.fetchone()
        if result:
            return {"id": result[0], "name": result[1], "email": result[2], "created_at": result[3]}
        else:
            raise HTTPException(status_code=500, detail="Failed to create client.")
    finally:
        cursor.close()
        conn.close()


@app.get("/clients")
def get_all_clients():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email, created_at FROM clients")
        clients = cursor.fetchall()
        return [
            {"id": row[0], "name": row[1], "email": row[2], "created_at": row[3]} for row in clients
        ]
    finally:
        cursor.close()
        conn.close()


@app.get("/clients/{id}")
def get_client_by_id(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email, created_at FROM clients WHERE id = %s", (id,))
        client = cursor.fetchone()
        if client:
            return {"id": client[0], "name": client[1], "email": client[2], "created_at": client[3]}
        else:
            raise HTTPException(status_code=404, detail="Client not found.")
    finally:
        cursor.close()
        conn.close()


@app.put("/clients/{id}")
def update_client(id: int, client: ClientUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM clients WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Client not found.")

        updates = []
        params = []
        if client.name:
            updates.append("name = %s")
            params.append(client.name)
        if client.email:
            updates.append("email = %s")
            params.append(client.email)

        params.append(id)
        update_query = f"UPDATE clients SET {', '.join(updates)} WHERE id = %s RETURNING id, name, email, created_at"
        cursor.execute(update_query, params)
        updated_client = cursor.fetchone()

        return {"id": updated_client[0], "name": updated_client[1], "email": updated_client[2],
                "created_at": updated_client[3]}
    finally:
        cursor.close()
        conn.close()


@app.delete("/clients/{id}", status_code=204)
def delete_client(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM clients WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Client not found.")

        cursor.execute("DELETE FROM clients WHERE id = %s", (id,))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Client deleted successfully."}
