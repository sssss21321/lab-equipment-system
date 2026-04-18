# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True, comment="设备名称")
    model = Column(String(200), nullable=True, comment="型号")
    manufacturer = Column(String(200), nullable=True, comment="制造商")
    serial_number = Column(String(100), nullable=True, unique=True, comment="序列号")
    location = Column(String(200), nullable=True, comment="存放位置")
    category = Column(String(100), nullable=True, comment="设备类别")
    purchase_date = Column(String(20), nullable=True, comment="购置日期")
    status = Column(String(50), default="normal", comment="状态: normal/maintenance/repairly/scraped")
    description = Column(Text, nullable=True, comment="设备描述")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
