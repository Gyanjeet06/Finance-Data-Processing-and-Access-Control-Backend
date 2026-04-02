from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.crud.crud_record import get_records
from app.schemas.record import RecordRead

router = APIRouter()


@router.get("/summary", summary="Dashboard summary")
def dashboard_summary(db: Session = Depends(get_db), _=Depends(require_roles("viewer", "analyst", "admin"))):
    records = get_records(db)
    totals = {"income": 0.0, "expense": 0.0}
    category_totals: dict[str, float] = defaultdict(float)
    recent_activity: list[RecordRead] = []

    for record in records:
        totals[record.entry_type] += record.amount
        category_totals[record.category or "Uncategorized"] += record.amount

    recent_records = sorted(records, key=lambda r: r.date, reverse=True)[:5]
    recent_activity = [RecordRead.from_orm(record) for record in recent_records]

    return {
        "total_income": totals["income"],
        "total_expense": totals["expense"],
        "net_balance": totals["income"] - totals["expense"],
        "category_totals": category_totals,
        "recent_activity": recent_activity,
    }


@router.get("/trends", summary="Dashboard trends")
def dashboard_trends(db: Session = Depends(get_db), _=Depends(require_roles("analyst", "admin"))):
    records = get_records(db)
    monthly_totals: dict[str, dict[str, float]] = {}

    for record in records:
        month = record.date.strftime("%Y-%m")
        if month not in monthly_totals:
            monthly_totals[month] = {"income": 0.0, "expense": 0.0}
        monthly_totals[month][record.entry_type] += record.amount

    sorted_months = sorted(monthly_totals)
    return {"monthly_trends": [{"month": month, **monthly_totals[month]} for month in sorted_months]}
