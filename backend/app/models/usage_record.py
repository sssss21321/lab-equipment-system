# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=False, index=True)
    user = Column(String(100), nullable=False, comment="使用者")
    purpose = Column(Text, nullable=True, comment="使用目的")
    start_time = Column(String(30), nullable=False, comment="开始时间")
    end_time = Column(String(30), nullable=True, comment="结束时间")
    notes = Column(Text, nullable=True, comment="备注")
    created_at = Column(DateTime, server_default=func.now())
