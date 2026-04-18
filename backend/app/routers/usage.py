# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usage_record import UsageRecordCreate, UsageRecordUpdate, UsageRecordOut, UsageRecordDetail
from app import crud
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=dict)
def list_usage(
    equipment_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    items = crud.usage_record.get_usage_records(db, equipment_id=equipment_id, skip=skip, limit=page_size)
    total = crud.usage_record.get_usage_count(db, equipment_id=equipment_id)
    return {
        "items": [UsageRecordOut.model_validate(item).model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{record_id}", response_model=dict)
def get_usage(record_id: int, db: Session = Depends(get_db)):
    obj = crud.usage_record.get_usage_record(db, record_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")
    result = UsageRecordDetail.model_validate(obj)
    eq = crud.equipment.get_equipment(db, obj.equipment_id)
    if eq:
        result.equipment_name = eq.name
    return result.model_dump()

@router.post("/", response_model=dict, status_code=201)
def create_usage(data: UsageRecordCreate, db: Session = Depends(get_db)):
    eq = crud.equipment.get_equipment(db, data.equipment_id)
    if not eq:
        raise HTTPException(status_code=400, detail="Equipment not found")
    obj = crud.usage_record.create_usage_record(db, data)
    return UsageRecordOut.model_validate(obj).model_dump()

@router.put("/{record_id}", response_model=dict)
def update_usage(record_id: int, data: UsageRecordUpdate, db: Session = Depends(get_db)):
    obj = crud.usage_record.update_usage_record(db, record_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Record not found")
    return UsageRecordOut.model_validate(obj).model_dump()

@router.delete("/{record_id}", status_code=204)
def delete_usage(record_id: int, db: Session = Depends(get_db)):
    success = crud.usage_record.delete_usage_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
