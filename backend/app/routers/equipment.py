# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentOut, EquipmentDetail
from app import crud
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=dict)
def list_equipment(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    # 返回 dict 而不是 SQLAlchemy 对象
    items = crud.equipment.get_all_equipment(db, skip=skip, limit=page_size, search=search, status=status)
    total = crud.equipment.get_equipment_count(db, search=search, status=status)
    # 转换为纯 Python dict，避免 Pydantic 序列化 SQLAlchemy 对象失败
    return {
        "items": [EquipmentOut.model_validate(item).model_dump() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/{equipment_id}", response_model=dict)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    obj = crud.equipment.get_equipment(db, equipment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Equipment not found")
    usage_count = crud.equipment.get_equipment_usage_count(db, equipment_id)
    result = EquipmentDetail.model_validate(obj)
    result.usage_count = usage_count
    return result.model_dump()

@router.post("/", response_model=dict, status_code=201)
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db)):
    obj = crud.equipment.create_equipment(db, data)
    return EquipmentOut.model_validate(obj).model_dump()

@router.put("/{equipment_id}", response_model=dict)
def update_equipment(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db)):
    obj = crud.equipment.update_equipment(db, equipment_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return EquipmentOut.model_validate(obj).model_dump()

@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    success = crud.equipment.delete_equipment(db, equipment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipment not found")
