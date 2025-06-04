# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# import models, schemas, crud
# from database import SessionLocal, engine
# from fastapi.middleware.cors import CORSMiddleware
#
# models.Base.metadata.create_all(bind=engine)
#
# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @app.post("/register")
# def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.create_user(db, user)
#
# @app.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     auth = crud.authenticate_user(db, user)
#     if not auth:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     return auth
#
# @app.post("/transaction")
# def transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
#     return crud.create_transaction(db, txn)
#
# @app.get("/transactions/{user_id}")
# def transactions(user_id: int, db: Session = Depends(get_db)):
#     return crud.get_user_transactions(db, user_id)

#HEREHEREHEREHEREE FINAL:
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# import models, schemas, crud
# from database import SessionLocal, engine
# from fastapi.middleware.cors import CORSMiddleware
#
# models.Base.metadata.create_all(bind=engine)
#
# app = FastAPI(title="Fraud Detection API")
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @app.get("/")
# def root():
#     return {"message": "Fraud Detection API is running!"}
#
# @app.post("/register")
# def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.create_user(db, user)
#
# @app.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     auth = crud.authenticate_user(db, user)
#     if not auth:
#         raise HTTPException(status_code=400, detail="Invalid credentials")
#     return {"message": "Login successful", "user_id": auth.id}
#
# @app.post("/transaction")
# def create_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
#     result = crud.create_transaction(db, txn)
#     return {
#         "transaction_id": result.id,
#         "amount": result.amount,
#         "category": result.category,
#         "is_fraud": result.is_fraud,
#         "timestamp": result.timestamp.isoformat()
#     }
#
# @app.get("/transactions/{user_id}")
# def get_transactions(user_id: int, db: Session = Depends(get_db)):
#     transactions = crud.get_user_transactions(db, user_id)
#     return {
#         "user_id": user_id,
#         "transactions": [
#             {
#                 "id": txn.id,
#                 "amount": txn.amount,
#                 "category": txn.category,
#                 "is_fraud": txn.is_fraud,
#                 "timestamp": txn.timestamp.isoformat()
#             }
#             for txn in transactions
#         ]
#     }
#
# @app.get("/stats/{user_id}")
# def get_stats(user_id: int, db: Session = Depends(get_db)):
#     return crud.get_user_stats(db, user_id)
# main.py - Complete with session auth and terminal_id
from fastapi import FastAPI, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import secrets

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory session storage
active_sessions = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(session_token: str = Cookie(None, alias="session_token")):
    """Get current logged-in user from session"""
    if not session_token or session_token not in active_sessions:
        raise HTTPException(status_code=401, detail="Please login first")

    user_info = active_sessions[session_token]
    return user_info


@app.get("/")
def root():
    return {"message": "Fraud Detection API is running!"}


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = crud.create_user(db, user)
        return {
            "message": "User registered successfully",
            "user_id": new_user.id,
            "username": new_user.username
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    auth_user = crud.authenticate_user(db, user)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    session_token = secrets.token_urlsafe(32)

    active_sessions[session_token] = {
        "user_id": auth_user.id,
        "username": auth_user.username
    }

    response = JSONResponse({
        "message": "Login successful",
        "user_id": auth_user.id,
        "username": auth_user.username
    })

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=False,
        max_age=86400,
        samesite="lax",
        secure=False,  # Set to False for localhost
        path="/",  # Explicitly set path
        domain=None
    )

    return response


@app.post("/logout")
def logout(session_token: str = Cookie(None, alias="session_token")):
    if session_token and session_token in active_sessions:
        del active_sessions[session_token]

    response = JSONResponse({"message": "Logged out successfully"})
    response.delete_cookie("session_token")
    return response


@app.get("/me")
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"],
        "logged_in": True
    }


@app.post("/transaction")
def create_transaction(
        txn: schemas.TransactionCreate,
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create transaction with terminal_id"""

    # Validate terminal_id range
    if not (1 <= txn.terminal_id <= 999):
        raise HTTPException(status_code=400, detail="Terminal ID must be between 1 and 999")

    result = crud.create_transaction_with_user_id(db, txn, current_user["user_id"])

    return {
        "transaction_id": result.id,
        "user_id": result.user_id,
        "terminal_id": result.terminal_id,
        "amount": result.amount,
        "category": result.category,
        "is_fraud": result.is_fraud,
        "timestamp": result.timestamp.isoformat(),
        "user": current_user["username"]
    }


@app.get("/transactions")
def get_my_transactions(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    transactions = crud.get_user_transactions(db, current_user["user_id"])
    return {
        "user": current_user["username"],
        "transaction_count": len(transactions),
        "transactions": [
            {
                "id": txn.id,
                "terminal_id": txn.terminal_id,
                "amount": txn.amount,
                "category": txn.category,
                "is_fraud": txn.is_fraud,
                "timestamp": txn.timestamp.isoformat()
            }
            for txn in transactions
        ]
    }


@app.get("/stats")
def get_my_stats(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    stats = crud.get_user_stats(db, current_user["user_id"])
    stats["username"] = current_user["username"]
    return stats


@app.get("/terminal/{terminal_id}/stats")
def get_terminal_stats(terminal_id: int, db: Session = Depends(get_db)):
    return crud.get_terminal_stats(db, terminal_id)