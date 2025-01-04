from sqlalchemy import select
from sqlmodel import SQLModel, Session


def get_model_by_id(model: type[SQLModel], id: str, db: Session):
    if not isinstance(model, type) or not issubclass(model, SQLModel):
        raise ValueError(f"You must pass a valid SQLModel")
    
    model = db.execute(select(model).where(model.id == id)).scalar_one_or_none()
    return model