from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db

app = FastAPI(title="Todo API")

# Wide-open CORS is fine for local dev where the frontend and backend run as
# separate containers on different ports. This is NOT a production security
# posture -- we'll tighten it (or drop it entirely in favor of an nginx
# reverse proxy under one origin) in a later phase.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # create_all covers the current single-table schema; once schema changes
    # need to be versioned and reviewable, switch to Alembic migrations.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    # Exercises the DB connection, not just the process -- this is what a
    # Kubernetes readiness probe should check later, so the pod isn't marked
    # ready before it can actually serve traffic.
    db.execute(models.Todo.__table__.select().limit(1))
    return {"status": "ok"}


@app.get("/todos", response_model=list[schemas.TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@app.post("/todos", response_model=schemas.TodoOut, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.patch("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(
    todo_id: int, changes: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return crud.update_todo(db, db_todo, changes)


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    crud.delete_todo(db, db_todo)
