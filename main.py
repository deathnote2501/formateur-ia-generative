from fastapi import FastAPI, Depends, APIRouter # Added APIRouter
from fastapi.middleware.cors import CORSMiddleware # New import for CORS

from app.core.db_users import auth_backend, get_user_manager
from app.core.models import User, UserRead, UserCreate, UserUpdate
from fastapi_users import FastAPIUsers

# Import new routers for courses and slides
from app.api.endpoints import courses as courses_router
from app.api.endpoints import slides as slides_router

app = FastAPI(
    title="Formation Platform API",
    description="API for managing courses, slides, and user interactions.",
    version="0.1.0",
    # You can add more metadata here: openapi_url, docs_url, redoc_url, etc.
)

# CORS Middleware Configuration
origins = [
    "http://localhost:5173", # Default SvelteKit dev port
    # "http://localhost:3000", // Example: if you use a different frontend port
    # "https://your-deployed-frontend.com", // Example: deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all standard methods
    allow_headers=["*"], # Allows all headers
)


# Initialize FastAPIUsers
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Auth routes (from fastapi-users)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
# Users routes (from fastapi-users)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True), # requires_verification can be True or False based on your needs
    prefix="/users",
    tags=["users"],
)

# New API v1 router for courses and slides
api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(courses_router.router) # Will be /api/v1/courses
api_router_v1.include_router(slides_router.router)
# Slides router paths like /courses/{id}/slides/ will become /api/v1/courses/{id}/slides/
# and /slides/{id} will become /api/v1/slides/{id}

app.include_router(api_router_v1)


# Root/utility endpoints
@app.get("/ping", tags=["Utilities"])
async def ping():
    """A simple ping endpoint to check if the API is responsive."""
    return {"ping": "pong"}

# Protected route example (can be moved or expanded)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True) # Assuming verified is desired
@app.get("/protected-route", tags=["Tests"])
async def protected_route(user: User = Depends(current_active_verified_user)):
    """A protected route that requires an active and verified user."""
    return {"message": f"Hello {user.email}, you are on a protected route!"}

# Optional: Add startup/shutdown events, middleware, etc.
# @app.on_event("startup")
# async def on_startup():
#     # Initialize database, etc.
#     pass

# @app.on_event("shutdown")
# async def on_shutdown():
#     # Clean up resources
#     pass
