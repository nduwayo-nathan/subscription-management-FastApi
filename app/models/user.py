from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Store hashed password here

    def set_password(self, password: str):
        """Hash the password before saving."""
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
