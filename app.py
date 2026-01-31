"""
The Leptin Method - שיטת הלפטין
Hebrew Weight Loss Tracking App with Knowledge Base
"""

import streamlit as st
import json
import requests
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="שיטת הלפטין",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean CSS - No HTML in markdown
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&display=swap');

:root {
    --bg-dark: #0f0f1a;
    --bg-card: #1a1a2e;
    --accent: #e94560;
    --success: #00d9a5;
    --water: #00b4d8;
    --text: #ffffff;
    --text-dim: rgba(255,255,255,0.6);
}

.stApp {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
}

* {
    font-family: 'Heebo', sans-serif !important;
}

.stApp, .stMarkdown, p, span, label, div {
    direction: rtl;
    text-align: right;
}

#MainMenu, footer, header, .stDeployButton {display: none !important;}

.block-container {
    padding: 1rem !important;
    max-width: 100% !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 54px;
    background: linear-gradient(135deg, #e94560, #ff6b6b) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 4px 15px rgba(233,69,96,0.3);
}

/* Inputs */
input, .stTextInput input, .stNumberInput input {
    background: #1a1a2e !important;
    border: 2px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: white !important;
    min-height: 50px !important;
}

/* Sliders */
.stSlider > div > div {
    background: rgba(255,255,255,0.1) !important;
}

.stSlider [data-baseweb="slider"] div {
    background: #e94560 !important;
}

/* Checkboxes */
.stCheckbox label {
    background: #1a1a2e;
    padding: 1rem;
    border-radius: 12px;
    margin: 0.3rem 0;
    border: 2px solid transparent;
    transition: all 0.2s;
}

.stCheckbox label:has(input:checked) {
    border-color: #00d9a5;
    background: rgba(0,217,165,0.1);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #1a1a2e;
    border-radius: 12px;
    padding: 0.4rem;
}

.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.5);
    border-radius: 10px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #e94560, #ff6b6b) !important;
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #1a1a2e !important;
    border-radius: 12px !important;
}

/* Metrics */
div[data-testid="metric-container"] {
    background: #1a1a2e;
    padding: 1rem;
    border-radius: 12px;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #e94560, #00d9a5) !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===== KNOWLEDGE BASE =====

WEEK_DATA = {
    1: {
        "phase": "הצפה",
        "phase_icon": "🌊",
        "title": "שבוע 1 - הצפת הלפטין",
        "focus": "התחל להגדיל צריכת מים בהדרגה",
        "instructions": [
            "אכול כרגיל ללא שינויים",
            "התחל להגדיל שתיית מים בהדרגה",
            "הימנע מהוספת פירות או ממתיקים למים"
        ],
        "allowed": "כל המזונות מותרים. נוזלים לקווטה: מים, סודה ללא סוכר, תה ללא סוכר",
        "forbidden": "אין הגבלות השבוע",
        "tips": [
            "צפה לעלייה זמנית בביקורי שירותים",
            "השתמש באפליקציית תזכורת מים",
            "צפה בכל התכנים היומיים למוטיבציה"
        ],
        "exercise": "אימון כוח עדיף על אירובי. התמקד בטכניקה לפני עצימות.",
        "treat_rules": None
    },
    2: {
        "phase": "הצפה",
        "phase_icon": "🌊",
        "title": "שבוע 2 - מיקוד בירקות",
        "focus": "סדר אכילה לפטיני: ירקות קודם",
        "instructions": [
            "התחל 'סדר אכילה לפטיני': ירקות ראשונים",
            "מלא 50% משתי הארוחות הגדולות בירקות מנקים",
            "אפשרות: 50% פעם אחת + שייק לפטין"
        ],
        "allowed": "חלבונים: בשר, ביצים, דגים, מוצרי חלב. ירקות: ארטישוק, אספרגוס, בצל, ברוקולי, גזר, כרוב, כרובית, מלפפון, פטריות, פלפל, קישוא, חסה, תרד. שומנים: ללא הגבלה",
        "forbidden": "ירקות שלא נחשבים מנקים: סלק, בטטה, תפו״א, חומוס, שעועית, עדשים, אפונה",
        "tips": [
            "הכן ירקות פעמיים בשבוע (5-10 דקות)",
            "השתמש בירקות קפואים לנוחות",
            "במסעדה - בקש רוטב בצד"
        ],
        "exercise": "תוכנית כוח 3-5 פעמים בשבוע. בצע 5 תרגילי מניעת פציעות (FFF) בין סטים.",
        "treat_rules": None
    },
    3: {
        "phase": "ניקוי",
        "phase_icon": "✨",
        "title": "שבוע 3 - תחילת הניקוי",
        "focus": "חופשה אסטרטגית מסוכר וקמח",
        "instructions": [
            "חופשה מסוכר (לבן/חום, סילאן, מייפל, אגבה)",
            "חופשה מכל סוגי הקמחים (כולל ללא גלוטן/שקדים)",
            "הגבל לפרי אחד ביום"
        ],
        "allowed": "חלבונים: ביצים, דגים, עוף, בשר, מוצרי חלב, טופו, סייטן. ירקות: כל ירקות הניקוי (50% מהארוחה). שומנים: טחינה, חמאה, שמנים, זיתים, אבוקדו. פחמימות: קטניות, קינואה, כוסמת, 4 כפות שיבולת שועל",
        "forbidden": "שוקולד, חטיפי אנרגיה, פירות יבשים, תמרים, מיץ, חלווה, פודינג אינסטנט",
        "tips": [
            "צפה לרעב/חשקים בימים הראשונים",
            "אל תשקול את עצמך - התמקד באיזון הורמונלי",
            "שתף קשיים בצ'אט כדי לשבור בידוד"
        ],
        "exercise": "אימון כוח: 3 סטים של 6-8 חזרות. מנוחה 2-4 דקות בין סטים.",
        "treat_rules": None
    },
    4: {
        "phase": "ניקוי",
        "phase_icon": "✨",
        "title": "שבוע 4 - יום פינוק ראשון",
        "focus": "המשך ניקוי + יום פינוק ראשון",
        "instructions": [
            "המשך כללי שבוע 3",
            "יום פינוק ראשון מוצג השבוע",
            "ההנחיות יינתנו ביום חמישי"
        ],
        "allowed": "חלבונים: ביצים, דגים, עוף, בשר, מוצרי חלב, טופו, סייטן. ירקות: כל ירקות הניקוי. שומנים: טחינה, חמאה, שמנים, זיתים, אבוקדו. פחמימות: קטניות, קינואה, כוסמת, 4 כפות שיבולת שועל",
        "forbidden": "סוכר, קמח, מזון טחון, שוקולד, חטיפים",
        "tips": [
            "הכנס ליום הפינוק הראשון בזהירות",
            "זכור: 50% ירקות גם ביום פינוק"
        ],
        "exercise": "אימון כוח: 3 סטים של 6-8 חזרות.",
        "treat_rules": "יום פינוק: צלחת 50% ירקות מנקים + 50% כל דבר"
    },
    5: {
        "phase": "ניקוי מתקדם",
        "phase_icon": "💪",
        "title": "שבוע 5 - ניקוי מתקדם",
        "focus": "2-3 ארוחות ביום, חלון אכילה 8-12 שעות",
        "instructions": [
            "הימנעות קפדנית מסוכר, קמח ומזון מטוגן",
            "2-3 ארוחות ביום, ללא נשנושים",
            "בחר חלון אכילה של 8-12 שעות",
            "הימנע מאגוזים ובוטנים בשלב זה"
        ],
        "allowed": "חלבונים: כולם (ללא הגבלת שומן). ירקות: כל ירקות הניקוי (50%). שומנים: מוגבל ל-2-3 כפות 'שומן מרוכז' ליום. פחמימות: קטניות, כוסמת, קינואה, עד 4 כפות שיבולת שועל. פירות: 1 מנה (פירות יער ללא הגבלה)",
        "forbidden": "סוכר, קמח, מזון מטוגן, אגוזים, בוטנים",
        "tips": [
            "השתמש במים לניהול רעב בין ארוחות",
            "אם מרגיש צורך בנשנוש - השתמש בארוחה מיני/פרי רק בימי מעבר ראשונים"
        ],
        "exercise": "אימון כוח ממשיך. מומלץ: 14 שעות צום אחרי ארוחת פינוק לאיפוס רגישות לאינסולין.",
        "treat_rules": "ארוחת פינוק אחת: 50% ירקות + 50% כל דבר. יום פינוק מבוטל אם שברת כללים פעמיים בשבוע."
    },
    6: {
        "phase": "ניקוי מתקדם",
        "phase_icon": "💪",
        "title": "שבוע 6 - המשך ניקוי מתקדם",
        "focus": "חיזוק ההרגלים",
        "instructions": [
            "המשך כללי שבוע 5",
            "2-3 ארוחות ביום",
            "חלון אכילה 8-12 שעות"
        ],
        "allowed": "חלבונים: כולם. ירקות: 50% מנקים. שומנים: 2-3 כפות ליום. פחמימות: קטניות, כוסמת, קינואה. פירות: 1 מנה",
        "forbidden": "סוכר, קמח, מזון מטוגן, אגוזים",
        "tips": [
            "מנות שומן מרוכז: כף שמן/חמאה/טחינה = 1 מנה",
            "חצי אבוקדו = 1 מנה",
            "15 זיתים = 1 מנה"
        ],
        "exercise": "אימון כוח 3-5 פעמים בשבוע.",
        "treat_rules": "ארוחת פינוק אחת בשבוע"
    },
    7: {
        "phase": "ניקוי מתקדם",
        "phase_icon": "💪",
        "title": "שבוע 7 - סיום שלב הניקוי",
        "focus": "שבוע אחרון של ניקוי מתקדם",
        "instructions": [
            "המשך כללי שבוע 5-6",
            "התכונן למעבר לשלב התחזוקה"
        ],
        "allowed": "חלבונים: כולם. ירקות: 50% מנקים. שומנים: 2-3 כפות ליום. פחמימות: קטניות, כוסמת, קינואה. פירות: 1 מנה",
        "forbidden": "סוכר, קמח, מזון מטוגן, אגוזים",
        "tips": [
            "אתה בסוף שלב הניקוי!",
            "הגוף שלך עבר שינוי הורמונלי משמעותי"
        ],
        "exercise": "אימון כוח 3-5 פעמים בשבוע.",
        "treat_rules": "ארוחת פינוק אחת בשבוע"
    },
    8: {
        "phase": "מעבר",
        "phase_icon": "🔄",
        "title": "שבוע 8 - שבוע מעבר",
        "focus": "מעבר לשלב התחזוקה",
        "instructions": [
            "שבוע מעבר בין ניקוי לתחזוקה",
            "בחר את המסלול שלך לשלב הבא"
        ],
        "allowed": "לפי כללי ניקוי מתקדם",
        "forbidden": "סוכר, קמח",
        "tips": [
            "זה הזמן לבחור מסלול: מהיר, ניקוי או מתון"
        ],
        "exercise": "המשך אימון כוח.",
        "treat_rules": "ארוחת פינוק אחת"
    },
    9: {
        "phase": "מסלולים",
        "phase_icon": "🎯",
        "title": "שבוע 9+ - שלב המסלולים",
        "focus": "בחר את המסלול המתאים לך",
        "instructions": [
            "מסלול מהיר: קטניות בלבד + פרי אחד",
            "מסלול ניקוי: קטניות + קינואה/כוסמת + פרי + כף דבש",
            "מסלול מתון: קטניות + פחמימות רמה 2-6 פעם ביום"
        ],
        "allowed": "לפי המסלול שנבחר",
        "forbidden": "סוכר לבן, קמח לבן",
        "tips": [],
        "exercise": "אימון כוח 3-5 פעמים בשבוע + הליכה 4-6 ק״מ.",
        "treat_rules": "מהיר: 2 ימי פינוק. ניקוי/מתון: יום פינוק אחד."
    }
}

TRACK_DATA = {
    "fast": {
        "name": "מסלול מהיר",
        "icon": "🚀",
        "carbs": "קטניות בלבד + פרי אחד ביום",
        "treats": "2 ימי פינוק בשבוע (רווח של 2 ימים לפטיניים ביניהם)",
        "tips": [
            "חלבון רזה עדיף (חזה עוף, דג לבן, בקר רזה)",
            "50% ירקות מנקים פעמיים ביום",
            "2-3 מנות שומן ביום"
        ]
    },
    "cleanse": {
        "name": "מסלול ניקוי",
        "icon": "✨",
        "carbs": "קטניות + קינואה/כוסמת + עד 4 כפות שיבולת שועל + פרי + כף דבש",
        "treats": "2 ימי פינוק: ארוחה אחת 50/50 + 2-3 פירות נוספים",
        "tips": [
            "הימנע מסוכר וקמח מלבד ימי פינוק",
            "הגבל שיבולת שועל ל-4 כפות ביום"
        ]
    },
    "moderate": {
        "name": "מסלול מתון",
        "icon": "🍚",
        "carbs": "קטניות + פחמימות רמה 2-6 (תפו״א, אורז) פעם ביום ברבע צלחת",
        "treats": "יום פינוק אחד: ארוחה אחת 50/50 (ללא פירות נוספים)",
        "tips": [
            "ללא קמח לבן או סוכר לבן",
            "סיכון ל'חסימת אינסולין' גבוה יותר",
            "דורש כנות עצמית גבוהה"
        ]
    }
}

CLEANING_VEGGIES = ["מלפפון", "עגבנייה", "בצל", "ברוקולי", "כרובית", "כרוב", "קישוא", "חסה", "תרד", "פטריות", "פלפל", "חציל", "עגבניות שרי", "שעועית ירוקה", "אספרגוס", "כרפס", "קולורבי"]

MOTIVATION_TIPS = [
    "התקדמות, לא שלמות.",
    "כל יום שאתה עומד ביעדים - הגוף משתנה.",
    "אתה לא צריך להיות מושלם, רק עקבי.",
    "המים הם הדלק של השינוי.",
    "80% מספיק. עקרון פארטו.",
    "הרגל חדש נבנה בזכות עקביות, לא מאמץ.",
    "היום הזה לא יחזור. עשה אותו נכון."
]

# ===== STORAGE =====

def get_gist_data():
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")
        if not token or not gist_id:
            return get_default_data()
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers, timeout=10)
        if response.status_code == 200:
            gist = response.json()
            if "leptin_data.json" in gist["files"]:
                return json.loads(gist["files"]["leptin_data.json"]["content"])
        return get_default_data()
    except:
        return get_default_data()


def save_gist_data(data):
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")
        if not token:
            return False
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        payload = {"files": {"leptin_data.json": {"content": json.dumps(data, ensure_ascii=False, indent=2)}}}
        if gist_id:
            requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=payload, timeout=10)
        else:
            payload["public"] = False
            response = requests.post("https://api.github.com/gists", headers=headers, json=payload, timeout=10)
            if response.status_code == 201:
                st.info(f"GIST_ID: {response.json()['id']}")
        return True
    except:
        return False


def get_default_data():
    return {"user_settings": {"start_date": None, "track": None, "name": ""}, "daily_logs": {}}


# ===== HELPERS =====

def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def calc_program_day(start_date_str):
    try:
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        delta = (datetime.now() - start).days + 1
        week = min(13, max(1, (delta - 1) // 7 + 1))
        return delta, week
    except:
        return 1, 1


def get_week_data(week):
    if week > 9:
        return WEEK_DATA[9]
    return WEEK_DATA.get(week, WEEK_DATA[1])


def init_log(data):
    today = get_today()
    if today not in data["daily_logs"]:
        data["daily_logs"][today] = {
            "water": 0, "water_before": 0, "veggies": False, "protein": False,
            "window": 0, "fats": 0, "treat": False, "slip": False, "done": False
        }
    return data


def calc_score(log):
    s = 0
    if log.get("water", 0) >= 2: s += 20
    if log.get("water", 0) >= 3: s += 10
    if log.get("water_before", 0) >= 3: s += 10
    if log.get("veggies"): s += 25
    if log.get("protein"): s += 15
    if log.get("fats", 0) <= 3: s += 10
    if 0 < log.get("window", 0) <= 12: s += 10
    if log.get("slip") and not log.get("treat"): s -= 20
    return max(0, min(100, s))


def get_streak(data):
    logs = data.get("daily_logs", {})
    streak = 0
    for i in range(30):
        d = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        if d in logs and calc_score(logs[d]) >= 70:
            streak += 1
        else:
            break
    return streak


# ===== AUTH =====

def check_auth():
    if st.session_state.get("auth"):
        return True

    st.markdown("## 🔥 שיטת הלפטין")
    st.markdown("*המסע שלך להצלחה*")
    st.markdown("---")

    pw = st.text_input("סיסמה", type="password")
    if st.button("כניסה"):
        if pw == st.secrets.get("PASSWORD", "leptin2024"):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("סיסמה שגויה")
    return False


# ===== SCREENS =====

def show_onboarding(data):
    st.markdown("## 🔥 שיטת הלפטין")
    st.markdown("### ברוכים הבאים!")
    st.markdown("---")

    name = st.text_input("מה השם שלך?")
    st.markdown("**מתי התחלת את התוכנית?**")
    start = st.date_input("תאריך התחלה", value=datetime.now(), max_value=datetime.now(), label_visibility="collapsed")

    st.info("💡 האפליקציה תחשב אוטומטית באיזה שבוע אתה ותציג את הכללים המתאימים")

    if st.button("🚀 מתחילים!"):
        data["user_settings"]["name"] = name or "אלוף"
        data["user_settings"]["start_date"] = start.strftime("%Y-%m-%d")
        save_gist_data(data)
        st.session_state.app_data = data
        st.rerun()


def show_main(data):
    settings = data["user_settings"]
    day, week = calc_program_day(settings["start_date"])
    week_info = get_week_data(week)

    data = init_log(data)
    log = data["daily_logs"][get_today()]
    score = calc_score(log)
    streak = get_streak(data)

    # Header
    st.markdown(f"## שלום {settings.get('name', '')}!")
    st.markdown(f"**{week_info['phase_icon']} {week_info['title']}**")
    st.markdown(f"יום {day} | שבוע {week} מתוך 13")

    # Score
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("ציון יומי", f"{score}%")
    col2.metric("רצף", f"{streak} ימים")
    col3.metric("התקדמות", f"{week}/13")

    st.progress(score / 100)

    # Motivation
    import random
    st.info(f"💡 {random.choice(MOTIVATION_TIPS)}")

    # Week focus
    st.markdown("---")
    st.markdown(f"### 🎯 המיקוד השבועי")
    st.markdown(f"**{week_info['focus']}**")

    # Daily tracking
    st.markdown("---")
    st.markdown("### 📊 מעקב יומי")

    # Water
    st.markdown("#### 💧 מים")
    water = st.slider("כמה ליטר שתית?", 0.0, 6.0, float(log.get("water", 0)), 0.5)
    if water != log.get("water"):
        log["water"] = water
        save_gist_data(data)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("➖", key="wb-"):
            log["water_before"] = max(0, log.get("water_before", 0) - 1)
            save_gist_data(data)
            st.rerun()
    with c2:
        st.markdown(f"**2 כוסות לפני ארוחה: {log.get('water_before', 0)}/3**")
    with c3:
        if st.button("➕", key="wb+"):
            log["water_before"] = min(6, log.get("water_before", 0) + 1)
            save_gist_data(data)
            st.rerun()

    # Nutrition
    st.markdown("#### 🥗 תזונה")

    veg = st.checkbox("אכלתי 50% ירקות מנקים ב-2 ארוחות", value=log.get("veggies", False))
    if veg != log.get("veggies"):
        log["veggies"] = veg
        save_gist_data(data)

    prot = st.checkbox("כללתי חלבון בכל ארוחה", value=log.get("protein", False))
    if prot != log.get("protein"):
        log["protein"] = prot
        save_gist_data(data)

    with st.expander("📋 ירקות מנקים"):
        st.markdown(", ".join(CLEANING_VEGGIES))
        st.warning("לא נחשבים: תפו״א, בטטה, סלק, תירס, קטניות")

    # Timing & Fats
    st.markdown("#### ⏰ תזמון ושומנים")

    win = st.slider("חלון אכילה (שעות)", 0, 16, log.get("window", 0))
    if win != log.get("window"):
        log["window"] = win
        save_gist_data(data)

    fc1, fc2, fc3 = st.columns([1, 2, 1])
    with fc1:
        if st.button("➖", key="f-"):
            log["fats"] = max(0, log.get("fats", 0) - 1)
            save_gist_data(data)
            st.rerun()
    with fc2:
        fats = log.get("fats", 0)
        st.markdown(f"**שומנים: {fats} כפות** {'✅' if fats <= 3 else '⚠️'}")
    with fc3:
        if st.button("➕", key="f+"):
            log["fats"] = log.get("fats", 0) + 1
            save_gist_data(data)
            st.rerun()

    # Phase specific
    st.markdown("---")
    st.markdown("### 📖 הנחיות השבוע")

    for inst in week_info["instructions"]:
        st.markdown(f"• {inst}")

    with st.expander("✅ מזון מותר"):
        st.markdown(week_info["allowed"])

    with st.expander("🚫 מזון אסור"):
        st.markdown(week_info["forbidden"])

    if week_info.get("treat_rules"):
        with st.expander("🎉 כללי יום פינוק"):
            st.markdown(week_info["treat_rules"])

    # Track selection for week 9+
    if week >= 9:
        st.markdown("---")
        st.markdown("### 🛤️ המסלול שלך")
        track = settings.get("track")

        if not track:
            track = st.radio("בחר מסלול:", ["fast", "cleanse", "moderate"],
                           format_func=lambda x: f"{TRACK_DATA[x]['icon']} {TRACK_DATA[x]['name']}")
            if st.button("שמור מסלול"):
                settings["track"] = track
                save_gist_data(data)
                st.rerun()
        else:
            t = TRACK_DATA[track]
            st.markdown(f"**{t['icon']} {t['name']}**")
            st.markdown(f"פחמימות: {t['carbs']}")
            st.markdown(f"פינוקים: {t['treats']}")

    # Treat & Slip
    st.markdown("---")
    treat = st.checkbox("🎉 יום פינוק", value=log.get("treat", False))
    if treat != log.get("treat"):
        log["treat"] = treat
        save_gist_data(data)

    if week >= 3 and not treat:
        slip = st.checkbox("⚠️ אכלתי מזון אסור", value=log.get("slip", False))
        if slip != log.get("slip"):
            log["slip"] = slip
            save_gist_data(data)

    # Rescue
    if score < 60 or log.get("slip"):
        st.markdown("---")
        st.warning("🆘 גלגלי הצלה")
        r1, r2, r3 = st.columns(3)
        if r1.button("💧 מים"):
            st.success("הוסף 1-2 ליטר!")
        if r2.button("🥗 ירקות"):
            st.success("הגדל 50%!")
        if r3.button("⏰ דחייה"):
            st.success("מחר דחה ארוחה!")

    # Tips
    if week_info.get("tips"):
        st.markdown("---")
        st.markdown("### 💡 טיפים")
        for tip in week_info["tips"]:
            st.markdown(f"• {tip}")

    # Complete
    st.markdown("---")
    if st.button("✅ סיים יום"):
        log["done"] = True
        save_gist_data(data)
        if score >= 80:
            st.balloons()
            st.success("🏆 יום מעולה!")
        elif score >= 60:
            st.success("👍 יום טוב!")
        else:
            st.info("💪 מחר יום חדש!")


def show_history(data):
    st.markdown("## 📅 היסטוריה")

    logs = data.get("daily_logs", {})
    if not logs:
        st.info("אין היסטוריה")
        return

    streak = get_streak(data)
    st.metric("רצף נוכחי", f"{streak} ימים")

    for d in sorted(logs.keys(), reverse=True)[:14]:
        log = logs[d]
        score = calc_score(log)
        date_obj = datetime.strptime(d, "%Y-%m-%d")
        day_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

        icon = "🏆" if score >= 80 else "✅" if score >= 60 else "⚠️"
        treat = " 🎉" if log.get("treat") else ""

        with st.expander(f"{icon} {day_names[date_obj.weekday()]} {date_obj.strftime('%d/%m')} - {score}%{treat}"):
            st.markdown(f"💧 מים: {log.get('water', 0)} ליטר")
            st.markdown(f"🥗 ירקות: {'✅' if log.get('veggies') else '❌'}")
            st.markdown(f"🍗 חלבון: {'✅' if log.get('protein') else '❌'}")
            st.markdown(f"🥑 שומנים: {log.get('fats', 0)}")


def show_info(data):
    st.markdown("## 📚 מידע")

    settings = data["user_settings"]
    _, week = calc_program_day(settings.get("start_date", get_today()))

    st.markdown("### 🥗 ירקות מנקים")
    st.markdown(", ".join(CLEANING_VEGGIES))
    st.warning("לא נחשבים: תפו״א, בטטה, סלק, תירס, אפונה, קטניות")

    st.markdown("---")
    st.markdown("### 🥑 מנות שומן מרוכז")
    st.markdown("""
    • 1 כף שמן/חמאה/טחינה = 1 מנה
    • חצי אבוקדו = 1 מנה
    • 15 זיתים = 1 מנה
    • 2 פרוסות לחם טחינה = 1 מנה
    """)

    st.markdown("---")
    st.markdown("### 🍷 אלכוהול")
    st.markdown("כוס יין אדום יבש או 1/3 בירה ביום")

    st.markdown("---")
    st.markdown("### 🥛 חלב")
    st.markdown("עד 40 מ״ל ליום לקפה (פחות מ-48 קלוריות ל-100 מ״ל)")

    st.markdown("---")
    st.markdown("### 🛤️ המסלולים (שבוע 9+)")

    for key, t in TRACK_DATA.items():
        with st.expander(f"{t['icon']} {t['name']}"):
            st.markdown(f"**פחמימות:** {t['carbs']}")
            st.markdown(f"**פינוקים:** {t['treats']}")
            for tip in t['tips']:
                st.markdown(f"• {tip}")


def show_settings(data):
    st.markdown("## ⚙️ הגדרות")

    settings = data["user_settings"]
    day, week = calc_program_day(settings.get("start_date", get_today()))

    st.metric("יום בתוכנית", day)
    st.metric("שבוע", f"{week} מתוך 13")

    st.markdown("---")

    name = st.text_input("שם", value=settings.get("name", ""))
    start = st.date_input("תאריך התחלה",
                         value=datetime.strptime(settings["start_date"], "%Y-%m-%d") if settings.get("start_date") else datetime.now())

    if week >= 9:
        track = st.radio("מסלול", ["fast", "cleanse", "moderate"],
                        index=["fast", "cleanse", "moderate"].index(settings.get("track") or "fast"),
                        format_func=lambda x: TRACK_DATA[x]["name"])
    else:
        track = None

    if st.button("💾 שמור"):
        settings["name"] = name
        settings["start_date"] = start.strftime("%Y-%m-%d")
        if track:
            settings["track"] = track
        save_gist_data(data)
        st.success("נשמר!")
        st.rerun()

    st.markdown("---")
    if st.button("🚪 התנתק"):
        st.session_state.auth = False
        st.rerun()


def main():
    if not check_auth():
        return

    if "app_data" not in st.session_state:
        st.session_state.app_data = get_gist_data()

    data = st.session_state.app_data

    if not data["user_settings"].get("start_date"):
        show_onboarding(data)
        return

    tabs = st.tabs(["📊 היום", "📅 היסטוריה", "📚 מידע", "⚙️"])

    with tabs[0]:
        show_main(data)
    with tabs[1]:
        show_history(data)
    with tabs[2]:
        show_info(data)
    with tabs[3]:
        show_settings(data)


if __name__ == "__main__":
    main()
