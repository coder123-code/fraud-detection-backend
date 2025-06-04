# from pydantic import BaseModel
#
# class UserCreate(BaseModel):
#     username: str
#     password: str

# class UserLogin(BaseModel):
#     username: str
#     password: str
#
# class TransactionCreate(BaseModel):
#     user_id: int
#     amount: float
#     category: str
#
# class TransactionOut(TransactionCreate):
#     is_late_night: bool
#     distance_from_prev_txn: float
#     rolling_30d_amt: float
#     is_fraud: bool
#     timestamp: str






# from pydantic import BaseModel
# from datetime import datetime
#
# class UserCreate(BaseModel):
#     username: str
#     password: str
#
# class UserLogin(BaseModel):
#     username: str
#     password: str
#
# class TransactionCreate(BaseModel):
#     user_id: int
#     amount: float
#     category: str




# schemas.py - Updated with terminal_id
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TransactionCreate(BaseModel):
    terminal_id: int  # NEW - Required field
    amount: float
    category: str