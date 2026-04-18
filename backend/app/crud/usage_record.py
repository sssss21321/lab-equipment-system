# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from app.models.usage_record import UsageRecord
from app.schemas.usage_record import UsageRecordCreate, UsageRecordUpdate
from typing import List, Optional

def get_usage_records(db: Session, equipment_id: Optional[int] = None,
                       skip: int = 0, limit: int = 100) -> List[UsageRecord]:
    query = db.query(UsageRecord)
    if equipment_id:
        query = query.filter(UsageRecord.equipment_id == equipment_id)
    return query.order_by(UsageRecord.id.desc()).offset(skip).limit(limit).all()

def get_usage_record(db: Session, record_id: int) -> Optional[UsageRecord]:
    return db.query(UsageRecord).filter(UsageRecord.id == record_id).first()

def create_usage_record(db: Session, data: UsageRecordCreate) -> UsageRecord:
    obj = UsageRecord(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_usage_record(db: Session, record_id: int, data: UsageRecordUpdate) -> Optional[UsageRecord]:
    obj = db.query(UsageRecord).filter(UsageRecord.id == record_id).first()
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_usage_record(db: Session, record_id: int) -> bool:
    obj = db.query(UsageRecord).filter(UsageRecord.id == record_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def get_usage_count(db: Session, equipment_id: Optional[int] = None) -> int:
    query = db.query(UsageRecord)
    if equipment_id:
        query = query.filter(UsageRecord.equipment_id == equipment_id)
    return query.count()
