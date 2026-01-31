"""
The Leptin Method - שיטת הלפטין
Modern 2026 UI - Masculine Design
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

# ===== 2026 MODERN UI - MASCULINE PALETTE =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800;900&display=swap');

/* === COLOR SYSTEM - Masculine & High Contrast === */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: #1a1a24;
    --bg-elevated: #222230;

    --accent-primary: #00d4aa;
    --accent-secondary: #00a896;
    --accent-tertiary: #05668d;

    --text-primary: #ffffff;
    --text-secondary: #a0a0b0;
    --text-muted: #606070;

    --success: #00d4aa;
    --warning: #f4a261;
    --error: #ef476f;
    --info: #118ab2;

    --border: rgba(255,255,255,0.08);
    --shadow: 0 4px 24px rgba(0,0,0,0.4);
}

/* === GLOBAL === */
* {
    font-family: 'Heebo', -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
}

/* RTL */
.stApp, .stMarkdown, p, span, label, div, h1, h2, h3, h4, h5, h6 {
    direction: rtl;
    text-align: right;
}

/* Hide Streamlit defaults */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    padding: 1rem 1rem 3rem 1rem !important;
    max-width: 100% !important;
}

/* === TYPOGRAPHY === */
h1, h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}

h2 {
    font-size: 1.5rem !important;
    margin-bottom: 0.5rem !important;
}

h3 {
    font-size: 1.2rem !important;
    color: var(--text-secondary) !important;
}

p, span, label {
    color: var(--text-secondary);
    line-height: 1.6;
}

/* === CARDS === */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem;
    text-align: center;
}

/* === BUTTONS === */
.stButton > button {
    width: 100%;
    min-height: 52px;
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%) !important;
    color: var(--bg-primary) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(0, 212, 170, 0.3);
    transition: all 0.2s ease;
    text-shadow: none;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0, 212, 170, 0.4);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Secondary buttons (in columns) */
div[data-testid="column"] .stButton > button {
    background: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    box-shadow: none;
    border: 1px solid var(--border) !important;
}

div[data-testid="column"] .stButton > button:hover {
    background: var(--bg-card) !important;
    border-color: var(--accent-primary) !important;
}

/* === INPUTS === */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.875rem 1rem !important;
    font-size: 1rem !important;
    min-height: 52px !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--text-muted) !important;
}

/* === SLIDERS === */
.stSlider > div > div > div {
    background: var(--bg-elevated) !important;
}

.stSlider [data-baseweb="slider"] > div {
    background: var(--bg-elevated) !important;
}

.stSlider [data-baseweb="slider"] > div > div {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
}

.stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
    color: var(--text-primary) !important;
    font-weight: 600;
}

.stSlider [role="slider"] {
    background: var(--accent-primary) !important;
    border: 3px solid var(--bg-primary) !important;
    box-shadow: var(--shadow);
}

/* === CHECKBOXES === */
.stCheckbox {
    padding: 0.25rem 0;
}

.stCheckbox > label {
    background: var(--bg-card) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    margin: 0.25rem 0;
    min-height: 56px;
    display: flex !important;
    align-items: center !important;
    transition: all 0.2s ease;
    cursor: pointer;
}

.stCheckbox > label:hover {
    border-color: rgba(0, 212, 170, 0.3) !important;
    background: var(--bg-elevated) !important;
}

.stCheckbox > label:has(input:checked) {
    border-color: var(--accent-primary) !important;
    background: rgba(0, 212, 170, 0.08) !important;
}

.stCheckbox > label > span {
    color: var(--text-primary) !important;
    font-size: 0.95rem;
}

/* Checkbox icon */
.stCheckbox [data-testid="stCheckbox"] > div:first-child {
    background: var(--bg-elevated) !important;
    border: 2px solid var(--text-muted) !important;
    border-radius: 6px;
}

.stCheckbox > label:has(input:checked) [data-testid="stCheckbox"] > div:first-child {
    background: var(--accent-primary) !important;
    border-color: var(--accent-primary) !important;
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border-radius: 14px;
    padding: 6px;
    gap: 4px;
    border: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-weight: 500;
    border-radius: 10px;
    padding: 0.625rem 0.75rem;
    font-size: 0.9rem;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: var(--bg-elevated);
}

.stTabs [aria-selected="true"] {
    background: var(--accent-primary) !important;
    color: var(--bg-primary) !important;
    font-weight: 700 !important;
}

/* === METRICS === */
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 1.75rem !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    font-weight: 500;
}

div[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
}

/* === PROGRESS BAR === */
.stProgress > div > div > div {
    background: var(--bg-elevated) !important;
    border-radius: 8px;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent-tertiary), var(--accent-primary)) !important;
    border-radius: 8px;
}

/* === EXPANDER === */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-weight: 600;
    padding: 0.875rem 1rem;
}

.streamlit-expanderHeader:hover {
    border-color: var(--accent-primary) !important;
}

.streamlit-expanderContent {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    padding: 1rem;
}

/* === ALERTS === */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
}

div[data-baseweb="notification"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

.stSuccess {
    background: rgba(0, 212, 170, 0.1) !important;
    border-right: 4px solid var(--success) !important;
}

.stInfo {
    background: rgba(17, 138, 178, 0.1) !important;
    border-right: 4px solid var(--info) !important;
}

.stWarning {
    background: rgba(244, 162, 97, 0.1) !important;
    border-right: 4px solid var(--warning) !important;
}

.stError {
    background: rgba(239, 71, 111, 0.1) !important;
    border-right: 4px solid var(--error) !important;
}

/* === DIVIDERS === */
hr {
    border: none;
    height: 1px;
    background: var(--border);
    margin: 1.5rem 0;
}

/* === DATE INPUT === */
.stDateInput > div > div > input {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
}

/* === RADIO === */
.stRadio > div {
    gap: 0.5rem;
}

.stRadio > div > label {
    background: var(--bg-card) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.875rem 1rem !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease;
}

.stRadio > div > label:hover {
    border-color: var(--accent-primary) !important;
}

.stRadio > div > label[data-checked="true"] {
    border-color: var(--accent-primary) !important;
    background: rgba(0, 212, 170, 0.08) !important;
}

/* === CUSTOM CLASSES === */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 1rem 0 0.75rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.stat-highlight {
    color: var(--accent-primary);
    font-weight: 800;
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}

::-webkit-scrollbar-thumb {
    background: var(--bg-elevated);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}
</style>
""", unsafe_allow_html=True)

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
def load_data():
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")
        if not token or not gist_id:
            return {"settings": {"start_date": None, "track": None, "name": ""}, "logs": {}}
        headers = {"Authorization": f"token {token}"}
        r = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers, timeout=10)
        if r.ok and "leptin_data.json" in r.json().get("files", {}):
            return json.loads(r.json()["files"]["leptin_data.json"]["content"])
    except:
        pass
    return {"settings": {"start_date": None, "track": None, "name": ""}, "logs": {}}

def save_data(data):
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")
        if not token:
            return
        headers = {"Authorization": f"token {token}"}
        payload = {"files": {"leptin_data.json": {"content": json.dumps(data, ensure_ascii=False)}}}
        if gist_id:
            requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=payload, timeout=10)
        else:
            payload["public"] = False
            r = requests.post("https://api.github.com/gists", headers=headers, json=payload, timeout=10)
            if r.status_code == 201:
                st.toast(f"GIST_ID: {r.json()['id']}")
    except:
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
        data["logs"][t] = {"water": 0, "water_before": 0, "veggies": False, "protein": False, "window": 0, "fats": 0, "treat": False, "slip": False}
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

    # Header
    st.markdown(f"## שלום {s.get('name', '')} 👋")
    st.caption(f"{w['icon']} {w['title']}")

    # Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("ציון", f"{sc}%")
    c2.metric("רצף", f"{st_count}")
    c3.metric("יום", f"{day}")

    st.progress(sc / 100)

    # Tip
    import random
    st.info(f"💡 {random.choice(TIPS)}")

    st.markdown("---")

    # Focus
    st.markdown(f"### 🎯 {w['focus']}")

    st.markdown("---")

    # WATER
    st.markdown("#### 💧 מים")
    water = st.slider("ליטרים", 0.0, 6.0, float(log.get("water", 0)), 0.5, label_visibility="collapsed")
    if water != log.get("water"):
        log["water"] = water
        save_data(data)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("➖", key="w-"):
            log["water_before"] = max(0, log.get("water_before", 0) - 1)
            save_data(data)
            st.rerun()
    with col2:
        wb = log.get("water_before", 0)
        st.markdown(f"**לפני ארוחה: {wb}/3** {'✓' if wb >= 3 else ''}")
    with col3:
        if st.button("➕", key="w+"):
            log["water_before"] = min(6, log.get("water_before", 0) + 1)
            save_data(data)
            st.rerun()

    st.markdown("---")

    # NUTRITION
    st.markdown("#### 🥗 תזונה")

    veg = st.checkbox("50% ירקות מנקים ב-2 ארוחות", value=log.get("veggies", False))
    if veg != log.get("veggies"):
        log["veggies"] = veg
        save_data(data)

    prot = st.checkbox("חלבון בכל ארוחה", value=log.get("protein", False))
    if prot != log.get("protein"):
        log["protein"] = prot
        save_data(data)

    with st.expander("רשימת ירקות מנקים"):
        st.markdown(VEGGIES)
        st.caption("❌ לא: תפו״א, בטטה, סלק, תירס, קטניות")

    st.markdown("---")

    # TIMING
    st.markdown("#### ⏰ תזמון")
    win = st.slider("חלון אכילה (שעות)", 0, 16, log.get("window", 0), label_visibility="collapsed")
    if win != log.get("window"):
        log["window"] = win
        save_data(data)

    if win > 0:
        if win <= 10:
            st.success(f"חלון {win} שעות - מצוין")
        elif win <= 12:
            st.info(f"חלון {win} שעות - טוב")
        else:
            st.warning(f"חלון {win} שעות - נסה לקצר")

    st.markdown("---")

    # FATS
    st.markdown("#### 🥑 שומנים")
    fc1, fc2, fc3 = st.columns([1, 2, 1])
    with fc1:
        if st.button("➖", key="f-"):
            log["fats"] = max(0, log.get("fats", 0) - 1)
            save_data(data)
            st.rerun()
    with fc2:
        f = log.get("fats", 0)
        color = "stat-highlight" if f <= 3 else ""
        st.markdown(f"**{f} כפות** {'✓' if f <= 3 else '⚠️'}")
    with fc3:
        if st.button("➕", key="f+"):
            log["fats"] = log.get("fats", 0) + 1
            save_data(data)
            st.rerun()

    st.caption("מקסימום 2-3 כפות (שמן, טחינה, אבוקדו)")

    st.markdown("---")

    # WEEKLY RULES
    st.markdown("#### 📋 הנחיות השבוע")
    for inst in w["instructions"]:
        st.markdown(f"• {inst}")

    with st.expander("✅ מותר"):
        st.markdown(w["allowed"])

    with st.expander("🚫 אסור"):
        st.markdown(w["forbidden"])

    if w.get("treat"):
        with st.expander("🎉 פינוק"):
            st.markdown(w["treat"])

    # TRACK (week 9+)
    if week >= 9:
        st.markdown("---")
        st.markdown("#### 🛤️ מסלול")
        track = s.get("track")
        if not track:
            track = st.radio("בחר:", list(TRACKS.keys()), format_func=lambda x: f"{TRACKS[x]['icon']} {TRACKS[x]['name']}", horizontal=True)
            if st.button("שמור מסלול"):
                s["track"] = track
                save_data(data)
                st.rerun()
        else:
            t = TRACKS[track]
            st.markdown(f"**{t['icon']} {t['name']}** | {t['carbs']} | {t['treats']}")

    st.markdown("---")

    # TREAT & SLIP
    treat = st.checkbox("🎉 יום פינוק", value=log.get("treat", False))
    if treat != log.get("treat"):
        log["treat"] = treat
        save_data(data)

    if week >= 3 and not treat:
        slip = st.checkbox("⚠️ אכלתי אסור", value=log.get("slip", False))
        if slip != log.get("slip"):
            log["slip"] = slip
            save_data(data)

    # RESCUE
    if sc < 60 or log.get("slip"):
        st.markdown("---")
        st.warning("🆘 גלגלי הצלה")
        r1, r2, r3 = st.columns(3)
        if r1.button("💧 מים"):
            st.success("הוסף 1-2 ליטר")
        if r2.button("🥗 ירקות"):
            st.success("הגדל 50%")
        if r3.button("⏰ דחייה"):
            st.success("מחר דחה ארוחה")

    # TIPS
    if w.get("tips"):
        st.markdown("---")
        st.markdown("#### 💡 טיפים")
        for tip in w["tips"]:
            st.markdown(f"• {tip}")

    # COMPLETE
    st.markdown("---")
    if st.button("✅ סיום יום"):
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

    data = st.session_state.data

    if not data["settings"].get("start_date"):
        onboarding(data)
        return

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
