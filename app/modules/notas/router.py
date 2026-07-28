from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.models import User
from app.modules.notas import service
from app.modules.notas.schemas import NoteCreate, NoteRead, NoteUpdate

router = APIRouter(prefix="/notas", tags=["notas"])


@router.get("", response_model=list[NoteRead])
def list_notas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return service.list_notes(db, current_user.id)


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_nota(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_note(db, current_user.id, payload)


@router.get("/{note_id}", response_model=NoteRead)
def get_nota(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_note_for_user(db, note_id, current_user.id)


@router.patch("/{note_id}", response_model=NoteRead)
def update_nota(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = service.get_note_for_user(db, note_id, current_user.id)
    return service.update_note(db, note, payload)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nota(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    note = service.get_note_for_user(db, note_id, current_user.id)
    service.delete_note(db, note)
