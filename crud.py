# from sqlalchemy.orm import Session
# import models, schemas
# import joblib
# from datetime import datetime, timedelta
# from sqlalchemy import and_
#
# model = joblib.load("fraud_detector_model.pkl")
#
# def create_user(db: Session, user: schemas.UserCreate):
#     db_user = models.User(username=user.username, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
# def authenticate_user(db: Session, user: schemas.UserLogin):
#     return db.query(models.User).filter_by(username=user.username, password=user.password).first()
#
# def create_transaction(db: Session, txn: schemas.TransactionCreate):
#     now = datetime.utcnow()
#     hour = now.hour
#     is_late_night = hour < 5
#
#     past_30_days = now - timedelta(days=30)
#     past_txns = db.query(models.Transaction).filter(
#         and_(
#             models.Transaction.user_id == txn.user_id,
#             models.Transaction.timestamp >= past_30_days
#         )
#     ).all()
#     rolling_30d_amt = sum(t.amount for t in past_txns)
#
#     category_encoded = 1 if txn.category.lower() == "travel" else 0
#
#     features = [[
#         txn.amount,
#         int(is_late_night),
#         rolling_30d_amt,
#         0.0,  # distance_from_prev_txn skipped
#         category_encoded
#     ]]
#
#     prediction = model.predict(features)[0]
#
#     db_txn = models.Transaction(
#         user_id=txn.user_id,
#         amount=txn.amount,
#         category=txn.category,
#         is_late_night=is_late_night,
#         distance_from_prev_txn=0.0,
#         rolling_30d_amt=rolling_30d_amt,
#         is_fraud=bool(prediction)
#     )
#     db.add(db_txn)
#     db.commit()
#     db.refresh(db_txn)
#     return db_txn
#
# def get_user_transactions(db: Session, user_id: int):
#     return db.query(models.Transaction).filter_by(user_id=user_id).all()
# crud.py - Simple CRUD operations for fraud detection
# crud.py - Fixed to match your Google Colab model features

# crud.py - Exact match to your Google Colab training

# crud.py - Fixed rolling sum bug and feature names
#final fraud code HEREHEREHERE:
# from sqlalchemy.orm import Session
# from sqlalchemy import and_, desc
# import models, schemas
# import joblib
# from datetime import datetime, timedelta
# import numpy as np
# import pandas as pd
#
# # Load model
# try:
#     model_data = joblib.load("fraud_detector_model_fixed.pkl")
#     print(f"✅ Model loaded successfully: {type(model_data)}")
#
#     if isinstance(model_data, dict):
#         model = model_data.get('model')
#         le = model_data.get('le_category')
#     else:
#         model = model_data
#         le = None
#
# except Exception as e:
#     print(f"❌ Error loading model: {e}")
#     model = None
#     le = None
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     """Create new user"""
#     db_user = models.User(username=user.username, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def authenticate_user(db: Session, user: schemas.UserLogin):
#     """Login user"""
#     return db.query(models.User).filter_by(username=user.username, password=user.password).first()
#
#
# def create_transaction(db: Session, txn: schemas.TransactionCreate):
#     """Create transaction with FIXED rolling sum calculation"""
#
#     # Get current time
#     now = datetime.utcnow()
#     hour = now.hour
#     is_late_night = 1 if hour <= 5 or hour >= 23 else 0
#
#     print(f"🕐 Current hour: {hour}")
#     print(f"🌙 Is late night: {is_late_night}")
#
#     # 🔧 FIXED: Rolling 30-day amount calculation
#     past_30_days = now - timedelta(days=30)
#     past_txns = db.query(models.Transaction).filter(
#         and_(
#             models.Transaction.user_id == txn.user_id,
#             models.Transaction.timestamp >= past_30_days
#         )
#     ).all()
#
#     # Calculate rolling sum properly
#     rolling_30d_amt = 0.0
#     for txn_record in past_txns:
#         if txn_record.amount is not None:
#             rolling_30d_amt += float(txn_record.amount)
#
#     # Ensure reasonable value
#     if rolling_30d_amt > 1000000:  # Cap at 1 million
#         rolling_30d_amt = 0.0
#         print("⚠️ Rolling amount too high, resetting to 0")
#
#     print(f"💰 Rolling 30d amount: ${rolling_30d_amt:.2f}")
#
#     # Distance (simplified)
#     distance_from_prev_txn = 0.0
#
#     # Category encoding
#     category_mapping = {
#         'grocery': 'grocery_pos',
#         'gas': 'gas_transport',
#         'shopping': 'shopping_pos',
#         'entertainment': 'entertainment',
#         'restaurant': 'food_dining',
#         'travel': 'travel',
#         'misc': 'misc_pos'
#     }
#
#     training_category = category_mapping.get(txn.category.lower(), 'misc_pos')
#
#     # Simple category encoding (0-13 based on common fraud dataset categories)
#     manual_categories = [
#         'grocery_pos', 'gas_transport', 'misc_net', 'grocery_net', 'shopping_net',
#         'shopping_pos', 'entertainment', 'personal_care', 'health_fitness', 'travel',
#         'kids_pets', 'food_dining', 'home', 'misc_pos'
#     ]
#     category_encoded = manual_categories.index(training_category) if training_category in manual_categories else 0
#     print(f"📋 Category: {txn.category} -> {training_category} -> encoded: {category_encoded}")
#
#     # 🎯 Create features as DataFrame with proper column names
#     feature_names = ['amt', 'is_late_night', 'rolling_30d_amt', 'distance_from_prev_txn', 'category_encoded']
#
#     features_df = pd.DataFrame([[
#         float(txn.amount),
#         int(is_late_night),
#         float(rolling_30d_amt),
#         float(distance_from_prev_txn),
#         int(category_encoded)
#     ]], columns=feature_names)
#
#     print(f"💰 Features for model:")
#     print(features_df.to_string(index=False))
#
#     # Predict with model
#     prediction = 0
#     probability = 0.0
#
#     if model is not None:
#         try:
#             # Use DataFrame instead of array to provide feature names
#             prediction = model.predict(features_df)[0]
#             if hasattr(model, 'predict_proba'):
#                 prob_array = model.predict_proba(features_df)[0]
#                 probability = prob_array[1] if len(prob_array) > 1 else prob_array[0]
#
#             print(f"🤖 Model prediction: {prediction}")
#             print(f"📊 Fraud probability: {probability:.4f}")
#
#             # Test with Colab example using DataFrame
#             colab_df = pd.DataFrame([[1500.0, 1, 5000, 0.0, 0]], columns=feature_names)
#             colab_pred = model.predict(colab_df)[0]
#             colab_prob = model.predict_proba(colab_df)[0][1] if hasattr(model, 'predict_proba') else 0
#             print(f"🧪 Colab example test: Fraud={colab_pred}, Prob={colab_prob:.4f}")
#
#         except Exception as e:
#             print(f"❌ Model prediction failed: {e}")
#             # Fallback rules
#             if txn.amount >= 1000 and is_late_night:
#                 prediction = 1
#                 probability = 0.8
#             elif txn.amount >= 2000:
#                 prediction = 1
#                 probability = 0.7
#             else:
#                 prediction = 0
#                 probability = 0.1
#     else:
#         print("❌ No model available")
#         prediction = 1 if txn.amount > 1000 else 0
#         probability = 0.8 if prediction else 0.2
#
#     # Save transaction
#     db_txn = models.Transaction(
#         user_id=txn.user_id,
#         amount=txn.amount,
#         category=txn.category,
#         is_late_night=bool(is_late_night),
#         rolling_30d_amt=rolling_30d_amt,
#         is_fraud=bool(prediction)
#     )
#     db.add(db_txn)
#     db.commit()
#     db.refresh(db_txn)
#
#     print(f"✅ Transaction saved: ID={db_txn.id}, Fraud={db_txn.is_fraud}")
#
#     return db_txn
#
#
# def get_user_transactions(db: Session, user_id: int):
#     """Get user transactions"""
#     return db.query(models.Transaction).filter_by(user_id=user_id).order_by(desc(models.Transaction.timestamp)).all()
#
#
# def get_user_stats(db: Session, user_id: int):
#     """Get user stats"""
#     transactions = get_user_transactions(db, user_id)
#
#     if not transactions:
#         return {"message": "No transactions found"}
#
#     total_amount = sum(t.amount for t in transactions)
#     fraud_count = sum(1 for t in transactions if t.is_fraud)
#
#     return {
#         "total_transactions": len(transactions),
#         "total_amount": total_amount,
#         "fraud_transactions": fraud_count,
#         "fraud_rate": fraud_count / len(transactions) if len(transactions) > 0 else 0,
#         "average_amount": total_amount / len(transactions) if len(transactions) > 0 else 0
#     }

# crud.py - Complete with timezone fix
# from sqlalchemy.orm import Session
# from sqlalchemy import and_, desc
# import models, schemas
# import joblib
# from datetime import datetime, timedelta
# import pandas as pd
# import pytz
#
# # Load model
# try:
#     model_data = joblib.load("fraud_detector_model.pkl")
#     if isinstance(model_data, dict):
#         model = model_data.get('model')
#         le = model_data.get('le_category')
#     else:
#         model = model_data
#         le = None
# except Exception as e:
#     print(f"❌ Error loading model: {e}")
#     model = None
#     le = None
#
#
# def get_local_time():
#     """Get current time in Indian timezone"""
#     utc_now = datetime.utcnow()
#     ist = pytz.timezone('Asia/Kolkata')
#     utc = pytz.UTC
#     utc_time = utc.localize(utc_now)
#     local_time = utc_time.astimezone(ist)
#     return local_time
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     """Create new user"""
#     db_user = models.User(username=user.username, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def authenticate_user(db: Session, user: schemas.UserLogin):
#     """Login user"""
#     return db.query(models.User).filter_by(username=user.username, password=user.password).first()
#
#
# def create_transaction(db: Session, txn: schemas.TransactionCreate):
#     """Create transaction with correct local time"""
#
#     # Get current time in Indian timezone
#     local_time = get_local_time()
#     hour = local_time.hour
#     is_late_night = 1 if hour <= 5 or hour >= 23 else 0
#
#     print(f"🕐 Local time: {local_time.strftime('%Y-%m-%d %H:%M:%S')} IST")
#     print(f"🌙 Is late night: {is_late_night}")
#
#     # Get rolling 30-day amount
#     past_30_days = datetime.utcnow() - timedelta(days=30)
#     past_txns = db.query(models.Transaction).filter(
#         and_(
#             models.Transaction.user_id == txn.user_id,
#             models.Transaction.timestamp >= past_30_days
#         )
#     ).all()
#
#     rolling_30d_amt = 0.0
#     for txn_record in past_txns:
#         if txn_record.amount is not None and txn_record.amount < 1000000:
#             rolling_30d_amt += float(txn_record.amount)
#
#     if rolling_30d_amt > 100000:
#         rolling_30d_amt = min(rolling_30d_amt, 100000)
#
#     print(f"💰 Rolling 30d amount: ${rolling_30d_amt:.2f}")
#
#     # Distance (simplified)
#     distance_from_prev_txn = 0.0
#
#     # Category encoding
#     category_mapping = {
#         'grocery': 'grocery_pos', 'gas': 'gas_transport', 'shopping': 'shopping_pos',
#         'entertainment': 'entertainment', 'restaurant': 'food_dining', 'travel': 'travel',
#         'misc': 'misc_pos'
#     }
#
#     training_category = category_mapping.get(txn.category.lower(), 'misc_pos')
#     manual_categories = [
#         'grocery_pos', 'gas_transport', 'misc_net', 'grocery_net', 'shopping_net',
#         'shopping_pos', 'entertainment', 'personal_care', 'health_fitness', 'travel',
#         'kids_pets', 'food_dining', 'home', 'misc_pos'
#     ]
#     category_encoded = manual_categories.index(training_category) if training_category in manual_categories else 0
#     print(f"📋 Category: {txn.category} -> {training_category} -> encoded: {category_encoded}")
#
#     # Create features DataFrame
#     feature_names = ['amt', 'is_late_night', 'rolling_30d_amt', 'distance_from_prev_txn', 'category_encoded']
#     features_df = pd.DataFrame([[
#         float(txn.amount),
#         int(is_late_night),
#         float(rolling_30d_amt),
#         float(distance_from_prev_txn),
#         int(category_encoded)
#     ]], columns=feature_names)
#
#     print(f"💰 Features for model:")
#     print(features_df.to_string(index=False))
#
#     # Predict with model
#     prediction = 0
#     probability = 0.0
#
#     if model is not None:
#         try:
#             prediction = model.predict(features_df)[0]
#             if hasattr(model, 'predict_proba'):
#                 prob_array = model.predict_proba(features_df)[0]
#                 probability = prob_array[1] if len(prob_array) > 1 else prob_array[0]
#
#             print(f"🤖 Model prediction: {prediction}")
#             print(f"📊 Fraud probability: {probability:.4f}")
#
#         except Exception as e:
#             print(f"❌ Model prediction failed: {e}")
#             prediction = 1 if txn.amount > 1000 else 0
#             probability = 0.8 if prediction else 0.2
#     else:
#         print("❌ No model available")
#         prediction = 1 if txn.amount > 1000 else 0
#         probability = 0.8 if prediction else 0.2
#
#     # Save transaction with LOCAL TIME
#     db_txn = models.Transaction(
#         user_id=txn.user_id,
#         amount=txn.amount,
#         category=txn.category,
#         is_late_night=bool(is_late_night),
#         rolling_30d_amt=rolling_30d_amt,
#         is_fraud=bool(prediction),
#         timestamp=local_time.replace(tzinfo=None)
#     )
#     db.add(db_txn)
#     db.commit()
#     db.refresh(db_txn)
#
#     print(f"✅ Transaction saved: ID={db_txn.id}, Fraud={db_txn.is_fraud}")
#
#     return db_txn
#
#
# def get_user_transactions(db: Session, user_id: int):
#     """Get user transactions"""
#     return db.query(models.Transaction).filter_by(user_id=user_id).order_by(desc(models.Transaction.timestamp)).all()
#
#
# def get_user_stats(db: Session, user_id: int):
#     """Get user stats"""
#     transactions = get_user_transactions(db, user_id)
#
#     if not transactions:
#         return {"message": "No transactions found"}
#
#     total_amount = sum(t.amount for t in transactions)
#     fraud_count = sum(1 for t in transactions if t.is_fraud)
#
#     return {
#         "total_transactions": len(transactions),
#         "total_amount": total_amount,
#         "fraud_transactions": fraud_count,
#         "fraud_rate": fraud_count / len(transactions) if len(transactions) > 0 else 0,
#         "average_amount": total_amount / len(transactions) if len(transactions) > 0 else 0
#     }


# crud.py - Complete with terminal_id logic
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
import models, schemas
import joblib
from datetime import datetime, timedelta
import pandas as pd
import pytz

# Load model
try:
    model_data = joblib.load("fraud_detector_model_fixed.pkl")
    if isinstance(model_data, dict):
        model = model_data.get('model')
        le = model_data.get('le_category')
    else:
        model = model_data
        le = None
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None
    le = None


def get_local_time():
    """Get current time in Indian timezone"""
    utc_now = datetime.utcnow()
    ist = pytz.timezone('Asia/Kolkata')
    utc = pytz.UTC
    utc_time = utc.localize(utc_now)
    local_time = utc_time.astimezone(ist)
    return local_time


def create_user(db: Session, user: schemas.UserCreate):
    """Create new user"""
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user: schemas.UserLogin):
    """Login user"""
    return db.query(models.User).filter_by(username=user.username, password=user.password).first()


def create_transaction_with_user_id(db: Session, txn: schemas.TransactionCreate, user_id: int):
    """Create transaction with terminal_id"""

    # Get current time in Indian timezone
    local_time = get_local_time()
    hour = local_time.hour
    is_late_night = 1 if hour <= 5 or hour >= 23 else 0

    print(f"🕐 Local time: {local_time.strftime('%Y-%m-%d %H:%M:%S')} IST")
    print(f"🏪 Terminal ID: {txn.terminal_id}")
    print(f"💰 Amount: ${txn.amount}")
    print(f"📋 Category: {txn.category}")
    print(f"🌙 Is late night: {is_late_night}")

    # Terminal risk factor
    terminal_risk = 0.0
    if txn.terminal_id >= 900:  # High-risk terminals
        terminal_risk = 0.3
    elif txn.terminal_id >= 500:  # Medium-risk terminals
        terminal_risk = 0.1
    # Low-risk terminals (1-499) = 0.0

    print(f"🏪 Terminal risk factor: {terminal_risk}")

    # Category encoding
    category_mapping = {
        'grocery': 'grocery_pos', 'gas': 'gas_transport', 'shopping': 'shopping_pos',
        'entertainment': 'entertainment', 'restaurant': 'food_dining', 'travel': 'travel',
        'misc': 'misc_pos'
    }

    training_category = category_mapping.get(txn.category.lower(), 'misc_pos')
    manual_categories = [
        'grocery_pos', 'gas_transport', 'misc_net', 'grocery_net', 'shopping_net',
        'shopping_pos', 'entertainment', 'personal_care', 'health_fitness', 'travel',
        'kids_pets', 'food_dining', 'home', 'misc_pos'
    ]
    category_encoded = manual_categories.index(training_category) if training_category in manual_categories else 0

    # Create features for model (simplified)
    feature_names = ['amt', 'is_late_night', 'rolling_30d_amt', 'distance_from_prev_txn', 'category_encoded']

    enhanced_amount = float(txn.amount) * (1 + terminal_risk)

    features_df = pd.DataFrame([[
        enhanced_amount,
        int(is_late_night),
        1000.0,  # Fixed value
        0.0,  # Fixed value
        int(category_encoded)
    ]], columns=feature_names)

    print(f"🔍 Features for model:")
    print(features_df.to_string(index=False))

    # Predict with model
    prediction = 0
    probability = 0.0

    if model is not None:
        try:
            prediction = model.predict(features_df)[0]
            if hasattr(model, 'predict_proba'):
                prob_array = model.predict_proba(features_df)[0]
                probability = prob_array[1] if len(prob_array) > 1 else prob_array[0]

            # Adjust probability based on terminal risk
            probability = min(probability + terminal_risk, 1.0)

            print(f"🤖 Model prediction: {prediction}")
            print(f"📊 Fraud probability: {probability:.4f}")

        except Exception as e:
            print(f"❌ Model prediction failed: {e}")
            # Simple rule-based fallback
            if txn.amount > 2000 or terminal_risk > 0.2:
                prediction = 1
                probability = 0.8
            else:
                prediction = 0
                probability = 0.2
    else:
        print("❌ No model available, using rules")
        if txn.amount > 2000 or terminal_risk > 0.2:
            prediction = 1
            probability = 0.8
        else:
            prediction = 0
            probability = 0.2

    # Save transaction
    db_txn = models.Transaction(
        user_id=user_id,
        terminal_id=txn.terminal_id,
        amount=txn.amount,
        category=txn.category,
        is_late_night=bool(is_late_night),
        is_fraud=bool(prediction),
        timestamp=local_time.replace(tzinfo=None)
    )
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)

    print(f"✅ Transaction saved: ID={db_txn.id}, Fraud={db_txn.is_fraud}")

    return db_txn


def get_user_transactions(db: Session, user_id: int):
    """Get user transactions"""
    return db.query(models.Transaction).filter_by(user_id=user_id).order_by(desc(models.Transaction.timestamp)).all()


def get_terminal_stats(db: Session, terminal_id: int):
    """Get stats for a specific terminal"""
    transactions = db.query(models.Transaction).filter_by(terminal_id=terminal_id).all()

    if not transactions:
        return {"message": "No transactions found for this terminal"}

    total_amount = sum(t.amount for t in transactions)
    fraud_count = sum(1 for t in transactions if t.is_fraud)

    return {
        "terminal_id": terminal_id,
        "total_transactions": len(transactions),
        "total_amount": total_amount,
        "fraud_transactions": fraud_count,
        "fraud_rate": fraud_count / len(transactions) if len(transactions) > 0 else 0,
        "average_amount": total_amount / len(transactions) if len(transactions) > 0 else 0
    }


def get_user_stats(db: Session, user_id: int):
    """Get user stats"""
    transactions = get_user_transactions(db, user_id)

    if not transactions:
        return {"message": "No transactions found"}

    total_amount = sum(t.amount for t in transactions)
    fraud_count = sum(1 for t in transactions if t.is_fraud)

    terminal_usage = {}
    for txn in transactions:
        terminal_usage[txn.terminal_id] = terminal_usage.get(txn.terminal_id, 0) + 1

    most_used_terminal = max(terminal_usage.items(), key=lambda x: x[1]) if terminal_usage else (None, 0)

    return {
        "total_transactions": len(transactions),
        "total_amount": total_amount,
        "fraud_transactions": fraud_count,
        "fraud_rate": fraud_count / len(transactions) if len(transactions) > 0 else 0,
        "average_amount": total_amount / len(transactions) if len(transactions) > 0 else 0,
        "terminals_used": len(terminal_usage),
        "most_used_terminal": most_used_terminal[0] if most_used_terminal[0] else None,
        "most_used_terminal_count": most_used_terminal[1]
    }