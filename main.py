from fastapi import FastAPI
from src.routes.ws import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.mount('/', app=sio_app)






