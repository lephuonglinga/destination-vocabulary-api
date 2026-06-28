from urllib.parse import unquote

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["vocabulary"])


def register_vocabulary_routes(app_router: APIRouter, data: dict):
    @app_router.get("/api")
    def get_levels():
        return list(data.keys())

    @app_router.get("/api/{level}")
    def get_level(level: str):
        if level not in data:
            raise HTTPException(404)
        return level

    @app_router.get("/api/{level}/units")
    def get_units(level: str):
        if level not in data:
            raise HTTPException(404)
        return list(data[level].keys())

    @app_router.get("/api/{level}/units/{unit_name}")
    def get_terms(level: str, unit_name: str):
        if level not in data:
            raise HTTPException(404)

        unit_name = unquote(unit_name)

        if unit_name not in data[level]:
            raise HTTPException(404)

        return data[level][unit_name]
