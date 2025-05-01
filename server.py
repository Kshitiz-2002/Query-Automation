from fastapi import FastAPI, routing, Response
from fastapi.middleware.cors import CORSMiddleware 
from routers.query.query import router as query_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(query_router)

@app.get('/')
def _default_router():
    return Response('Server is running!')

