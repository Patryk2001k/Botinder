from contextlib import contextmanager
from app.models import Session, User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_user_by_username(username: str) -> dict:
    with session_scope() as session:
        query = select(User).where(User.username == username)
        result = session.execute(query).scalars().first()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        dict_name = result.username
        dict_name = {
            'username': result.username,
            'hashed_password': result.hashed_password,
            'disabled': result.disabled
        }
        return dict_name

def create_user(username: str, hashed_password: str, disabled: bool) -> dict:
    with session_scope() as session:
        new_user = User(username=username, hashed_password=hashed_password, disabled=disabled)
        try:
            session.add(new_user)
            session.commit()

            dict_name = new_user.username
            dict_name = {
                'username': new_user.username,
                'hashed_password': new_user.hashed_password,
                'disabled': new_user.disabled
            }
            return dict_name
        except SQLAlchemyError as e:
            session.rollback()
            return {'error': str(e)}

