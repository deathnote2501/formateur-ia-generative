from fastapi import FastAPI, Depends # Added Depends

from app.core.db_users import auth_backend, get_user_manager # UserManager is not directly used here
from app.core.models import User, UserRead, UserCreate, UserUpdate # User is SQLAlchemy model, others Pydantic
from fastapi_users import FastAPIUsers

app = FastAPI()

# Initialize FastAPIUsers
fastapi_users = FastAPIUsers[User, int]( # User is SQLAlchemy model, int is the ID type
    get_user_manager,
    [auth_backend],
)

# Auth routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
# Register routes
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), # UserRead is response, UserCreate is request
    prefix="/auth",
    tags=["auth"],
)
# Users routes - get_users_router now takes requires_verification directly
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)

# The dependency for current active verified user
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

@app.get("/ping")
async def ping():
    return {"ping": "pong"}

@app.get("/protected-route")
async def protected_route(user: User = Depends(current_active_verified_user)):
    return {"message": f"Hello {user.email}, you are on a protected route!"}
