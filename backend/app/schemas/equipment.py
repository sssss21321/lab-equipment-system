# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EquipmentBase(BaseModel):
    name: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    purchase_date: Optional[str] = None
    status: str = "normal"
    description: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    purchase_date: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

class EquipmentOut(EquipmentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EquipmentDetail(EquipmentOut):
    usage_count: int = 0
