import streamlit as st
import pandas as pd
import time
import io
from datetime import datetime
import json
import base64
from PIL import Image
from streamlit_js_eval import streamlit_js_eval

# Page configuration
st.set_page_config(
    page_title="Security Organization Controls Mapping Tool",
    page_icon="assets/pwc_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with security-focused color scheme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables for security color scheme */
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
        --security-red: #dc2626;
        --security-green: #16a34a;
        --security-amber: #d97706;
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
    }
    
    .main-header {
        background: var(--accent-gradient);
        background-size: 300% 300%;
        animation: gradientFlow 8s ease-in-out infinite;
        color: white;
        padding: 2rem 2.5rem;
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 24px 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(21, 50, 67, 0.15);
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .main-header::before {
        content: '🔒';
        position: absolute;
        top: -50%;
        right: -25%;
        width: 50%;
        height: 200%;
        font-size: 8rem;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -20%;
        width: 40%;
        height: 150%;
        background: radial-gradient(circle, rgba(40, 75, 99, 0.08) 0%, transparent 70%);
        animation: float 8s ease-in-out infinite reverse;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(10deg); }
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }
    
    .progress-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin-top: 2rem;
        width: 70%;
        max-width: 600px;
        position: relative;
        z-index: 1;
    }
    
    .progress-segment {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    
    .progress-label {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    
    .progress-bar-segment {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }
    
    .progress-fill-segment {
        height: 100%;
        border-radius: 10px;
        transition: width 0.6s ease;
        position: relative;
    }
    
    .progress-fill-segment.complete {
        background:RGB(235, 242, 250);
        width: 100%;
        box-shadow: 0 0 8px rgba(235, 242, 250, 0.8);
    }
    
    .progress-fill-segment.incomplete {
        width: 0%;
        background: rgba(235, 242, 250, 0.8);
    }
    
    .loading-container {
        background:  rgba(235, 242, 250, 0.8);
        border: 2px solid #003459;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: left;
        box-shadow: 0 4px 20px rgba(21, 50, 67, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 28px;
        height: 28px;
        border: 3px solid var(--light-gray);
        border-top: 3px solid var(--primary-navy);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 1rem;
        vertical-align: middle;
        filter: drop-shadow(0 2px 4px rgba(21, 50, 67, 0.2));
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        color: var(--primary-navy);
        font-size: 1.2rem;
        font-weight: 600;
        display: inline-block;
        vertical-align: middle;
    }
    
    .step-header {
        display: flex;
        align-items: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-navy);
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
        box-shadow: 0 4px 12px rgba(21, 50, 67, 0.3);
        transition: all 0.3s ease;
    }
    
    .step-number:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(21, 50, 67, 0.4);
    }
    
    .step-number.completed {
        background: linear-gradient(135deg, #B4B8AB 0%, #284B63 100%);
        box-shadow: 0 4px 12px rgba(180, 184, 171, 0.3);
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
        background: linear-gradient(135deg, var(--light-gray) 0%, var(--light-cream) 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.1);
    }
    
    .stFileUploader label {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-navy);
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
    
    .control-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 1px solid var(--light-gray);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
        border-left: 5px solid var(--primary-navy);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .control-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, rgba(180, 184, 171, 0.1), transparent);
        border-radius: 0 16px 0 50px;
    }
    
    .control-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(21, 50, 67, 0.1);
        border-left-color: var(--primary-sage);
    }
    
    .control-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin-bottom: 1rem;
    }
    
    .control-content {
        color: #475569;
        line-height: 1.7;
        margin-bottom: 1.25rem;
        font-size: 1rem;
    }
    
    .control-meta {
        color: #64748b;
        font-size: 0.95rem;
        background: #ebf2fa;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        border-left: 3px solid var(--primary-sage);
        font-style: italic;
    }
    
    .soc-badge {
        background: var(--subtle-gradient);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 8px rgba(21, 50, 67, 0.3);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 1px solid #e6f7f1;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        border-top: 4px solid var(--primary-navy);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, transparent 0%, rgba(21, 50, 67, 0.02) 100%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 35px rgba(21, 50, 67, 0.1);
        border-top-color: var(--primary-sage);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary-navy);
        margin: 1rem 0;
        line-height: 1;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .button-container {
        margin: 2rem 0;
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
        box-shadow: 0 4px 15px rgba(20, 33, 61, 0.3) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(20, 33, 61, 0.7) !important;
        background: var(--subtle-gradient) !important;
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
    
    [data-testid="stSidebarNav"] + div [data-testid="baseButton-secondary"] {
        background: var(--orange-gradient) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
        animation: orangeFlow 3s ease-in-out infinite !important;
    }
    
    [data-testid="stSidebarNav"] + div [data-testid="baseButton-secondary"]:hover {
        background: linear-gradient(135deg, #e55a2b 0%, #d4761a 50%, #e55a2b 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6) !important;
    }
    
    [data-testid="stSidebarNav"] + div [data-testid="baseButton-secondary"]:active {
        transform: translateY(0) !important;
    }
    
    @keyframes orangeFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid #e6f7f1 !important;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-passed {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: var(--security-green);
        border: 1px solid var(--security-green);
    }
    
    .status-failed {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: var(--security-red);
        border: 1px solid var(--security-red);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: var(--security-amber);
        border: 1px solid var(--security-amber);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: var(--security-red);
        border: 1px solid var(--security-red);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: var(--security-amber);
        border: 1px solid var(--security-amber);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: var(--security-green);
        border: 1px solid var(--security-green);
    }
    
    /* Hide Streamlit elements */
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(21, 50, 67, 0.15) !important;
    }
    
    /* Regular button styling - matches Run GenAI Workflows */
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
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.7) !important;
        background: var(--subtle-gradient) !important;
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
    
    /* Download button styling - reduced width */
    .stDownloadButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(21, 50, 67, 0.3) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        width: auto !important;
        min-width: 200px !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.7) !important;
        background: var(--subtle-gradient) !important;
    }
    
    .stDownloadButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stDownloadButton > button:disabled {
        background: #94a3b8 !important;
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Special styling for consolidated download button */
    .consolidated-download .stDownloadButton > button {
        background: linear-gradient(135deg, #3c6e71 0%, #2a5256 50%, #3c6e71 100%) !important;
        box-shadow: 0 4px 15px rgba(60, 110, 113, 0.3) !important;
    }
    
    .consolidated-download .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #2a5256 0%, #1e3d40 50%, #2a5256 100%) !important;
        box-shadow: 0 8px 25px rgba(60, 110, 113, 0.7) !important;
    }
    
    /* Workflow checkbox styling from ghg_scope3_app.py */
    .workflow-container-marker {
        display: none;
    }
    
    .workflow-container-please {
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'uploading': False,
        'workflow_selected': False,
        'controls_extracted': False,
        'uploaded_file': None,
        'uploaded_itgc_file': None,
        'extracting': False,
        'running_workflows': False,
        'workflows_complete': False,
        'file_analysis_data': None,
        'itgc_analysis_data': None,
        'soc_controls': [],
        'selected_workflows': ['Extract SOC Tables and Map ITGC', 'Extract CUEC', 'Extract Subservice Orgs'],
        'progress': 0,
        'show_reset_confirmation': False
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Helper functions
def calculate_progress():
    """Calculate overall progress percentage"""
    progress = 0
    # Require both files for step 1 completion
    if st.session_state.uploaded_file and st.session_state.uploaded_itgc_file:
        progress += 25
    if st.session_state.workflow_selected:
        progress += 25
    if st.session_state.workflows_complete:
        progress += 25
    if st.session_state.controls_extracted:
        progress += 25
    return progress

def reset_analysis():
    """Reset all analysis states"""
    st.session_state.uploaded_file = None
    st.session_state.uploaded_itgc_file = None
    st.session_state.uploading = False
    st.session_state.workflow_selected = False
    st.session_state.controls_extracted = False
    st.session_state.extracting = False
    st.session_state.running_workflows = False
    st.session_state.workflows_complete = False
    st.session_state.file_analysis_data = None
    st.session_state.itgc_analysis_data = None
    st.session_state.soc_controls = []
    st.session_state.selected_workflows = ['Extract SOC Tables and Map ITGC', 'Extract CUEC', 'Extract Subservice Orgs']
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

def get_mock_itgc_mapping_data():
    """Return mock ITGC mapping data"""
    return [
        {
            "soc_control_id": "CC6.1",
            "soc_control_description": "Logical and physical access controls",
            "itgc_code": "AC-1",
            "itgc_description": "Access Control Policy and Procedures",
            "mapping_confidence": "High",
            "test_result": "Passed",
            "evidence_page": "Page 15"
        },
        {
            "soc_control_id": "CC6.2", 
            "soc_control_description": "System access authentication",
            "itgc_code": "IA-2",
            "itgc_description": "Identification and Authentication",
            "mapping_confidence": "High",
            "test_result": "Failed",
            "evidence_page": "Page 23"
        },
        {
            "soc_control_id": "CC7.1",
            "soc_control_description": "System monitoring activities",
            "itgc_code": "AU-2",
            "itgc_description": "Audit Events",
            "mapping_confidence": "Medium",
            "test_result": "Passed",
            "evidence_page": "Page 31"
        },
        {
            "soc_control_id": "CC7.2",
            "soc_control_description": "Data backup and recovery",
            "itgc_code": "CP-9",
            "itgc_description": "Information System Backup",
            "mapping_confidence": "High", 
            "test_result": "Warning",
            "evidence_page": "Page 28"
        }
    ]

def get_mock_cuec_data():
    """Return mock CUEC (Complementary User Entity Controls) data"""
    return [
        {
            "cuec_id": "CUEC-001",
            "control_description": "User reviews and approves all journal entries before posting",
            "business_process": "Financial Reporting",
            "control_frequency": "Monthly",
            "responsible_party": "Finance Manager",
            "testing_required": "Yes",
            "evidence_location": "Page 42"
        },
        {
            "cuec_id": "CUEC-002",
            "control_description": "Management reviews exception reports for unusual transactions",
            "business_process": "Transaction Processing", 
            "control_frequency": "Weekly",
            "responsible_party": "Operations Manager",
            "testing_required": "Yes",
            "evidence_location": "Page 38"
        },
        {
            "cuec_id": "CUEC-003",
            "control_description": "User entities maintain proper segregation of duties in payment processing",
            "business_process": "Accounts Payable",
            "control_frequency": "Daily",
            "responsible_party": "AP Supervisor",
            "testing_required": "No",
            "evidence_location": "Page 45"
        }
    ]

def get_mock_subservice_data():
    """Return mock Subservice Organizations data"""
    return [
        {
            "subservice_org": "CloudTech Solutions",
            "service_description": "Cloud infrastructure and hosting services",
            "soc_report_type": "SOC 2 Type II",
            "report_period": "Jan 1, 2023 - Dec 31, 2023",
            "relevant_controls": "CC6.1, CC6.2, CC7.1",
            "management_assessment": "Effective",
            "evidence_location": "Page 52"
        },
        {
            "subservice_org": "DataSecure Inc",
            "service_description": "Data backup and disaster recovery services",
            "soc_report_type": "SOC 1 Type II", 
            "report_period": "Jan 1, 2023 - Dec 31, 2023",
            "relevant_controls": "CC7.2, CC9.1",
            "management_assessment": "Effective with exceptions",
            "evidence_location": "Page 48"
        },
        {
            "subservice_org": "PaymentGateway Corp",
            "service_description": "Payment processing and transaction management",
            "soc_report_type": "SOC 2 Type II",
            "report_period": "Jul 1, 2023 - Jun 30, 2024", 
            "relevant_controls": "CC6.3, CC8.1",
            "management_assessment": "Effective",
            "evidence_location": "Page 55"
        }
    ]

# Initialize session state
init_session_state()

# Sidebar with reset button
with st.sidebar:
    @st.dialog("Are you sure you want to reset?")
    def reset_confirmation():
        st.markdown("""
        <div style="text-align: center;">
            <h4 style="color: #153243; margin-bottom: 1rem;">This will clear all uploaded files and extracted controls. This action cannot be undone.</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Yes, Reset", type="primary", use_container_width=True):
                streamlit_js_eval(js_expressions="parent.window.location.reload()")
        with col3:
            if st.button("Cancel", use_container_width=True):
                st.rerun()
    
    if st.button("🔄 Reset Analysis", type="primary", use_container_width=True):
        reset_confirmation()

# Header with progress bar
progress = calculate_progress()

# Determine which steps are complete
step1_complete = st.session_state.uploaded_file is not None and st.session_state.uploaded_itgc_file is not None
step2_complete = st.session_state.workflow_selected
step3_complete = st.session_state.workflows_complete
step4_complete = st.session_state.controls_extracted

header_html = f"""
<div class="main-header">
    <h1>Security Organization Controls Mapping Tool</h1>
    <p>Upload SOC reports and extract control test results</p>
    <div class="progress-container">
        <div class="progress-segment">
            <div class="progress-label">Upload Files</div>
            <div class="progress-bar-segment">
                <div class="progress-fill-segment {'complete' if step1_complete else 'incomplete'}"></div>
            </div>
        </div>
        <div class="progress-segment">
            <div class="progress-label">Choose Workflows</div>
            <div class="progress-bar-segment">
                <div class="progress-fill-segment {'complete' if step2_complete else 'incomplete'}"></div>
            </div>
        </div>
        <div class="progress-segment">
            <div class="progress-label">Run Workflows</div>
            <div class="progress-bar-segment">
                <div class="progress-fill-segment {'complete' if step3_complete else 'incomplete'}"></div>
            </div>
        </div>
        <div class="progress-segment">
            <div class="progress-label">Extract Controls</div>
            <div class="progress-bar-segment">
                <div class="progress-fill-segment {'complete' if step4_complete else 'incomplete'}"></div>
            </div>
        </div>
    </div>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# Step 1: Upload Files
step1_class = "completed" if st.session_state.uploaded_file and st.session_state.uploaded_itgc_file else ""
st.markdown(f"""
<div class="step-header">
    <div class="step-number {step1_class}">1</div>
    <div>Upload Files</div>
</div>""", unsafe_allow_html=True)

st.markdown("### ⏏ Upload System and Organization Controls report")
uploaded_file = st.file_uploader(
    "Choose a PDF file", 
    type=['pdf'], 
    help="Upload your SOC 2 audit report in PDF format",
    key="file_upload"
)

# ITGC File Upload Section - Always display
st.markdown("### ⏏ Upload ITGC Mapping File")

uploaded_itgc_file = st.file_uploader(
    "Choose an Excel file with ITGC mapping data", 
    type=['xlsx', 'xls'], 
    help="Upload an Excel file containing IT General Controls to map",
    key="itgc_file_upload"
)

# Handle SOC file upload
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    
    # Simulate file analysis
    st.session_state.file_analysis_data = {
        'pages': 42,
        'size': uploaded_file.size,
        'type': uploaded_file.type,
        'name': uploaded_file.name
    }

# Handle ITGC file upload
if uploaded_itgc_file is not None:
    st.session_state.uploaded_itgc_file = uploaded_itgc_file
    
    # Simulate ITGC file analysis
    st.session_state.itgc_analysis_data = {
        'size': uploaded_itgc_file.size,
        'type': uploaded_itgc_file.type,
        'name': uploaded_itgc_file.name,
        'records': 25  # Mock number of ITGC records
    }

# Check if both files are uploaded (recalculate after handling uploads)
both_uploaded = st.session_state.uploaded_file is not None and st.session_state.uploaded_itgc_file is not None

# Show success message only when both files are uploaded
if both_uploaded:
    st.success("SOC Report PDF and ITGC Mapping Excel uploaded successfully!")

# Step 2: Choose Workflows to Run
if both_uploaded:
    st.markdown("---")
    step2_class = "completed" if st.session_state.workflow_selected else ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step2_class}">2</div>
        <div>Choose Workflows to Run</div>
    </div>
    """, unsafe_allow_html=True)
    
    workflows = {
        'Extract SOC Tables and Map ITGC': 'Extract control test results and map IT General Controls from SOC reports',
        'Extract CUEC': 'Identify and extract Complementary User Entity Controls documentation',
        'Extract Subservice Orgs': 'Extract information about subservice organizations and their controls'
    }
    
    st.markdown("### Select the workflows you want to run:")
    st.markdown(" ")
    
    selected_workflows = []
    
    # Display workflow selection with simple checkboxes using ghg_scope3_app.py style
    for workflow, description in workflows.items():
        selected = workflow in st.session_state.selected_workflows
        
        # Use Streamlit container with specific styling
        container = st.container()
        with container:
            # Add a marker class to identify workflow containers
            st.markdown('<div class="workflow-container-please">', unsafe_allow_html=True)
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
        
        if workflow in st.session_state.selected_workflows:
            selected_workflows.append(workflow)
    
    if selected_workflows:
        st.session_state.selected_workflows = selected_workflows
        st.session_state.workflow_selected = True
        
        st.success(f"Selected {len(selected_workflows)} workflow(s): {', '.join(selected_workflows)}")
        
        # Run GenAI Workflows button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            if st.button("Run GenAI Workflows", key="run_workflows_btn", use_container_width=True):
                st.session_state.running_workflows = True
                st.session_state.workflows_complete = False
                st.rerun()
    else:
        st.session_state.workflow_selected = False
        st.warning("Please select at least one workflow to proceed.")

# Step 3: Run GenAI Workflows
if both_uploaded and st.session_state.workflow_selected and st.session_state.running_workflows:
    st.markdown("---")
    step3_class = "completed" if st.session_state.workflows_complete else ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step3_class}">3</div>
        <div>Running GenAI Workflows</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create progress tracking for each selected workflow
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Run each selected workflow with loading animation
    total_workflows = len(st.session_state.selected_workflows)
    
    for i, workflow in enumerate(st.session_state.selected_workflows):
        # Update status
        status_placeholder.markdown(f"""
        <div style="text-align: center; color: var(--primary-navy); font-weight: 600; margin: 1rem 0;">
            Running workflow {i+1} of {total_workflows}: {workflow}
        </div>
        """, unsafe_allow_html=True)
        
        # Show loading animation for this workflow
        progress_placeholder.markdown(f"""
        <div class="loading-container">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="loading-spinner"></div>
                <div style="flex: 1;">
                    <div class="loading-text">Processing: {workflow}</div>
                    <div class="loading-subtitle">Analyzing data and extracting insights...</div>
                </div>
                <div class="loading-dots">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulate processing time (5-9 seconds per workflow)
        import random
        processing_time = random.uniform(5, 9)
        time.sleep(0.4)
        
        # Show completion for this workflow
        progress_placeholder.success(f"{workflow} completed successfully!")
        # time.sleep(0.5)  # Brief pause to show completion
    
    # All workflows complete
    # status_placeholder.markdown("""
    # <div style="text-align: center; color: var(--security-green); font-weight: 700; font-size: 1.2rem; margin: 1rem 0;">
    #     🎉 All GenAI workflows completed successfully!
    # </div>
    # """, unsafe_allow_html=True)
    
    progress_placeholder.empty()  # Clear the loading area
    
    # Mark workflows as complete and proceed
    st.session_state.workflows_complete = True
    st.session_state.running_workflows = False
    # time.sleep(1)  # Brief pause before showing results
    st.rerun()

# Step 4: Control Test Results  
if both_uploaded and st.session_state.workflows_complete:
    st.markdown("---")
    
    # Automatically generate results when workflows are complete
    if not st.session_state.controls_extracted:
        st.session_state.controls_extracted = True
    
    step4_class = "completed"
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step4_class}">4</div>
        <div>Analysis Results</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("All analysis results generated successfully!")
    
    # Metrics Overview Cards
    st.markdown("### Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--security-green);">7/8</div>
            <div class="metric-label">ITGC Codes Mapped</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--security-amber);">1/8</div>
            <div class="metric-label">ITGC Codes Need Review</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--primary-navy);">6</div>
            <div class="metric-label">Extracted CUECs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: var(--primary-navy);">3</div>
            <div class="metric-label">Extracted Subservice Orgs</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Display results for each selected workflow in order
    for workflow in st.session_state.selected_workflows:
        if workflow == "Extract SOC Tables and Map ITGC":
            st.markdown("---")
            st.markdown("### 🟢 SOC Tables Mapped to ITGC Codes")
            
            try:
                itgc_df = pd.DataFrame(get_mock_itgc_mapping_data())
                st.dataframe(itgc_df, use_container_width=True, hide_index=True)
            except:
                itgc_df = pd.read_excel("./results.xlsx")
                st.dataframe(itgc_df, use_container_width=True, hide_index=True)

            # Download button
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                itgc_df.to_excel(writer, sheet_name='SOC ITGC Mapping', index=False)
            excel_data = output.getvalue()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.download_button(
                    label="Download Mapped ITGCs",
                    data=excel_data,
                    file_name="SOC mapping results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
        elif workflow == "Extract CUEC":
            st.markdown("---")
            st.markdown("### 🟢 Extracted Complementary User Entity Controls (CUEC)")
            
            try:
                cuec_df = pd.read_excel("./CEUC results.xlsx")
                st.dataframe(cuec_df, use_container_width=True, hide_index=True)
            except:
                cuec_df = pd.DataFrame(get_mock_cuec_data())
                st.dataframe(cuec_df, use_container_width=True, hide_index=True)
            
            # Download button
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                cuec_df.to_excel(writer, sheet_name='CUEC Results', index=False)
            excel_data = output.getvalue()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.download_button(
                    label="Download Extracted CUECs",
                    data=excel_data,
                    file_name="CUEC results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
        elif workflow == "Extract Subservice Orgs":
            st.markdown("---")
            st.markdown("### 🟢 Extracted Subservice Organizations")
            
            # Read from uploaded Excel file instead of mock data
            try:
                subservice_df = pd.read_excel("./Subservice results.xlsx")
                st.dataframe(subservice_df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
                # Fallback to mock data if there's an error
                subservice_df = pd.DataFrame(get_mock_subservice_data())
                st.dataframe(subservice_df, use_container_width=True, hide_index=True)
            
            # Download button - use the same data that was displayed
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                subservice_df.to_excel(writer, sheet_name='Subservice Orgs', index=False)
            excel_data = output.getvalue()
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.download_button(
                    label="Download Subservice Orgs",
                    data=excel_data,
                    file_name="Subservice results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    # Add consolidated download button after all individual downloads
    if st.session_state.selected_workflows:
        st.markdown("---")
        st.markdown("### 🟩 Download Consolidated Spreadsheet")
        
        # Create consolidated Excel file with all results
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            if "Extract SOC Tables and Map ITGC" in st.session_state.selected_workflows:
                itgc_df = pd.DataFrame(get_mock_itgc_mapping_data())
                itgc_df.to_excel(writer, sheet_name='SOC ITGC Mapping', index=False)
            
            if "Extract CUEC" in st.session_state.selected_workflows:
                cuec_df = pd.DataFrame(get_mock_cuec_data())
                cuec_df.to_excel(writer, sheet_name='CUEC Results', index=False)
            
            if "Extract Subservice Orgs" in st.session_state.selected_workflows:
                subservice_df = pd.DataFrame(get_mock_subservice_data())
                subservice_df.to_excel(writer, sheet_name='Subservice Orgs', index=False)
        
        consolidated_data = output.getvalue()
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.download_button(
                label="Download Consolidated Results",
                data=consolidated_data,
                file_name="results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
        # col1, col2, col3 = st.columns([2, 3, 1])
        # with col1:
        # st.markdown('<div class="consolidated-download">', unsafe_allow_html=True)
        # st.download_button(
        #     label="Download Consolidated Results",
        #     data=consolidated_data,
        #     file_name="results.xlsx",
        #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        #     use_container_width=True
        # )
        # st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin: 2rem 0;">
    🔒 Security Organization Controls Mapping Tool<br>
    Built for SOC Report Analysis and Control Testing
</div>
""", unsafe_allow_html=True)