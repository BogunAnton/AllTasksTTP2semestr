from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

expected_username = "user"
expected_password = "password"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == expected_username
    correct_password = credentials.password == expected_password
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/login")
async def login(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return "You got my secret, welcome"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)