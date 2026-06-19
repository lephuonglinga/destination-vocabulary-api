# app.py
from fastapi import FastAPI, HTTPException
from urllib.parse import unquote

app = FastAPI()

data = {}


def load_level(level_name: str, path: str):
    units = {}
    current_unit = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("# "):
                current_unit = line[2:]
                units[current_unit] = []
                continue

            if ";" in line and current_unit:
                term, definition = line.split(";", 1)

                units[current_unit].append({
                    "term": term.strip(),
                    "definition": definition.strip()
                })

    return units


@app.on_event("startup")
def startup():
    global data

    data = {
        "b1": load_level("b1", "data/b1.txt"),
        "b2": load_level("b2", "data/b2.txt"),
        "c1&c2": load_level("c1&c2", "data/c1&c2.txt")
    }


@app.get("/")
def root():
    return {"message": "Vocabulary API"}


@app.get("/api")
def get_levels():
    return list(data.keys())


@app.get("/api/{level}")
def get_level(level: str):
    if level not in data:
        raise HTTPException(404)

    return level


@app.get("/api/{level}/units")
def get_units(level: str):
    if level not in data:
        raise HTTPException(404)

    return list(data[level].keys())


@app.get("/api/{level}/units/{unit_name}")
def get_terms(level: str, unit_name: str):
    if level not in data:
        raise HTTPException(404)

    unit_name = unquote(unit_name)

    if unit_name not in data[level]:
        raise HTTPException(404)

    return data[level][unit_name]

