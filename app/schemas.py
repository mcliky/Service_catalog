from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any

class PartCreate(BaseModel):
    material_id: Optional[int] = None
    part_code: Optional[str] = None
    status: Optional[str] = None
    supplier_id: Optional[str] = None
    unit_cost: Optional[float] = None
    availability: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    compatibleAssets: Optional[List[str]] = None

class PartUpdate(BaseModel):
    material_id: Optional[int] = None
    part_code: Optional[str] = None
    status: Optional[str] = None
    supplier_id: Optional[str] = None
    unit_cost: Optional[float] = None
    availability: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    compatibleAssets: Optional[List[str]] = None

class PartResponse(PartCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
