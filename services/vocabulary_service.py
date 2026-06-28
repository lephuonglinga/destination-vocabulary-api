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
