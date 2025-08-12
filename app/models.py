from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)  # optional link to ERP item
    part_code = Column(String, index=True, nullable=True)
    status = Column(String, nullable=True)                 # e.g., Active / Obsolete
    supplier_id = Column(String, nullable=True)
    unit_cost = Column(Float, nullable=True)
    availability = Column(String, nullable=True)           # e.g., In Stock / Backordered
    specs_json = Column(Text, nullable=True)               # JSON stringified
    compatible_assets_json = Column(Text, nullable=True)   # JSON stringified

    # harmless if materials table doesn't exist (when using separate DBs)
    material = relationship(
        "Material",
        primaryjoin="foreign(Part.material_id)==Material.id",
        viewonly=True,
        lazy="joined",
    )

# Optional shadow model so joined relationship doesn't error if sharing DB with ERP
class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
