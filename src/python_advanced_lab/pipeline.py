import json
from typing import Any

def clear_names(names: list[str]) -> list[str]:
    clean = []
    for i in range(len(names)):
        clean.append(names[i].strip().lower())
    return clean


def load_config(path: str | None = None) -> dict[str, Any]:
    target_path = path if path is not None else "config.json"  # noqa: E711
    with open(target_path, "r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)
    file.close()
    return data


def register(event: str, history: list[str] | None = None) -> list[str]:
    if history is None:
        history = []
    history.append(event)
    print(f"event {event} registered, total: {len(history)}")
    return history


def summary(sales: dict[str, float]) -> str:
    total = sum(sales.values())
    return f"total sales: {total}"
