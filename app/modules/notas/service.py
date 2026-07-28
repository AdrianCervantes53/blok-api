from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.notas.models import Note
from app.modules.notas.schemas import NoteCreate, NoteUpdate


def list_notes(db: Session, user_id: int) -> list[Note]:
    return list(
        db.scalars(
            select(Note).where(Note.user_id == user_id).order_by(Note.updated_at.desc())
        ).all()
    )


def get_note_for_user(db: Session, note_id: int, user_id: int) -> Note:
    note = db.get(Note, note_id)
    if note is None or note.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


def create_note(db: Session, user_id: int, payload: NoteCreate) -> Note:
    note = Note(user_id=user_id, title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note: Note, payload: NoteUpdate) -> Note:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(note, field, value)
    note.updated_at = datetime.now(UTC)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()
