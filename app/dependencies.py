from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app import crud, models
from app.database import get_db

DbSession = Annotated[Session, Depends(get_db)]

def get_current_user_from_session(
    request: Request,
    db: DbSession,
) -> models.User | None:
    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    if not str(user_id).isdigit():
        return None

    return crud.get_user_by_id(db, int(user_id))

CurrentUser = Annotated[models.User | None, Depends(get_current_user_from_session)]