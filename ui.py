import base64
import os
import requests
import streamlit as st

IMAGE_PATH = "cokie.png"

def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    return ""

bg_image_data = get_base64_image(IMAGE_PATH)

API_HOST = os.getenv("API_HOST", "http://api:8000")
API_URL = f"{API_HOST}/predict"

st.set_page_config(
    page_title="ChefAI - Cuisine Classifier",
    page_icon="🍳",
    layout="centered"
)

custom_css = f"""
<style>
    /* Bright background image with minimal tint */
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.15), rgba(15, 23, 42, 0.15)), url('{bg_image_data}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stMain"] {{
        background: transparent !important;
    }}

    /* Ultra-transparent liquid glass container effect */
    .block-container {{
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.25) 0%, rgba(15, 23, 42, 0.38) 100%) !important;
        backdrop-filter: blur(12px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(12px) saturate(200%) !important;
        border: 1px solid rgba(255, 255, 255, 0.28) !important;
        border-radius: 24px !important;
        padding: 2.5rem 2rem !important;
        margin-top: 2rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
    }}

    /* Standard app text styling */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown, .stCaption {{
        color: #ffffff !important;
        text-shadow: none !important;
    }}

    /* Style the User Manual button */
    [data-testid="stPopover"] button {{
        background-color: rgba(30, 41, 59, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }}
    [data-testid="stPopover"] button p {{
        color: #ffffff !important;
    }}
    [data-testid="stPopover"] button:hover {{
        background-color: rgba(51, 65, 85, 1) !important;
        border-color: #38bdf8 !important;
    }}

    /* POPDOWN CONTAINER BACKGROUND */
    div[data-baseweb="popover"] {{
        background-color: #0f172a !important;
    }}
    div[data-baseweb="popover"] > div,
    [data-testid="stPopoverBody"] {{
        background-color: #0f172a !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.85) !important;
    }}

    /* TEXT OVERRIDES INSIDE POPOVER */
    [data-testid="stPopoverBody"] p,
    [data-testid="stPopoverBody"] li,
    [data-testid="stPopoverBody"] span,
    [data-testid="stPopoverBody"] strong,
    [data-testid="stPopoverBody"] h3,
    [data-testid="stPopoverBody"] div {{
        color: #ffffff !important;
        background: transparent !important;
    }}

    /* Divider lines inside popover */
    [data-testid="stPopoverBody"] hr {{
        border: none !important;
        height: 1px !important;
        background-color: rgba(255, 255, 255, 0.25) !important;
        margin: 12px 0 !important;
    }}

    /* Input text area styling */
    .stTextArea textarea {{
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
    }}

    .ing-tag {{
        display: inline-block;
        background: rgba(245, 158, 11, 0.25);
        color: #FBBF24 !important;
        border: 1px solid rgba(245, 158, 11, 0.5);
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.88rem;
        font-weight: 500;
    }}

    .result-badge {{
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #ffffff !important;
        padding: 16px 24px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

col_title, col_manual = st.columns([3, 1])

with col_title:
    st.title("ChefAI Classifier")
    st.caption("Machine Learning Recipe Cuisine Prediction System")

with col_manual:
    st.write("")
    with st.popover("User Manual"):
        st.markdown("### How to Use ChefAI")
        st.markdown(
            "**Step 1:** Enter recipe ingredients separated by commas in the text box.\n\n"
            "**Step 2:** Click **Predict Cuisine** to run inference.\n\n"
            "---\n"
            "### Example Presets\n"
            "Copy and paste any set into the text area to test:\n\n"
            "- **Italian:** `pasta, parmesan cheese, olive oil, garlic, fresh basil, tomatoes`\n"
            "- **Indian:** `turmeric, garam masala, cumin seeds, coriander, ginger, ghee, mustard oil`\n"
            "- **Mexican:** `corn tortillas, jalapeno, cilantro, avocado, lime, black beans, salsa`\n"
            "- **Japanese:** `miso paste, dashi, mirin, soy sauce, seaweed, tofu, scallions`\n"
            "- **Greek:** `feta cheese, black olives, garlic, oregano, olive oil`\n\n"
            "---\n"
            "**Backend Status:** Check status at the bottom."
        )

st.divider()

st.subheader("Enter Ingredients")
raw_input = st.text_area(
    "Ingredients List:",
    value="feta cheese, black olives, garlic, oregano, olive oil",
    height=120,
    help="Enter ingredients separated by commas."
)

parsed_list = [ing.strip().lower() for ing in raw_input.split(",") if ing.strip()]

if parsed_list:
    st.write("**Detected Ingredients:**")
    chips_html = "".join([f'<span class="ing-tag">{ing}</span>' for ing in parsed_list])
    st.markdown(chips_html, unsafe_allow_html=True)
    st.write("")

predict_clicked = st.button("Predict Cuisine", type="primary", use_container_width=True)

if predict_clicked:
    if not parsed_list:
        st.warning("Please enter at least one valid ingredient before predicting.")
    else:
        with st.spinner("Running XGBoost model inference..."):
            try:
                response = requests.post(
                    API_URL, 
                    json={"ingredients": parsed_list},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    cuisine_name = result.get("cuisine", "Unknown").title()
                    
                    st.divider()
                    st.subheader("Prediction Result")
                    st.markdown(
                        f'<div class="result-badge">Predicted Cuisine: {cuisine_name}</div>', 
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"Server Error ({response.status_code}): Unable to complete prediction.")
            except requests.exceptions.ConnectionError:
                st.error(f"Connection Failed: Could not connect to FastAPI server at {API_HOST}. Ensure container is running.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

st.divider()

try:
    health_check = requests.post(API_URL, json={"ingredients": ["test"]}, timeout=1)
    if health_check.status_code == 200:
        st.caption("🟢 **API Status:** Connected to Containerized FastAPI (XGBoost Engine Ready)")
    else:
        st.caption("🟡 **API Status:** Server responding with issues")
except Exception:
    st.caption("🔴 **API Status:** Disconnected (Ensure Docker container `cuisine-api` is running on port 8000)")