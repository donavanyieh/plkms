import streamlit as st
import pandas as pd
import time
import io
from datetime import datetime
import json
import base64
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
import io

# Page configuration
st.set_page_config(
    page_title="IFRS Sustainability Reporting - Gap Analysis",
    page_icon="pwc_logo.png",
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
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
    }
    
    .main-header {
        background: white;
        padding: 2rem 2.5rem;
        margin: -1rem -1rem 3rem -1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .logo-container {
        margin-bottom: 0;
    }
    .logo-container img {
        max-height: 120px;
        width: auto;
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0;
        color: var(--primary-navy);
    }
    
    .progress-bar {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 10px;
        height: 8px;
        margin: 1.5rem 0 0 0;
        overflow: hidden;
        position: relative;
        z-index: 1;
        width: 60%;
        min-width: 300px;
    }
    
    .progress-fill {
        background: #ebf2fa;
        height: 100%;
        border-radius: 10px;
        transition: width 0.6s ease;
        box-shadow: 0 0 10px rgba(154, 205, 50, 0.5);
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
    
    .progress-checkpoint {
        position: absolute;
        right: -4px;
        top: 50%;
        transform: translateY(-50%);
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: white;
        border: 2px solid rgba(255, 255, 255, 0.5);
        z-index: 2;
        transition: all 0.3s ease;
    }
    
    .progress-checkpoint.complete {
        background: #B4B8AB;
        border-color: white;
        box-shadow: 0 0 10px rgba(235, 242, 250, 0.8);
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
    
    .topic-card {
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
    
    .topic-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, rgba(180, 184, 171, 0.1), transparent);
        border-radius: 0 16px 0 50px;
    }
    
    .topic-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(21, 50, 67, 0.1);
        border-left-color: var(--primary-sage);
    }
    
    .topic-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin-bottom: 1rem;
    }
    
    .topic-content {
        color: #475569;
        line-height: 1.7;
        margin-bottom: 1.25rem;
        font-size: 1rem;
    }
    
    .topic-citation {
        color: #64748b;
        font-size: 0.95rem;
        background: #ebf2fa;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        border-left: 3px solid var(--primary-sage);
        font-style: italic;
    }
    
    .ifrs-badge {
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
        border-top: 4px solid var(--primary-green);
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
        background: linear-gradient(135deg, transparent 0%, rgba(0, 135, 90, 0.02) 100%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 35px rgba(0, 135, 90, 0.1);
        border-top-color: var(--accent-lime);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--forest-dark);
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
        background: var(--eco-gradient) !important;
        color: black !important;
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
        background: var(--forest-gradient) !important;
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
    
    /* Enhanced Reset Button Styling - Primary Orange Style */
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
    
    .download-section {
        background: linear-gradient(135deg, #e6f7f1 0%, #f0fdf4 100%);
        border: 1px solid var(--secondary-teal);
        border-radius: 16px;
        padding: 2rem;
        margin: 3rem 0;
        box-shadow: 0 4px 15px rgba(32, 178, 170, 0.1);
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--primary-green) 50%, transparent 100%);
        margin: 3rem 0;
        border: none;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-complete {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: var(--forest-dark);
        border: 1px solid var(--primary-green);
    }
    
    .status-partial {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #92400e;
        border: 1px solid #fbbf24;
    }
    
    .status-missing {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #dc2626;
        border: 1px solid #f87171;
    }
    
    .priority-high {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #dc2626;
        border: 1px solid #f87171;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #92400e;
        border: 1px solid #fbbf24;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #e0f2fe, #bae6fd);
        color: var(--ocean-blue);
        border: 1px solid #38bdf8;
    }
    
    .toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--eco-gradient);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 135, 90, 0.3);
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
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
        box-shadow: 0 4px 15px rgba(0, 135, 90, 0.15) !important;
    }
    
    .info-tooltip {
        background: var(--forest-dark);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        position: absolute;
        z-index: 1000;
        max-width: 300px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Add/Remove button styling */
    .action-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .add-button {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-emerald) 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(0, 135, 90, 0.3);
    }
    
    .add-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 135, 90, 0.4);
    }
    
    .remove-button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    }
    
    .remove-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
    }
    
    .topic-actions {
        display: flex;
        gap: 0.75rem;
        justify-content: flex-end;
        margin-top: 1rem;
    }
    
    .add-topic-form {
        background: linear-gradient(135deg, #e6f7f1 0%, #f0fdf4 100%);
        border: 1px solid var(--secondary-teal);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(32, 178, 170, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with better organization
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'uploading' : False,
        'materiality_extracted': False,
        'gap_analysis_complete': False,
        'uploaded_file': None,
        'extracting': False,
        'analyzing': False,
        'file_analysis_data': None,
        'materiality_topics': [],
        'gap_analysis_results': None,
        'progress': 0,
        'show_add_form': False,
        'topics_modified': False,
        'logo_uploaded': False,
        'show_reset_confirmation': False  # New state for confirmation dialog
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Helper functions
def calculate_progress():
    """Calculate overall progress percentage"""
    progress = 0
    if st.session_state.uploaded_file:
        progress += 33
    if st.session_state.materiality_extracted:
        progress += 33
    if st.session_state.gap_analysis_complete:
        progress += 34
    return progress

def reset_analysis():
    """Reset all analysis states"""
    st.session_state.uploaded_file = None
    st.session_state.uploading = False
    st.session_state.materiality_extracted = False
    st.session_state.gap_analysis_complete = False
    st.session_state.extracting = False
    st.session_state.analyzing = False
    st.session_state.file_analysis_data = None
    st.session_state.materiality_topics = []
    st.session_state.gap_analysis_results = None
    st.session_state.show_add_form = False
    st.session_state.topics_modified = False
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

def get_mock_materiality_data():
    """Return mock materiality data for demonstration"""
    return [
        {
            "topic": "Water Management",
            "reasoning": "Extensive discussion of water consumption metrics, stress assessment protocols, and conservation initiatives across all manufacturing facilities with quantitative targets.",
            "citation": "Pages 23-25, 31-33, Appendix B",
            "ifrs_requirement": "IFRS S1"
        },
        {
            "topic": "Pollution Control",
            "reasoning": "Comprehensive coverage of air quality monitoring systems, waste reduction programs, and emission control strategies with detailed measurement frameworks.",
            "citation": "Pages 15-18, 28-30, Figure 4.2",
            "ifrs_requirement": "IFRS S1"
        },
        {
            "topic": "Sustainable Agriculture",
            "reasoning": "In-depth analysis of agricultural supply chain sustainability, biodiversity impact assessments, and responsible sourcing certification programs.",
            "citation": "Pages 12-14, 26-27, Case Study 2",
            "ifrs_requirement": "IFRS S1"
        },
        {
            "topic": "Energy Efficiency",
            "reasoning": "Detailed reporting on renewable energy adoption, energy consumption reduction targets, and carbon footprint analysis with year-over-year comparisons.",
            "citation": "Pages 8-11, 19-21, Executive Summary",
            "ifrs_requirement": "IFRS S1"
        }
    ]

def get_mock_gap_analysis():
    """Return mock gap analysis data"""
    return {
        'IFRS Requirement': [
            'IFRS S2.1', 'IFRS S2.2', 'IFRS S2.3', 'IFRS S2.4',
            'IFRS S1.1', 'IFRS S1.2', 'IFRS S1.3', 'IFRS S1.4'
        ],
        'Materiality Topic': [
            'Water Management', 'Water Management', 'Water Management', 'Energy Efficiency',
            'Pollution Control', 'Pollution Control', 'Sustainable Agriculture', 'Sustainable Agriculture'
        ],
        'Required Action': [
            'Disclose quantitative water consumption metrics',
            'Conduct water stress risk assessment',
            'Describe water conservation strategy',
            'Report energy transition timeline',
            'Report emission reduction targets',
            'Disclose waste management practices',
            'Assess agricultural supply chain risks',
            'Biodiversity impact measurement'
        ],
        'Status': [
            'Partial', 'Missing', 'Complete', 'Partial',
            'Complete', 'Partial', 'Missing', 'Missing'
        ],
        'Gap': [
            'Yes', 'Yes', 'No', 'Yes',
            'No', 'Yes', 'Yes', 'Yes'
        ],
        'Priority': [
            'High', 'Medium', 'Low', 'High',
            'Low', 'Medium', 'High', 'Medium'
        ],
        'Recommendation': [
            'Include facility-level water usage data with quarterly reporting',
            'Implement water stress analysis using WRI Aqueduct tool',
            'Continue current reporting approach with annual updates',
            'Develop comprehensive energy transition roadmap',
            'Maintain existing emissions framework with scope 3 expansion',
            'Expand waste metrics to include circularity indicators',
            'Develop comprehensive agricultural risk assessment framework',
            'Implement biodiversity measurement using TNFD guidelines'
        ]
    }

def add_topic(topic_data):
    """Add a new topic to the materiality topics list"""
    st.session_state.materiality_topics.append(topic_data)
    st.session_state.topics_modified = True
    # Reset gap analysis since topics have changed
    st.session_state.gap_analysis_complete = False
    st.session_state.gap_analysis_results = None

def remove_topic(index):
    """Remove a topic from the materiality topics list"""
    if 0 <= index < len(st.session_state.materiality_topics):
        st.session_state.materiality_topics.pop(index)
        st.session_state.topics_modified = True
        # Reset gap analysis since topics have changed
        st.session_state.gap_analysis_complete = False
        st.session_state.gap_analysis_results = None

# Initialize session state
init_session_state()

# Sidebar with reset button
with st.sidebar:
    # Confirmation dialog using Streamlit's native dialog
    @st.dialog("Are you sure you want to reset?")
    def reset_confirmation():
        st.markdown("""
        <div style="text-align: center;">
            <h4 style="color: #153243; margin-bottom: 1rem;">This will clear all uploaded files, extracted topics, and analysis results. This action cannot be undone.</h4>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Yes, Reset", type="primary", use_container_width=True):
                streamlit_js_eval(js_expressions="parent.window.location.reload()")
        with col3:
            if st.button("Cancel", use_container_width=True):
                st.rerun()
    
    # Reset button that triggers the dialog
    if st.button("🔄 Reset Analysis", type="primary", use_container_width=True):
        reset_confirmation()

# Header with progress bar and logo
progress = calculate_progress()

# Determine which steps are complete
step1_complete = st.session_state.uploaded_file is not None
step2_complete = st.session_state.materiality_extracted
step3_complete = st.session_state.gap_analysis_complete

# Create header HTML with conditional logo display
with open("pwc_logo.png", "rb") as f:
    base64_icon = base64.b64encode(f.read()).decode()
header_html = f"""
<div class="main-header">
    <div class="logo-container">
        <img src="data:image/png;base64,{base64_icon}" alt="PwC Logo">
    </div>
    <h1>IFRS Sustainability Reporting Gap Analysis</h1>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

step1_class = "completed" if st.session_state.uploaded_file else ""
st.markdown(f"""
<div class="step-header">
    <div class="step-number {step1_class}">1</div>
    <div>Upload Sustainability Report</div>
</div>""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a PDF file", 
    type=['pdf'], 
    help="Upload your company's sustainability report in PDF format",
    key="file_upload"
)

if uploaded_file is not None and not st.session_state.uploading:
    st.session_state.uploaded_file = uploaded_file
    
    
    # Simulate file analysis
    st.session_state.file_analysis_data = {
        'pages': 45,
        'size': uploaded_file.size,
        'type': uploaded_file.type,
        'name': uploaded_file.name
    }
    
    file_data = st.session_state.file_analysis_data
    formatted_size = format_file_size(file_data['size'])

    st.markdown(f"""
    <div class="file-summary">
        <div class="file-info">
            <div class="file-name">{file_data['name']}</div>
            <div class="file-details"><b>Uploaded successfully</b>: {formatted_size} • {file_data['pages']} pages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.uploading = True
    st.rerun()

if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    
    # Simulate file analysis
    st.session_state.file_analysis_data = {
        'pages': 45,
        'size': uploaded_file.size,
        'type': uploaded_file.type,
        'name': uploaded_file.name
    }
    
    file_data = st.session_state.file_analysis_data
    formatted_size = format_file_size(file_data['size'])

    st.markdown(f"""
    <div class="file-summary">
        <div class="file-info">
            <div class="file-name">{file_data['name']}</div>
            <div class="file-details"><b>Uploaded successfully</b>: {formatted_size} • {file_data['pages']} pages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Step 2: Extract Materiality Topics
if st.session_state.uploaded_file:
    st.markdown("---")
    step2_class = "completed" if st.session_state.materiality_extracted else ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step2_class}">2</div>
        <div>Extract Materiality Topics</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.materiality_extracted and not st.session_state.extracting:
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            if st.button("🔍 Extract Materiality Topics", key="extract_btn", use_container_width=True):
                st.session_state.extracting = True
                # st.session_state
                st.rerun()
        
        with col2:
            st.info("💡 This will analyze your PDF to identify material sustainability topics")
    
    if st.session_state.extracting:
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <span class="loading-text">Analyzing PDF for materiality topics...</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulate processing time
        time.sleep(1)
        st.session_state.materiality_topics = get_mock_materiality_data()
        st.session_state.materiality_extracted = True
        st.session_state.extracting = False
        st.rerun()
    
    if st.session_state.materiality_extracted:
        st.success("✅ Materiality topics extracted successfully!")
        
        st.markdown("### ➤ Identified Materiality Topics")
        
        # if st.session_state.topics_modified:
        #     st.info("ℹ️ Topics have been modified. Please run the gap analysis again to update results.")
        #     time.sleep(3)
        #     st.session_state.topics_modified = False

        
        # Display topics with integrated remove buttons
        for i, topic_data in enumerate(st.session_state.materiality_topics):
            col1, col2 = st.columns([20, 1])
            
            with col1:
                st.markdown(f"""
                <div class="topic-card">
                    <div class="ifrs-badge">{topic_data['ifrs_requirement']}</div>
                    <div class="topic-title">{topic_data['topic']}</div>
                    <div class="topic-content">
                        <strong>Reasoning:</strong> {topic_data['reasoning']}
                    </div>
                    <div class="topic-citation">
                        <strong>Source:</strong> {topic_data['citation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Remove button positioned inside the card area
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Spacer
                if st.button("🗑️", key=f"remove_{i}", help=f"Remove {topic_data['topic']}"):
                    remove_topic(i)
                    st.rerun()
        
        # Add topic button and form below the topics
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            if st.button("➕ Add Topic", key="show_add_form_btn", use_container_width=True):
                st.session_state.show_add_form = not st.session_state.show_add_form
                st.rerun()
        
        # Add topic form
        if st.session_state.show_add_form:
            st.markdown("### Add New Materiality Topic")
            
            with st.form(key="add_topic_form"):
                topic_name = st.selectbox("Topic Name", ["Water", "Agriculture"])
                reasoning = st.text_area("Reasoning", placeholder="Explain why this topic is material to your organization...")
                citation = st.text_input("Citation/Source", placeholder="e.g., Pages 5-7")
                
                col1, col2 = st.columns(2)
                with col1:
                    ifrs_requirement = st.selectbox("IFRS Requirement", ["IFRS S1", "IFRS S2"])

                st.markdown("")
                col1, col2, col3 = st.columns(3)
                with col1:
                    submit = st.form_submit_button("Add Topic", type="primary")
                    cancel = st.form_submit_button("Cancel")
                
                if submit and topic_name and reasoning:
                    new_topic = {
                        "topic": topic_name,
                        "reasoning": reasoning,
                        "citation": citation,
                        "ifrs_requirement": ifrs_requirement
                    }
                    add_topic(new_topic)
                    st.session_state.show_add_form = False
                    st.rerun()
                elif cancel:
                    st.session_state.show_add_form = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Gap Analysis
if st.session_state.materiality_extracted:
    st.markdown("---")
    step3_class = "completed" if st.session_state.gap_analysis_complete else ""
    st.markdown(f"""
    <div class="step-header">
        <div class="step-number {step3_class}">3</div>
        <div>Run Gap Analysis Pipeline</div>
    </div>""", unsafe_allow_html=True)
    
    if not st.session_state.gap_analysis_complete and not st.session_state.analyzing:
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            if st.button("📊 Run Gap Analysis", key="analyze_btn", use_container_width=True):
                st.session_state.analyzing = True
                st.rerun()
        
        with col2:
            st.info("💡 This will compare your report against IFRS requirements")
    
    if st.session_state.analyzing:
        st.markdown("""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <span class="loading-text">Analyzing gaps against IFRS requirements...</span>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.session_state.gap_analysis_results = get_mock_gap_analysis()
        st.session_state.gap_analysis_complete = True
        st.session_state.analyzing = False
        st.session_state.topics_modified = False  # Reset the flag after analysis
        st.rerun()
    
    if st.session_state.gap_analysis_complete:
        st.success("✅ Gap analysis completed successfully!")
        
        # Calculate metrics from results
        df = pd.DataFrame(st.session_state.gap_analysis_results)
        total_requirements = len(df)
        gaps_identified = len(df[df['Gap'] == 'Yes'])
        compliance_rate = int(((total_requirements - gaps_identified) / total_requirements) * 100)
        high_priority = len(df[df['Priority'] == 'High'])
        
        # Enhanced metrics display
        st.markdown("### ➤ Gap Analysis Summary")
        st.markdown("""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Total Requirements</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Gaps Identified</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{}%</div>
                <div class="metric-label">Compliance Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">High Priority</div>
            </div>
        </div>
        """.format(total_requirements, gaps_identified, compliance_rate, high_priority), unsafe_allow_html=True)
        
        # Enhanced results table with better formatting
        st.markdown("### ➤ Gap Analysis Results")
        
        # Add status and priority badges to dataframe for display
        df_display = df.copy()
        
        # Format status column with badges
        def format_status(status):
            if status == 'Complete':
                return f'<span class="status-badge status-complete">{status}</span>'
            elif status == 'Partial':
                return f'<span class="status-badge status-partial">{status}</span>'
            else:
                return f'<span class="status-badge status-missing">{status}</span>'
        
        def format_priority(priority):
            if priority == 'High':
                return f'<span class="status-badge priority-high">{priority}</span>'
            elif priority == 'Medium':
                return f'<span class="status-badge priority-medium">{priority}</span>'
            else:
                return f'<span class="status-badge priority-low">{priority}</span>'
        
        # Apply formatting (note: this won't show in st.dataframe, but we can use it for display)
        st.dataframe(df, use_container_width=True, hide_index=True)

        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ifrs_gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Gap Analysis', index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"ifrs_gap_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        # # Action items section
        # st.markdown("---")
        # st.markdown("""
        # <div class="step-header">
        #     <div class="step-number">4</div>
        #     <div>Priority Action Items</div>
        # </div>""", unsafe_allow_html=True)
        
        # high_priority_items = df[df['Priority'] == 'High']
        # if not high_priority_items.empty:
        #     for _, item in high_priority_items.iterrows():
        #         st.markdown(f"""
        #         <div class="topic-card">
        #             <div class="topic-title">
        #                 {item['IFRS Requirement']} - {item['Materiality Topic']}
        #                 <span class="status-badge priority-high">High Priority</span>
        #             </div>
        #             <div class="topic-content">
        #                 <strong>Required Action:</strong> {item['Required Action']}<br>
        #                 <strong>Current Status:</strong> {item['Status']}<br>
        #                 <strong>Recommendation:</strong> {item['Recommendation']}
        #             </div>
        #         </div>
        #         """, unsafe_allow_html=True)
        # else:
        #     st.info("🎉 No high-priority gaps identified!")
        
        # # Summary insights
        # st.markdown("### 💡 Key Insights")
        
        # insights_col1, insights_col2 = st.columns(2)
        
        # with insights_col1:
        #     st.markdown(f"""
        #     **Compliance Overview:**
        #     - Your report covers {compliance_rate}% of IFRS requirements
        #     - {gaps_identified} areas need attention
        #     - Focus on {high_priority} high-priority items first
        #     """)
        
        # with insights_col2:
        #     # Most common gaps
        #     gap_topics = df[df['Gap'] == 'Yes']['Materiality Topic'].value_counts()
        #     if not gap_topics.empty:
        #         most_gaps = gap_topics.index[0]
        #         gap_count = gap_topics.iloc[0]
        #         st.markdown(f"""
        #         **Areas for Improvement:**
        #         - {most_gaps} has the most gaps ({gap_count} items)
        #         - Missing assessments need immediate attention
        #         - Consider implementing systematic monitoring
        #         """)

# Footer with additional information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin: 2rem 0;">
    🌱 IFRS Sustainability Reporting Gap Analysis Tool<br>
    Built by AI Factory SG
</div>
""", unsafe_allow_html=True)