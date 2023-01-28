from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.vcac import vcac_router
from domain.program import program_router


app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(vcac_router.router)
app.include_router(program_router.router)
