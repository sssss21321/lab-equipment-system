# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsageRecordBase(BaseModel):
    equipment_id: int
    user: str
    purpose: Optional[str] = None
    start_time: str
    end_time: Optional[str] = None
    notes: Optional[str] = None

class UsageRecordCreate(UsageRecordBase):
    pass

class UsageRecordUpdate(BaseModel):
    user: Optional[str] = None
    purpose: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    notes: Optional[str] = None

class UsageRecordOut(UsageRecordBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsageRecordDetail(UsageRecordOut):
    equipment_name: Optional[str] = None
