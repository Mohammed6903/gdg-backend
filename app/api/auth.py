from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.crud import get_user_by_email, create_user
from app.db.session import get_db
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "key01010"  # Use a strong secret in production
ALGORITHM = "HS256"

router = APIRouter()
security = HTTPBearer()

# ======= Schemas =======
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str | None = None
    city: str
    state: str
    country: str
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None = None
    city: str
    state: str
    country: str
    role: str

# ======= Auth Dependency =======
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        user = await get_user_by_email(email, db)  # only function you have
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ======= Routes =======
@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        phone=current_user.phone,
        city=current_user.city,
        state=current_user.state,
        country=current_user.country,
        role=current_user.role
    )

@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    user = await get_user_by_email(request.email, db)
    if not user or not bcrypt.checkpw(request.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token_payload = {
        "userId": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "role": user.role, "token": token}

@router.post("/register")
async def register(request: RegisterRequest, db=Depends(get_db)):
    existing_user = await get_user_by_email(request.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    user_data = request.model_dump()
    user_data["password"] = hashed_password

    user = await create_user(user_data, db)
    return {"message": "Registration successful", "user_id": user.id, "role": user.role}
