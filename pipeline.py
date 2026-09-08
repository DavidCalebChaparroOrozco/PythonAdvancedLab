import json


def clear_names(names: list[str]) -> list[str]:
    clean = []
    for i in range(len(names)):
        clean.append(names[i].strip().lower())
    return clean


def load_config(path: str | None = None) -> dict:
    if path is None:
        return "config.json"
    file = open(path)
    data = json.load(file)

    file.close()
    return data


def register(event, history=None):
    if history is None:
        history = []
    history.append(event)
    print(f"event {event} registered, total: {len(history)}")
    return history


def summary(sales: dict[str, float]) -> str:
    total = sum(sales.values())
    return f"total sales: {total}"
