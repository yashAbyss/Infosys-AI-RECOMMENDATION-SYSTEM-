# import streamlit as st
# import pandas as pd
# import numpy as np
# import random
# from preprocess_data import process_data

# from content_based_filtering import content_based_recommendation
# from collaborative_based_filtering import collaborative_filtering_recommendations
# from hybrid_approach import hybrid_recommendation_filtering
# from item_based_collaborative_filtering import item_based_collaborative_filtering
# st.set_page_config(page_title="AI based Ecommerce Recommendation system", layout="wide", page_icon="🛍️")
# st.markdown("""
# <style>
#     .block-container {
#         padding-top: 5rem;
#         padding-bottom: 2rem;
#     }
#     /* Product Card Styling */
#     div[data-testid="column"] {
#         background-color: #ffffff;
#         border: 1px solid #e0e0e0;
#         border-radius: 8px;
#         padding: 15px;
#         text-align: center;
#         box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
#         transition: transform 0.2s;
#         height: 100%;
#         display: flex;
#         flex-direction: column;
#         justify-content: space-between;
#     }
#     div[data-testid="column"]:hover {
#         transform: translateY(-5px);
#         box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
#     }
#     /* Clickable Image Wrapper */
#     .product-img-link {
#         display: block;
#         cursor: pointer;
#     }
#     .product-img {
#         height: 200px;
#         width: 100%;
#         object-fit: contain;
#         margin-bottom: 10px;
#         border-radius: 4px;
#         transition: transform 0.3s ease;
#     }
#     .product-img:hover {
#         transform: scale(1.05);
#     }
#     /* Detail View specific styling */
#     .detail-img {
#         height: 400px;
#         width: 100%;
#         object-fit: contain;
#         border-radius: 8px;
#         border: 1px solid #eee;
#     }
#     .product-title {
#         font-size: 14px;
#         font-weight: 600;
#         color: #333;
#         margin-top: 10px;
#         height: 40px;
#         overflow: hidden;
#         display: -webkit-box;
#         -webkit-line-clamp: 2;
#         -webkit-box-orient: vertical;
#     }
#     .product-brand {
#         font-size: 12px;
#         color: #777;
#         margin-bottom: 5px;
#     }
#     .product-rating {
#         color: #ffa41c;
#         font-size: 14px;
#     }
#     .section-header {
#         font-size: 24px;
#         font-weight: bold;
#         margin-top: 40px;
#         margin-bottom: 20px;
#         border-bottom: 2px solid #f0f0f0;
#         padding-bottom: 5px;
#     }
#     /* Custom Header Styling */
#     .title-text {
#         font-size: 40px !important;
#         background: -webkit-linear-gradient(45deg, #FF4B2B, #FF416C);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         font-weight: 800 !important;
#         padding-top: 0px;
#         margin-bottom: 0px;
#         line-height: 1.2;
#     }
#     .cat-img {
#         height: 150px;
#         width: 100%;
#         object-fit: cover;
#         border-radius: 50%;
#         margin-bottom: 10px;
#         transition: transform 0.3s ease;
#         border: 2px solid #fff;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#     }
#     .cat-img:hover {
#         transform: scale(1.1);
#         border-color: #ff4b2b;
#     }
#     .cat-label {
#         font-weight: bold;
#         color: #333;
#         margin-top: 10px;
#         text-align: center;
#         width: 100%;
#         display: block;
#         font-size: 14px;
#     }
#     .cat-container {
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         justify-content: center;
#         text-decoration: none;
#     }
#     /* Smart Badge Styling */
#     .badge {
#         position: absolute;
#         top: 10px;
#         right: 10px;
#         background-color: #ff4b2b;
#         color: white;
#         padding: 5px 10px;
#         border-radius: 20px;
#         font-size: 10px;
#         font-weight: bold;
#         z-index: 10;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.2);
#     }
#     .badge-value {
#         background-color: #00b894;
#     }
#     .product-card-container {
#         position: relative; /* For badge positioning */
#     }

# </style>
# """, unsafe_allow_html=True)
# if 'selected_product' not in st.session_state:
#     st.session_state['selected_product'] = None
# def set_selected_product(product):
#     """Callback to set the selected product in session state."""
#     st.session_state['selected_product'] = product
# def clear_query_params():
#     """Clears query params to prevent sticking to the detail view on refresh."""
#     st.query_params.clear()
# @st.cache_data
# def load_and_process_data():
#     """Loads and processes the dataset once."""
#     try:
#         raw_data = pd.read_csv("clean_data.csv")
#         data = process_data(raw_data)
#         if 'ImageURL' in data.columns:
#             data['ImageURL'] = data['ImageURL'].astype(str)
#         return data
#     except FileNotFoundError:
#         st.error("Error: 'clean_data.csv' not found.")
#         return None
#     except Exception as e:
#         st.error(f"Error processing data: {e}")
#         return None
# def get_smart_placeholder(name, prod_id):
#     """Returns a high-quality placeholder image based on product keywords."""
#     name_lower = str(name).lower()
#     placeholders = {
#         'nail': [
#             "https://images.unsplash.com/photo-1632516643720-e7f5d7d6ecc9?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1519014816548-bf5fe059e98b?auto=format&fit=crop&w=400&q=80",
#         ],
#         'shampoo': [
#             "https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1556228720-19277026dfb6?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1585232351009-3135dfeb7e38?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&w=400&q=80",
#         ],
#         'conditioner': [
#              "https://images.unsplash.com/photo-1576426863848-c218516d9b1a?auto=format&fit=crop&w=400&q=80",
#              "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?auto=format&fit=crop&w=400&q=80",
#         ],
#         'makeup': [
#             "https://images.unsplash.com/photo-1596462502278-27bfdd403348?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1522335789203-abd652396e00?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?auto=format&fit=crop&w=400&q=80",
#         ],
#         'generic': [
#             "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1616940842431-c426588288d0?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1608248597279-f99d160bfbc8?auto=format&fit=crop&w=400&q=80",
#             "https://images.unsplash.com/photo-1571781535009-ff1a3b538333?auto=format&fit=crop&w=400&q=80",
#         ]
#     }
#     category = 'generic'
#     if 'nail' in name_lower or 'lacquer' in name_lower or 'polish' in name_lower:
#         category = 'nail'
#     elif 'shampoo' in name_lower or 'wash' in name_lower:
#         category = 'shampoo'
#     elif 'conditioner' in name_lower or 'mask' in name_lower:
#         category = 'conditioner'
#     elif 'lip' in name_lower or 'eye' in name_lower or 'powder' in name_lower or 'up' in name_lower:
#         category = 'makeup'
#     try:
#         seed_val = int(str(prod_id).replace("-", "").replace(" ", "")[:8], 16) if isinstance(prod_id, str) else int(prod_id)
#     except:
#         seed_val = hash(str(prod_id))
#     random.seed(seed_val)
#     images = placeholders.get(category, placeholders['generic'])
#     selected_image = random.choice(images)
#     random.seed(None)
#     return selected_image
# def get_product_image_url(product_row):
#     """Refactored to be reusable."""
#     image_url = product_row.get('ImageURL', '')
#     if pd.isna(image_url) or image_url == '' or str(image_url).lower() == 'nan' or 'placehold.co' in str(image_url):
#          prod_id = product_row.get('ProdID', 'default')
#          prod_name = product_row.get('Name', '')
#          image_url = get_smart_placeholder(prod_name, prod_id)
#     return image_url
# def sort_by_rating(df):
#     """Helper to sort any dataframe by Rating (High -> Low)."""
#     if df is not None and not df.empty and 'Rating' in df.columns:
#         return df.sort_values(by='Rating', ascending=False)
#     return df

# def view_product_details(product_row, data):
#     """Renders the detailed view of a selected product."""
#     if 'view_history' not in st.session_state:
#         st.session_state['view_history'] = []
#     current_id = product_row.get('ProdID', product_row.get('Name'))

#     if current_id in st.session_state['view_history']:
#         st.session_state['view_history'].remove(current_id)
#     st.session_state['view_history'].insert(0, current_id)
#     if len(st.session_state['view_history']) > 10:
#         st.session_state['view_history'].pop()
#     if st.button("← Back to Shopping"):
#         set_selected_product(None)
#         clear_query_params()
#         st.rerun()
#     st.markdown("---")
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         img_url = get_product_image_url(product_row)
#         st.markdown(f'<img src="{img_url}" class="detail-img">', unsafe_allow_html=True)
#     with col2:
#         st.title(product_row.get('Name', 'Unknown Product'))
#         st.subheader(product_row.get('Brand', 'Generic Brand'))
#         rating = product_row.get('Rating', 0)
#         stars = "⭐" * int(min(round(rating), 5))
#         st.markdown(f"### {rating} {stars}")
#         st.markdown("#### Product Description")
#         st.write("Experience premium quality with this top-rated product. Perfect for your daily beauty routine.")
#         st.markdown(f"#### Price: **${random.randint(15, 60)}.99**")

#     st.markdown("---")
#     st.markdown("<div class='section-header'>✨ Similar Items</div>", unsafe_allow_html=True)
#     try:
#         similar_items = content_based_recommendation(data, item_name=product_row['Name'], top_n=4)
#         similar_items = sort_by_rating(similar_items)
#         display_product_grid(similar_items, section_key="detail_rec_content")
#     except Exception as e:
#         st.info("No similar products found.")
#     st.markdown("<div class='section-header'>👥 Users Also Bought/Liked</div>", unsafe_allow_html=True)
#     item_collab_recs = pd.DataFrame()
#     try:
#         prod_id = product_row.get('ProdID')
#         if prod_id:
#             item_collab_recs = item_based_collaborative_filtering(data, product_id=prod_id, top_n=4)
#             item_collab_recs = sort_by_rating(item_collab_recs)
#             if not item_collab_recs.empty:
#                 display_product_grid(item_collab_recs, section_key="detail_rec_item")
#             else:
#                 st.info("Not enough data to see what others bought.")
#         else:
#              st.info("Product ID not available for recommendations.")
#     except Exception as e:
#          st.info("Not enough purchase history for this item.")
# def display_product_card(product_row, key_suffix=""):
#     """Displays a single product card."""
#     image_url = get_product_image_url(product_row)
#     if 'ProdID' in product_row and pd.notna(product_row['ProdID']):
#         prod_id = int(product_row['ProdID'])
#         badge_html = ""
#         rating_val = product_row.get('Rating', 0)
#         if rating_val >= 4.5:
#              badge_html = "<div class='badge'>🏆 Top Rated</div>"
#         elif rating_val >= 4.0:
#              badge_html = "<div class='badge badge-value'>✨ Great Value</div>"
#         st.markdown(
#             f'<div class="product-card-container">'
#             f'{badge_html}'
#             f'<a href="./?product_id={prod_id}" target="_self">'
#             f'<img src="{image_url}" class="product-img" title="Click to view details">'
#             f'</a>'
#             f'</div>',
#             unsafe_allow_html=True
#         )
#     else:
#         prod_id = random.randint(0, 100000)
#         st.markdown(f'<img src="{image_url}" class="product-img">', unsafe_allow_html=True)
#     st.markdown(f"<div class='product-title'>{product_row.get('Name', 'Unknown Product')}</div>", unsafe_allow_html=True)
#     st.markdown(f"<div class='product-brand'>{product_row.get('Brand', 'Generic')}</div>", unsafe_allow_html=True)
#     rating = product_row.get('Rating', 0)
#     stars = "⭐" * int(min(round(rating), 5))
#     st.markdown(f"<div class='product-rating'>{rating} {stars}</div>", unsafe_allow_html=True)
#     st.button("Details",
#              key=f"btn_det_{prod_id}_{key_suffix}",
#              on_click=set_selected_product,
#              args=(product_row,))
# def display_product_grid(products_df, section_key):
#     """Renders a grid of product cards."""
#     if products_df is None or products_df.empty:
#         st.info("No products found.")
#         return
#     cols = st.columns(4)
#     indices = products_df.index.tolist()
#     for i, idx in enumerate(indices):
#         col = cols[i % 4]
#         with col:
#             display_product_card(products_df.loc[idx], key_suffix=f"{section_key}_{i}")
# def main():
#     data = load_and_process_data()
#     if data is None:
#         return

#     try:
#         query_params = st.query_params
#         q_category = query_params.get("category")
#         if q_category:
#              st.session_state['search_input'] = str(q_category).strip()
#              if hasattr(st, 'query_params'):
#                  st.query_params.clear()
#              elif hasattr(st, 'experimental_set_query_params'):
#                  st.experimental_set_query_params()
#         q_prod_id = query_params.get("product_id")
#         if q_prod_id:
#              q_prod_id = str(q_prod_id).strip()
#              found_product = data[data['ProdID'].astype(str) == q_prod_id]
#              if not found_product.empty:
#                  st.session_state['selected_product'] = found_product.iloc[0]
#                  st.toast(f"Auto-loading Product: {q_prod_id}")
#                  if hasattr(st, 'query_params'):
#                      st.query_params.clear()
#                  elif hasattr(st, 'experimental_set_query_params'):
#                      st.experimental_set_query_params()
#     except Exception as e:
#         st.error(f"Error parsing query params: {e}")
#         try:
#              q_params = st.experimental_get_query_params()
#              q_prod_id = q_params.get("product_id", [None])[0]
#              if q_prod_id:
#                   found_product = data[data['ProdID'].astype(str) == str(q_prod_id)]
#                   if not found_product.empty:
#                        st.session_state['selected_product'] = found_product.iloc[0]
#         except:
#              pass
#     with st.sidebar:
#         st.title("👤 Account")
#         target_user_id = st.number_input("User ID (Simulation)", min_value=1, value=4, step=1)
#         st.divider()
#         st.subheader("Navigation")
#         if st.button("🏠 Home"):
#             set_selected_product(None)
#             clear_query_params()
#             st.rerun()
#         st.radio("Go to:", ["Wishlist", "Orders"], label_visibility="collapsed")
#         st.divider()

#     if st.session_state['selected_product'] is not None:
#         view_product_details(st.session_state['selected_product'], data)
#     else:
#         col1, col2 = st.columns([3, 2])
#         with col1:
#              st.markdown('<h1 class="title-text">AI-Based Ecommerce<br>Recommendation System</h1>', unsafe_allow_html=True)
#         with col2:
#             st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
#             if 'search_input' not in st.session_state:
#                 st.session_state['search_input'] = ""
#             search_query = st.text_input("Search products...", value=st.session_state['search_input'], placeholder="🔍 Search for 'Nail Polish', 'Shampoo'...", label_visibility="collapsed", key="search_widget")
#             if search_query: st.session_state['search_input'] = search_query

#         if search_query:
#             st.markdown(f"<div class='section-header'>Results for '{search_query}'</div>", unsafe_allow_html=True)
#             try:
#                 search_results = data[data['Name'].astype(str).str.contains(search_query, case=False, na=False)]
#                 search_results = sort_by_rating(search_results)
#                 if search_results.empty:
#                     st.warning(f"No products found matching '{search_query}'. Trying hybrid recommendation...")
#                     search_results = hybrid_recommendation_filtering(data, item_name=search_query, target_user_id=target_user_id, top_n=10)
#                     search_results = sort_by_rating(search_results)
#                     if search_results.empty:
#                         st.error("No results found.")
#                 else:
#                     st.success(f"Found {len(search_results)} items.")
#                 display_product_grid(search_results, section_key="search")
#             except Exception as e:
#                 st.error(f"Search error: {e}")
#         else:
#             st.markdown("<div class='section-header'>📦 Shop by Category</div>", unsafe_allow_html=True)
#             cat_cols = st.columns(6)
#             categories = [
#                 {"name": "Nail Polish", "img": "https://images.unsplash.com/photo-1604654894610-df63bc536371?q=80&w=300&auto=format&fit=crop"},
#                 {"name": "Skin Care", "img": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=300&auto=format&fit=crop"},
#                 {"name": "Hair Care", "img": "https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=300&auto=format&fit=crop"},
#                 {"name": "Makeup", "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=300&auto=format&fit=crop"},
#                 {"name": "Fragrance", "img": "https://images.unsplash.com/photo-1541643600914-78b084683601?q=80&w=300&auto=format&fit=crop"},
#                 {"name": "Lips", "img": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?q=80&w=300&auto=format&fit=crop"}
#             ]
#             if 'view_history' in st.session_state and st.session_state['view_history']:
#                 st.markdown("<div class='section-header'>🕒 Recently Viewed</div>", unsafe_allow_html=True)
#                 history_ids = st.session_state['view_history']
#                 history_items = data[data['ProdID'].isin(history_ids)]
#                 history_items = history_items[history_items['ProdID'].isin(history_ids) | history_items['Name'].isin(history_ids)]
#                 display_product_grid(history_items, section_key="history")


#             for i, cat in enumerate(categories):
#                 with cat_cols[i]:
#                     cat_name = cat['name']
#                     img_url = cat['img']
#                     st.markdown(
#                         f'<a href="./?category={cat_name}" target="_self" class="cat-container">'
#                         f'<img src="{img_url}" class="cat-img" title="Shop {cat_name}">'
#                         f'<div class="cat-label">{cat_name}</div>'
#                         f'</a>',
#                         unsafe_allow_html=True
#                     )

#             st.markdown(f"<div class='section-header'>💙 Recommended for You (User {target_user_id})</div>", unsafe_allow_html=True)
#             try:
#                 collab_recs = collaborative_filtering_recommendations(data, target_user_id=target_user_id, top_n=4)
#                 collab_recs = sort_by_rating(collab_recs)
#                 if not collab_recs.empty:
#                     display_product_grid(collab_recs, section_key="collab")
#             except:
#                 pass
#     st.markdown("---")
#     st.caption("© 2024 ShopEasy E-Commerce Demo | Powered by Streamlit & Hybrid Recommendation System")
# if __name__ == "__main__":
#     main()



# # //////////////////////////////////////////////////////////////////////////////////////////////////////////



import streamlit as st
import pandas as pd
import numpy as np
import random
from preprocess_data import process_data

from content_based_filtering import content_based_recommendation
from collaborative_based_filtering import collaborative_filtering_recommendations
from hybrid_approach import hybrid_recommendation_filtering
from item_based_collaborative_filtering import item_based_collaborative_filtering

st.set_page_config(page_title="AI based Ecommerce Recommendation system", layout="wide", page_icon="🛍️")

st.markdown("""
<style>
    /* Global Background and Smooth Scrolling */
    .main {
        background:#bae6fd;
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    /* Modern Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    ::-webkit-scrollbar-thumb {
        background: #FF416C;
        border-radius: 10px;
    }

    /* Glassmorphism Product Card */
    div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px !important;
        padding: 20px !important;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }

    div[data-testid="column"]:hover {
        transform: translateY(-10px) scale(1.02) !important;
        box-shadow: 0 15px 45px rgba(255, 65, 108, 0.2) !important;
        border: 1px solid #FF416C !important;
    }

    /* Bouncing Image Animation */
    .product-img {
        height: 200px;
        width: 100%;
        object-fit: contain;
        margin-bottom: 15px;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.1));
        transition: transform 0.3s ease;
    }

    div[data-testid="column"]:hover .product-img {
        transform: scale(1.1);
    }

    /* Elegant Typography */
    .product-title {
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 10px;
        height: 45px;
        overflow: hidden;
    }

    .product-brand {
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 10px;
        font-weight: 800;
        color: #FF416C;
        margin-bottom: 8px;
    }

    /* Section Headers with Animated Underline */
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 28px;
        font-weight: 800;
        color: #2d3436;
        margin-top: 50px;
        margin-bottom: 30px;
        position: relative;
        display: inline-block;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        width: 50%;
        height: 4px;
        bottom: -5px;
        left: 0;
        background: linear-gradient(90deg, #FF4B2B, #FF416C);
        border-radius: 2px;
    }

    /* Interactive Category Circles */
    .cat-img {
        height: 140px;
        width: 140px;
        object-fit: cover;
        border-radius: 50%;
        margin-bottom: 15px;
        transition: all 0.5s ease;
        border: 4px solid white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    .cat-container:hover .cat-img {
        transform: rotate(10deg) scale(1.1);
        border-color: #FF416C;
        box-shadow: 0 15px 30px rgba(255, 65, 108, 0.3);
    }

    .cat-label {
        font-weight: 700;
        color: #2d3436;
        font-size: 16px;
        transition: color 0.3s ease;
    }
    
    .cat-container:hover .cat-label {
        color: #FF416C;
    }

    /* Floating Details Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px !important;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.3) !important;
    }

    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(255, 75, 43, 0.5) !important;
    }

    /* Detail View Adjustments */
    .detail-img {
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        transition: transform 0.5s ease;
    }
    .detail-img:hover {
        transform: scale(1.02);
    }

    /* Smart Badge Gradient */
    .badge {
        background: linear-gradient(45deg, #FF4B2B, #FF416C) !important;
        border: 2px solid white;
        font-family: 'Inter', sans-serif;
        padding: 6px 12px !important;
    }
    
    .badge-value {
        background: linear-gradient(45deg, #00b894, #00cec9) !important;
    }

    /* Search Bar UI */
    div[data-baseweb="input"] {
        border-radius: 15px !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
        background: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #FF416C !important;
        box-shadow: 0 4px 20px rgba(255, 65, 108, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

if 'selected_product' not in st.session_state:
    st.session_state['selected_product'] = None
if 'view_history' not in st.session_state:
    st.session_state['view_history'] = []

def set_selected_product(product):
    """Callback to set the selected product in session state."""
    st.session_state['selected_product'] = product

def clear_query_params():
    """Clears query params to prevent sticking to the detail view on refresh."""
    st.query_params.clear()

@st.cache_data
def load_and_process_data():
    """Loads and processes the dataset once."""
    try:
        raw_data = pd.read_csv("clean_data.csv")
        data = process_data(raw_data)
        if 'ImageURL' in data.columns:
            data['ImageURL'] = data['ImageURL'].astype(str)
        return data
    except FileNotFoundError:
        st.error("Error: 'clean_data.csv' not found.")
        return None
    except Exception as e:
        st.error(f"Error processing data: {e}")
        return None

def get_smart_placeholder(name, prod_id):
    """Returns a high-quality placeholder image based on product keywords."""
    name_lower = str(name).lower()
    placeholders = {
        'nail': ["https://images.unsplash.com/photo-1632516643720-e7f5d7d6ecc9?auto=format&fit=crop&w=400&q=80"],
        'shampoo': ["https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?auto=format&fit=crop&w=400&q=80"],
        'makeup': ["https://images.unsplash.com/photo-1596462502278-27bfdd403348?auto=format&fit=crop&w=400&q=80"],
        'generic': ["https://images.unsplash.com/photo-1556228578-0d85b1a4d571?auto=format&fit=crop&w=400&q=80"]
    }
    category = 'generic'
    if 'nail' in name_lower or 'lacquer' in name_lower or 'polish' in name_lower:
        category = 'nail'
    elif 'shampoo' in name_lower or 'wash' in name_lower:
        category = 'shampoo'
    elif 'lip' in name_lower or 'makeup' in name_lower:
        category = 'makeup'
    
    try:
        seed_val = int(str(prod_id).replace("-", "").replace(" ", "")[:8], 16) if isinstance(prod_id, str) else int(prod_id)
    except:
        seed_val = hash(str(prod_id))
    
    random.seed(seed_val)
    images = placeholders.get(category, placeholders['generic'])
    selected_image = random.choice(images)
    random.seed(None)
    return selected_image

def get_product_image_url(product_row):
    """Refactored to be reusable."""
    image_url = product_row.get('ImageURL', '')
    if pd.isna(image_url) or image_url == '' or str(image_url).lower() == 'nan' or 'placehold.co' in str(image_url):
         prod_id = product_row.get('ProdID', 'default')
         prod_name = product_row.get('Name', '')
         image_url = get_smart_placeholder(prod_name, prod_id)
    return image_url

def sort_by_rating(df):
    """Helper to sort any dataframe by Rating (High -> Low)."""
    if df is not None and not df.empty and 'Rating' in df.columns:
        return df.sort_values(by='Rating', ascending=False)
    return df

def view_product_details(product_row, data):
    """Renders the detailed view of a selected product and tracks history."""
    # Add to Recently Viewed
    current_id = product_row.get('ProdID')
    if current_id is not None:
        if current_id in st.session_state['view_history']:
            st.session_state['view_history'].remove(current_id)
        st.session_state['view_history'].insert(0, current_id)
        if len(st.session_state['view_history']) > 10:
            st.session_state['view_history'].pop()

    if st.button("← Back to Shopping"):
        set_selected_product(None)
        clear_query_params()
        st.rerun()

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        img_url = get_product_image_url(product_row)
        st.markdown(f'<img src="{img_url}" class="detail-img">', unsafe_allow_html=True)
    with col2:
        st.title(product_row.get('Name', 'Unknown Product'))
        st.subheader(product_row.get('Brand', 'Generic Brand'))
        rating = product_row.get('Rating', 0)
        stars = "⭐" * int(min(round(rating), 5))
        st.markdown(f"### {rating} {stars}")
        st.markdown("#### Product Description")
        st.write("Experience premium quality with this top-rated product. Perfect for your daily beauty routine.")
        st.markdown(f"#### Price: **${random.randint(15, 60)}.99**")

    st.markdown("---")
    st.markdown("<div class='section-header'>✨ Similar Items</div>", unsafe_allow_html=True)
    try:
        similar_items = content_based_recommendation(data, item_name=product_row['Name'], top_n=4)
        similar_items = sort_by_rating(similar_items)
        display_product_grid(similar_items, section_key="detail_rec_content")
    except:
        st.info("No similar products found.")

    st.markdown("<div class='section-header'>👥 Users Also Bought/Liked</div>", unsafe_allow_html=True)
    try:
        prod_id = product_row.get('ProdID')
        if prod_id:
            item_collab_recs = item_based_collaborative_filtering(data, product_id=prod_id, top_n=4)
            item_collab_recs = sort_by_rating(item_collab_recs)
            if not item_collab_recs.empty:
                display_product_grid(item_collab_recs, section_key="detail_rec_item")
            else:
                st.info("Not enough data to see what others bought.")
    except:
         st.info("Not enough purchase history for this item.")

def display_product_card(product_row, key_suffix=""):
    """Displays a single product card."""
    image_url = get_product_image_url(product_row)
    prod_id = product_row.get('ProdID', random.randint(0, 100000))
    
    badge_html = ""
    rating_val = product_row.get('Rating', 0)
    if rating_val >= 4.5:
         badge_html = "<div class='badge'>🏆 Top Rated</div>"
    elif rating_val >= 4.0:
         badge_html = "<div class='badge badge-value'>✨ Great Value</div>"

    st.markdown(
        f'<div class="product-card-container">'
        f'{badge_html}'
        f'<img src="{image_url}" class="product-img">'
        f'</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(f"<div class='product-title'>{product_row.get('Name', 'Unknown Product')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='product-brand'>{product_row.get('Brand', 'Generic')}</div>", unsafe_allow_html=True)
    stars = "⭐" * int(min(round(rating_val), 5))
    st.markdown(f"<div class='product-rating'>{rating_val} {stars}</div>", unsafe_allow_html=True)
    
    st.button("Details",
             key=f"btn_det_{prod_id}_{key_suffix}",
             on_click=set_selected_product,
             args=(product_row,))

def display_product_grid(products_df, section_key):
    """Renders a grid of product cards."""
    if products_df is None or products_df.empty:
        st.info("No products found.")
        return
    cols = st.columns(4)
    indices = products_df.index.tolist()
    for i, idx in enumerate(indices):
        col = cols[i % 4]
        with col:
            display_product_card(products_df.loc[idx], key_suffix=f"{section_key}_{i}")

def main():
    data = load_and_process_data()
    if data is None: return

    # Query Param Logic
    query_params = st.query_params
    if "product_id" in query_params:
        q_prod_id = str(query_params["product_id"])
        found_product = data[data['ProdID'].astype(str) == q_prod_id]
        if not found_product.empty:
            st.session_state['selected_product'] = found_product.iloc[0]

    with st.sidebar:
        st.title("👤 Account")
        target_user_id = st.number_input("User ID (Simulation)", min_value=1, value=4, step=1)
        st.divider()
        st.subheader("Navigation")
        if st.button("🏠 Home"):
            set_selected_product(None)
            clear_query_params()
            st.rerun()
        st.radio("Go to:", ["Wishlist", "Orders"], label_visibility="collapsed")
        st.divider()

    if st.session_state['selected_product'] is not None:
        view_product_details(st.session_state['selected_product'], data)
    else:
        col1, col2 = st.columns([3, 2])
        with col1:
             st.markdown('<h1 class="title-text">AI-Based Ecommerce<br>Recommendation System</h1>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
            search_query = st.text_input("Search products...", placeholder="🔍 Search...", label_visibility="collapsed", key="search_widget")

        if search_query:
            st.markdown(f"<div class='section-header'>Results for '{search_query}'</div>", unsafe_allow_html=True)
            search_results = data[data['Name'].astype(str).str.contains(search_query, case=False, na=False)]
            display_product_grid(sort_by_rating(search_results), section_key="search")
        else:
            st.markdown("<div class='section-header'>📦 Shop by Category</div>", unsafe_allow_html=True)
            cat_cols = st.columns(6)
            categories = [
                {"name": "Nail Polish", "img": "https://images.unsplash.com/photo-1604654894610-df63bc536371?q=80&w=300&auto=format&fit=crop"},
                {"name": "Skin Care", "img": "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?q=80&w=300&auto=format&fit=crop"},
                {"name": "Hair Care", "img": "https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=300&auto=format&fit=crop"},
                {"name": "Makeup", "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?q=80&w=300&auto=format&fit=crop"},
                {"name": "Fragrance", "img": "https://images.unsplash.com/photo-1541643600914-78b084683601?q=80&w=300&auto=format&fit=crop"},
                {"name": "Lips", "img": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?q=80&w=300&auto=format&fit=crop"}
            ]
            for i, cat in enumerate(categories):
                with cat_cols[i]:
                    st.markdown(f'<a href="./?category={cat["name"]}" target="_self" class="cat-container"><img src="{cat["img"]}" class="cat-img"><div class="cat-label">{cat["name"]}</div></a>', unsafe_allow_html=True)

            # --- RECENTLY VIEWED SECTION ---
            if st.session_state['view_history']:
                st.markdown("<div class='section-header'>🕒 Recently Viewed</div>", unsafe_allow_html=True)
                history_ids = st.session_state['view_history']
                history_items = data[data['ProdID'].isin(history_ids)].copy()
                # Sort to maintain the order of history (most recent first)
                history_items['ProdID'] = history_items['ProdID'].astype(type(history_ids[0]))
                history_items = history_items.set_index('ProdID').loc[history_ids].reset_index()
                display_product_grid(history_items, section_key="history")

            st.markdown(f"<div class='section-header'>💙 Recommended for You (User {target_user_id})</div>", unsafe_allow_html=True)
            try:
                collab_recs = collaborative_filtering_recommendations(data, target_user_id=target_user_id, top_n=4)
                display_product_grid(sort_by_rating(collab_recs), section_key="collab")
            except: pass

    st.markdown("---")
    st.caption("© 2024 ShopEasy E-Commerce Demo | Powered by Streamlit & Hybrid Recommendation System")

if __name__ == "__main__":
    main()