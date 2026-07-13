from sqlalchemy.orm import Session

from app import models, schemas


def get_todos(db: Session) -> list[models.Todo]:
    return db.query(models.Todo).order_by(models.Todo.id).all()


def get_todo(db: Session, todo_id: int) -> models.Todo | None:
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_todo(db: Session, todo: schemas.TodoCreate) -> models.Todo:
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(
    db: Session, db_todo: models.Todo, changes: schemas.TodoUpdate
) -> models.Todo:
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(db_todo, field, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, db_todo: models.Todo) -> None:
    db.delete(db_todo)
    db.commit()
