from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

from response import success_response, error_response

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
        try:
            return json.load(file)
        except (json.JSONDecodeError, TypeError):
            return []

def save_users(users):
    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)

@app.get("/api/users")
def get_users():
    users = load_users()
    return success_response("Users fetched successfully", data=users)

@app.post("/api/users")
def add_user(user: User):
    users = load_users()
    if not isinstance(users, list):
        users = []
    if any(isinstance(u, dict) and u.get('name') == user.name for u in users):
        error_response("User already exists", status_code=400)
    users.append(user.dict())
    save_users(users)
    return success_response("User added successfully", data=user.dict())

@app.delete("/api/users/{index}")
def delete_user(index: int):
    users = load_users()
    if index < 0 or index >= len(users):
        error_response("User not found", status_code=404)
    deleted_user = users.pop(index)
    save_users(users)
    return success_response("User deleted", data=deleted_user)
