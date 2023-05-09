from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi_jwt_auth import AuthJWT
from jwt_secret import JWTSettings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic.error_wrappers import ValidationError as PydanticValidationError

# Importing the different routers for the different routes
from routes.auth import router as auth_router
from routes.access_code import router as token_router
from routes.visitor import router as visitor_router
from routes.tenant import router as tenant_router
from routes.chat import router as chat_router
from routes.user import router as user_router

import uvicorn

# Create a FastAPI instance
app = FastAPI()

# Define allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:58875",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load JWT config
@AuthJWT.load_config
def get_config():
    return JWTSettings()

# Handle AuthJWTExceptions
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )


# Include all routers for their respective routes
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(token_router)
app.include_router(visitor_router)
app.include_router(tenant_router)
app.include_router(chat_router)

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
