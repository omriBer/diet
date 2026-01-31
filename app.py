"""
The Leptin Method - שיטת הלפטין
Modern Hebrew Weight Loss Tracking Application
Redesigned for Android touch screens with psychology-driven UX
"""

import streamlit as st
import json
import requests
from datetime import datetime, timedelta
import math

# Page config
st.set_page_config(
    page_title="שיטת הלפטין",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== MODERN CSS DESIGN =====
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800&display=swap');

    /* Root variables - Masculine color scheme */
    :root {
        --primary: #1a1a2e;
        --secondary: #16213e;
        --accent: #0f3460;
        --highlight: #e94560;
        --success: #00d9a5;
        --warning: #ffc107;
        --water: #00b4d8;
        --veggie: #52b788;
        --protein: #ff6b35;
        --gradient-dark: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        --gradient-accent: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
        --gradient-success: linear-gradient(135deg, #00d9a5 0%, #00b894 100%);
        --gradient-water: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%);
        --card-bg: rgba(255,255,255,0.05);
        --text-primary: #ffffff;
        --text-secondary: rgba(255,255,255,0.7);
    }

    /* Global styles */
    .stApp {
        background: var(--gradient-dark);
        font-family: 'Heebo', sans-serif;
    }

    /* RTL Support */
    .stApp, .stMarkdown, div[data-testid="stMarkdownContainer"], p, h1, h2, h3, h4, label {
        direction: rtl;
        text-align: right;
        color: var(--text-primary);
    }

    /* Hide default elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Main container */
    .main .block-container {
        padding: 0.5rem 1rem 2rem 1rem;
        max-width: 100%;
    }

    /* Zone cards */
    .zone-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .zone-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    .zone-icon {
        font-size: 2rem;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        background: var(--card-bg);
    }

    .zone-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
        color: var(--text-primary);
    }

    .zone-subtitle {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin: 0;
    }

    /* Hero header */
    .hero-header {
        background: var(--gradient-accent);
        border-radius: 25px;
        padding: 1.5rem;
        margin: 0 0 1rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    }

    .hero-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        color: white;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
    }

    /* Day badge */
    .day-badge {
        display: inline-block;
        background: rgba(0,0,0,0.3);
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-weight: 600;
        margin-top: 0.75rem;
    }

    /* Progress ring */
    .progress-ring-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        padding: 1rem 0;
    }

    .progress-ring {
        position: relative;
        width: 120px;
        height: 120px;
    }

    .progress-ring svg {
        transform: rotate(-90deg);
    }

    .progress-ring-circle {
        fill: none;
        stroke: rgba(255,255,255,0.1);
        stroke-width: 8;
    }

    .progress-ring-progress {
        fill: none;
        stroke-width: 8;
        stroke-linecap: round;
        transition: stroke-dashoffset 0.5s ease;
    }

    .progress-ring-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }

    .progress-ring-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
    }

    .progress-ring-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }

    /* Touch-friendly buttons */
    .stButton > button {
        width: 100%;
        min-height: 56px;
        padding: 0.875rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Heebo', sans-serif;
        border-radius: 16px;
        border: none;
        background: var(--gradient-accent);
        color: white;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
        transition: all 0.3s ease;
        touch-action: manipulation;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.5);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Counter buttons */
    .counter-btn {
        min-width: 60px !important;
        min-height: 60px !important;
        border-radius: 50% !important;
        font-size: 1.5rem !important;
        padding: 0 !important;
    }

    /* Metric display */
    .metric-display {
        text-align: center;
        padding: 1rem;
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: var(--gradient-water);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-unit {
        font-size: 1rem;
        color: var(--text-secondary);
    }

    .metric-target {
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    /* Checklist items */
    .check-item {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 70px;
    }

    .check-item.completed {
        border-color: var(--success);
        background: rgba(0, 217, 165, 0.1);
    }

    .check-icon {
        font-size: 1.5rem;
        width: 45px;
        height: 45px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--card-bg);
        flex-shrink: 0;
    }

    .check-content {
        flex: 1;
    }

    .check-title {
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
        color: var(--text-primary);
    }

    .check-desc {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin: 0.25rem 0 0 0;
    }

    .check-status {
        font-size: 1.5rem;
    }

    /* Psychology tip box */
    .psych-tip {
        background: linear-gradient(135deg, rgba(233, 69, 96, 0.2) 0%, rgba(255, 107, 107, 0.1) 100%);
        border-radius: 16px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border-right: 4px solid var(--highlight);
    }

    .psych-tip-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: var(--highlight);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .psych-tip-text {
        font-size: 0.9rem;
        color: var(--text-primary);
        line-height: 1.5;
    }

    /* Phase indicator */
    .phase-indicator {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 0.5rem 0;
    }

    .phase-progress {
        display: flex;
        gap: 4px;
        flex: 1;
        margin: 0 1rem;
    }

    .phase-dot {
        flex: 1;
        height: 8px;
        border-radius: 4px;
        background: rgba(255,255,255,0.1);
    }

    .phase-dot.active {
        background: var(--gradient-accent);
    }

    .phase-dot.completed {
        background: var(--success);
    }

    /* Infographic stats */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin: 1rem 0;
    }

    .stat-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
    }

    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: white;
    }

    .stat-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }

    /* Login screen */
    .login-container {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 2rem;
    }

    .login-logo {
        text-align: center;
        margin-bottom: 2rem;
    }

    .login-logo-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .login-title {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin: 0;
    }

    .login-subtitle {
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }

    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background: var(--card-bg) !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        min-height: 56px !important;
        font-family: 'Heebo', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--highlight) !important;
        box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2) !important;
    }

    /* Checkbox styling */
    .stCheckbox {
        padding: 0.75rem 0;
    }

    .stCheckbox > label {
        min-height: 56px;
        display: flex;
        align-items: center;
        padding: 0.5rem 1rem;
        background: var(--card-bg);
        border-radius: 16px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }

    .stCheckbox > label:hover {
        background: rgba(255,255,255,0.08);
    }

    .stCheckbox > label > div[data-testid="stCheckbox"] > div:first-child {
        transform: scale(1.3);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: var(--text-secondary);
        font-weight: 600;
        padding: 0.75rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        background: var(--gradient-accent) !important;
        color: white !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--card-bg);
        border-radius: 16px;
        font-weight: 600;
    }

    /* Rescue wheel */
    .rescue-card {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 152, 0, 0.1) 100%);
        border: 2px solid var(--warning);
        border-radius: 20px;
        padding: 1.25rem;
        margin: 0.75rem 0;
    }

    .rescue-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--warning);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .rescue-actions {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .rescue-action {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .rescue-action:hover {
        background: rgba(255,255,255,0.1);
    }

    /* Streamer animation */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }

    .pulse-animation {
        animation: pulse 2s infinite;
    }

    /* Success celebration */
    .success-celebration {
        background: var(--gradient-success);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }

    .success-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .success-text {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ===== GITHUB GIST STORAGE =====

def get_gist_data():
    """Load data from GitHub Gist"""
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")

        if not token or not gist_id:
            return get_default_data()

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(
            f"https://api.github.com/gists/{gist_id}",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            gist = response.json()
            if "leptin_data.json" in gist["files"]:
                content = gist["files"]["leptin_data.json"]["content"]
                return json.loads(content)

        return get_default_data()
    except Exception:
        return get_default_data()


def save_gist_data(data):
    """Save data to GitHub Gist"""
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")

        if not token:
            return False

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        payload = {
            "description": "Leptin Method Tracker Data",
            "files": {
                "leptin_data.json": {
                    "content": json.dumps(data, ensure_ascii=False, indent=2)
                }
            }
        }

        if gist_id:
            response = requests.patch(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers,
                json=payload,
                timeout=10
            )
        else:
            payload["public"] = False
            response = requests.post(
                "https://api.github.com/gists",
                headers=headers,
                json=payload,
                timeout=10
            )
            if response.status_code == 201:
                new_gist_id = response.json()["id"]
                st.info(f"GIST_ID חדש: {new_gist_id}")

        return response.status_code in [200, 201]
    except Exception:
        return False


def get_default_data():
    """Return default data structure"""
    return {
        "user_settings": {
            "start_date": None,
            "track": None,
            "name": ""
        },
        "daily_logs": {}
    }


# ===== HELPER FUNCTIONS =====

CLEANING_VEGGIES = ["מלפפון", "עגבנייה", "בצל", "פטריות", "כרובית", "כרוב", "ברוקולי", "שעועית ירוקה", "קישוא", "חסה", "תרד"]

PSYCHOLOGY_TIPS = {
    "water": [
        "מים הם הדלק של הגוף. כל כוס מקרבת אותך להצלחה.",
        "שתייה לפני אוכל = שליטה מלאה. אתה בוחר.",
        "הגוף שלך צועק למים. תן לו מה שהוא צריך."
    ],
    "veggies": [
        "ירקות = נשק סודי. הם עובדים בשבילך 24/7.",
        "50% ירקות = 100% שליטה על הרעב.",
        "כל ירק שאתה אוכל משנה את ההורמונים לטובתך."
    ],
    "general": [
        "היום הזה לא יחזור. תעשה אותו נכון.",
        "אתה לא צריך להיות מושלם. רק עקבי.",
        "כל יום שאתה עומד ביעדים - הגוף משתנה.",
        "ההצלחה שלך נבנית מהחלטות קטנות."
    ],
    "streak": [
        "רצף של {} ימים! המומנטום בצד שלך.",
        "יום {} ברצף - ההרגלים נבנים.",
        "כבר {} ימים. אל תשבור את הרצף!"
    ]
}


def get_today_key():
    return datetime.now().strftime("%Y-%m-%d")


def calculate_program_day(start_date_str):
    """Calculate current day and week from start date"""
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = (today - start).days + 1
        week = min(13, max(1, (delta - 1) // 7 + 1))
        day_in_week = ((delta - 1) % 7) + 1
        return delta, week, day_in_week
    except:
        return 1, 1, 1


def get_phase(week):
    if week <= 2:
        return "flood", "ההצפה", "🌊"
    elif week <= 7:
        return "cleanse", "הניקוי", "✨"
    elif week == 8:
        return "transition", "מעבר", "🔄"
    else:
        return "tracks", "המסלולים", "🎯"


def init_daily_log(data):
    today = get_today_key()
    if today not in data["daily_logs"]:
        data["daily_logs"][today] = {
            "water_liters": 0,
            "water_before_meals": 0,
            "veggies_50_percent": False,
            "protein_every_meal": False,
            "eating_window_hours": 0,
            "fats_count": 0,
            "treat_day": False,
            "forbidden_food": False,
            "notes": "",
            "completed": False
        }
    return data


def calculate_score(log):
    """Calculate daily score out of 100"""
    score = 0

    # Water (35 points)
    water = log.get("water_liters", 0)
    if water >= 2:
        score += 15
    if water >= 3:
        score += 10
    if water >= 4:
        score += 5
    if log.get("water_before_meals", 0) >= 3:
        score += 5

    # Veggies (25 points)
    if log.get("veggies_50_percent"):
        score += 25

    # Protein (20 points)
    if log.get("protein_every_meal"):
        score += 20

    # Fats limit (10 points)
    if log.get("fats_count", 0) <= 3:
        score += 10

    # Eating window (10 points)
    if 0 < log.get("eating_window_hours", 0) <= 12:
        score += 10

    # Penalty for forbidden food
    if log.get("forbidden_food") and not log.get("treat_day"):
        score -= 15

    return max(0, min(100, score))


def get_streak(data):
    """Calculate current streak of good days"""
    logs = data.get("daily_logs", {})
    streak = 0
    today = datetime.now()

    for i in range(30):
        check_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        if check_date in logs:
            if calculate_score(logs[check_date]) >= 70:
                streak += 1
            else:
                break
        else:
            break

    return streak


def get_random_tip(category):
    """Get a random psychology tip"""
    import random
    tips = PSYCHOLOGY_TIPS.get(category, PSYCHOLOGY_TIPS["general"])
    return random.choice(tips)


# ===== AUTHENTICATION =====

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div class="login-container">
        <div class="login-logo">
            <div class="login-logo-icon">🔥</div>
            <h1 class="login-title">שיטת הלפטין</h1>
            <p class="login-subtitle">המסע שלך להצלחה מתחיל כאן</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input("", type="password", placeholder="הזן סיסמה", label_visibility="collapsed")

    if st.button("כניסה", use_container_width=True):
        if password == st.secrets.get("PASSWORD", "leptin2024"):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("סיסמה שגויה")

    return False


# ===== UI COMPONENTS =====

def render_progress_ring(value, max_value, label, color="#e94560"):
    """Render a circular progress indicator"""
    percentage = min(100, (value / max_value) * 100) if max_value > 0 else 0
    circumference = 2 * math.pi * 52
    offset = circumference - (percentage / 100) * circumference

    return f"""
    <div class="progress-ring">
        <svg width="120" height="120">
            <circle class="progress-ring-circle" cx="60" cy="60" r="52"/>
            <circle class="progress-ring-progress" cx="60" cy="60" r="52"
                stroke="{color}"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{offset}"/>
        </svg>
        <div class="progress-ring-text">
            <div class="progress-ring-value">{int(percentage)}%</div>
            <div class="progress-ring-label">{label}</div>
        </div>
    </div>
    """


def render_zone_header(icon, title, subtitle=""):
    """Render a zone section header"""
    return f"""
    <div class="zone-header">
        <div class="zone-icon">{icon}</div>
        <div>
            <h3 class="zone-title">{title}</h3>
            <p class="zone-subtitle">{subtitle}</p>
        </div>
    </div>
    """


def render_psych_tip(tip):
    """Render a psychology tip box"""
    return f"""
    <div class="psych-tip">
        <div class="psych-tip-title">🧠 תזכורת מנטלית</div>
        <div class="psych-tip-text">{tip}</div>
    </div>
    """


def render_check_item(icon, title, desc, is_completed):
    """Render a checklist item"""
    status = "completed" if is_completed else ""
    check = "✓" if is_completed else "○"
    return f"""
    <div class="check-item {status}">
        <div class="check-icon">{icon}</div>
        <div class="check-content">
            <p class="check-title">{title}</p>
            <p class="check-desc">{desc}</p>
        </div>
        <div class="check-status">{check}</div>
    </div>
    """


# ===== SCREENS =====

def show_onboarding(data):
    """Show onboarding for new users"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🔥 שיטת הלפטין</h1>
        <p class="hero-subtitle">91 ימים שישנו לך את החיים</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="zone-card">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">בוא נתחיל את המסע</h3>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("השם שלך", placeholder="איך לקרוא לך?")

    st.markdown("##### מתי התחלת את התוכנית?")
    start_date = st.date_input(
        "תאריך התחלה",
        value=datetime.now(),
        max_value=datetime.now(),
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="psych-tip">
        <div class="psych-tip-title">💡 למה תאריך התחלה?</div>
        <div class="psych-tip-text">האפליקציה תחשב אוטומטית באיזה יום ושבוע אתה, ותתאים את הכללים בהתאם לשלב שלך בתוכנית.</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 יאללה, מתחילים!", use_container_width=True):
        data["user_settings"]["name"] = name or "אלוף"
        data["user_settings"]["start_date"] = start_date.strftime("%Y-%m-%d")
        save_gist_data(data)
        st.session_state["app_data"] = data
        st.rerun()


def show_daily_tracking(data):
    """Main daily tracking interface"""
    settings = data["user_settings"]
    start_date = settings.get("start_date")
    name = settings.get("name", "אלוף")

    program_day, week, day_in_week = calculate_program_day(start_date)
    phase_id, phase_name, phase_icon = get_phase(week)

    today = get_today_key()
    data = init_daily_log(data)
    log = data["daily_logs"][today]

    score = calculate_score(log)
    streak = get_streak(data)

    # Hero Header
    st.markdown(f"""
    <div class="hero-header">
        <h1 class="hero-title">שלום, {name}!</h1>
        <p class="hero-subtitle">{phase_icon} שלב {phase_name}</p>
        <div class="day-badge">יום {program_day} | שבוע {week}</div>
    </div>
    """, unsafe_allow_html=True)

    # Progress Overview
    st.markdown(f"""
    <div class="zone-card">
        <div class="progress-ring-container">
            {render_progress_ring(score, 100, "ציון יומי", "#e94560")}
            {render_progress_ring(week, 13, "שבועות", "#00d9a5")}
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-value">{streak}</div>
                <div class="stat-label">ימים ברצף</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-value">{program_day}/91</div>
                <div class="stat-label">ימים בתוכנית</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Psychology tip
    if streak > 0:
        tip = PSYCHOLOGY_TIPS["streak"][streak % 3].format(streak)
    else:
        tip = get_random_tip("general")
    st.markdown(render_psych_tip(tip), unsafe_allow_html=True)

    # ===== ZONE 1: WATER =====
    st.markdown(f"""
    <div class="zone-card">
        {render_zone_header("💧", "הצפת הלפטין", "2-4 ליטר + 2 כוסות לפני כל ארוחה")}
        <div class="metric-display">
            <div class="metric-value">{log.get('water_liters', 0)}</div>
            <div class="metric-unit">ליטר</div>
            <div class="metric-target">יעד: 3-4 ליטר</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    wcol1, wcol2, wcol3 = st.columns([1, 2, 1])
    with wcol1:
        if st.button("➖", key="water_minus", use_container_width=True):
            log["water_liters"] = max(0, log.get("water_liters", 0) - 0.5)
            save_gist_data(data)
            st.rerun()
    with wcol2:
        water_val = st.slider("מים", 0.0, 6.0, float(log.get("water_liters", 0)), 0.5,
                             label_visibility="collapsed", key="water_slider")
        if water_val != log.get("water_liters"):
            log["water_liters"] = water_val
            save_gist_data(data)
    with wcol3:
        if st.button("➕", key="water_plus", use_container_width=True):
            log["water_liters"] = min(6, log.get("water_liters", 0) + 0.5)
            save_gist_data(data)
            st.rerun()

    # Water before meals counter
    st.markdown("**2 כוסות לפני ארוחה:**")
    wm_col1, wm_col2, wm_col3 = st.columns([1, 2, 1])
    with wm_col1:
        if st.button("➖", key="wm_minus"):
            log["water_before_meals"] = max(0, log.get("water_before_meals", 0) - 1)
            save_gist_data(data)
            st.rerun()
    with wm_col2:
        wm_count = log.get("water_before_meals", 0)
        st.markdown(f"<h3 style='text-align:center'>{wm_count} / 3 ארוחות</h3>", unsafe_allow_html=True)
    with wm_col3:
        if st.button("➕", key="wm_plus"):
            log["water_before_meals"] = min(6, log.get("water_before_meals", 0) + 1)
            save_gist_data(data)
            st.rerun()

    # ===== ZONE 2: NUTRITION =====
    st.markdown(f"""
    <div class="zone-card">
        {render_zone_header("🥗", "תזונה", "ירקות מנקים + חלבון")}
    </div>
    """, unsafe_allow_html=True)

    veggies = st.checkbox(
        "🥒 אכלתי 50% ירקות מנקים לפחות ב-2 ארוחות",
        value=log.get("veggies_50_percent", False),
        key="veggies_check"
    )
    if veggies != log.get("veggies_50_percent"):
        log["veggies_50_percent"] = veggies
        save_gist_data(data)

    protein = st.checkbox(
        "🍗 כללתי חלבון בכל ארוחה",
        value=log.get("protein_every_meal", False),
        key="protein_check"
    )
    if protein != log.get("protein_every_meal"):
        log["protein_every_meal"] = protein
        save_gist_data(data)

    with st.expander("📋 ירקות מנקים"):
        st.markdown(", ".join(CLEANING_VEGGIES))
        st.markdown("**לא נכללים:** תפו״א, בטטה, גזר מבושל")

    # ===== ZONE 3: TIMING & FATS =====
    st.markdown(f"""
    <div class="zone-card">
        {render_zone_header("⏰", "תזמון ושומנים", "חלון אכילה + שומנים מרוכזים")}
    </div>
    """, unsafe_allow_html=True)

    # Eating window
    st.markdown("**חלון אכילה (שעות):**")
    ew_hours = st.slider("חלון אכילה", 0, 16, log.get("eating_window_hours", 0),
                         label_visibility="collapsed", key="ew_slider")
    if ew_hours != log.get("eating_window_hours"):
        log["eating_window_hours"] = ew_hours
        save_gist_data(data)

    if ew_hours > 0:
        if ew_hours <= 10:
            st.success(f"✅ חלון {ew_hours} שעות - מצוין!")
        elif ew_hours <= 12:
            st.info(f"👍 חלון {ew_hours} שעות - טוב")
        else:
            st.warning(f"⚠️ חלון {ew_hours} שעות - נסה לקצר")

    # Fats counter
    st.markdown("**שומנים מרוכזים (כפות):**")
    fat_col1, fat_col2, fat_col3 = st.columns([1, 2, 1])
    with fat_col1:
        if st.button("➖", key="fat_minus"):
            log["fats_count"] = max(0, log.get("fats_count", 0) - 1)
            save_gist_data(data)
            st.rerun()
    with fat_col2:
        fats = log.get("fats_count", 0)
        color = "#00d9a5" if fats <= 3 else "#e94560"
        st.markdown(f"<h2 style='text-align:center; color:{color}'>{fats} כפות</h2>", unsafe_allow_html=True)
    with fat_col3:
        if st.button("➕", key="fat_plus"):
            log["fats_count"] = log.get("fats_count", 0) + 1
            save_gist_data(data)
            st.rerun()

    st.caption("טחינה, שמן, אבוקדו - מקסימום 2-3 כפות")

    # ===== ZONE 4: PHASE RULES =====
    st.markdown(f"""
    <div class="zone-card">
        {render_zone_header(phase_icon, f"כללי שלב {phase_name}", f"שבוע {week}")}
    </div>
    """, unsafe_allow_html=True)

    if phase_id == "flood":
        st.markdown("""
        <div class="psych-tip">
            <div class="psych-tip-title">🌊 שלב ההצפה</div>
            <div class="psych-tip-text">
                התמקד במים וירקות בלבד!<br>
                אין הגבלות מזון - רק בונים הרגלים.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif phase_id == "cleanse":
        st.markdown("""
        <div class="psych-tip" style="border-color: #ff6b35;">
            <div class="psych-tip-title" style="color: #ff6b35;">✨ שלב הניקוי - כללים</div>
            <div class="psych-tip-text">
                <strong>🚫 אסור:</strong> סוכר, דבש, קמח, פסטה, אורז, תירס, תפו״א<br>
                <strong>✅ מותר:</strong> עדשים, חומוס, שעועית, קינואה, כוסמת
            </div>
        </div>
        """, unsafe_allow_html=True)

        if not log.get("treat_day"):
            forbidden = st.checkbox("⚠️ אכלתי מזון אסור היום",
                                   value=log.get("forbidden_food", False),
                                   key="forbidden_check")
            if forbidden != log.get("forbidden_food"):
                log["forbidden_food"] = forbidden
                save_gist_data(data)

    elif phase_id == "tracks":
        track = settings.get("track")
        if not track:
            st.markdown("**בחר מסלול:**")
            track = st.radio("מסלול", ["fast", "cleanse", "moderate"],
                           format_func=lambda x: {
                               "fast": "🚀 מהיר - עדשים בלבד",
                               "cleanse": "✨ ניקוי - קטניות + קינואה",
                               "moderate": "🍚 מתון - אורז/תפו״א פעם ביום"
                           }.get(x),
                           label_visibility="collapsed",
                           horizontal=True)
            if st.button("שמור מסלול"):
                settings["track"] = track
                save_gist_data(data)
                st.rerun()

    # Treat day toggle
    st.markdown("---")
    treat = st.checkbox("🎉 יום פינוק", value=log.get("treat_day", False), key="treat_check")
    if treat != log.get("treat_day"):
        log["treat_day"] = treat
        save_gist_data(data)

    if treat:
        st.info("ביום פינוק עדיין חובה: מים + 50% ירקות")

    # ===== RESCUE WHEELS =====
    if score < 60 or log.get("forbidden_food"):
        st.markdown("""
        <div class="rescue-card">
            <div class="rescue-title">🆘 גלגלי הצלה</div>
        </div>
        """, unsafe_allow_html=True)

        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            if st.button("💧 עוד מים", use_container_width=True):
                st.success("הוסף 1-2 ליטר!")
        with rc2:
            if st.button("🥗 עוד ירקות", use_container_width=True):
                st.success("הגדל ב-50%!")
        with rc3:
            if st.button("⏰ דחה ארוחה", use_container_width=True):
                st.success("מחר דחה 1-3 שעות!")

    # ===== COMPLETE DAY =====
    st.markdown("---")
    if st.button("✅ סיים את היום", use_container_width=True):
        log["completed"] = True
        save_gist_data(data)

        if score >= 80:
            st.balloons()
            st.markdown("""
            <div class="success-celebration">
                <div class="success-icon">🏆</div>
                <div class="success-text">יום מעולה! המשך כך!</div>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 60:
            st.success("👍 יום טוב! מחר נשפר עוד קצת")
        else:
            st.info("💪 כל יום חדש הוא הזדמנות. מחר נעשה יותר טוב!")


def show_history(data):
    """Show history view"""
    st.markdown("""
    <div class="zone-card">
        <h2 style="text-align: center;">📅 היסטוריה</h2>
    </div>
    """, unsafe_allow_html=True)

    logs = data.get("daily_logs", {})
    if not logs:
        st.info("אין עדיין היסטוריה")
        return

    # Weekly summary
    start_date = data["user_settings"].get("start_date")
    if start_date:
        _, current_week, _ = calculate_program_day(start_date)

        # Count good days this week
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        good_days = 0
        for i in range(7):
            day_key = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            if day_key in logs and calculate_score(logs[day_key]) >= 70:
                good_days += 1

        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">{good_days}/7</div>
                <div class="stat-label">ימים טובים השבוע</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-value">{get_streak(data)}</div>
                <div class="stat-label">רצף נוכחי</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Daily logs
    sorted_dates = sorted(logs.keys(), reverse=True)[:14]

    for date_str in sorted_dates:
        log = logs[date_str]
        score = calculate_score(log)

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_display = date_obj.strftime("%d/%m")
        day_name = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"][date_obj.weekday()]

        if score >= 80:
            status = "🏆"
        elif score >= 60:
            status = "✅"
        else:
            status = "⚠️"

        treat = " 🎉" if log.get("treat_day") else ""

        with st.expander(f"{status} יום {day_name} ({date_display}) - {score}%{treat}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"💧 מים: {log.get('water_liters', 0)} ליטר")
                st.markdown(f"🥗 ירקות: {'✅' if log.get('veggies_50_percent') else '❌'}")
            with col2:
                st.markdown(f"🍗 חלבון: {'✅' if log.get('protein_every_meal') else '❌'}")
                st.markdown(f"🥑 שומנים: {log.get('fats_count', 0)} כפות")


def show_settings(data):
    """Settings page"""
    st.markdown("""
    <div class="zone-card">
        <h2 style="text-align: center;">⚙️ הגדרות</h2>
    </div>
    """, unsafe_allow_html=True)

    settings = data["user_settings"]

    # Current status
    if settings.get("start_date"):
        program_day, week, _ = calculate_program_day(settings["start_date"])
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-value">יום {program_day}</div>
                <div class="stat-label">בתוכנית</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📆</div>
                <div class="stat-value">שבוע {week}</div>
                <div class="stat-label">מתוך 13</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Edit settings
    new_name = st.text_input("שם", value=settings.get("name", ""))

    new_start = st.date_input(
        "תאריך התחלה",
        value=datetime.strptime(settings["start_date"], "%Y-%m-%d") if settings.get("start_date") else datetime.now()
    )

    if week >= 9:
        new_track = st.radio(
            "מסלול",
            ["fast", "cleanse", "moderate"],
            index=["fast", "cleanse", "moderate"].index(settings.get("track") or "fast"),
            format_func=lambda x: {"fast": "🚀 מהיר", "cleanse": "✨ ניקוי", "moderate": "🍚 מתון"}.get(x),
            horizontal=True
        )
    else:
        new_track = None

    if st.button("💾 שמור שינויים", use_container_width=True):
        settings["name"] = new_name
        settings["start_date"] = new_start.strftime("%Y-%m-%d")
        if new_track:
            settings["track"] = new_track
        save_gist_data(data)
        st.success("נשמר!")
        st.rerun()

    st.markdown("---")

    if st.button("🚪 התנתק", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()


def main():
    """Main app entry point"""

    if not check_password():
        return

    if "app_data" not in st.session_state:
        st.session_state["app_data"] = get_gist_data()

    data = st.session_state["app_data"]

    if not data["user_settings"].get("start_date"):
        show_onboarding(data)
        return

    # Navigation
    tabs = st.tabs(["📊 היום", "📅 היסטוריה", "⚙️ הגדרות"])

    with tabs[0]:
        show_daily_tracking(data)

    with tabs[1]:
        show_history(data)

    with tabs[2]:
        show_settings(data)


if __name__ == "__main__":
    main()
