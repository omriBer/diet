"""
The Leptin Method - שיטת הלפטין
Mobile-First 2026 UI - Light/Dark Mode
"""

import streamlit as st
import json
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="שיטת הלפטין",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== THEME STATE =====
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # Default to light mode

def get_theme_css():
    is_dark = st.session_state.theme == "dark"

    if is_dark:
        # Dark Mode - Masculine Palette
        colors = """
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-card: #21262d;
        --bg-elevated: #30363d;
        --bg-input: #21262d;

        --accent-primary: #00d4aa;
        --accent-secondary: #00a896;
        --accent-gradient: linear-gradient(135deg, #00d4aa 0%, #00a896 100%);
        --accent-glow: rgba(0, 212, 170, 0.25);

        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-muted: #484f58;
        --text-on-accent: #0d1117;

        --border-color: rgba(240, 246, 252, 0.1);
        --border-hover: rgba(0, 212, 170, 0.4);

        --success-bg: rgba(0, 212, 170, 0.12);
        --warning-bg: rgba(244, 162, 97, 0.12);
        --error-bg: rgba(248, 81, 73, 0.12);
        --info-bg: rgba(56, 139, 253, 0.12);

        --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.5);
        """
    else:
        # Light Mode - Clean Masculine Palette
        colors = """
        --bg-primary: #ffffff;
        --bg-secondary: #f6f8fa;
        --bg-card: #ffffff;
        --bg-elevated: #f6f8fa;
        --bg-input: #ffffff;

        --accent-primary: #0891b2;
        --accent-secondary: #0e7490;
        --accent-gradient: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);
        --accent-glow: rgba(8, 145, 178, 0.15);

        --text-primary: #1f2937;
        --text-secondary: #4b5563;
        --text-muted: #9ca3af;
        --text-on-accent: #ffffff;

        --border-color: #e5e7eb;
        --border-hover: rgba(8, 145, 178, 0.5);

        --success-bg: rgba(16, 185, 129, 0.1);
        --warning-bg: rgba(245, 158, 11, 0.1);
        --error-bg: rgba(239, 68, 68, 0.1);
        --info-bg: rgba(59, 130, 246, 0.1);

        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
        --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
        """

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap');

/* ========== CSS VARIABLES ========== */
:root {{
    {colors}

    /* Semantic Colors */
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #3b82f6;

    /* Spacing - Mobile First */
    --space-xs: 0.25rem;
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 1.5rem;
    --space-xl: 2rem;

    /* Touch Targets - Extra Large for Mobile */
    --touch-min: 56px;
    --touch-comfortable: 64px;
    --touch-large: 72px;

    /* Border Radius */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;

    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 200ms ease;
}}

/* ========== GLOBAL RESET ========== */
*, *::before, *::after {{
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}}

* {{
    font-family: 'Heebo', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

/* ========== APP CONTAINER ========== */
.stApp {{
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}}

[data-testid="stAppViewContainer"] {{
    background: var(--bg-primary) !important;
}}

[data-testid="stHeader"] {{
    background: transparent !important;
}}

/* RTL Support */
.stApp, .stMarkdown, p, span, label, div, h1, h2, h3, h4, h5, h6 {{
    direction: rtl;
    text-align: right;
}}

/* Hide Streamlit Defaults */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none !important;
}}

/* Mobile-First Container */
.block-container {{
    padding: var(--space-md) var(--space-md) 5rem var(--space-md) !important;
    max-width: 100% !important;
}}

@media (min-width: 768px) {{
    .block-container {{
        max-width: 640px !important;
        margin: 0 auto;
        padding: var(--space-lg) var(--space-lg) 5rem var(--space-lg) !important;
    }}
}}

/* ========== TYPOGRAPHY ========== */
h1 {{
    color: var(--text-primary) !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    margin-bottom: var(--space-sm) !important;
    line-height: 1.2 !important;
}}

h2 {{
    color: var(--text-primary) !important;
    font-size: 1.375rem !important;
    font-weight: 700 !important;
    margin-bottom: var(--space-sm) !important;
}}

h3 {{
    color: var(--text-primary) !important;
    font-size: 1.125rem !important;
    font-weight: 600 !important;
    margin-bottom: var(--space-sm) !important;
}}

h4 {{
    color: var(--text-secondary) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}}

p, span, label {{
    color: var(--text-secondary) !important;
    font-size: 0.9375rem !important;
    line-height: 1.6 !important;
}}

.stCaption, [data-testid="stCaptionContainer"] {{
    color: var(--text-muted) !important;
    font-size: 0.8125rem !important;
}}

/* ========== BUTTONS - LARGE & TOUCH FRIENDLY ========== */
.stButton > button {{
    width: 100%;
    min-height: var(--touch-large);
    background: var(--accent-gradient) !important;
    color: var(--text-on-accent) !important;
    font-weight: 700 !important;
    font-size: 1.125rem !important;
    border: none !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-normal);
    cursor: pointer;
    padding: 1rem 1.5rem !important;
    letter-spacing: 0.01em;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg), 0 0 30px var(--accent-glow);
}}

.stButton > button:active {{
    transform: translateY(0);
    box-shadow: var(--shadow-sm);
}}

/* Secondary Buttons (in columns) - Still Large */
div[data-testid="column"] .stButton > button {{
    min-height: var(--touch-comfortable);
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    box-shadow: var(--shadow-sm);
    font-size: 1.25rem !important;
    font-weight: 600 !important;
}}

div[data-testid="column"] .stButton > button:hover {{
    border-color: var(--accent-primary) !important;
    background: var(--bg-elevated) !important;
    box-shadow: var(--shadow-md);
}}

/* ========== INPUTS - LARGE & CLEAR ========== */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {{
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1rem 1.25rem !important;
    font-size: 1.125rem !important;
    min-height: var(--touch-comfortable) !important;
    transition: all var(--transition-fast);
}}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {{
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
    outline: none !important;
}}

.stTextInput > div > div > input::placeholder {{
    color: var(--text-muted) !important;
    font-size: 1rem !important;
}}

/* Input Labels - Larger & Clearer */
.stTextInput > label,
.stNumberInput > label,
.stSlider > label,
.stDateInput > label {{
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    margin-bottom: var(--space-sm) !important;
}}

/* ========== SLIDERS - LARGE THUMB & TRACK ========== */
.stSlider {{
    padding: var(--space-md) 0;
}}

.stSlider > div > div > div {{
    background: var(--bg-elevated) !important;
}}

.stSlider [data-baseweb="slider"] > div {{
    background: var(--bg-elevated) !important;
    height: 12px !important;
    border-radius: 6px !important;
}}

.stSlider [data-baseweb="slider"] > div > div {{
    background: var(--accent-gradient) !important;
    height: 12px !important;
}}

.stSlider [role="slider"] {{
    background: var(--accent-primary) !important;
    border: 4px solid var(--bg-primary) !important;
    box-shadow: var(--shadow-lg);
    width: 36px !important;
    height: 36px !important;
    top: -12px !important;
}}

.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {{
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}}

/* ========== CHECKBOXES - LARGE TOUCH TARGETS ========== */
.stCheckbox {{
    padding: var(--space-sm) 0;
}}

.stCheckbox > label {{
    background: var(--bg-card) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.25rem var(--space-lg) !important;
    min-height: var(--touch-large);
    display: flex !important;
    align-items: center !important;
    transition: all var(--transition-fast);
    cursor: pointer;
    margin: var(--space-sm) 0;
    gap: var(--space-md);
}}

.stCheckbox > label:hover {{
    border-color: var(--border-hover) !important;
    background: var(--bg-elevated) !important;
    transform: translateX(-2px);
}}

.stCheckbox > label:has(input:checked) {{
    border-color: var(--accent-primary) !important;
    background: var(--success-bg) !important;
    border-width: 3px;
}}

.stCheckbox > label > span {{
    color: var(--text-primary) !important;
    font-size: 1.0625rem !important;
    font-weight: 500 !important;
    line-height: 1.4;
}}

/* Checkbox Icon - Larger */
.stCheckbox [data-testid="stCheckbox"] > div:first-child {{
    background: var(--bg-elevated) !important;
    border: 2px solid var(--text-muted) !important;
    border-radius: 8px !important;
    transition: all var(--transition-fast);
    min-width: 28px !important;
    min-height: 28px !important;
}}

.stCheckbox > label:has(input:checked) [data-testid="stCheckbox"] > div:first-child {{
    background: var(--accent-primary) !important;
    border-color: var(--accent-primary) !important;
}}

/* ========== TABS - LARGE & EASY TO TAP ========== */
.stTabs [data-baseweb="tab-list"] {{
    background: var(--bg-card);
    border-radius: var(--radius-xl);
    padding: 8px;
    gap: 6px;
    border: 1px solid var(--border-color);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}}

.stTabs [data-baseweb="tab"] {{
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    border-radius: var(--radius-md) !important;
    padding: 0.875rem 1rem !important;
    min-height: var(--touch-min);
    white-space: nowrap;
    transition: all var(--transition-fast);
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: var(--text-secondary) !important;
    background: var(--bg-elevated) !important;
}}

.stTabs [aria-selected="true"] {{
    background: var(--accent-gradient) !important;
    color: var(--text-on-accent) !important;
    font-weight: 700 !important;
    box-shadow: var(--shadow-sm);
}}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    display: none !important;
}}

/* ========== METRICS - LARGE & PROMINENT ========== */
[data-testid="stMetricValue"] {{
    color: var(--text-primary) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    line-height: 1.2;
}}

[data-testid="stMetricLabel"] {{
    color: var(--text-muted) !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

div[data-testid="metric-container"] {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: var(--space-lg) var(--space-md);
    text-align: center;
}}

/* ========== PROGRESS BAR - THICK & VISIBLE ========== */
.stProgress {{
    margin: var(--space-md) 0;
}}

.stProgress > div > div > div {{
    background: var(--bg-elevated) !important;
    border-radius: 10px !important;
    height: 16px !important;
}}

.stProgress > div > div > div > div {{
    background: var(--accent-gradient) !important;
    border-radius: 10px !important;
}}

/* ========== EXPANDER - LARGE TOUCH TARGET ========== */
.streamlit-expanderHeader {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 1.125rem var(--space-lg) !important;
    min-height: var(--touch-comfortable);
    transition: all var(--transition-fast);
}}

.streamlit-expanderHeader:hover {{
    border-color: var(--border-hover) !important;
    background: var(--bg-elevated) !important;
}}

.streamlit-expanderContent {{
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-lg) var(--radius-lg) !important;
    padding: var(--space-lg) !important;
    font-size: 1rem !important;
}}

[data-testid="stExpander"] details {{
    border: none !important;
}}

/* ========== ALERTS ========== */
.stAlert, [data-testid="stAlert"] {{
    border-radius: var(--radius-md) !important;
    border: none !important;
    padding: var(--space-md) !important;
}}

.stSuccess, [data-testid="stAlert"][data-baseweb*="positive"] {{
    background: var(--success-bg) !important;
    border-right: 4px solid var(--success) !important;
}}

.stInfo, [data-testid="stAlert"][data-baseweb*="info"] {{
    background: var(--info-bg) !important;
    border-right: 4px solid var(--info) !important;
}}

.stWarning, [data-testid="stAlert"][data-baseweb*="warning"] {{
    background: var(--warning-bg) !important;
    border-right: 4px solid var(--warning) !important;
}}

.stError, [data-testid="stAlert"][data-baseweb*="negative"] {{
    background: var(--error-bg) !important;
    border-right: 4px solid var(--error) !important;
}}

/* ========== DATE INPUT - LARGE ========== */
.stDateInput > div > div > input {{
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    min-height: var(--touch-comfortable) !important;
    font-size: 1.125rem !important;
    padding: 1rem !important;
}}

.stDateInput > div > div > input:focus {{
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
}}

/* ========== RADIO - LARGE TOUCH TARGETS ========== */
.stRadio > div {{
    gap: var(--space-md);
}}

.stRadio > div > label {{
    background: var(--bg-card) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.125rem var(--space-lg) !important;
    color: var(--text-primary) !important;
    min-height: var(--touch-comfortable);
    font-size: 1rem !important;
    font-weight: 500 !important;
    transition: all var(--transition-fast);
    cursor: pointer;
}}

.stRadio > div > label:hover {{
    border-color: var(--border-hover) !important;
    background: var(--bg-elevated) !important;
    transform: translateX(-2px);
}}

.stRadio > div > label[data-checked="true"] {{
    border-color: var(--accent-primary) !important;
    background: var(--success-bg) !important;
    border-width: 3px;
}}

/* ========== DIVIDERS ========== */
hr {{
    border: none !important;
    height: 1px !important;
    background: var(--border-color) !important;
    margin: var(--space-lg) 0 !important;
}}

/* ========== SCROLLBAR ========== */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}

::-webkit-scrollbar-track {{
    background: var(--bg-secondary);
}}

::-webkit-scrollbar-thumb {{
    background: var(--bg-elevated);
    border-radius: 3px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: var(--text-muted);
}}

/* ========== THEME TOGGLE BUTTON ========== */
.theme-toggle {{
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 999999;
    background: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: 8px 12px !important;
    color: var(--text-primary) !important;
    font-size: 1.25rem;
    cursor: pointer;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-fast);
    min-width: 44px;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.theme-toggle:hover {{
    transform: scale(1.05);
    box-shadow: var(--shadow-lg);
}}

/* ========== CUSTOM UTILITY CLASSES ========== */
.zone-header {{
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    margin-bottom: var(--space-md);
}}

.stat-accent {{
    color: var(--accent-primary) !important;
    font-weight: 700 !important;
}}

/* ========== TASK CARDS ========== */
.task-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-xl);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
    box-shadow: var(--shadow-sm);
}}

.card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-md);
}}

.card-title {{
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}}

/* ========== QUICK ADD BUTTONS ========== */
.quick-add-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-sm);
    margin: var(--space-md) 0;
}}

/* ========== TOGGLE BUTTONS (for nutrition) ========== */
.toggle-btn {{
    min-height: 80px !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    font-size: 1rem !important;
    text-align: center !important;
}}

.toggle-btn.active {{
    background: var(--success-bg) !important;
    border-color: var(--accent-primary) !important;
    border-width: 3px !important;
}}

/* ========== WATER GLASSES ========== */
.glasses-row {{
    display: flex;
    justify-content: center;
    gap: var(--space-md);
    margin: var(--space-md) 0;
}}

.glass-btn {{
    width: 56px !important;
    height: 56px !important;
    min-height: 56px !important;
    border-radius: 50% !important;
    font-size: 1.5rem !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

/* ========== TIME INPUT ========== */
.stTimeInput > div > div > input {{
    background: var(--bg-input) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    min-height: var(--touch-comfortable) !important;
    font-size: 1.25rem !important;
    padding: 1rem !important;
    text-align: center !important;
}}

.stTimeInput > div > div > input:focus {{
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 4px var(--accent-glow) !important;
}}

.stTimeInput > label {{
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.9375rem !important;
}}

/* ========== WINDOW METER ========== */
.window-meter {{
    background: var(--bg-elevated);
    border-radius: var(--radius-md);
    padding: var(--space-md);
    text-align: center;
    margin-top: var(--space-md);
}}

.window-value {{
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent-primary);
}}

.window-label {{
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-top: var(--space-xs);
}}

/* ========== NUTRITION GRID ========== */
.nutrition-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--space-sm);
}}

/* ========== FAT COUNTER ========== */
.fat-counter {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-md);
    padding: var(--space-md);
    background: var(--bg-elevated);
    border-radius: var(--radius-lg);
}}

.fat-value {{
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--text-primary);
    min-width: 60px;
    text-align: center;
}}

/* ========== COMPACT HEADER ========== */
.compact-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: var(--space-md);
}}

.score-badge {{
    background: var(--accent-gradient);
    color: var(--text-on-accent);
    padding: var(--space-sm) var(--space-md);
    border-radius: var(--radius-lg);
    font-weight: 700;
    font-size: 1.125rem;
}}

/* ========== MOBILE OPTIMIZATIONS ========== */
@media (max-width: 480px) {{
    h1 {{ font-size: 1.625rem !important; }}
    h2 {{ font-size: 1.375rem !important; }}
    h3 {{ font-size: 1.125rem !important; }}

    .stButton > button {{
        min-height: var(--touch-comfortable);
        font-size: 1rem !important;
        padding: 0.875rem 1rem !important;
    }}

    div[data-testid="column"] {{
        padding: 0 4px !important;
    }}

    div[data-testid="column"] .stButton > button {{
        min-height: var(--touch-min);
        font-size: 1.125rem !important;
        padding: 0.75rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.5rem !important;
    }}

    .stCheckbox > label {{
        padding: 1rem !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        padding: 0.75rem 0.875rem !important;
        font-size: 0.9375rem !important;
    }}
}}

/* Extra small screens */
@media (max-width: 360px) {{
    .block-container {{
        padding: var(--space-sm) var(--space-sm) 5rem var(--space-sm) !important;
    }}

    .stButton > button {{
        font-size: 0.9375rem !important;
    }}
}}

/* ========== SAFE AREA (iOS) ========== */
@supports (padding-bottom: env(safe-area-inset-bottom)) {{
    .block-container {{
        padding-bottom: calc(5rem + env(safe-area-inset-bottom)) !important;
    }}
}}
</style>
"""

# Apply theme CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)

# ===== KNOWLEDGE BASE =====
WEEK_DATA = {
    1: {
        "phase": "הצפה", "icon": "🌊",
        "title": "שבוע 1 - הצפת הלפטין",
        "focus": "התחל להגדיל צריכת מים בהדרגה",
        "instructions": ["אכול כרגיל ללא שינויים", "הגדל שתיית מים בהדרגה", "הימנע מממתיקים במים"],
        "allowed": "כל המזונות. נוזלים: מים, סודה ללא סוכר, תה ללא סוכר",
        "forbidden": "אין הגבלות",
        "tips": ["צפה לעלייה בביקורי שירותים", "השתמש באפליקציית תזכורת מים"],
        "treat": None
    },
    2: {
        "phase": "הצפה", "icon": "🌊",
        "title": "שבוע 2 - מיקוד בירקות",
        "focus": "סדר אכילה לפטיני - ירקות קודם",
        "instructions": ["ירקות ראשונים בכל ארוחה", "50% ירקות מנקים ב-2 ארוחות גדולות"],
        "allowed": "חלבונים: בשר, ביצים, דגים, חלב. ירקות מנקים. שומנים: ללא הגבלה",
        "forbidden": "ירקות לא מנקים: תפו״א, בטטה, סלק, קטניות",
        "tips": ["הכן ירקות מראש פעמיים בשבוע", "במסעדה - רוטב בצד"],
        "treat": None
    },
    3: {
        "phase": "ניקוי", "icon": "✨",
        "title": "שבוע 3 - תחילת הניקוי",
        "focus": "חופשה מסוכר וקמח",
        "instructions": ["ללא סוכר (לבן, חום, סילאן, מייפל)", "ללא קמח מכל סוג", "פרי אחד ביום"],
        "allowed": "חלבונים: ביצים, דגים, עוף, בשר, חלב, טופו. ירקות מנקים. שומנים: טחינה, חמאה, שמן, זיתים, אבוקדו. פחמימות: קטניות, קינואה, כוסמת",
        "forbidden": "סוכר, קמח, שוקולד, חטיפים, פירות יבשים, מיץ",
        "tips": ["צפה לחשקים בימים הראשונים", "אל תשקול - התמקד בתהליך"],
        "treat": None
    },
    4: {
        "phase": "ניקוי", "icon": "✨",
        "title": "שבוע 4 - יום פינוק ראשון",
        "focus": "המשך ניקוי + יום פינוק",
        "instructions": ["המשך כללי שבוע 3", "יום פינוק ראשון השבוע"],
        "allowed": "כמו שבוע 3",
        "forbidden": "סוכר, קמח, מעובדים",
        "tips": ["50% ירקות גם ביום פינוק"],
        "treat": "צלחת 50% ירקות + 50% כל דבר"
    },
    5: {
        "phase": "ניקוי מתקדם", "icon": "💪",
        "title": "שבוע 5 - ניקוי מתקדם",
        "focus": "2-3 ארוחות, חלון 8-12 שעות",
        "instructions": ["2-3 ארוחות ביום בלבד", "חלון אכילה 8-12 שעות", "ללא אגוזים"],
        "allowed": "חלבונים: כולם. ירקות: 50% מנקים. שומנים: 2-3 כפות. פחמימות: קטניות, קינואה. פרי: 1 (יער ללא הגבלה)",
        "forbidden": "סוכר, קמח, טיגון, אגוזים",
        "tips": ["מים לניהול רעב בין ארוחות"],
        "treat": "ארוחה אחת 50/50. מבוטל אם שברת כללים פעמיים"
    },
    6: {
        "phase": "ניקוי מתקדם", "icon": "💪",
        "title": "שבוע 6 - חיזוק הרגלים",
        "focus": "המשך ניקוי מתקדם",
        "instructions": ["המשך כללי שבוע 5", "2-3 ארוחות", "חלון 8-12 שעות"],
        "allowed": "כמו שבוע 5",
        "forbidden": "סוכר, קמח, טיגון, אגוזים",
        "tips": ["כף שמן = 1 מנה", "חצי אבוקדו = 1 מנה", "15 זיתים = 1 מנה"],
        "treat": "ארוחת פינוק אחת בשבוע"
    },
    7: {
        "phase": "ניקוי מתקדם", "icon": "💪",
        "title": "שבוע 7 - סיום ניקוי",
        "focus": "שבוע אחרון של ניקוי",
        "instructions": ["המשך כללי שבוע 5-6", "התכונן למעבר לתחזוקה"],
        "allowed": "כמו שבוע 5-6",
        "forbidden": "סוכר, קמח, טיגון, אגוזים",
        "tips": ["הגוף עבר שינוי הורמונלי משמעותי"],
        "treat": "ארוחת פינוק אחת"
    },
    8: {
        "phase": "מעבר", "icon": "🔄",
        "title": "שבוע 8 - מעבר",
        "focus": "בחירת מסלול תחזוקה",
        "instructions": ["שבוע מעבר", "בחר מסלול: מהיר / ניקוי / מתון"],
        "allowed": "לפי ניקוי מתקדם",
        "forbidden": "סוכר, קמח",
        "tips": ["הזמן לבחור את המסלול שלך"],
        "treat": "ארוחת פינוק אחת"
    },
    9: {
        "phase": "מסלולים", "icon": "🎯",
        "title": "שבוע 9+ - תחזוקה",
        "focus": "המשך במסלול שבחרת",
        "instructions": ["מהיר: קטניות + פרי", "ניקוי: קטניות + קינואה + פרי + דבש", "מתון: קטניות + פחמימות פעם ביום"],
        "allowed": "לפי המסלול",
        "forbidden": "סוכר לבן, קמח לבן",
        "tips": [],
        "treat": "מהיר: 2 ימי פינוק. ניקוי/מתון: 1"
    }
}

TRACKS = {
    "fast": {"name": "מהיר", "icon": "🚀", "carbs": "קטניות + פרי", "treats": "2 ימי פינוק"},
    "cleanse": {"name": "ניקוי", "icon": "✨", "carbs": "קטניות + קינואה + פרי + דבש", "treats": "1 יום פינוק + פירות"},
    "moderate": {"name": "מתון", "icon": "🍚", "carbs": "קטניות + פחמימות פעם ביום", "treats": "1 יום פינוק"}
}

VEGGIES = "מלפפון, עגבנייה, בצל, ברוקולי, כרובית, כרוב, קישוא, חסה, תרד, פטריות, פלפל, חציל, שעועית ירוקה, אספרגוס, כרפס"

TIPS = [
    "התקדמות, לא שלמות",
    "80% מספיק - עקרון פארטו",
    "עקביות חשובה ממושלמות",
    "המים הם הדלק של השינוי",
    "כל יום שאתה עומד ביעדים - הגוף משתנה"
]

# ===== STORAGE =====
DEFAULT_DATA = {
    "settings": {"start_date": None, "track": None, "name": "", "theme": "light"},
    "logs": {}
}

def load_data():
    """Load data from GitHub Gist with robust error handling."""
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")
        if not token or not gist_id:
            return DEFAULT_DATA.copy()
        headers = {"Authorization": f"token {token}"}
        r = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers, timeout=10)
        if r.ok:
            gist_data = r.json()
            if "files" in gist_data and "leptin_data.json" in gist_data["files"]:
                content = gist_data["files"]["leptin_data.json"].get("content", "")
                if content and isinstance(content, str):
                    parsed = json.loads(content)
                    # Ensure data structure is valid
                    if isinstance(parsed, dict) and "settings" in parsed and "logs" in parsed:
                        # Ensure theme exists
                        if "theme" not in parsed["settings"]:
                            parsed["settings"]["theme"] = "light"
                        return parsed
    except (json.JSONDecodeError, requests.RequestException, KeyError, TypeError):
        pass
    return DEFAULT_DATA.copy()

def save_data(data):
    """Save data to GitHub Gist with validation."""
    if not isinstance(data, dict):
        return
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")
        if not token:
            return
        headers = {"Authorization": f"token {token}"}
        content = json.dumps(data, ensure_ascii=False, default=str)
        payload = {"files": {"leptin_data.json": {"content": content}}}
        if gist_id:
            requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=payload, timeout=10)
        else:
            payload["public"] = False
            r = requests.post("https://api.github.com/gists", headers=headers, json=payload, timeout=10)
            if r.status_code == 201:
                st.toast(f"GIST_ID: {r.json()['id']}")
    except (requests.RequestException, TypeError, ValueError):
        pass

# ===== HELPERS =====
def today():
    return datetime.now().strftime("%Y-%m-%d")

def calc_day_week(start):
    try:
        d = (datetime.now() - datetime.strptime(start, "%Y-%m-%d")).days + 1
        return d, min(13, max(1, (d-1)//7 + 1))
    except:
        return 1, 1

def get_week(w):
    return WEEK_DATA.get(w if w <= 9 else 9, WEEK_DATA[1])

def init_log(data):
    t = today()
    if t not in data["logs"]:
        data["logs"][t] = {
            "water": 0,
            "water_before": 0,
            "veggies": False,
            "protein": False,
            "window": 0,
            "fats": 0,
            "treat": False,
            "slip": False,
            "first_meal": "08:00",
            "last_meal": "18:00"
        }
    # Ensure existing logs have time fields
    log = data["logs"][t]
    if "first_meal" not in log:
        log["first_meal"] = "08:00"
    if "last_meal" not in log:
        log["last_meal"] = "18:00"
    return data

def score(log):
    s = 0
    s += 20 if log.get("water", 0) >= 2 else 0
    s += 10 if log.get("water", 0) >= 3 else 0
    s += 10 if log.get("water_before", 0) >= 3 else 0
    s += 25 if log.get("veggies") else 0
    s += 15 if log.get("protein") else 0
    s += 10 if log.get("fats", 0) <= 3 else 0
    s += 10 if 0 < log.get("window", 0) <= 12 else 0
    s -= 20 if log.get("slip") and not log.get("treat") else 0
    return max(0, min(100, s))

def streak(data):
    c = 0
    for i in range(30):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        if d in data["logs"] and score(data["logs"][d]) >= 70:
            c += 1
        else:
            break
    return c

# ===== AUTH =====
def auth():
    if st.session_state.get("auth"):
        return True

    st.markdown("## ⚡ שיטת הלפטין")
    st.caption("המסע שלך לשינוי אמיתי")
    st.markdown("---")

    pw = st.text_input("סיסמה", type="password", placeholder="הזן סיסמה")
    if st.button("התחבר"):
        if pw == st.secrets.get("PASSWORD", "leptin2024"):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("סיסמה שגויה")
    return False

# ===== THEME TOGGLE =====
def render_theme_toggle():
    icon = "🌙" if st.session_state.theme == "light" else "☀️"
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button(icon, key="theme_toggle", help="החלף ערכת נושא"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            if "data" in st.session_state:
                st.session_state.data["settings"]["theme"] = st.session_state.theme
                save_data(st.session_state.data)
            st.rerun()

# ===== SCREENS =====
def onboarding(data):
    st.markdown("## ⚡ שיטת הלפטין")
    st.markdown("### ברוך הבא למסע")
    st.markdown("---")

    name = st.text_input("השם שלך", placeholder="איך קוראים לך?")

    st.markdown("**מתי התחלת?**")
    start = st.date_input("תאריך", value=datetime.now(), max_value=datetime.now(), label_visibility="collapsed")

    st.info("האפליקציה תחשב אוטומטית את השבוע והכללים המתאימים")

    if st.button("🚀 להתחיל"):
        data["settings"]["name"] = name or "אלוף"
        data["settings"]["start_date"] = start.strftime("%Y-%m-%d")
        data["settings"]["theme"] = st.session_state.theme
        save_data(data)
        st.session_state.data = data
        st.rerun()

def main_screen(data):
    s = data["settings"]
    day, week = calc_day_week(s["start_date"])
    w = get_week(week)

    data = init_log(data)
    log = data["logs"][today()]
    sc = score(log)
    st_count = streak(data)

    # ===== COMPACT HEADER =====
    col_name, col_score = st.columns([3, 1])
    with col_name:
        st.markdown(f"### שלום {s.get('name', '')} 👋")
        st.caption(f"{w['icon']} יום {day} | {w['title']}")
    with col_score:
        st.metric("ציון", f"{sc}%")

    st.progress(sc / 100)

    # ===== CARD 1: HYDRATION =====
    st.markdown("#### 💧 מים")

    # Water amount display
    water_val = log.get("water", 0)
    col_amount, col_reset = st.columns([4, 1])
    with col_amount:
        st.markdown(f"**{water_val:.1f} ליטר** {'✅' if water_val >= 2 else ''}")
    with col_reset:
        if st.button("🔄", key="water_reset", help="איפוס"):
            log["water"] = 0
            save_data(data)
            st.rerun()

    # Quick add buttons
    w1, w2, w3 = st.columns(3)
    with w1:
        if st.button("☕ 250ml", key="w250", use_container_width=True):
            log["water"] = min(6, log.get("water", 0) + 0.25)
            save_data(data)
            st.rerun()
    with w2:
        if st.button("🥤 500ml", key="w500", use_container_width=True):
            log["water"] = min(6, log.get("water", 0) + 0.5)
            save_data(data)
            st.rerun()
    with w3:
        if st.button("🍶 1L", key="w1000", use_container_width=True):
            log["water"] = min(6, log.get("water", 0) + 1.0)
            save_data(data)
            st.rerun()

    # Water before meals - toggle glasses
    st.markdown("**לפני ארוחות:**")
    wb = log.get("water_before", 0)
    g1, g2, g3 = st.columns(3)
    with g1:
        icon1 = "🔵" if wb >= 1 else "⚪"
        if st.button(icon1, key="glass1", use_container_width=True):
            log["water_before"] = 0 if wb >= 1 and wb < 2 else 1
            if wb >= 1:
                log["water_before"] = 0
            else:
                log["water_before"] = 1
            save_data(data)
            st.rerun()
    with g2:
        icon2 = "🔵" if wb >= 2 else "⚪"
        if st.button(icon2, key="glass2", use_container_width=True):
            if wb >= 2:
                log["water_before"] = 1
            else:
                log["water_before"] = 2
            save_data(data)
            st.rerun()
    with g3:
        icon3 = "🔵" if wb >= 3 else "⚪"
        if st.button(icon3, key="glass3", use_container_width=True):
            if wb >= 3:
                log["water_before"] = 2
            else:
                log["water_before"] = 3
            save_data(data)
            st.rerun()

    st.markdown("---")

    # ===== CARD 2: NUTRITION GRID =====
    st.markdown("#### 🥗 תזונה")

    # Toggle buttons for veggies and protein
    n1, n2 = st.columns(2)
    with n1:
        veg_active = log.get("veggies", False)
        veg_icon = "✅" if veg_active else "🥬"
        veg_style = "primary" if veg_active else "secondary"
        if st.button(f"{veg_icon}\nירקות 50%", key="veg_toggle", use_container_width=True, type=veg_style):
            log["veggies"] = not veg_active
            save_data(data)
            st.rerun()
    with n2:
        prot_active = log.get("protein", False)
        prot_icon = "✅" if prot_active else "🍗"
        prot_style = "primary" if prot_active else "secondary"
        if st.button(f"{prot_icon}\nחלבון", key="prot_toggle", use_container_width=True, type=prot_style):
            log["protein"] = not prot_active
            save_data(data)
            st.rerun()

    # Fats counter in nutrition section
    st.markdown("**🥑 שומנים:**")
    fc1, fc2, fc3 = st.columns([1, 2, 1])
    with fc1:
        if st.button("➖", key="f-", use_container_width=True):
            log["fats"] = max(0, log.get("fats", 0) - 1)
            save_data(data)
            st.rerun()
    with fc2:
        f = log.get("fats", 0)
        status = "✅" if f <= 3 else "⚠️"
        st.markdown(f"<div style='text-align:center;font-size:1.5rem;font-weight:700;'>{f} כפות {status}</div>", unsafe_allow_html=True)
    with fc3:
        if st.button("➕", key="f+", use_container_width=True):
            log["fats"] = log.get("fats", 0) + 1
            save_data(data)
            st.rerun()

    st.caption("מקסימום 2-3 כפות ביום")

    with st.expander("📋 ירקות מנקים"):
        st.markdown(VEGGIES)
        st.caption("❌ לא: תפו״א, בטטה, סלק, תירס, קטניות")

    st.markdown("---")

    # ===== CARD 3: TIMING =====
    st.markdown("#### ⏰ חלון אכילה")

    # Time inputs
    from datetime import time as dt_time

    # Get saved times or defaults
    first_meal = log.get("first_meal", "08:00")
    last_meal = log.get("last_meal", "18:00")

    t1, t2 = st.columns(2)
    with t1:
        first_time = st.time_input("ארוחה ראשונה", value=dt_time(int(first_meal.split(":")[0]), int(first_meal.split(":")[1])), key="first_meal_input")
    with t2:
        last_time = st.time_input("ארוחה אחרונה", value=dt_time(int(last_meal.split(":")[0]), int(last_meal.split(":")[1])), key="last_meal_input")

    # Calculate window
    first_minutes = first_time.hour * 60 + first_time.minute
    last_minutes = last_time.hour * 60 + last_time.minute
    window_hours = max(0, (last_minutes - first_minutes) / 60)

    # Save times and window
    new_first = f"{first_time.hour:02d}:{first_time.minute:02d}"
    new_last = f"{last_time.hour:02d}:{last_time.minute:02d}"
    if new_first != log.get("first_meal") or new_last != log.get("last_meal"):
        log["first_meal"] = new_first
        log["last_meal"] = new_last
        log["window"] = int(window_hours)
        save_data(data)

    # Window meter
    if window_hours > 0:
        remaining = max(0, 12 - window_hours)
        progress_val = min(1.0, window_hours / 12)

        if window_hours <= 10:
            st.success(f"חלון: {window_hours:.1f} שעות - מצוין! 🎯")
        elif window_hours <= 12:
            st.info(f"חלון: {window_hours:.1f} שעות - טוב 👍")
        else:
            st.warning(f"חלון: {window_hours:.1f} שעות - נסה לקצר ⚠️")

        st.progress(progress_val)

    st.markdown("---")

    # ===== WEEKLY INFO (Collapsible) =====
    with st.expander(f"📋 הנחיות שבוע {week}"):
        for inst in w["instructions"]:
            st.markdown(f"• {inst}")
        st.markdown("---")
        st.markdown("**✅ מותר:**")
        st.markdown(w["allowed"])
        st.markdown("**🚫 אסור:**")
        st.markdown(w["forbidden"])
        if w.get("treat"):
            st.markdown("**🎉 פינוק:**")
            st.markdown(w["treat"])

    # TRACK (week 9+)
    if week >= 9:
        track = s.get("track")
        if not track:
            st.markdown("#### 🛤️ בחר מסלול")
            track = st.radio("", list(TRACKS.keys()), format_func=lambda x: f"{TRACKS[x]['icon']} {TRACKS[x]['name']}", horizontal=True, label_visibility="collapsed")
            if st.button("שמור מסלול"):
                s["track"] = track
                save_data(data)
                st.rerun()
        else:
            t = TRACKS[track]
            st.info(f"**{t['icon']} {t['name']}** | {t['carbs']} | {t['treats']}")

    # TREAT & SLIP
    treat_col, slip_col = st.columns(2)
    with treat_col:
        treat_active = log.get("treat", False)
        treat_btn = "🎉 יום פינוק ✓" if treat_active else "🎉 יום פינוק"
        if st.button(treat_btn, key="treat_toggle", use_container_width=True, type="primary" if treat_active else "secondary"):
            log["treat"] = not treat_active
            save_data(data)
            st.rerun()

    with slip_col:
        if week >= 3 and not log.get("treat"):
            slip_active = log.get("slip", False)
            slip_btn = "⚠️ החלקה ✓" if slip_active else "⚠️ החלקה"
            if st.button(slip_btn, key="slip_toggle", use_container_width=True, type="primary" if slip_active else "secondary"):
                log["slip"] = not slip_active
                save_data(data)
                st.rerun()

    # RESCUE (if needed)
    if sc < 60 or log.get("slip"):
        st.warning("🆘 גלגלי הצלה: הוסף מים, ירקות, או דחה ארוחה מחר")

    st.markdown("---")

    # ===== FINISH DAY BUTTON =====
    if st.button("✅ סיום יום", use_container_width=True, type="primary"):
        save_data(data)
        if sc >= 80:
            st.balloons()
            st.success("🏆 יום מעולה!")
        elif sc >= 60:
            st.success("👍 יום טוב!")
        else:
            st.info("💪 מחר יום חדש!")

def history_screen(data):
    st.markdown("## 📅 היסטוריה")

    if not data["logs"]:
        st.info("אין נתונים")
        return

    st.metric("רצף", f"{streak(data)} ימים")

    days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    for d in sorted(data["logs"].keys(), reverse=True)[:14]:
        log = data["logs"][d]
        sc = score(log)
        dt = datetime.strptime(d, "%Y-%m-%d")

        icon = "🏆" if sc >= 80 else "✅" if sc >= 60 else "⚠️"
        treat = " 🎉" if log.get("treat") else ""

        with st.expander(f"{icon} {days[dt.weekday()]} {dt.strftime('%d/%m')} - {sc}%{treat}"):
            c1, c2 = st.columns(2)
            c1.markdown(f"💧 {log.get('water', 0)} ליטר")
            c1.markdown(f"🥗 {'✓' if log.get('veggies') else '✗'}")
            c2.markdown(f"🍗 {'✓' if log.get('protein') else '✗'}")
            c2.markdown(f"🥑 {log.get('fats', 0)} כפות")

def info_screen():
    st.markdown("## 📚 מידע")

    st.markdown("### 🥗 ירקות מנקים")
    st.markdown(VEGGIES)
    st.caption("❌ לא נחשבים: תפו״א, בטטה, סלק, תירס, קטניות")

    st.markdown("---")
    st.markdown("### 🥑 מנות שומן")
    st.markdown("• 1 כף שמן/חמאה/טחינה = 1\n• חצי אבוקדו = 1\n• 15 זיתים = 1")

    st.markdown("---")
    st.markdown("### 🍷 אלכוהול")
    st.markdown("כוס יין יבש או 1/3 בירה ליום")

    st.markdown("---")
    st.markdown("### 🛤️ מסלולים")
    for k, v in TRACKS.items():
        with st.expander(f"{v['icon']} {v['name']}"):
            st.markdown(f"**פחמימות:** {v['carbs']}")
            st.markdown(f"**פינוקים:** {v['treats']}")

def settings_screen(data):
    st.markdown("## ⚙️ הגדרות")

    # Theme toggle at top of settings
    st.markdown("### 🎨 ערכת נושא")
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("☀️ בהיר", use_container_width=True, type="primary" if st.session_state.theme == "light" else "secondary"):
            st.session_state.theme = "light"
            data["settings"]["theme"] = "light"
            save_data(data)
            st.rerun()
    with theme_col2:
        if st.button("🌙 כהה", use_container_width=True, type="primary" if st.session_state.theme == "dark" else "secondary"):
            st.session_state.theme = "dark"
            data["settings"]["theme"] = "dark"
            save_data(data)
            st.rerun()

    st.markdown("---")

    s = data["settings"]
    day, week = calc_day_week(s.get("start_date", today()))

    c1, c2 = st.columns(2)
    c1.metric("יום", day)
    c2.metric("שבוע", f"{week}/13")

    st.markdown("---")

    name = st.text_input("שם", value=s.get("name", ""))
    start = st.date_input("תאריך התחלה", value=datetime.strptime(s["start_date"], "%Y-%m-%d") if s.get("start_date") else datetime.now())

    if week >= 9:
        track = st.radio("מסלול", list(TRACKS.keys()), index=list(TRACKS.keys()).index(s.get("track") or "fast"), format_func=lambda x: TRACKS[x]["name"], horizontal=True)
    else:
        track = None

    if st.button("💾 שמור"):
        s["name"] = name
        s["start_date"] = start.strftime("%Y-%m-%d")
        if track:
            s["track"] = track
        save_data(data)
        st.success("נשמר!")
        st.rerun()

    st.markdown("---")
    if st.button("🚪 התנתק"):
        st.session_state.auth = False
        st.rerun()

# ===== MAIN =====
def main():
    if not auth():
        return

    if "data" not in st.session_state:
        st.session_state.data = load_data()
        # Sync theme from saved data
        saved_theme = st.session_state.data.get("settings", {}).get("theme", "light")
        if saved_theme != st.session_state.theme:
            st.session_state.theme = saved_theme
            st.rerun()

    data = st.session_state.data

    if not data["settings"].get("start_date"):
        render_theme_toggle()
        onboarding(data)
        return

    render_theme_toggle()

    tabs = st.tabs(["📊 היום", "📅 היסטוריה", "📚 מידע", "⚙️"])

    with tabs[0]:
        main_screen(data)
    with tabs[1]:
        history_screen(data)
    with tabs[2]:
        info_screen()
    with tabs[3]:
        settings_screen(data)

if __name__ == "__main__":
    main()
