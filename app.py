from fastapi import FastAPI

from controllers.coach_controller import router as coach_router
from controllers.exam_controller import router as exam_router
from controllers.vocabulary_controller import register_vocabulary_routes
from services.vocabulary_service import load_vocabulary, set_vocabulary

app = FastAPI(title="Destination Vocabulary API")

data = {}


@app.on_event("startup")
def startup():
    global data
    data = load_vocabulary()
    set_vocabulary(data)
    register_vocabulary_routes(app, data)


@app.get("/")
def root():
    return {"message": "Vocabulary API"}


app.include_router(coach_router, prefix="/api")
app.include_router(exam_router, prefix="/api")
