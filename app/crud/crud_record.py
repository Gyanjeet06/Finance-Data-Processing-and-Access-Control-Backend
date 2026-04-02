from datetime import datetime
from typing import Any

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate


def get_record(db: Session, record_id: int) -> Record | None:
    return db.query(Record).filter(Record.id == record_id).first()


def get_records(
    db: Session,
    owner_id: int | None = None,
    category: str | None = None,
    entry_type: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> list[Record]:
    filters = []
    if owner_id is not None:
        filters.append(Record.owner_id == owner_id)
    if category:
        filters.append(Record.category == category)
    if entry_type:
        filters.append(Record.entry_type == entry_type)
    if start_date is not None:
        filters.append(Record.date >= start_date)
    if end_date is not None:
        filters.append(Record.date <= end_date)

    query = db.query(Record)
    if filters:
        query = query.filter(and_(*filters))
    return query.order_by(Record.date.desc()).all()


def create_record(db: Session, record_in: RecordCreate) -> Record:
    record = Record(**record_in.dict())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_record(db: Session, record: Record, updates: RecordUpdate) -> Record:
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(record, field, value)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record: Record) -> None:
    db.delete(record)
    db.commit()


def get_dashboard_summary(db: Session) -> dict[str, Any]:
    rows = db.query(
        Record.entry_type,
        func.sum(Record.amount).label("total"),
    ).group_by(Record.entry_type).all()

    return {row.entry_type: row.total for row in rows}
