from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.crud.crud_record import create_record, delete_record, get_record, get_records, update_record
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate

router = APIRouter()


@router.post("/", response_model=RecordRead, summary="Create a financial record")
def add_record(record_in: RecordCreate, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    return create_record(db, record_in)


@router.get("/", response_model=list[RecordRead], summary="List financial records")
def list_records(
    category: str | None = Query(None, description="Filter by category"),
    entry_type: str | None = Query(None, description="Filter by entry type: income or expense"),
    start_date: datetime | None = Query(None, description="Filter records from this date"),
    end_date: datetime | None = Query(None, description="Filter records until this date"),
    db: Session = Depends(get_db),
    _=Depends(require_roles("analyst", "admin")),
):
    return get_records(db, category=category, entry_type=entry_type, start_date=start_date, end_date=end_date)


@router.get("/{record_id}", response_model=RecordRead, summary="Get a record by id")
def read_record(record_id: int, db: Session = Depends(get_db), _=Depends(require_roles("analyst", "admin"))):
    record = get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=RecordRead, summary="Update a financial record")
def change_record(record_id: int, updates: RecordUpdate, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    record = get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return update_record(db, record, updates)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a financial record")
def remove_record(record_id: int, db: Session = Depends(get_db), _=Depends(require_roles("admin"))):
    record = get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    delete_record(db, record)
