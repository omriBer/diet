"""
The Leptin Method - שיטת הלפטין
Hebrew Weight Loss Tracking Application
Cloud-ready with password protection and GitHub Gist storage
"""

import streamlit as st
import json
import requests
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="שיטת הלפטין",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# RTL and mobile-friendly CSS
st.markdown("""
<style>
    /* RTL Support */
    .stApp, .stMarkdown, .stText, div[data-testid="stMarkdownContainer"] {
        direction: rtl;
        text-align: right;
    }

    /* Fix input fields for RTL */
    input, textarea, .stTextInput input, .stNumberInput input {
        direction: rtl;
        text-align: right;
    }

    /* Mobile-friendly styling */
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
    }

    /* Big buttons for mobile */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        border-radius: 10px;
        margin: 0.25rem 0;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Week badge */
    .week-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }

    /* Metric card */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }

    /* Info boxes */
    .info-box {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #2196f3;
        margin: 0.5rem 0;
    }

    .warning-box {
        background: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #ff9800;
        margin: 0.5rem 0;
    }

    .success-box {
        background: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #4caf50;
        margin: 0.5rem 0;
    }

    /* Login container */
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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

    except Exception as e:
        st.error(f"שגיאה בטעינת נתונים: {e}")
        return get_default_data()


def save_gist_data(data):
    """Save data to GitHub Gist"""
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        gist_id = st.secrets.get("GIST_ID", "")

        if not token:
            st.warning("לא הוגדר GitHub Token - הנתונים לא יישמרו")
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
            # Update existing gist
            response = requests.patch(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers,
                json=payload,
                timeout=10
            )
        else:
            # Create new gist (private)
            payload["public"] = False
            response = requests.post(
                "https://api.github.com/gists",
                headers=headers,
                json=payload,
                timeout=10
            )
            if response.status_code == 201:
                new_gist_id = response.json()["id"]
                st.info(f"נוצר Gist חדש! העתק את ה-ID להגדרות: {new_gist_id}")

        return response.status_code in [200, 201]

    except Exception as e:
        st.error(f"שגיאה בשמירת נתונים: {e}")
        return False


def get_default_data():
    """Return default data structure"""
    return {
        "user_settings": {
            "current_week": 1,
            "track": None,
            "start_date": None
        },
        "daily_logs": {}
    }


# ===== AUTHENTICATION =====

def check_password():
    """Simple password protection"""

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div class="main-header">
        <h1>💧 שיטת הלפטין</h1>
        <p>אפליקציית מעקב אישית</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔐 התחברות")

    password = st.text_input("סיסמה", type="password", key="password_input")

    if st.button("כניסה", use_container_width=True):
        correct_password = st.secrets.get("PASSWORD", "leptin2024")

        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("סיסמה שגויה")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        💧 הצפת לפטין | התקדמות, לא שלמות
    </div>
    """, unsafe_allow_html=True)

    return False


# ===== HELPER FUNCTIONS =====

CLEANING_VEGGIES = [
    "מלפפון", "עגבנייה", "בצל", "פטריות", "כרובית",
    "כרוב", "ברוקולי", "שעועית ירוקה", "קישוא", "חסה", "תרד"
]

LEPTIN_CARBS = ["עדשים", "חומוס", "שעועית", "קינואה", "כוסמת"]


def get_today_key():
    """Get today's date as a string key"""
    return datetime.now().strftime("%Y-%m-%d")


def get_phase(week):
    """Determine the current phase based on week number"""
    if week <= 2:
        return "flood"
    elif week <= 7:
        return "cleanse"
    elif week == 8:
        return "transition"
    else:
        return "tracks"


def get_phase_name(phase):
    """Get Hebrew phase name"""
    names = {
        "flood": "🌊 שלב ההצפה",
        "cleanse": "✨ שלב הניקוי",
        "transition": "🔄 שבוע מעבר",
        "tracks": "🛤️ שלב המסלולים"
    }
    return names.get(phase, "")


def init_daily_log(data):
    """Initialize today's log if not exists"""
    today = get_today_key()
    if today not in data["daily_logs"]:
        data["daily_logs"][today] = {
            "water_liters": 0,
            "water_before_meals": 0,
            "veggies_50_percent": False,
            "protein_every_meal": False,
            "eating_window_start": None,
            "eating_window_end": None,
            "fats_count": 0,
            "treat_day": False,
            "sugar_flour": False,
            "treat_meals_used": 0,
            "notes": "",
            "rescue_activated": False,
            "completed": False
        }
    return data


def calculate_daily_score(log, week, track):
    """Calculate daily compliance score"""
    phase = get_phase(week)
    score = 0
    max_score = 0

    # Water - 30 points
    max_score += 30
    if log.get("water_liters", 0) >= 2:
        score += 15
    if log.get("water_liters", 0) >= 3:
        score += 10
    if log.get("water_before_meals", 0) >= 3:
        score += 5

    # Veggies - 25 points
    max_score += 25
    if log.get("veggies_50_percent", False):
        score += 25

    # Protein - 15 points
    max_score += 15
    if log.get("protein_every_meal", False):
        score += 15

    # Eating window - 15 points
    max_score += 15
    if log.get("eating_window_start") and log.get("eating_window_end"):
        score += 15

    # Fats limit - 15 points
    max_score += 15
    if log.get("fats_count", 0) <= 3:
        score += 15

    # Phase penalties
    if phase in ["cleanse", "tracks"] and not log.get("treat_day", False):
        if log.get("sugar_flour", False):
            score -= 20

    return max(0, score), max_score


def show_rescue_wheels():
    """Display rescue protocol options"""
    st.markdown("""
    <div class="warning-box">
        <h4>🆘 גלגלי הצלה - פרוטוקול חירום</h4>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💧 הגבר מים", use_container_width=True):
            st.success("✅ הוסף/י עוד 1-2 ליטר מים!")

    with col2:
        if st.button("🥗 הגבר ירקות", use_container_width=True):
            st.success("✅ הגדל/י ירקות ב-50%!")

    with col3:
        if st.button("⏰ דחה ארוחה", use_container_width=True):
            st.success("✅ מחר דחה/י ארוחה ראשונה!")


# ===== UI SCREENS =====

def show_onboarding(data):
    """Show onboarding screen for new users"""
    st.markdown("""
    <div class="main-header">
        <h1>💧 שיטת הלפטין</h1>
        <p>ברוכים הבאים למסע שלכם!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🌟 בואו נתחיל!")

    week = st.selectbox(
        "באיזה שבוע את/ה נמצא/ת?",
        options=list(range(1, 14)),
        index=0,
        format_func=lambda x: f"שבוע {x}"
    )

    track = None
    if week >= 9:
        st.markdown("#### 🛤️ בחר/י מסלול:")
        track = st.radio(
            "מסלול",
            options=["fast", "cleanse", "moderate"],
            format_func=lambda x: {
                "fast": "🚀 מסלול מהיר - עדשים בלבד, 2 ארוחות פינוק",
                "cleanse": "✨ מסלול ניקוי - קטניות + קינואה, 1 ארוחת פינוק",
                "moderate": "🍚 מסלול מתון - אורז/תפו\"א פעם ביום"
            }.get(x),
            label_visibility="collapsed"
        )

    if st.button("🚀 התחל מסע!", use_container_width=True, type="primary"):
        data["user_settings"]["current_week"] = week
        data["user_settings"]["track"] = track
        data["user_settings"]["start_date"] = get_today_key()
        save_gist_data(data)
        st.session_state["app_data"] = data
        st.rerun()


def show_daily_tracking(data):
    """Show main daily tracking interface"""
    settings = data["user_settings"]
    week = settings["current_week"]
    track = settings.get("track")
    phase = get_phase(week)

    today = get_today_key()
    data = init_daily_log(data)
    log = data["daily_logs"][today]

    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>💧 שיטת הלפטין</h1>
        <div class="week-badge">שבוע {week} | {get_phase_name(phase)}</div>
        <p style="margin-top: 10px;">{datetime.now().strftime("%d/%m/%Y")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Daily score
    score, max_score = calculate_daily_score(log, week, track)
    progress = score / max_score if max_score > 0 else 0

    st.markdown(f"### 📊 ציון יומי: {score}/{max_score}")
    st.progress(progress)

    # Treat Day Toggle
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### 🎉 יום פינוק?")
    with col2:
        treat_day = st.checkbox("יום פינוק", value=log.get("treat_day", False),
                                label_visibility="collapsed", key="treat_day")

    if treat_day != log.get("treat_day"):
        log["treat_day"] = treat_day
        save_gist_data(data)

    if treat_day:
        st.markdown("""
        <div class="info-box">
            ⚠️ <strong>יום פינוק:</strong> עדיין חובה לשתות מים ולאכול 50% ירקות!
        </div>
        """, unsafe_allow_html=True)

    # ===== WATER TRACKING =====
    st.markdown("---")
    st.markdown("## 💧 הצפת הלפטין - מים")

    st.markdown("""
    <div class="info-box">
        🎯 יעד: 2-4 ליטר ביום<br>
        ⚡ כלל הזהב: 2 כוסות לפני כל נגיסה!
    </div>
    """, unsafe_allow_html=True)

    water_col1, water_col2 = st.columns([2, 2])
    with water_col1:
        water_liters = st.number_input(
            "כמה ליטרים שתית היום?",
            min_value=0.0,
            max_value=6.0,
            value=float(log.get("water_liters", 0)),
            step=0.5,
            key="water_liters"
        )

    with water_col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>💧 {water_liters}</h2>
            <p>ליטר</p>
        </div>
        """, unsafe_allow_html=True)

    if water_liters != log.get("water_liters"):
        log["water_liters"] = water_liters
        save_gist_data(data)

    # Water before meals
    st.markdown("##### 🥤 2 כוסות לפני ארוחה:")
    water_before = log.get("water_before_meals", 0)

    wcol1, wcol2, wcol3, wcol4 = st.columns(4)
    with wcol1:
        if st.button("➕", key="add_water", use_container_width=True):
            log["water_before_meals"] = min(water_before + 1, 6)
            save_gist_data(data)
            st.rerun()
    with wcol2:
        if st.button("➖", key="sub_water", use_container_width=True):
            log["water_before_meals"] = max(water_before - 1, 0)
            save_gist_data(data)
            st.rerun()
    with wcol3:
        st.markdown(f"**{water_before}/3** ארוחות")
    with wcol4:
        st.markdown("✅" if water_before >= 3 else "⏳")

    # ===== NUTRITION TRACKING =====
    st.markdown("---")
    st.markdown("## 🥗 תזונה - ירקות וחלבון")

    with st.expander("📋 רשימת ירקות מנקים"):
        st.markdown(", ".join(CLEANING_VEGGIES))
        st.markdown("⚠️ **לא נכללים:** תפוח אדמה, בטטה")

    veggies = st.checkbox(
        "🥒 אכלתי 50% ירקות מנקים לפחות ב-2 ארוחות",
        value=log.get("veggies_50_percent", False),
        key="veggies"
    )
    if veggies != log.get("veggies_50_percent"):
        log["veggies_50_percent"] = veggies
        save_gist_data(data)

    protein = st.checkbox(
        "🍗 כללתי חלבון בכל ארוחה",
        value=log.get("protein_every_meal", False),
        key="protein"
    )
    if protein != log.get("protein_every_meal"):
        log["protein_every_meal"] = protein
        save_gist_data(data)

    # ===== EATING WINDOW =====
    st.markdown("---")
    st.markdown("## ⏰ חלון אכילה")
    st.markdown("יעד: 8-12 שעות")

    ew_col1, ew_col2 = st.columns(2)
    with ew_col1:
        start_time = st.time_input("ארוחה ראשונה", value=None, key="eating_start")
    with ew_col2:
        end_time = st.time_input("ארוחה אחרונה", value=None, key="eating_end")

    if start_time:
        log["eating_window_start"] = start_time.strftime("%H:%M")
        save_gist_data(data)
    if end_time:
        log["eating_window_end"] = end_time.strftime("%H:%M")
        save_gist_data(data)

    if start_time and end_time:
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        window_hours = (end_dt - start_dt).seconds / 3600

        if window_hours <= 12:
            st.markdown(f"""
            <div class="success-box">
                ✅ חלון אכילה: {window_hours:.1f} שעות - מעולה!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="warning-box">
                ⚠️ חלון אכילה: {window_hours:.1f} שעות - נסה לקצר
            </div>
            """, unsafe_allow_html=True)

    # ===== FATS TRACKING =====
    st.markdown("---")
    st.markdown("## 🥑 שומנים מרוכזים")
    st.markdown("מגבלה: 2-3 כפות ביום (טחינה, שמן, אבוקדו)")

    fat_col1, fat_col2, fat_col3 = st.columns([1, 2, 1])
    with fat_col1:
        if st.button("➖", key="sub_fat", use_container_width=True):
            log["fats_count"] = max(log.get("fats_count", 0) - 1, 0)
            save_gist_data(data)
            st.rerun()
    with fat_col2:
        fats = log.get("fats_count", 0)
        color = "green" if fats <= 3 else "red"
        st.markdown(f"<h2 style='text-align:center; color:{color}'>{fats} כפות</h2>",
                    unsafe_allow_html=True)
    with fat_col3:
        if st.button("➕", key="add_fat", use_container_width=True):
            log["fats_count"] = log.get("fats_count", 0) + 1
            save_gist_data(data)
            st.rerun()

    # ===== PHASE-SPECIFIC CONTENT =====
    st.markdown("---")

    if phase == "flood":
        st.markdown("""
        <div class="info-box">
            <h4>🌊 שלב ההצפה (שבועות 1-2)</h4>
            <p>התמקד/י במים וירקות בלבד! אין הגבלות מזון.</p>
        </div>
        """, unsafe_allow_html=True)

        sugar_flour = st.checkbox("📝 אכלתי סוכר/קמח (לתיעוד בלבד)",
                                  value=log.get("sugar_flour", False),
                                  key="sugar_flour_flood")
        if sugar_flour != log.get("sugar_flour"):
            log["sugar_flour"] = sugar_flour
            save_gist_data(data)

    elif phase == "cleanse":
        st.markdown("""
        <div class="warning-box">
            <h4>✨ שלב הניקוי (שבועות 3-7)</h4>
            <p><strong>אסור:</strong> סוכר, דבש, קמח, פסטה, אורז, תירס, תפו"א</p>
            <p><strong>מותר:</strong> עדשים, חומוס, שעועית, קינואה, כוסמת</p>
        </div>
        """, unsafe_allow_html=True)

        if not log.get("treat_day"):
            sugar_flour = st.checkbox(
                "⚠️ אכלתי מזון אסור (סוכר/קמח/מעובד)",
                value=log.get("sugar_flour", False),
                key="sugar_flour_cleanse"
            )
            if sugar_flour != log.get("sugar_flour"):
                log["sugar_flour"] = sugar_flour
                save_gist_data(data)
                if sugar_flour:
                    st.warning("אל דאגה! התקדמות לא שלמות. מחר יום חדש! 💪")

    elif phase == "tracks":
        st.markdown("### 🛤️ המסלול שלך")

        if track == "fast":
            st.markdown("""
            <div class="info-box">
                <h4>🚀 מסלול מהיר</h4>
                <p>✅ מותר: עדשים בלבד | 🎉 2 ארוחות פינוק בשבוע</p>
            </div>
            """, unsafe_allow_html=True)
        elif track == "cleanse":
            st.markdown("""
            <div class="info-box">
                <h4>✨ מסלול ניקוי</h4>
                <p>✅ מותר: קטניות + קינואה/כוסמת | 🎉 1 ארוחת פינוק + פירות</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <h4>🍚 מסלול מתון</h4>
                <p>✅ מותר: אורז/תפו"א פעם ביום | 🎉 1 ארוחת פינוק</p>
            </div>
            """, unsafe_allow_html=True)

        if not log.get("treat_day"):
            sugar_flour = st.checkbox(
                "⚠️ אכלתי מזון מחוץ למסלול",
                value=log.get("sugar_flour", False),
                key="sugar_flour_tracks"
            )
            if sugar_flour != log.get("sugar_flour"):
                log["sugar_flour"] = sugar_flour
                save_gist_data(data)

    # ===== RESCUE WHEELS =====
    st.markdown("---")

    if score < max_score * 0.6 or log.get("sugar_flour"):
        show_rescue_wheels()
    else:
        with st.expander("🆘 גלגלי הצלה"):
            show_rescue_wheels()

    # ===== NOTES =====
    st.markdown("---")
    st.markdown("### 📝 הערות")
    notes = st.text_area(
        "הערות ליום",
        value=log.get("notes", ""),
        label_visibility="collapsed",
        placeholder="רשום/י הערות, תובנות או תחושות..."
    )
    if notes != log.get("notes"):
        log["notes"] = notes
        save_gist_data(data)

    # ===== COMPLETE DAY =====
    st.markdown("---")
    if st.button("✅ סיים יום", use_container_width=True, type="primary"):
        log["completed"] = True
        save_gist_data(data)

        if score >= max_score * 0.8:
            st.balloons()
            st.success("🎉 יום מצוין! המשיכ/י כך!")
        elif score >= max_score * 0.6:
            st.success("👍 יום טוב! יש מקום לשיפור קטן")
        else:
            st.info("💪 כל יום הוא הזדמנות חדשה!")


def show_history(data):
    """Show history of past days"""
    st.markdown("## 📅 היסטוריה")

    logs = data.get("daily_logs", {})
    if not logs:
        st.info("אין עדיין היסטוריה")
        return

    sorted_dates = sorted(logs.keys(), reverse=True)

    for date_str in sorted_dates[:14]:
        log = logs[date_str]
        week = data["user_settings"]["current_week"]
        track = data["user_settings"].get("track")
        score, max_score = calculate_daily_score(log, week, track)

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_display = date_obj.strftime("%d/%m/%Y")

        if score >= max_score * 0.8:
            status = "🌟"
        elif score >= max_score * 0.6:
            status = "✅"
        else:
            status = "⚠️"

        treat = "🎉" if log.get("treat_day") else ""

        with st.expander(f"{status} {date_display} - {score}/{max_score} {treat}"):
            st.markdown(f"💧 מים: {log.get('water_liters', 0)} ליטר")
            st.markdown(f"🥤 מים לפני ארוחות: {log.get('water_before_meals', 0)}/3")
            st.markdown(f"🥗 ירקות 50%: {'✅' if log.get('veggies_50_percent') else '❌'}")
            st.markdown(f"🍗 חלבון: {'✅' if log.get('protein_every_meal') else '❌'}")
            st.markdown(f"🥑 שומנים: {log.get('fats_count', 0)} כפות")
            if log.get("notes"):
                st.markdown(f"📝 {log.get('notes')}")


def show_settings(data):
    """Show settings page"""
    st.markdown("## ⚙️ הגדרות")

    settings = data["user_settings"]

    new_week = st.selectbox(
        "שבוע נוכחי",
        options=list(range(1, 14)),
        index=settings["current_week"] - 1,
        format_func=lambda x: f"שבוע {x}"
    )

    new_track = settings.get("track")
    if new_week >= 9:
        st.markdown("#### 🛤️ מסלול:")
        track_options = ["fast", "cleanse", "moderate"]
        current_index = track_options.index(settings.get("track") or "fast")
        new_track = st.radio(
            "מסלול",
            options=track_options,
            index=current_index,
            format_func=lambda x: {"fast": "🚀 מהיר", "cleanse": "✨ ניקוי", "moderate": "🍚 מתון"}.get(x),
            label_visibility="collapsed",
            horizontal=True
        )

    if st.button("💾 שמור הגדרות", use_container_width=True):
        settings["current_week"] = new_week
        settings["track"] = new_track if new_week >= 9 else None
        save_gist_data(data)
        st.success("✅ ההגדרות נשמרו!")
        st.rerun()

    st.markdown("---")

    # Logout
    if st.button("🚪 התנתק", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()


def main():
    """Main application entry point"""

    # Check authentication
    if not check_password():
        return

    # Load data from Gist
    if "app_data" not in st.session_state:
        st.session_state["app_data"] = get_gist_data()

    data = st.session_state["app_data"]

    # Check if onboarding needed
    if data["user_settings"].get("start_date") is None:
        show_onboarding(data)
        return

    # Navigation
    tabs = st.tabs(["📊 מעקב יומי", "📅 היסטוריה", "⚙️ הגדרות"])

    with tabs[0]:
        show_daily_tracking(data)

    with tabs[1]:
        show_history(data)

    with tabs[2]:
        show_settings(data)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        💧 הצפת לפטין | ✨ התקדמות, לא שלמות | 💪 יום אחד בכל פעם
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
