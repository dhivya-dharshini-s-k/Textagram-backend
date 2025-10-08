from models.role import Role
from sqlalchemy.orm import Session

def seed_roles(db: Session):
    roles_data = [
        {"id": 1, "name": "admin"},
        {"id": 2, "name": "user"}
    ]

    for role_info in roles_data:
        existing = db.query(Role).filter_by(id=role_info["id"]).first()
        if not existing:
            db.add(Role(id=role_info["id"], name=role_info["name"]))
    db.commit()
