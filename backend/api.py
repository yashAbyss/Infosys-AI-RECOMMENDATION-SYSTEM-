
# import sys
# import os

# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, PROJECT_ROOT)

# from fastapi import FastAPI, HTTPException
# import pandas as pd

# from preprocess_data import process_data
# from rating_based_recommendation import get_top_rated_items
# from collaborative_based_filtering import collaborative_filtering_recommendations
# from hybrid_approach import hybrid_recommendation_filtering

# # ------------------ FASTAPI APP ------------------
# app = FastAPI(
#     title="AI Enabled Recommendation Engine",
#     version="1.0.0"
# )

# # ------------------ LOAD DATA ONCE ------------------
# try:
#     raw_data = pd.read_csv(os.path.join(PROJECT_ROOT, "clean_data.csv"))
#     data = process_data(raw_data)
# except Exception as e:
#     raise RuntimeError(f"Failed to load data: {e}")

# # ------------------ HEALTH CHECK ------------------

# @app.get("/")
# def health():
#     return {"status": "API running"}

# # ------------------ TOP RATED ------------------

# @app.get("/recommend/top-rated")
# def top_rated(top_n: int = 10):
#     result = get_top_rated_items(data, top_n)
#     return result.to_dict(orient="records")

# # ------------------ COLLABORATIVE ------------------

# @app.get("/recommend/collaborative")
# def collaborative(user_id: int, top_n: int = 10):

#     if user_id not in data["ID"].values:
#         raise HTTPException(404, "User ID not found")

#     result = collaborative_filtering_recommendations(
#         data=data,
#         target_user_id=user_id,
#         top_n=top_n
#     )

#     if result.empty:
#         raise HTTPException(404, "No recommendations found")

#     return result.to_dict(orient="records")

# # ------------------ HYBRID ------------------

# @app.get("/recommend/hybrid")
# def hybrid(user_id: int, product_name: str, top_n: int = 10):

#     if user_id not in data["ID"].values:
#         raise HTTPException(404, "User ID not found")

#     result = hybrid_recommendation_filtering(
#         data=data,
#         item_name=product_name,
#         target_user_id=user_id,
#         top_n=top_n
#     )

#     if result.empty:
#         raise HTTPException(404, "No hybrid recommendations found")

#     return result.to_dict(orient="records")

# @app.get("/products")
# def get_all_products():
#     products = (
#         data["Name"]
#         .dropna()
#         .unique()
#         .tolist()
#     )
#     products.sort()
#     return products



# ------------------ PATH FIX (CRITICAL) ------------------
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# ------------------ IMPORTS ------------------
from fastapi import FastAPI, HTTPException
import pandas as pd

from preprocess_data import process_data
from rating_based_recommendation import get_top_rated_items
from collaborative_based_filtering import collaborative_filtering_recommendations
from hybrid_approach import hybrid_recommendation_filtering

# ------------------ FASTAPI APP ------------------
app = FastAPI(
    title="AI Enabled Recommendation Engine",
    version="1.0.0"
)

# ------------------ LOAD DATA ONCE ------------------
try:
    raw_data = pd.read_csv(os.path.join(PROJECT_ROOT, "clean_data.csv"))
    data = process_data(raw_data)
except Exception as e:
    raise RuntimeError(f"Failed to load data: {e}")

# ------------------ HEALTH CHECK ------------------
@app.get("/")
def health():
    return {"status": "API running"}

# ------------------ TOP RATED ------------------
@app.get("/recommend/top-rated", tags=["Recommendations"])
def top_rated(top_n: int = 10):
    result = get_top_rated_items(data, top_n)

    # 🔥 FIX: NaN → None (JSON safe)
    result = result.where(pd.notnull(result), None)

    return result.to_dict(orient="records")

# ------------------ COLLABORATIVE ------------------
@app.get("/recommend/collaborative", tags=["Recommendations"])
def collaborative(user_id: int, top_n: int = 10):

    if user_id not in data["ID"].values:
        raise HTTPException(status_code=404, detail="User ID not found")

    result = collaborative_filtering_recommendations(
        data=data,
        target_user_id=user_id,
        top_n=top_n
    )

    if result.empty:
        raise HTTPException(status_code=404, detail="No recommendations found")

    # 🔥 FIX: NaN → None (JSON safe)
    result = result.where(pd.notnull(result), None)

    return result.to_dict(orient="records")

# ------------------ HYBRID ------------------
@app.get("/recommend/hybrid", tags=["Recommendations"])
def hybrid(user_id: int, product_name: str, top_n: int = 10):

    if user_id not in data["ID"].values:
        raise HTTPException(status_code=404, detail="User ID not found")

    result = hybrid_recommendation_filtering(
        data=data,
        item_name=product_name,
        target_user_id=user_id,
        top_n=top_n
    )

    if result.empty:
        raise HTTPException(status_code=404, detail="No hybrid recommendations found")

    # 🔥 FIX: NaN → None (JSON safe)
    result = result.where(pd.notnull(result), None)

    return result.to_dict(orient="records")

# ------------------ PRODUCTS (FOR STREAMLIT DROPDOWN) ------------------
@app.get("/products", tags=["Metadata"])
def get_all_products():
    products = (
        data["Name"]
        .dropna()
        .unique()
        .tolist()
    )
    products.sort()
    return products

