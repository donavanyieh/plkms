import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="GHG Scope 3 Category 1 Classification",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with sustainability-focused color scheme matching Main.py
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
        background: var(--accent-gradient);
        background-size: 300% 300%;
        animation: gradientFlow 8s ease-in-out infinite;
        color: white;
        padding: 2rem 2.5rem;
        margin: -1rem -1rem 2rem -1rem;
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
    
    .title {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0 0 0.75rem 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }
    
    .section-title {
        display: flex;
        align-items: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        padding: 1rem 0;
        border-bottom: 3px solid transparent;
        background: transparent;
        border-image: var(--accent-gradient) 1;
        border-bottom: 3px solid;
        border-image-slice: 1;
    }
    
    .step-number {
        background: linear-gradient(135deg, #284B63 20%,  #B4B8AB 80%);
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
        box-shadow: 0 4px 12px rgba(180, 184, 171, 0.3);
        transition: all 0.3s ease;
    }
    
    .step-number:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(21, 50, 67, 0.4);
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--primary-navy) 50%, transparent 100%);
        margin: 3rem 0;
        border: none;
    }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0.5rem;
        text-align: center;
        border: 1px solid var(--light-gray);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        border-top: 4px solid var(--primary-sage);
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
        background: linear-gradient(135deg, transparent 0%, rgba(112, 121, 140, 0.02) 100%);
        pointer-events: none;
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 35px rgba(21, 50, 67, 0.1);
        border-top-color: var(--secondary-blue);
    }
    
    .metric-number {
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
    
    .workflow-item {
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
    
    .workflow-item::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, rgba(180, 184, 171, 0.1), transparent);
        border-radius: 0 16px 0 50px;
    }
    
    .workflow-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(21, 50, 67, 0.1);
        border-left-color: var(--primary-sage);
    }
    
    .workflow-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-navy);
        margin-bottom: 1rem;
    }
    
    .workflow-description {
        color: #475569;
        line-height: 1.7;
        margin-bottom: 1.25rem;
        font-size: 1rem;
    }
    
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-success {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: var(--primary-navy);
        border: 1px solid var(--primary-sage);
    }
    
    .status-info {
        background: linear-gradient(135deg, #e0f2fe, #bae6fd);
        color: var(--secondary-blue);
        border: 1px solid #38bdf8;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #92400e;
        border: 1px solid #fbbf24;
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
    
    .stTabs [data-baseweb="tab-list"] {
        background: var(--light-gradient);
        border-radius: 16px;
        padding: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 12px;
        color: #6b7280;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: var(--primary-navy);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .content-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem 0 2rem 0;
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
        background: linear-gradient(135deg, var(--light-gray) 0%, #f0fdf4 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(21, 50, 67, 0.1);
    }
    
    .stFileUploader label {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-navy);
    }
    
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06) !important;
        border: 1px solid var(--light-gray) !important;
    }
    
    .loading-container {
        background: rgba(235, 242, 250, 0.8);
        border: 2px solid var(--primary-navy);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: left;
        box-shadow: 0 4px 20px rgba(21, 50, 67, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        margin: 2rem 0;
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
    
    /* Hide Streamlit elements */
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Success message styling */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(21, 50, 67, 0.15) !important;
    }
    
    /* Spacing utilities */
    .section-spacing {
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables with default values"""
    defaults = {
        'client_data': None,
        'purchased_goods_data': None,
        'data_uploaded': False,
        'edit_mode': False,
        'edited_data': None
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

def load_excel_file(uploaded_file):
    """Load Excel file and return both sheets"""
    try:
        client_data = pd.read_excel(uploaded_file, sheet_name=0)
        purchased_goods_data = pd.read_excel(uploaded_file, sheet_name=1)
        return client_data, purchased_goods_data, None
    except Exception as e:
        return None, None, str(e)

def perform_eda(df):
    """Perform comprehensive EDA on the purchased goods data"""
    eda_results = {}
    
    eda_results['shape'] = df.shape
    eda_results['columns'] = list(df.columns)
    eda_results['dtypes'] = df.dtypes.to_dict()
    eda_results['missing_values'] = df.isnull().sum().to_dict()
    eda_results['duplicates'] = df.duplicated().sum()
    eda_results['memory_usage'] = df.memory_usage(deep=True).sum()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        eda_results['numeric_summary'] = df[numeric_cols].describe()
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        eda_results['categorical_summary'] = {col: df[col].value_counts().head(10) for col in categorical_cols}
    
    return eda_results

def create_clean_visualizations(df):
    """Create clean, professional visualizations"""
    figs = []
    
    # Clean color palette
    colors = ['#1c2541', '#1f2937', '#374151', '#6b7280', '#e9ecef']
    
    # Missing values analysis
    if df.isnull().sum().sum() > 0:
        missing_data = df.isnull().sum()
        fig_missing = px.bar(
            x=missing_data.index, 
            y=missing_data.values,
            title="Missing Values by Column",
            labels={'x': 'Columns', 'y': 'Missing Values'},
            color_discrete_sequence=[colors[0]],
            template='plotly_white'
        )
        fig_missing.update_layout(
            height=400,
            title_font_size=16,
            title_font_color='#1f2937',
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=40, t=60, b=40)
        )
        figs.append(('missing_values', fig_missing))
    
    # Data types distribution
    dtype_counts = df.dtypes.value_counts()
    fig_dtypes = px.pie(
        values=dtype_counts.values,
        names=[str(x) for x in dtype_counts.index],
        title="Data Types Distribution",
        color_discrete_sequence=colors,
        template='plotly_white'
    )
    fig_dtypes.update_layout(
        height=400,
        title_font_size=16,
        title_font_color='#1f2937',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=60, b=40)
    )
    figs.append(('dtypes', fig_dtypes))
    
    # Numeric columns distribution
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0 and len(numeric_cols) <= 4:
        fig_numeric = make_subplots(
            rows=2, cols=2,
            subplot_titles=numeric_cols[:4]
        )
        
        for i, col in enumerate(numeric_cols[:4]):
            row = (i // 2) + 1
            col_pos = (i % 2) + 1
            fig_numeric.add_trace(
                go.Histogram(x=df[col], name=col, showlegend=False, marker_color=colors[0]),
                row=row, col=col_pos
            )
        
        fig_numeric.update_layout(
            title="Numeric Columns Distribution", 
            height=500,
            title_font_size=16,
            title_font_color='#1f2937',
            template='plotly_white',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        figs.append(('numeric_dist', fig_numeric))
    
    return figs

def save_dataframe_to_excel(df):
    """Convert dataframe to downloadable Excel file"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

# Client Information Management
def handle_client_data_editing():
    """Handle client data editing with proper persistence"""
    
    # Initialize edited_data if entering edit mode
    if st.session_state.edit_mode and st.session_state.edited_data is None:
        if st.session_state.client_data is not None:
            st.session_state.edited_data = st.session_state.client_data.copy()
    
    # Display section
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    
    # Button handling
    col1, col2, col3 = st.columns([1, 1, 8])
    
    if not st.session_state.edit_mode:
        with col1:
            if st.button("📝 Edit Data", key="edit_client"):
                st.session_state.edit_mode = True
                st.session_state.edited_data = st.session_state.client_data.copy()
                st.rerun()
    else:
        with col1:
            if st.button("💾 Save Changes", key="save_client"):
                # Save the edited data back to main client_data
                st.session_state.client_data = st.session_state.edited_data.copy()
                st.session_state.edit_mode = False
                st.session_state.edited_data = None
                st.success("Changes saved successfully!")
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel", key="cancel_client"):
                st.session_state.edit_mode = False
                st.session_state.edited_data = None
                st.rerun()
    
    st.markdown("---")
    
    # Data display
    if st.session_state.edit_mode:
        # Edit mode - show data editor
        if st.session_state.edited_data is not None:
            # Use callback to update session state
            def update_data():
                st.session_state.edited_data = st.session_state.client_editor
            
            st.data_editor(
                st.session_state.edited_data,
                use_container_width=True,
                hide_index=True,
                key="client_editor",
                on_change=update_data
            )
        else:
            st.error("No data available for editing")
    else:
        # Display mode - show read-only dataframe
        if st.session_state.client_data is not None:
            st.dataframe(
                st.session_state.client_data,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("No client data available")
    
    st.markdown('</div>', unsafe_allow_html=True)

def simulate_genai_pipeline(selected_workflows):
    """Enhanced pipeline simulation with professional loading UI"""
    total_steps = len(selected_workflows) * 3
    current_step = 0
    
    for workflow in selected_workflows:
        # Initialize
        current_step += 1
        progress_bar = st.progress(current_step / total_steps)
        st.markdown(f"""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <span class="loading-text">Initializing {workflow}...</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
        
        # Process
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        st.markdown(f"""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <span class="loading-text">Processing {workflow}...</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
        
        # Complete
        current_step += 1
        progress_bar.progress(current_step / total_steps)
        st.markdown(f"""
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <span class="loading-text">Completed {workflow}</span>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
    
    progress_bar.progress(1.0)
    st.markdown("""
    <div class="loading-container">
        <div class="loading-spinner"></div>
        <span class="loading-text">All workflows completed successfully</span>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1)

# Header
st.markdown("""
<div class="main-header">
    <h1 class="title">GHG Scope 3 Category 1 Classification</h1>
    <p class="subtitle">AI-powered classification and analysis of purchased goods for greenhouse gas emissions reporting</p>
</div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown(f"""
<div class="section-title" style="margin-top: 1rem;">
    <div class="step-number">1</div>
    <div>Upload Excel File</div>
</div>""", unsafe_allow_html=True)
st.markdown(" ")
with st.container():
    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=['xlsx', 'xls'],
        help="The Excel file should contain two sheets: first sheet for client information, second sheet for purchased goods data."
    )

if uploaded_file is not None:
    with st.spinner("Loading Excel file..."):
        client_data, purchased_goods_data, error = load_excel_file(uploaded_file)
    
    if error:
        st.error(f"Error loading file: {error}")
    else:
        st.session_state.client_data = client_data
        st.session_state.purchased_goods_data = purchased_goods_data
        st.session_state.data_uploaded = True
        st.success("File uploaded successfully")
        
# Client Information Section
if st.session_state.data_uploaded:
    st.markdown("---")
    st.markdown(f"""
    <div class="section-title">
        <div class="step-number">2</div>
        <div>Client Information</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    handle_client_data_editing()

# Purchased Goods Analysis Section
if st.session_state.data_uploaded:
    st.markdown(f"""
    <div class="section-title">
        <div class="step-number">3</div>
        <div>Purchased Goods Analysis</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    with st.container():
        # Data table
        st.markdown("**Purchased Goods Data**")
        st.dataframe(st.session_state.purchased_goods_data, use_container_width=True)
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # EDA metrics
    eda_results = perform_eda(st.session_state.purchased_goods_data)
    
    st.markdown("**Data Overview**")
    
    st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-number">{eda_results["shape"][0]:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Rows</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-number">{eda_results["shape"][1]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Columns</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-number">{eda_results["duplicates"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Duplicates</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        total_missing = sum(eda_results['missing_values'].values())
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-number">{total_missing}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Missing Values</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["Visualizations", "Data Summary", "Column Analysis"])
    
    with tab1:
        visualizations = create_clean_visualizations(st.session_state.purchased_goods_data)
        for viz_name, fig in visualizations:
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Types**")
            dtype_df = pd.DataFrame({
                'Column': eda_results['dtypes'].keys(),
                'Data Type': [str(v) for v in eda_results['dtypes'].values()]
            })
            st.dataframe(dtype_df, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("**Missing Values**")
            missing_df = pd.DataFrame({
                'Column': eda_results['missing_values'].keys(),
                'Missing Count': eda_results['missing_values'].values()
            })
            missing_df = missing_df[missing_df['Missing Count'] > 0]
            if len(missing_df) > 0:
                st.dataframe(missing_df, hide_index=True, use_container_width=True)
            else:
                st.markdown('<span class="status-badge status-success">No missing values</span>', unsafe_allow_html=True)
    
    with tab3:
        selected_column = st.selectbox(
            "Select column for analysis:",
            eda_results['columns']
        )
        
        if selected_column:
            col_data = st.session_state.purchased_goods_data[selected_column]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{selected_column} Statistics**")
                if col_data.dtype in ['int64', 'float64']:
                    st.write(col_data.describe())
                else:
                    st.write(f"Unique values: {col_data.nunique()}")
                    st.write(f"Most common: {col_data.mode().iloc[0] if len(col_data.mode()) > 0 else 'N/A'}")
            
            with col2:
                st.markdown(f"**{selected_column} Distribution**")
                if col_data.dtype == 'object':
                    value_counts = col_data.value_counts().head(10)
                    st.dataframe(value_counts, use_container_width=True)
                else:
                    fig = px.histogram(
                        x=col_data, 
                        title=f"Distribution of {selected_column}",
                        color_discrete_sequence=['#1c2541'],
                        template='plotly_white'
                    )
                    fig.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
                    st.plotly_chart(fig, use_container_width=True)

# GenAI Pipeline Section
if st.session_state.data_uploaded:
    st.markdown(f"""
    <div class="section-title">
        <div class="step-number">4</div>
        <div>GenAI Pipeline</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown("Select the workflows you would like to run:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="workflow-item">', unsafe_allow_html=True)
            data_cleaning = st.checkbox("Data Cleaning")
            st.markdown('<div class="workflow-title">Data Cleaning</div>', unsafe_allow_html=True)
            st.markdown('<div class="workflow-description">Remove duplicates, standardize formats, and handle missing values</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="workflow-item">', unsafe_allow_html=True)
            info_augmentation = st.checkbox("Information Augmentation")
            st.markdown('<div class="workflow-title">Information Augmentation</div>', unsafe_allow_html=True)
            st.markdown('<div class="workflow-description">Enrich data with supplier details, product categories, and emission factors</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="workflow-item">', unsafe_allow_html=True)
            classification = st.checkbox("Classification", value=True)
            st.markdown('<div class="workflow-title">Classification</div>', unsafe_allow_html=True)
            st.markdown('<div class="workflow-description">Classify purchased goods into appropriate GHG Scope 3 categories</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        # Pipeline execution
        selected_workflows = []
        if data_cleaning:
            selected_workflows.append("Data Cleaning")
        if info_augmentation:
            selected_workflows.append("Information Augmentation")
        if classification:
            selected_workflows.append("Classification")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if len(selected_workflows) > 0:
                st.markdown(f'<span class="status-badge status-info">Selected: {", ".join(selected_workflows)}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-badge status-warning">Please select at least one workflow</span>', unsafe_allow_html=True)
        
        with col2:
            if st.button("Run Pipeline", disabled=len(selected_workflows)==0):
                simulate_genai_pipeline(selected_workflows)
                st.success("Pipeline completed successfully")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem; margin: 2rem 0;">
    🌱 GHG Scope 3 Category 1 Classification Tool<br>
    Built by AI Factory SG
</div>
""", unsafe_allow_html=True)