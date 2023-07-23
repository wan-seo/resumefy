from dataclasses import dataclass, field
from typing import Any, Dict, Iterable


def all_dict_list(value: Any) -> bool:
    return isinstance(value, list) and all_dict(value)


def all_dict(value: Iterable) -> bool:
    return all(isinstance(item, dict) for item in value)


def create_dataclass(classname: str, data: Dict[str, Any]) -> Any:
    fields = {}
    for key, value in data.items():
        if isinstance(value, dict):
            fields[key] = field(
                default_factory=lambda: instantiate_dataclass(key, value)
            )
        elif all_dict_list(value):
            fields[key] = field(
                default_factory=lambda: [
                    instantiate_dataclass(key, item) for item in value
                ]
            )
        else:
            fields[key] = None

    new_class = type(classname, (), {"__annotations__": fields})
    return dataclass(new_class)


def instantiate_dataclass(classname: str, data: Dict[str, Any]) -> Any:
    new_class = create_dataclass(classname.capitalize(), data)
    instance_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            instance_data[key] = instantiate_dataclass(key, value)
        elif all_dict_list(value):
            instance_data[key] = [
                instantiate_dataclass(key, item) for item in value
            ]  # noqa
        else:
            instance_data[key] = value
    instance = new_class(**instance_data)

    return instance
