# from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
# from database import Base
# import datetime
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     password = Column(String(128), nullable=False)  # You can store hashed password here
#
# class Transaction(Base):
#     __tablename__ = "transactions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, nullable=False)
#     amount = Column(Float, nullable=False)
#     category = Column(String(50), nullable=False)
#     is_late_night = Column(Boolean, nullable=False)
#     distance_from_prev_txn = Column(Float, default=0.0)  # Skipped for now
#     rolling_30d_amt = Column(Float, nullable=False)
#     is_fraud = Column(Boolean, nullable=False)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# models.py
# from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
# from database import Base
# import datetime
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     password = Column(String(128), nullable=False)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#
#
# class Transaction(Base):
#     __tablename__ = "transactions"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, nullable=False)
#     amount = Column(Float, nullable=False)
#     category = Column(String(50), nullable=False)
#     is_late_night = Column(Boolean, nullable=False)
#     rolling_30d_amt = Column(Float, nullable=False)
#     is_fraud = Column(Boolean, nullable=False)
#     timestamp = Column(DateTime, default=datetime.datetime.utcnow)


# models.py - Complete with terminal_id
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    terminal_id = Column(Integer, nullable=False)  # NEW
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    is_late_night = Column(Boolean, nullable=False)
    is_fraud = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
