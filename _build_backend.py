# -*- coding: utf-8 -*-
import os

BASE = r'C:\Users\HP\.qclaw\workspace\lab-equipment-system\backend'

files = {}

files[f'{BASE}\\app\\__init__.py'] = ''

files[f'{BASE}\\app\\models\\__init__.py'] = 'from app.models.equipment import Equipment\nfrom app.models.usage_record import UsageRecord\n'

files[f'{BASE}\\app\\schemas\\__init__.py'] = ''

files[f'{BASE}\\app\\crud\\__init__.py'] = ''

files[f'{BASE}\\app\\routers\\__init__.py'] = ''

files[f'{BASE}\\app\\main.py'] = '''# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import equipment, usage

app = FastAPI(title="Lab Equipment API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Lab Equipment API is running", "version": "1.0.0"}

app.include_router(equipment.router, prefix="/api/equipment", tags=["Equipment"])
app.include_router(usage.router, prefix="/api/usage", tags=["Usage"])
'''

files[f'{BASE}\\app\\database.py'] = '''# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./lab_equipment.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

files[f'{BASE}\\app\\models\\equipment.py'] = '''# -*- coding: utf-8 -*-
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
'''

files[f'{BASE}\\app\\models\\usage_record.py'] = '''# -*- coding: utf-8 -*-
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
'''

files[f'{BASE}\\app\\schemas\\equipment.py'] = '''# -*- coding: utf-8 -*-
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
'''

files[f'{BASE}\\app\\schemas\\usage_record.py'] = '''# -*- coding: utf-8 -*-
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
'''

files[f'{BASE}\\app\\crud\\equipment.py'] = '''# -*- coding: utf-8 -*-
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
'''

files[f'{BASE}\\app\\crud\\usage_record.py'] = '''# -*- coding: utf-8 -*-
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
'''

files[f'{BASE}\\app\\routers\\equipment.py'] = '''# -*- coding: utf-8 -*-
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
    items = crud.equipment.get_all_equipment(db, skip=skip, limit=page_size, search=search, status=status)
    total = crud.equipment.get_equipment_count(db, search=search, status=status)
    return {"items": items, "total": total, "page": page, "page_size": page_size}

@router.get("/{equipment_id}", response_model=EquipmentDetail)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    obj = crud.equipment.get_equipment(db, equipment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="\\u8bbev\\u5907\\u4e0d\\u5b58\\u5728")
    usage_count = crud.equipment.get_equipment_usage_count(db, equipment_id)
    result = EquipmentDetail.model_validate(obj)
    result.usage_count = usage_count
    return result

@router.post("/", response_model=EquipmentOut, status_code=201)
def create_equipment(data: EquipmentCreate, db: Session = Depends(get_db)):
    return crud.equipment.create_equipment(db, data)

@router.put("/{equipment_id}", response_model=EquipmentOut)
def update_equipment(equipment_id: int, data: EquipmentUpdate, db: Session = Depends(get_db)):
    obj = crud.equipment.update_equipment(db, equipment_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="\\u8bbev\\u5907\\u4e0d\\u5b58\\u5728")
    return obj

@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    success = crud.equipment.delete_equipment(db, equipment_id)
    if not success:
        raise HTTPException(status_code=404, detail="\\u8bbev\\u5907\\u4e0d\\u5b58\\u5728")
'''

files[f'{BASE}\\app\\routers\\usage.py'] = '''# -*- coding: utf-8 -*-
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
    return {"items": items, "total": len(items), "page": page, "page_size": page_size}

@router.get("/{record_id}", response_model=UsageRecordDetail)
def get_usage(record_id: int, db: Session = Depends(get_db)):
    obj = crud.usage_record.get_usage_record(db, record_id)
    if not obj:
        raise HTTPException(status_code=404, detail="\\u8bb0\\u5f55\\u4e0d\\u5b58\\u5728")
    result = UsageRecordDetail.model_validate(obj)
    eq = crud.equipment.get_equipment(db, obj.equipment_id)
    if eq:
        result.equipment_name = eq.name
    return result

@router.post("/", response_model=UsageRecordOut, status_code=201)
def create_usage(data: UsageRecordCreate, db: Session = Depends(get_db)):
    eq = crud.equipment.get_equipment(db, data.equipment_id)
    if not eq:
        raise HTTPException(status_code=400, detail="\\u8bbev\\u5907\\u4e0d\\u5b58\\u5728")
    return crud.usage_record.create_usage_record(db, data)

@router.put("/{record_id}", response_model=UsageRecordOut)
def update_usage(record_id: int, data: UsageRecordUpdate, db: Session = Depends(get_db)):
    obj = crud.usage_record.update_usage_record(db, record_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="\\u8bb0\\u5f55\\u4e0d\\u5b58\\u5728")
    return obj

@router.delete("/{record_id}", status_code=204)
def delete_usage(record_id: int, db: Session = Depends(get_db)):
    success = crud.usage_record.delete_usage_record(db, record_id)
    if not success:
        raise HTTPException(status_code=404, detail="\\u8bb0\\u5f55\\u4e0d\\u5b58\\u5728")
'''

files[f'{BASE}\\run.py'] = '''# -*- coding: utf-8 -*-
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
'''

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {os.path.relpath(filepath, BASE)}')

print('\n=== All backend files created! ===')
