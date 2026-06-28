import random
import re

_vocabulary: dict = {}


def strip_term_label(term: str) -> str:
    return re.sub(r"\s+\([^)]+\)$", "", term.strip()).strip()


def set_vocabulary(data: dict):
    global _vocabulary
    _vocabulary = data


def get_terms_for_level(level: str) -> list[str]:
    if level not in _vocabulary:
        return []
    terms = []
    for unit_terms in _vocabulary[level].values():
        for item in unit_terms:
            terms.append(item["term"])
    return terms


def pick_random_distractors(level: str, word: str, count: int = 3) -> list[str]:
    target = strip_term_label(word).lower()
    seen = {target}
    candidates = []

    for term in get_terms_for_level(level):
        clean = strip_term_label(term)
        key = clean.lower()
        if key in seen:
            continue
        seen.add(key)
        candidates.append(clean)

    if len(candidates) < count:
        return []
    return random.sample(candidates, count)


def load_level(path: str) -> dict:
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
                    "definition": definition.strip(),
                })

    return units


def load_vocabulary() -> dict:
    return {
        "b1": load_level("data/b1.txt"),
        "b2": load_level("data/b2.txt"),
        "c1&c2": load_level("data/c1&c2.txt"),
    }
