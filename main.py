from http.client import HTTPResponse
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from jwt_secret import JWTSettings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException

# Importing the different routers for the different routes
from routes.auth import router as auth_router
from routes.estate import router as esate_router
from routes.user_role import router as user_role_router
from routes.notification import router as notification_router;
from routes.access_code import router as token_router
from routes.visitor import router as visitor_router
from routes.tenant import router as tenant_router
from routes.user import router as user_router
from routes.support_ticket_type import router as support_ticket_type_router
from routes.support_ticket import router as support_ticket_router
from routes.chat_message import router as chatMessage_router;

from fastapi.responses import HTMLResponse

from dotenv import load_dotenv
import os

load_dotenv()


clinet_url = os.environ.get('CLIENT_SERVER')
chat_server_url = os.environ.get('CHAT_SERVER')


import uvicorn

# Create a FastAPI instance
app = FastAPI()

# Define allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    clinet_url,
    chat_server_url,
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


# Include all routers for their respective routes
app.include_router(user_router)
app.include_router(esate_router)
app.include_router(user_role_router)
app.include_router(notification_router)
app.include_router(auth_router)
app.include_router(token_router)
app.include_router(visitor_router)
app.include_router(tenant_router)
app.include_router(support_ticket_router)
app.include_router(support_ticket_type_router)
app.include_router(chatMessage_router) 

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
