from pydantic import BaseModel


def dump_model(model: BaseModel, save_none: bool = False) -> dict:
    """Dumps BaseModel object with optionally skipping None-value fields"""
    if not model: return {}
    return {
        k: v for k, v in model.model_dump().items() 
        if v is not None or save_none
    }


def update_model_from(original: BaseModel, update: BaseModel) -> None:
    """Recursively updates original model with non-None values from update model"""
    for field, value in update.model_dump(exclude_unset=True).items():
        if value is not None:
            if (
                hasattr(original, field) 
                and isinstance(getattr(original, field), BaseModel)
                and isinstance(value, dict)
            ):
                # Recursively update nested models
                update_model_from(getattr(original, field), type(getattr(original, field))(**value))
            else:
                setattr(original, field, value)