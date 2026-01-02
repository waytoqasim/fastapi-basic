from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="User Management API")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

FILE_NAME = "users.json"

class User(BaseModel):
    name: str
    age: int

def load_users():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

def save_users(users):
    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)

@app.get("/api/users")
def get_users():
    return load_users()

@app.post("/api/users")
def add_user(user: User):
    users = load_users()
    users.append(user.dict())
    save_users(users)
    return {"message": "User added successfully", "user": user}

@app.delete("/api/users/{index}")
def delete_user(index: int):
    users = load_users()
    if index < 0 or index >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users.pop(index)
    save_users(users)
    return {"message": "User deleted", "user": deleted_user}
