from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GlucoseRecord
from app.schemas import GlucoseRequest, GlucoseUpdateRequest
from app.utils import day_end, day_start, fail, glucose_status, parse_date, parse_datetime, success

router = APIRouter(prefix="/glucose", tags=["血糖记录"])


def glucose_to_dict(record: GlucoseRecord) -> dict:
    value = Decimal(record.glucose_value)
    return {
        "recordId": record.record_id,
        "userId": record.user_id,
        "measureTime": record.measure_time.strftime("%Y-%m-%d %H:%M:%S"),
        "measureType": record.measure_type,
        "glucoseValue": float(value),
        "glucoseStatus": glucose_status(record.measure_type, value),
        "remark": record.remark,
    }


@router.post("")
def create_glucose(payload: GlucoseRequest, db: Session = Depends(get_db)):
    record = GlucoseRecord(
        user_id=payload.userId,
        measure_time=parse_datetime(payload.measureTime),
        measure_type=payload.measureType,
        glucose_value=Decimal(str(payload.glucoseValue)),
        remark=payload.remark,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return success(
        {
            "recordId": record.record_id,
            "glucoseStatus": glucose_status(record.measure_type, record.glucose_value),
        },
        "保存成功",
    )


@router.get("")
def list_glucose(
    userId: int,
    startDate: str | None = Query(default=None),
    endDate: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(GlucoseRecord).where(GlucoseRecord.user_id == userId)
    if startDate:
        stmt = stmt.where(GlucoseRecord.measure_time >= day_start(parse_date(startDate)))
    if endDate:
        stmt = stmt.where(GlucoseRecord.measure_time <= day_end(parse_date(endDate)))
    records = db.scalars(stmt.order_by(GlucoseRecord.measure_time.desc())).all()
    return success([glucose_to_dict(record) for record in records])


@router.put("/{recordId}")
def update_glucose(recordId: int, payload: GlucoseUpdateRequest, db: Session = Depends(get_db)):
    record = db.get(GlucoseRecord, recordId)
    if not record:
        return fail(404, "血糖记录不存在")
    if payload.measureTime is not None:
        record.measure_time = parse_datetime(payload.measureTime)
    if payload.measureType is not None:
        record.measure_type = payload.measureType
    if payload.glucoseValue is not None:
        record.glucose_value = Decimal(str(payload.glucoseValue))
    if payload.remark is not None:
        record.remark = payload.remark
    db.commit()
    db.refresh(record)
    return success(glucose_to_dict(record), "修改成功")


@router.delete("/{recordId}")
def delete_glucose(recordId: int, db: Session = Depends(get_db)):
    record = db.get(GlucoseRecord, recordId)
    if not record:
        return fail(404, "血糖记录不存在")
    db.delete(record)
    db.commit()
    return success({"recordId": recordId}, "删除成功")
