from fastapi import FastAPI, Depends, HTTPException, status, Query
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

# Пример ролей и разрешений
ROLES = {
    "admin": ["read", "create", "update", "delete"],
    "user": ["read", "update"],
    "guest": ["read"]
}

# Пример пользователей и их ролей
USERS = {
    "admin_user": {"username": "admin_user", "password": "admin_password", "role": "admin"},
    "regular_user": {"username": "regular_user", "password": "user_password", "role": "user"},
    "guest_user": {"username": "guest_user", "password": "guest_password", "role": "guest"}
}

# Секретный ключ для JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user or user["password"] != password:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_password_hash(password: str):
    # В данном примере мы не хешируем пароли, но в реальном приложении это необходимо
    return password

async def get_user(fake_db, username: str):
    if username in fake_db:
        user_dict = fake_db[username]
        return user_dict

async def get_current_user(token: str = Query(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(USERS, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def check_role(role: str):
    async def checker(token: str = Query(...)):
        user = await get_current_user(token)
        if role not in ROLES[user["role"]]:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return True
    return checker

@app.post("/token", response_model=Token)
async def login_for_access_token(username: str = Query(...), password: str = Query(...)):
    user = authenticate_user(USERS, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected_resource")
async def read_protected_resource(token: str = Depends(check_role("read"))):
    return {"message": "This is a protected resource"}

@app.post("/admin_resource")
async def create_resource(token: str = Depends(check_role("create"))):
    return {"message": "Resource created by admin"}

@app.put("/user_resource")
async def update_resource(token: str = Depends(check_role("update"))):
    return {"message": "Resource updated by user"}

@app.get("/guest_resource")
async def read_guest_resource(token: str = Depends(check_role("read"))):
    return {"message": "Resource read by guest"}

