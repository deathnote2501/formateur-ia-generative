from fastapi import FastAPI, Depends

# Assuming User, UserCreate, UserRead, UserUpdate are defined as planned
from app.core.schemas import UserCreate, UserRead, UserUpdate
from app.core.models import auth_backend, fastapi_users # User model is used by fastapi_users

app = FastAPI()

# Include JWT auth router
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# Include register router
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# Include users router
# This requires UserUpdate schema, which we created in the previous step.
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Placeholder for current_user dependency for protected routes
# from app.core.models import User # Already imported via fastapi_users
# current_active_user = fastapi_users.current_user(active=True)

# Example of a protected route:
# @app.get("/protected-route")
# async def protected_route(user: User = Depends(current_active_user)):
# return {"message": f"Hello {user.email}!"}

# Placeholder for database initialization or other startup events
# @app.on_event("startup")
# async def on_startup():
#     # Initialize database, etc.
#     pass
