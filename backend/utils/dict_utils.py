def to_dict_safe(obj):
    """
    Convierte un objeto Pydantic u objeto con .dict() / .model_dump() en dict.
    Si ya es dict, lo devuelve igual.
    """
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump()
    elif hasattr(obj, "dict"):     # Pydantic v1
        return obj.dict()
    elif isinstance(obj, dict):
        return obj
    else:
        # Fallback: lo convertimos por fuerza con vars()
        return vars(obj)
