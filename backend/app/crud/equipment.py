# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.equipment import Equipment
from app.models.usage_record import UsageRecord
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate
from typing import List, Optional

def get_all_equipment(db: Session, skip: int = 0, limit: int = 100,
                       search: Optional[str] = None, status: Optional[str] = None) -> List[Equipment]:
    query = db.query(Equipment)
    if search:
        keyword = f"%{search}%"
        query = query.filter(
            (Equipment.name.ilike(keyword)) |
            (Equipment.model.ilike(keyword)) |
            (Equipment.serial_number.ilike(keyword)) |
            (Equipment.location.ilike(keyword))
        )
    if status:
        query = query.filter(Equipment.status == status)
    return query.order_by(Equipment.id.desc()).offset(skip).limit(limit).all()

def get_equipment_count(db: Session, search: Optional[str] = None, status: Optional[str] = None) -> int:
    query = db.query(func.count(Equipment.id))
    if search:
        keyword = f"%{search}%"
        query = query.filter(
            (Equipment.name.ilike(keyword)) |
            (Equipment.model.ilike(keyword)) |
            (Equipment.serial_number.ilike(keyword))
        )
    if status:
        query = query.filter(Equipment.status == status)
    return query.scalar()

def get_equipment(db: Session, equipment_id: int) -> Optional[Equipment]:
    return db.query(Equipment).filter(Equipment.id == equipment_id).first()

def create_equipment(db: Session, data: EquipmentCreate) -> Equipment:
    obj = Equipment(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_equipment(db: Session, equipment_id: int, data: EquipmentUpdate) -> Optional[Equipment]:
    obj = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not obj:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_equipment(db: Session, equipment_id: int) -> bool:
    obj = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def get_equipment_usage_count(db: Session, equipment_id: int) -> int:
    return db.query(func.count(UsageRecord.id)).filter(UsageRecord.equipment_id == equipment_id).scalar()
