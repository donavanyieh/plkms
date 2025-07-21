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
    page_icon="assets/pwc_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
# def add_logo(logo_path, width, height):
#     """Read and return a resized logo"""
#     logo = Image.open(logo_path)
#     modified_logo = logo.resize((width, height))
#     return modified_logo

# my_logo = add_logo(logo_path="assets/pwc_logo.png", width=50, height=60)
# st.sidebar.image(my_logo)

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
        content: '';
        position: absolute;
        top: -50%;
        right: -25%;
        width: 50%;
        height: 200%;
        background: radial-gradient(circle, rgba(180, 184, 171, 0.1) 0%, transparent 70%);
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
    
    .logo-container {
        margin-bottom: 1.5rem;
        z-index: 10;
        position: relative;
    }
    .logo-container img {
        max-height: 80px;
        width: auto;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
        background: rgba(255, 255, 255, 0.95);
        padding: 10px 20px;
        border-radius: 12px;
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
        background: linear-gradient(90deg, #9acd32, #e6f7f1);
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
        background: linear-gradient(90deg, #B4B8AB, #284B63);
        width: 100%;
        box-shadow: 0 0 8px rgba(180, 184, 171, 0.6);
    }
    
    .progress-fill-segment.incomplete {
        width: 0%;
        background: rgba(255, 255, 255, 0.1);
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
        box-shadow: 0 0 10px rgba(180, 184, 171, 0.8);
    }
    
    .loading-container {
        background: var(--light-gradient);
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
    
    .reset-button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        margin-left: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .reset-button:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        transform: translateY(-1px) !important;
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

with st.sidebar:
    if st.button("Reset Analysis", key = "reset-button"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")


st.markdown("test")

# Footer with additional information
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin: 2rem 0;">
    🌱 IFRS Sustainability Reporting Gap Analysis Tool<br>
    Built by AI Factory SG
</div>
""", unsafe_allow_html=True)
