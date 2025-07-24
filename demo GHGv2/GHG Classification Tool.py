import streamlit as st
import pandas as pd
import time
import io
from datetime import datetime
import json
import base64
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="GHG Scope 3 Category 1 Classification",
    page_icon="assets/pwc_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with sustainability-focused color scheme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables for easy color management */
    :root {
        --primary-sage: #70798c;
        --primary-navy: #153243;
        --secondary-blue: #284B63;
        --alice-blue: #E3F2FD;
        --light-gray: #EEF0EB;
        --accent-gradient: linear-gradient(135deg, #153243 0%, #284B63 50%, #153243 100%);
        --subtle-gradient: linear-gradient(135deg, #284B63 0%, #153243 35%, #B4B8AB 100%);
        --light-gradient: linear-gradient(135deg, #e3f2fd 0%, #EEF0EB 100%);
        --orange-gradient: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ff6b35 100%);
        --green-gradient: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
    }
    
    .main-header {
        background: transparent;
        color: var(--primary-forest);
        padding: 2rem 0 1rem 0;
        margin: 0 0 2rem 0;
        text-align: left;
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .main-header .header-logo {
        height: 150px;
        width: auto;
        flex-shrink: 0;
    }
    
    .main-header .header-content {
        flex: 1;
    }
    
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        color: var(--primary-forest);
        letter-spacing: -0.3px;
    }
    
    .main-header p {
        font-size: 1rem;
        color: #6b7280;
        margin: 0;
        font-weight: 400;
    }
    
    .loading-container {
        background: linear-gradient(135deg, rgba(227, 242, 253, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
        border: 2px solid var(--primary-navy);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        text-align: left;
        box-shadow: 
            0 8px 32px rgba(21, 50, 67, 0.15),
            0 2px 8px rgba(21, 50, 67, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(15px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .loading-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    .loading-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .loading-spinner-container {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .loading-spinner {
        width: 28px;
        height: 28px;
        border: 3px solid rgba(21, 50, 67, 0.1);
        border-top: 3px solid var(--primary-navy);
        border-radius: 50%;
        animation: spin 1.2s linear infinite;
        filter: drop-shadow(0 2px 4px rgba(21, 50, 67, 0.2));
    }
    
    .loading-text-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .loading-text {
        color: var(--primary-forest);
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
        animation: fadeInOut 2s infinite;
    }
    
    .loading-subtitle {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0;
        opacity: 0.8;
    }
    
    .loading-dots {
        display: flex;
        gap: 0.25rem;
        margin-left: 0.5rem;
        align-self: center;
    }
    
    .loading-dot {
        width: 6px;
        height: 6px;
        background: var(--primary-navy);
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dot:nth-child(1) { animation-delay: -0.32s; }
    .loading-dot:nth-child(2) { animation-delay: -0.16s; }
    .loading-dot:nth-child(3) { animation-delay: 0; }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: scale(1);
            opacity: 0.3;
        }
        50% { 
            transform: scale(1.1);
            opacity: 0.1;
        }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes bounce {
        0%, 80%, 100% { 
            transform: scale(0);
            opacity: 0.5;
        } 
        40% { 
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Enhanced progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-navy) 0%, #16a34a 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(21, 50, 67, 0.3);
    }
    
    .stProgress > div > div > div {
        background: rgba(21, 50, 67, 0.1);
        border-radius: 10px;
        height: 12px !important;
    }
    
    .step-header {
        display: flex;
        align-items: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-forest);
        margin-bottom: 2.5rem;
        padding: 1rem 0;
        border-bottom: 3px solid transparent;
        background: transparent;
        border-image: var(--accent-gradient) 1;
        border-bottom: 3px solid;
        border-image-slice: 1;
    }
    
    .step-number {
        background: var(--accent-gradient);
        color: white;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        margin-right: 1.25rem;
        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.3);
        transition: all 0.3s ease;
    }
    
    .step-number:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(27, 94, 32, 0.4);
    }
    
    .step-number.completed {
        background: var(--green-gradient);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
    }
    
    .content-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid var(--light-gray);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .content-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 20px 20px 0 0;
    }
    
    .content-section:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 40px rgba(21, 50, 67, 0.08);
    }
    
    .stFileUploader > div > div {
        background: var(--light-gradient);
        border: 2px dashed var(--primary-sage);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--secondary-blue);
        background: linear-gradient(135deg, var(--light-gray) 0%, var(--alice-blue) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.1);
    }
    
    .stFileUploader label {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-forest);
    }
    
    .file-summary {
        background: #E8F9EE;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        box-shadow: 0 4px 15px rgba(2, 31, 32, 0.4);
        transition: all 0.3s ease;
    }
    
    .file-info {
        flex-grow: 1;
    }
    
    .file-name {
        font-weight: 700;
        color: #257549;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .file-details {
        color: var(--secondary-blue);
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(21, 50, 67, 0.3) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stButton > button:disabled {
        background: #94a3b8 !important;
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid #e6f7f1 !important;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
        width: 100%;
    }
    
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-top: 4px solid #153243;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.15);
        border-color: #cbd5e1;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #153243;
        margin: 0.5rem 0;
        line-height: 1.2;
        word-break: break-word;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
        line-height: 1.3;
    }
    
    .workflow-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e6f7f1;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .workflow-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.1);
    }
    
    .workflow-card.selected {
        border-color: var(--primary-navy);
        background: linear-gradient(135deg, #e3f2fd 0%, #f8fafc 100%);
    }
    
    .workflow-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--primary-forest);
        margin-bottom: 0.5rem;
    }
    
    .workflow-description {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .checkbox-container {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    /* Hide the marker div */
    .workflow-container-marker {
        display: none;
    }
    
    .workflow-container-please{
        border: 2px solid #e6f7f1;
        border-radius: 12px;
    }

    /* Style workflow containers that contain the marker */
    div[data-testid="container"]:has(.workflow-container-marker) {
        background: white;
        border: 2px solid #e6f7f1;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
    }
    
    div[data-testid="container"]:has(.workflow-container-marker):hover {
        border-color: #d1e7dd;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Style for selected workflows */
    div[data-testid="container"]:has(.workflow-container-marker):has(input[type="checkbox"]:checked) {
        border-color: var(--primary-navy);
        background: linear-gradient(135deg, #e3f2fd 0%, #f8fafc 100%);
        box-shadow: 0 4px 15px rgba(21, 50, 67, 0.1);
    }
    
    /* Simple workflow description styling */
    .workflow-description-simple {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-left: 2rem;
        font-style: italic;
    }
    
    /* Adjust description in selected state */
    div[data-testid="container"]:has(.workflow-container-marker):has(input[type="checkbox"]:checked) .workflow-description-simple {
        color: #475569;
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--primary-navy) 50%, transparent 100%);
        margin: 3rem 0;
        border: none;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Success message styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.15) !important;
    }
    
    .eda-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #e6f7f1;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        border-left: 5px solid var(--primary-navy);
        transition: all 0.3s ease;
    }
    
    .eda-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(21, 50, 67, 0.1);
    }
    
    .eda-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-forest);
        margin-bottom: 1rem;
    }
    
    .eda-content {
        color: #475569;
        line-height: 1.7;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'uploaded_excel': None,
        'client_info': None,
        'purchased_goods': None,
        'uploading': False,
        'file_processed': False,
        'selected_workflows': ['Data Cleaning', 'Information Augmentation', 'Classification'],  # Default all selected
        'pipeline_running': False,
        'pipeline_complete': False,
        'results': None,
        'workflow_status': {
            'Data Cleaning': {'running': False, 'complete': False, 'progress': 0},
            'Information Augmentation': {'running': False, 'complete': False, 'progress': 0},
            'Classification': {'running': False, 'complete': False, 'progress': 0}
        },
        'client_info_edited': False,
        'editing_client_info': False,
        'client_info_backup': None,
        'client_info_current': None,
        'show_reset_confirmation': False
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def reset_app():
    """Reset all app states"""
    st.session_state.uploaded_excel = None
    st.session_state.client_info = None
    st.session_state.purchased_goods = None
    st.session_state.uploading = False
    st.session_state.file_processed = False
    st.session_state.selected_workflows = ['Data Cleaning', 'Information Augmentation', 'Classification']
    st.session_state.pipeline_running = False
    st.session_state.pipeline_complete = False
    st.session_state.results = None
    st.session_state.workflow_status = {
        'Data Cleaning': {'running': False, 'complete': False, 'progress': 0},
        'Information Augmentation': {'running': False, 'complete': False, 'progress': 0},
        'Classification': {'running': False, 'complete': False, 'progress': 0}
    }
    st.session_state.client_info_edited = False
    st.session_state.editing_client_info = False
    st.session_state.client_info_backup = None
    st.session_state.client_info_current = None
    st.session_state.show_reset_confirmation = False

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def analyze_purchased_goods(df):
    """Perform basic EDA on purchased goods data"""
    analysis = {}
    
    # Basic statistics
    analysis['total_rows'] = len(df)
    analysis['total_columns'] = len(df.columns)
    # Check for duplicates in Line Item column if it exists
    if 'Line Item' in df.columns:
        analysis['duplicates'] = df['Line Item'].duplicated().sum()
    else:
        analysis['duplicates'] = df.duplicated().sum()
    analysis['missing_values'] = df.isnull().sum().sum()
    analysis['data_types'] = df.dtypes.value_counts().to_dict()
    
    # Identify potential spend columns (containing currency/numeric data)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    analysis['numeric_columns'] = numeric_cols
    
    # Basic statistics for numeric columns
    if numeric_cols:
        analysis['numeric_summary'] = df[numeric_cols].describe()
    
    # Memory usage
    analysis['memory_usage'] = df.memory_usage(deep=True).sum()
    
    # Detect columns with item descriptions
    description_keywords = ['description', 'desc', 'item', 'product', 'name', 'title']
    description_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in description_keywords)]
    
    # Check for items with descriptions (non-null values in description columns)
    items_with_descriptions = 0
    if description_columns:
        for col in description_columns:
            items_with_descriptions += df[col].notna().sum()
    
    analysis['description_columns'] = description_columns
    analysis['items_with_descriptions'] = min(items_with_descriptions, len(df))  # Cap at total rows to avoid double counting
    
    return analysis

def get_mock_classification_results():
    """Return classification results from Excel file"""
    try:
        # Read the mock results Excel file
        excel_path = "assets/Retail test data - mock_results.xlsx"
        
        # Read the three result tabs
        result_1 = pd.read_excel(excel_path, sheet_name="Result 1 - All Classified")
        result_2 = pd.read_excel(excel_path, sheet_name="Result 2 - Non Scope 3 Cat 1")
        result_3 = pd.read_excel(excel_path, sheet_name="Result 3 - Unable to Classify")
        
        # Count items in each tab
        all_classified_count = len(result_1)
        non_scope3_count = len(result_2)
        unable_to_classify_count = len(result_3)
        
        return {
            'total_items': all_classified_count + non_scope3_count + unable_to_classify_count,
            'all_classified_items': all_classified_count,
            'non_scope3_items': non_scope3_count,
            'unable_to_classify_items': unable_to_classify_count,
            'result_1_data': result_1,
            'result_2_data': result_2,
            'result_3_data': result_3
        }
    except Exception as e:
        # Fallback to original mock data if file reading fails
        return {
            'total_items': 1247,
            'all_classified_items': 1183,
            'non_scope3_items': 0,
            'unable_to_classify_items': 64,
            'error': f"Could not read Excel file: {str(e)}"
        }

def apply_conditional_formatting(df):
    """Apply conditional formatting to To Validate column and format NAICS confidence"""
    def highlight_to_validate(val):
        if val == 'N':
            return 'background-color: #d4edda'  # Light green
        elif val == 'Y':
            return 'background-color: #f8d7da'  # Light red
        else:
            return ''
    
    styled_df = df.style
    
    # Apply To Validate column formatting
    if 'To Validate' in df.columns:
        styled_df = styled_df.applymap(highlight_to_validate, subset=['To Validate'])
    
    # Format NAICS Confidence to 2 decimal places
    if 'NAICS Confidence' in df.columns:
        styled_df = styled_df.format({'NAICS Confidence': '{:.2f}'})
    
    return styled_df

# Initialize session state
init_session_state()

# Sidebar with reset button
with st.sidebar:
    @st.dialog("Are you sure you want to reset?")
    def reset_confirmation():
        st.markdown("""
        <div style="text-align: center;">
            <h4 style="color: #153243; margin-bottom: 1rem;">This will clear all uploaded files and analysis results. This action cannot be undone.</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Yes, Reset", type="primary", use_container_width=True):
                streamlit_js_eval(js_expressions="parent.window.location.reload()")
        with col3:
            if st.button("Cancel", use_container_width=True):
                st.rerun()
    
    if st.button("🔄 Reset Application", type="primary", use_container_width=True):
        reset_confirmation()

# Header
st.markdown("""
<div class="main-header">
    <img src="data:image/png;base64,{}" class="header-logo" alt="PwC Logo">
    <div class="header-content">
        <h1>ESG Reporting - GHG Scope 3 Category 1 Classification Tool</h1>
        <p>Classify purchased goods and services for carbon footprint analysis</p>
    </div>
</div>
""".format(base64.b64encode(open("assets/pwc_logo.png", "rb").read()).decode()), unsafe_allow_html=True)

# Step 1: Upload Excel File
step1_class = ""
st.markdown(f"""
<div class="step-header">
    <div class="step-number {step1_class}">1</div>
    <div>Upload Excel File</div>
</div>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an Excel file with client information and purchased goods data", 
    type=['xlsx', 'xls'], 
    help="Upload an Excel file with two tabs: 'Client Description' and 'Line Items'",
    key="file_upload"
)

if uploaded_file is not None and not st.session_state.file_processed:
    st.session_state.uploaded_excel = uploaded_file
    
    try:
        # Read Excel file with multiple sheets
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        
        # Check if required sheets exist
        required_sheets = ['Client Description', 'Line Items']
        available_sheets = list(excel_data.keys())
        
        if all(sheet in available_sheets for sheet in required_sheets):
            st.session_state.client_info = excel_data['Client Description']
            st.session_state.purchased_goods = excel_data['Line Items']
            st.session_state.file_processed = True
            
            # Display file summary
            file_size = format_file_size(uploaded_file.size)
            st.markdown(f"""
            <div class="file-summary">
                <div class="file-info">
                    <div class="file-name">{uploaded_file.name}</div>
                    <div class="file-details"><b>Uploaded successfully</b>: {file_size} • {len(available_sheets)} sheets</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.rerun()
        else:
            st.error(f"❌ Required sheets not found. Please ensure your Excel file contains: {', '.join(required_sheets)}")
            st.info(f"Available sheets: {', '.join(available_sheets)}")
            
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {str(e)}")

# Step 2: Display and Edit Client Information
if st.session_state.file_processed:
    st.markdown("---")
    step2_class = ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step2_class}">2</div>
        <div>Client Description</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("### Client Description Table")
    
    # Initialize client_info_current if not exists
    if st.session_state.client_info_current is None:
        st.session_state.client_info_current = st.session_state.client_info.copy()
    
    # Display table (editable or read-only based on state)
    if st.session_state.editing_client_info:
        # Create backup on first edit
        if st.session_state.client_info_backup is None:
            st.session_state.client_info_backup = st.session_state.client_info_current.copy()
        
        # Use data_editor and let it update client_info_current directly
        st.session_state.client_info_current = st.data_editor(
            st.session_state.client_info_current,
            use_container_width=True,
            hide_index=True,
            key="client_info_editor_active"
        )
        
        # Show Save Changes and Cancel buttons
        col1, col2, col3 = st.columns([2, 2, 8])
        with col1:
            if st.button("💾 Save Changes", key="save_client_info", use_container_width=True):
                # Save the current edited data as the main client_info
                st.session_state.client_info = st.session_state.client_info_current.copy()
                st.session_state.client_info_edited = True
                st.session_state.editing_client_info = False
                st.session_state.client_info_backup = None  # Clear backup
                st.success("✅ Client information saved successfully!")
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", key="cancel_client_info", use_container_width=True):
                # Restore from backup
                if st.session_state.client_info_backup is not None:
                    st.session_state.client_info_current = st.session_state.client_info_backup.copy()
                st.session_state.editing_client_info = False
                st.session_state.client_info_backup = None  # Clear backup
                st.rerun()
    else:
        # Display read-only table with the saved data
        st.dataframe(
            st.session_state.client_info,
            use_container_width=True,
            hide_index=True
        )
        
        # Show only Edit button
        col1, col2, col3 = st.columns([2, 2, 8])
        with col1:
            if st.button("✏️ Edit", key="edit_client_info", use_container_width=True):
                # Initialize current data from saved data when starting edit
                st.session_state.client_info_current = st.session_state.client_info.copy()
                st.session_state.editing_client_info = True
                st.rerun()

# Step 3: Purchased Goods Analysis
if st.session_state.file_processed:
    st.markdown("---")
    step3_class = ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step3_class}">3</div>
        <div>Line Items Analysis</div>
    </div>""", unsafe_allow_html=True)
    
    # Perform EDA
    analysis = analyze_purchased_goods(st.session_state.purchased_goods)
    
    # Calculate share of spend sum if available
    spend_columns = [col for col in st.session_state.purchased_goods.columns if 'spend' in col.lower() or 'amount' in col.lower() or 'cost' in col.lower() or 'price' in col.lower()]
    total_spend = 0
    if spend_columns:
        # Use the first spend-related column found
        spend_col = spend_columns[0]
        total_spend = st.session_state.purchased_goods[spend_col].sum() if pd.api.types.is_numeric_dtype(st.session_state.purchased_goods[spend_col]) else 0
    
    # Prepare conditional messages
    duplicates_action = "<div style='color: #dc2626; font-size: 0.8rem; margin-top: 0.5rem; font-weight: 600;'>Action Required</div>" if analysis['duplicates'] > 0 else ""
    missing_values_action = "<div style='color: #dc2626; font-size: 0.8rem; margin-top: 0.5rem; font-weight: 600;'>Action Required</div>" if analysis['missing_values'] > 0 else ""
    
    # Check if item descriptions are detected
    descriptions_detected = "No"
    descriptions_color = "#153243"
    descriptions_action = "<div style='color: #dc2626; font-size: 0.8rem; margin-top: 0.5rem; font-weight: 600;'>Action Required</div>"
    
    # Display metrics above the table
    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">{analysis['total_rows']:,}</div>
            <div class="metric-label">Number of Rows</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{analysis['duplicates']:,}</div>
            <div class="metric-label">Number of Duplicates</div>
            {duplicates_action}
        </div>
        <div class="metric-card">
            <div class="metric-value" style="color: {descriptions_color};">{descriptions_detected}</div>
            <div class="metric-label">Item Descriptions Detected</div>
            {descriptions_action}
        </div>
        <div class="metric-card">
            <div class="metric-value">{analysis['missing_values']:,}</div>
            <div class="metric-label">Missing Values</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">${total_spend:,.2f}</div>
            <div class="metric-label">Total Share of Spend</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Line Items Data")
    
    # Display the line items table with highlighting for duplicates and formatting
    df_display = st.session_state.purchased_goods.copy()
    
    # Check if 'Line Item' column exists and highlight duplicates
    if 'Line Item' in df_display.columns:
        # Create a function to highlight duplicate cells
        def highlight_duplicates(series):
            duplicated = series.duplicated(keep=False)
            return ['background-color: #fee2e2; border: 1px solid #ef4444' if is_dup else '' for is_dup in duplicated]
        
        # Apply styling to the dataframe
        styled_df = df_display.style.apply(highlight_duplicates, subset=['Line Item'])
        
        # Format Share of Spend column to 2 decimal places
        if 'Share of spend' in df_display.columns:
            styled_df = styled_df.format({'Share of spend': '{:.2f}'})
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        # If no Line Item column, display normally but still format Share of Spend
        styled_df = df_display.style
        if 'Share of Spend' in df_display.columns:
            styled_df = styled_df.format({'Share of Spend': '{:.2f}'})
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Step 4: GenAI Pipeline
if st.session_state.file_processed:
    st.markdown("---")
    step4_class = ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step4_class}">4</div>
        <div>GenAI Pipeline</div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("### Select Workflows to Run")
    st.markdown(" ")
    # Workflow options
    workflows = {
        'Data Cleaning': 'Clean and standardize line items data, remove duplicates, and handle missing values',
        'Information Augmentation': 'Enhance product descriptions with additional metadata and categorization hints',
        'Classification': 'Classify line items into GHG Scope 3 Category 1 subcategories using AI models'
    }
    
    # Display workflow selection with simple checkboxes
    for workflow, description in workflows.items():
        selected = workflow in st.session_state.selected_workflows
        
        # Use Streamlit container with specific styling
        container = st.container()
        with container:
            # Add a marker class to identify workflow containers
            st.markdown('<div class="workflow-container-please">', unsafe_allow_html=True)
            # st.markdown('<div class="workflow-container-marker"></div>', unsafe_allow_html=True)
            # Simple checkbox with clean styling
            st.markdown('<div style = "height: 10px"></div>', unsafe_allow_html = True)
            if st.checkbox(f"**{workflow}**", value=selected, key=f"workflow_{workflow}"):
                if workflow not in st.session_state.selected_workflows:
                    st.session_state.selected_workflows.append(workflow)
                    st.rerun()
            else:
                if workflow in st.session_state.selected_workflows:
                    st.session_state.selected_workflows.remove(workflow)
                    st.rerun()
            
            # Description below the checkbox
            st.markdown(f"<div class='workflow-description-simple'>{description}</div>", unsafe_allow_html=True)
            st.markdown('<div style = "height: 10px"></div>', unsafe_allow_html = True)
            st.markdown('</div>', unsafe_allow_html=True)
    # Run pipeline button
    if not st.session_state.pipeline_running and not st.session_state.pipeline_complete:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 6, 3])
        with col1:
            if st.button("Run GenAI Pipeline", key="run_pipeline", use_container_width=True):
                if st.session_state.selected_workflows:
                    st.session_state.pipeline_running = True
                    st.rerun()
                else:
                    st.error("Please select at least one workflow to run.")
    
    # Pipeline running state with individual workflow loading
    if st.session_state.pipeline_running:
        st.markdown('<div style = "height: 20px"></div>', unsafe_allow_html = True)
        
        # Display individual workflow loading states
        for workflow in st.session_state.selected_workflows:
            workflow_data = st.session_state.workflow_status[workflow]
            
            if workflow_data['running']:
                st.markdown(f"""
                <div class="loading-container">
                    <div class="loading-content">
                        <div class="loading-spinner-container">
                            <div class="loading-spinner"></div>
                        </div>
                        <div class="loading-text-container">
                            <div class="loading-text">Running {workflow}</div>
                            <div class="loading-subtitle">Processing workflow...</div>
                        </div>
                        <div class="loading-dots">
                            <div class="loading-dot"></div>
                            <div class="loading-dot"></div>
                            <div class="loading-dot"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Individual progress bar for this workflow
                progress_bar = st.progress(workflow_data['progress'])
                
            elif workflow_data['complete']:
                st.markdown(f"""
                <div style="background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                    <div style="color: #0ea5e9; font-weight: 600;">✅ {workflow} - Completed</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Create progress tracking for each selected workflow
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        progress_bar_placeholder = st.empty()
        
        # Run each selected workflow with loading animation
        total_workflows = len(st.session_state.selected_workflows)
        workflow_messages = ["Cleaning and standardizing line items data, performing item level clustering...", "Enhancing line items with additional data...", "Classifying line items into relevant NAICS codes..."]
        for i, workflow in enumerate(st.session_state.selected_workflows):
            # Clear previous progress bar before starting new workflow
            progress_bar_placeholder.empty()
            
            # Update status
            # status_placeholder.markdown(f"""
            # # <div style="text-align: center; color: var(--primary-navy); font-weight: 600; margin: 1rem 0;">
            # #     Running workflow {i+1} of {total_workflows}: {workflow}
            # # </div>
            # # """, unsafe_allow_html=True)
            
            # Brief pause to ensure previous bar is cleared
            time.sleep(0.1)
            
            # Create new progress bar for this workflow (fresh instance starting at 0)
            with progress_bar_placeholder.container():
                workflow_progress_bar = st.progress(0)
                
            # Ensure the bar visually starts at 0
            workflow_progress_bar.progress(0)
            # status_placeholder.markdown(f"""
            # <div style="text-align: center; color: var(--primary-navy); font-weight: 600; margin: 1rem 0;">
            #     Running workflow {i+1} of {total_workflows}: {workflow}
            # </div>
            # """, unsafe_allow_html=True)
            # Show loading animation for this workflow
            progress_placeholder.markdown(f"""
            <div class="loading-container">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div class="loading-spinner"></div>
                    <div style="flex: 1;">
                        <div class="loading-text">Running workflow {i+1}/3: {workflow}</div>
                        <div class="loading-subtitle">{workflow_messages[i]}</div>
                    </div>
                    <div class="loading-dots">
                        <div class="loading-dot"></div>
                        <div class="loading-dot"></div>
                        <div class="loading-dot"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate processing time (7-9 seconds per workflow)
            import random
            processing_time = random.uniform(7, 9)
            
            # Update progress bar gradually for this specific workflow (smoother progression)
            steps = 100  # More steps for smoother animation
            step_time = processing_time / steps
            for step in range(steps + 1):
                workflow_progress = step / steps
                workflow_progress_bar.progress(workflow_progress)
                time.sleep(step_time)
            
            # Show completion for this workflow
            # progress_placeholder.success(f"✅ {workflow} completed successfully!")
            # time.sleep(0.5)  # Brief pause to show completion
        
        # Clear the loading area
        progress_placeholder.empty()
        status_placeholder.empty()
        progress_bar_placeholder.empty()
        
        # Mark pipeline as complete and proceed
        st.session_state.pipeline_running = False
        st.session_state.pipeline_complete = True
        st.session_state.results = get_mock_classification_results()
        st.rerun()

# Step 5: Classification Results
if st.session_state.pipeline_complete:
    st.markdown("---")
    step5_class = ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step5_class}">5</div>
        <div>Classification Results</div>
    </div>""", unsafe_allow_html=True)
    
    # Display results
    if st.session_state.pipeline_complete:
        # st.success("✅ GenAI Pipeline completed successfully!")
        st.info(f'''
        **Pipeline completed successfully**

        After running the GenAI Pipeline, we have performing cleaning, information augmentation, and mapping to NAICS codes. At this point, there are **3 buckets of data:**
        1. Those line items that are **able to be matched to a NAICS code**
        2. Items that has been flagged out as **Non-Scope 3 Category 1 emissions factor**
        2. Items that is **unable to be classified**
        ''', icon = "✅")
        results = st.session_state.results
        
        st.markdown("### 🌱 Classification Overview")
        
        # Results metrics
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card" style="border-top: 4px solid #153243;">
                <div class="metric-value">{results['total_items']:,}</div>
                <div class="metric-label">Total Items</div>
            </div>
            <div class="metric-card" style="border-top: 4px solid #10b981;">
                <div class="metric-value">{results['all_classified_items']:,}</div>
                <div class="metric-label">Successfully Classified</div>
            </div>
            <div class="metric-card" style="border-top: 4px solid #f59e0b;">
                <div class="metric-value">{results['non_scope3_items']:,}</div>
                <div class="metric-label">Non Scope 3 Cat 1</div>
            </div>
            <div class="metric-card" style="border-top: 4px solid #ef4444;">
                <div class="metric-value">{results['unable_to_classify_items']:,}</div>
                <div class="metric-label">Unable to Classify</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
        # Display result tabs data
        st.markdown(f"\n")
        if 'result_1_data' in results:
            st.markdown("### 🌱 Results")
            
            tab1, tab2, tab3 = st.tabs(["All Classified", "Non Scope 3 Cat 1", "Unable to Classify"])
            
            with tab1:
                st.markdown(f"**{results['all_classified_items']:,} items** results successfully classified")
                if not results['result_1_data'].empty:
                    # Apply conditional formatting and NAICS Name header styling
                    styled_df = apply_conditional_formatting(results['result_1_data'])
                    
                    if 'NAICS Name' in results['result_1_data'].columns:
                        styled_df = styled_df.set_table_styles([
                            {'selector': 'th:contains("NAICS Name")', 
                             'props': [('background-color', '#10b981'), 
                                      ('color', 'white'), 
                                      ('font-weight', 'bold')]}
                        ])
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No data in this tab")
            
            with tab2:
                st.markdown(f"**{results['non_scope3_items']:,} items** flagged as Non-Scope 3 Category 1 items")
                if not results['result_2_data'].empty:
                    # Apply conditional formatting and NAICS Name header styling
                    styled_df = apply_conditional_formatting(results['result_2_data'])
                    
                    if 'NAICS Name' in results['result_2_data'].columns:
                        styled_df = styled_df.set_table_styles([
                            {'selector': 'th:contains("NAICS Name")', 
                             'props': [('background-color', '#10b981'), 
                                      ('color', 'white'), 
                                      ('font-weight', 'bold')]}
                        ])
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No data in this tab")
            
            with tab3:
                st.markdown(f"**{results['unable_to_classify_items']:,} items** unable to be classified")
                if not results['result_3_data'].empty:
                    # Apply conditional formatting and NAICS Name header styling
                    styled_df = apply_conditional_formatting(results['result_3_data'])
                    
                    if 'NAICS Name' in results['result_3_data'].columns:
                        styled_df = styled_df.set_table_styles([
                            {'selector': 'th:contains("NAICS Name")', 
                             'props': [('background-color', '#10b981'), 
                                      ('color', 'white'), 
                                      ('font-weight', 'bold')]}
                        ])
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No data in this tab")
        
        # Download results
        col1, col2, col3 = st.columns(3)
        
        # with col1:
        #     # Download all classified items as CSV
        #     if 'result_1_data' in results and not results['result_1_data'].empty:
        #         csv = results['result_1_data'].to_csv(index=False)
        #         st.download_button(
        #             label="Download All Classified (CSV)",
        #             data=csv,
        #             file_name=f"all_classified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        #             mime="text/csv",
        #             use_container_width=True
                # )
        
        with col1:
            # Download all results as Excel with multiple sheets
            if 'result_1_data' in results:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    if not results['result_1_data'].empty:
                        results['result_1_data'].to_excel(writer, sheet_name='All Classified', index=False)
                    if not results['result_2_data'].empty:
                        results['result_2_data'].to_excel(writer, sheet_name='Non Scope 3 Cat 1', index=False)
                    if not results['result_3_data'].empty:
                        results['result_3_data'].to_excel(writer, sheet_name='Unable to Classify', index=False)
                excel_data = output.getvalue()
                
                st.download_button(
                    label="Download All Results (Excel)",
                    data=excel_data,
                    file_name=f"ghg_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin: 2rem 0;">
    GHG Scope 3 Category 1 Classification Tool<br>
    Built by PwC - AI Factory SG
</div>
""", unsafe_allow_html=True)