import json
from .db import SessionLocal
from .models import Part

if __name__ == "__main__":
    db = SessionLocal()

    db.add(Part(
        material_id=1,
        part_code="P-001",
        status="Active",
        supplier_id="S-123",
        unit_cost=12.5,
        availability="In Stock",
        specs_json=json.dumps({"size": "10mm", "material": "Steel"}),
        compatible_assets_json=json.dumps(["Pump-X", "Compressor-Y"]),
    ))

    db.add(Part(
        material_id=2,
        part_code="P-002",
        status="Active",
        supplier_id="S-456",
        unit_cost=3.2,
        availability="In Stock",
        specs_json=json.dumps({"size": "5mm", "material": "Rubber"}),
        compatible_assets_json=json.dumps([]),
    ))

    db.commit()
    db.close()
    print("Seeded Service Catalog parts.")
