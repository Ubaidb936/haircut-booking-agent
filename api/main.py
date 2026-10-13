from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.hair_cut_book import router as hair_cut_bool_router

app = FastAPI(title="HairCut booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hair_cut_bool_router)