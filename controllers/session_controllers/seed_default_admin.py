from sqlalchemy.orm import Session
from models.users import User
from passlib.context import CryptContext

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_default_admin(db: Session):
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print("Admin user already exists, skipping creation.")
        return
    
    default_admin = User(
        username="admin",
        email="admin@francium.tech",
        encrypted_password=crypt.hash("admin12345"),
        role_id=1  

    )
    db.add(default_admin)
    db.commit()
    print("Admin Default")
    