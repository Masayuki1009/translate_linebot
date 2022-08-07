from email.policy import default
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, func

from app.db.dbbase import DbBase

def generate_uuid():
          return str(uuid4())

class Message(DbBase):
          __tablename__ = "message"

          id = Column(String, primary_key=True, default=generate_uuid, unique=True)
          user_id = Column(String, nullable=False)
          text = Column(String(256), nullable=False)
          translated_text = Column(String(256), nullable=False)
          created_at = Column(DateTime, default=func.now(), nullable=False)
          
          def to_dict(self):
                    return {
                              "id": self.id,
                              "user_id": self.user_id,
                              "text": self.text,
                              "translated_text": self.translated_text,
                              "createdAt": self.created_at,
                    }

