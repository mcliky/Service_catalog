from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from .db import Base, engine, SessionLocal
from .models import Part
from .schemas import PartCreate, PartResponse, PartUpdate

app = FastAPI(title="Service Catalog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Create tables on boot
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "Service Catalog OK"}

def _to_json(text_value: Optional[str]):
    if not text_value:
        return None
    try:
        return json.loads(text_value)
    except Exception:
        return None

def _to_response(p: Part) -> PartResponse:
    return PartResponse(
        id=p.id,
        material_id=p.material_id,
        part_code=p.part_code,
        status=p.status,
        supplier_id=p.supplier_id,
        unit_cost=p.unit_cost,
        availability=p.availability,
        specs=_to_json(p.specs_json),
        compatibleAssets=_to_json(p.compatible_assets_json),
    )

# --------- CRUD ---------

@app.get("/parts/", response_model=List[PartResponse])
def list_parts(db: Session = Depends(get_db)):
    rows = db.query(Part).all()
    return [_to_response(p) for p in rows]

@app.post("/parts/", response_model=PartResponse)
def create_part(item: PartCreate, db: Session = Depends(get_db)):
    p = Part(
        material_id=item.material_id,
        part_code=item.part_code,
        status=item.status,
        supplier_id=item.supplier_id,
        unit_cost=item.unit_cost,
        availability=item.availability,
        specs_json=json.dumps(item.specs) if item.specs else None,
        compatible_assets_json=json.dumps(item.compatibleAssets) if item.compatibleAssets else None,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return _to_response(p)

@app.get("/parts/{part_id}", response_model=PartResponse)
def get_part(part_id: int, db: Session = Depends(get_db)):
    p = db.get(Part, part_id)
    if not p:
        raise HTTPException(status_code=404, detail="Part not found")
    return _to_response(p)

@app.put("/parts/{part_id}", response_model=PartResponse)
def update_part(part_id: int, item: PartUpdate, db: Session = Depends(get_db)):
    p = db.get(Part, part_id)
    if not p:
        raise HTTPException(status_code=404, detail="Part not found")

    data = item.dict(exclude_unset=True)
    for k, v in data.items():
        if k == "specs":
            p.specs_json = json.dumps(v) if v is not None else None
        elif k == "compatibleAssets":
            p.compatible_assets_json = json.dumps(v) if v is not None else None
        else:
            setattr(p, k, v)

    db.commit()
    db.refresh(p)
    return _to_response(p)

@app.delete("/parts/{part_id}", status_code=204)
def delete_part(part_id: int, db: Session = Depends(get_db)):
    p = db.get(Part, part_id)
    if not p:
        raise HTTPException(status_code=404, detail="Part not found")
    db.delete(p)
    db.commit()
    return None
