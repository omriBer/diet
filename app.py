"""
The Leptin Method - שיטת הלפטין
Hebrew Weight Loss Tracking Application
"""

import streamlit as st
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

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

    /* Success button style */
    .success-btn > button {
        background-color: #28a745 !important;
        color: white !important;
    }

    /* Water button styling */
    .water-btn > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        padding: 1rem;
    }

    /* Card styling */
    .tracking-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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

    /* Progress styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
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

    /* Checkbox styling */
    .stCheckbox {
        padding: 0.5rem 0;
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

    /* Hide Streamlit branding for cleaner mobile look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 1.1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Data file path
DATA_FILE = Path("leptin_data.json")

# Valid cleaning vegetables
CLEANING_VEGGIES = [
    "מלפפון", "עגבנייה", "בצל", "פטריות", "כרובית",
    "כרוב", "ברוקולי", "שעועית ירוקה", "קישוא", "חסה", "תרד"
]

# Forbidden foods by phase
FORBIDDEN_CLEANSE = [
    "סוכר", "דבש", "סילאן", "אגבה", "קמח לבן", "קמח מלא",
    "פסטה", "אורז", "תירס", "תפוחי אדמה"
]

# Allowed Leptin carbs
LEPTIN_CARBS = ["עדשים", "חומוס", "שעועית", "קינואה", "כוסמת"]


def load_data():
    """Load user data from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "user_settings": {
            "current_week": 1,
            "track": None,
            "start_date": None
        },
        "daily_logs": {}
    }


def save_data(data):
    """Save user data to JSON file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_today_key():
    """Get today's date as a string key"""
    return datetime.now().strftime("%Y-%m-%d")


def get_phase(week):
    """Determine the current phase based on week number"""
    if week <= 2:
        return "flood"  # The Flood - שלב ההצפה
    elif week <= 7:
        return "cleanse"  # The Cleanse - שלב הניקוי
    elif week == 8:
        return "transition"  # Transition week
    else:
        return "tracks"  # The Tracks - שלב המסלולים


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
        save_data(data)
    return data


def calculate_daily_score(log, week, track):
    """Calculate daily compliance score"""
    phase = get_phase(week)
    score = 0
    max_score = 0

    # Water (always counts) - 30 points
    max_score += 30
    if log.get("water_liters", 0) >= 2:
        score += 15
    if log.get("water_liters", 0) >= 3:
        score += 10
    if log.get("water_before_meals", 0) >= 3:
        score += 5

    # Veggies (always counts) - 25 points
    max_score += 25
    if log.get("veggies_50_percent", False):
        score += 25

    # Protein - 15 points
    max_score += 15
    if log.get("protein_every_meal", False):
        score += 15

    # Eating window - 15 points
    max_score += 15
    start = log.get("eating_window_start")
    end = log.get("eating_window_end")
    if start and end:
        score += 15

    # Fats limit - 15 points
    max_score += 15
    if log.get("fats_count", 0) <= 3:
        score += 15

    # Phase-specific penalties (only from week 3+)
    if phase in ["cleanse", "tracks"] and not log.get("treat_day", False):
        if log.get("sugar_flour", False):
            score -= 20  # Penalty for forbidden foods

    return max(0, score), max_score


def show_rescue_wheels():
    """Display rescue protocol options"""
    st.markdown("""
    <div class="warning-box">
        <h3>🆘 גלגלי הצלה - פרוטוקול חירום</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### בחר/י פעולת הצלה:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💧 הגבר מים", use_container_width=True):
            st.success("✅ הוסף/י עוד 1-2 ליטר מים היום!")
            st.balloons()

    with col2:
        if st.button("🥗 הגבר ירקות", use_container_width=True):
            st.success("✅ הגדל/י את כמות הירקות ב-50%!")

    with col3:
        if st.button("⏰ דחה ארוחה", use_container_width=True):
            st.success("✅ מחר דחה/י את הארוחה הראשונה ב-1-3 שעות!")


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
                "fast": "🚀 מסלול מהיר - עדשים בלבד, 2 ארוחות פינוק בשבוע",
                "cleanse": "✨ מסלול ניקוי - קטניות + קינואה/כוסמת, 1 ארוחת פינוק + פירות",
                "moderate": "🍚 מסלול מתון - אורז/תפו\"א פעם ביום, 1 ארוחת פינוק"
            }.get(x),
            label_visibility="collapsed"
        )

    if st.button("🚀 התחל מסע!", use_container_width=True):
        data["user_settings"]["current_week"] = week
        data["user_settings"]["track"] = track
        data["user_settings"]["start_date"] = get_today_key()
        save_data(data)
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
        save_data(data)

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

    # Water liters
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
        save_data(data)

    # Water before meals button
    st.markdown("##### 🥤 2 כוסות לפני ארוחה:")
    water_before = log.get("water_before_meals", 0)

    wcol1, wcol2, wcol3, wcol4 = st.columns(4)
    with wcol1:
        if st.button("➕", key="add_water", use_container_width=True):
            log["water_before_meals"] = min(water_before + 1, 6)
            save_data(data)
            st.rerun()
    with wcol2:
        if st.button("➖", key="sub_water", use_container_width=True):
            log["water_before_meals"] = max(water_before - 1, 0)
            save_data(data)
            st.rerun()
    with wcol3:
        st.markdown(f"**{water_before}/3** ארוחות")
    with wcol4:
        if water_before >= 3:
            st.markdown("✅")
        else:
            st.markdown("⏳")

    # ===== NUTRITION TRACKING =====
    st.markdown("---")
    st.markdown("## 🥗 תזונה - ירקות וחלבון")

    # Valid veggies info
    with st.expander("📋 רשימת ירקות מנקים"):
        st.markdown(", ".join(CLEANING_VEGGIES))
        st.markdown("⚠️ **לא נכללים:** תפוח אדמה, בטטה")

    # Veggies checkbox
    veggies = st.checkbox(
        "🥒 אכלתי 50% ירקות מנקים לפחות ב-2 ארוחות",
        value=log.get("veggies_50_percent", False),
        key="veggies"
    )
    if veggies != log.get("veggies_50_percent"):
        log["veggies_50_percent"] = veggies
        save_data(data)

    # Protein checkbox
    protein = st.checkbox(
        "🍗 כללתי חלבון בכל ארוחה",
        value=log.get("protein_every_meal", False),
        key="protein"
    )
    if protein != log.get("protein_every_meal"):
        log["protein_every_meal"] = protein
        save_data(data)

    # ===== EATING WINDOW =====
    st.markdown("---")
    st.markdown("## ⏰ חלון אכילה")
    st.markdown("יעד: 8-12 שעות")

    ew_col1, ew_col2 = st.columns(2)
    with ew_col1:
        start_time = st.time_input(
            "ארוחה ראשונה",
            value=None,
            key="eating_start"
        )
    with ew_col2:
        end_time = st.time_input(
            "ארוחה אחרונה",
            value=None,
            key="eating_end"
        )

    if start_time:
        log["eating_window_start"] = start_time.strftime("%H:%M")
    if end_time:
        log["eating_window_end"] = end_time.strftime("%H:%M")
    save_data(data)

    if start_time and end_time:
        # Calculate window
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
            save_data(data)
            st.rerun()
    with fat_col2:
        fats = log.get("fats_count", 0)
        color = "green" if fats <= 3 else "red"
        st.markdown(f"<h2 style='text-align:center; color:{color}'>{fats} כפות</h2>",
                    unsafe_allow_html=True)
    with fat_col3:
        if st.button("➕", key="add_fat", use_container_width=True):
            log["fats_count"] = log.get("fats_count", 0) + 1
            save_data(data)
            st.rerun()

    # ===== PHASE-SPECIFIC CONTENT =====
    st.markdown("---")

    if phase == "flood":
        st.markdown("""
        <div class="info-box">
            <h4>🌊 שלב ההצפה (שבועות 1-2)</h4>
            <p>התמקד/י במים וירקות בלבד!</p>
            <p>אין הגבלות מזון - רק תתחיל/י להציף 💧</p>
        </div>
        """, unsafe_allow_html=True)

        # Optional sugar/flour logging (no penalty)
        st.checkbox("📝 אכלתי סוכר/קמח (לתיעוד בלבד)",
                   value=log.get("sugar_flour", False),
                   key="sugar_flour_flood")

    elif phase == "cleanse":
        st.markdown("""
        <div class="warning-box">
            <h4>✨ שלב הניקוי (שבועות 3-7)</h4>
            <p><strong>אסור:</strong> סוכר, דבש, סילאן, קמח, פסטה, אורז, תירס, תפו"א</p>
            <p><strong>פחמימות לפטין מותרות:</strong> עדשים, חומוס, שעועית, קינואה, כוסמת</p>
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
                save_data(data)
                if sugar_flour:
                    st.warning("אל דאגה! התקדמות לא שלמות. מחר יום חדש! 💪")

    elif phase == "tracks":
        st.markdown("### 🛤️ המסלול שלך")

        # Show track info
        if track == "fast":
            st.markdown("""
            <div class="info-box">
                <h4>🚀 מסלול מהיר</h4>
                <p>✅ מותר: עדשים בלבד</p>
                <p>🎉 2 ארוחות פינוק בשבוע</p>
            </div>
            """, unsafe_allow_html=True)
            max_treats = 2
        elif track == "cleanse":
            st.markdown("""
            <div class="info-box">
                <h4>✨ מסלול ניקוי</h4>
                <p>✅ מותר: קטניות + קינואה/כוסמת/שיבולת שועל</p>
                <p>🎉 1 ארוחת פינוק + פירות נוספים</p>
            </div>
            """, unsafe_allow_html=True)
            max_treats = 1
        else:  # moderate
            st.markdown("""
            <div class="info-box">
                <h4>🍚 מסלול מתון</h4>
                <p>✅ מותר: אורז/תפו"א פעם ביום</p>
                <p>🎉 1 ארוחת פינוק בשבוע</p>
            </div>
            """, unsafe_allow_html=True)
            max_treats = 1

        # Treat meals counter (weekly)
        st.markdown(f"##### 🍰 ארוחות פינוק השבוע: {log.get('treat_meals_used', 0)}/{max_treats}")

        if not log.get("treat_day"):
            sugar_flour = st.checkbox(
                "⚠️ אכלתי מזון מחוץ למסלול",
                value=log.get("sugar_flour", False),
                key="sugar_flour_tracks"
            )
            if sugar_flour != log.get("sugar_flour"):
                log["sugar_flour"] = sugar_flour
                save_data(data)

    # ===== RESCUE WHEELS =====
    st.markdown("---")

    # Show rescue wheels if score is low or user wants
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
        placeholder="רשום/י כאן הערות, תובנות או תחושות..."
    )
    if notes != log.get("notes"):
        log["notes"] = notes
        save_data(data)

    # ===== COMPLETE DAY BUTTON =====
    st.markdown("---")
    if st.button("✅ סיים יום", use_container_width=True, type="primary"):
        log["completed"] = True
        save_data(data)

        if score >= max_score * 0.8:
            st.balloons()
            st.success("🎉 יום מצוין! המשיכ/י כך!")
        elif score >= max_score * 0.6:
            st.success("👍 יום טוב! יש מקום לשיפור קטן")
        else:
            st.info("💪 כל יום הוא הזדמנות חדשה! התקדמות, לא שלמות!")


def show_history(data):
    """Show history of past days"""
    st.markdown("## 📅 היסטוריה")

    logs = data.get("daily_logs", {})
    if not logs:
        st.info("אין עדיין היסטוריה")
        return

    # Sort by date descending
    sorted_dates = sorted(logs.keys(), reverse=True)

    for date_str in sorted_dates[:14]:  # Last 14 days
        log = logs[date_str]
        week = data["user_settings"]["current_week"]
        track = data["user_settings"].get("track")
        score, max_score = calculate_daily_score(log, week, track)

        # Format date
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_display = date_obj.strftime("%d/%m/%Y")

        # Status emoji
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
            st.markdown(f"🍗 חלבון בכל ארוחה: {'✅' if log.get('protein_every_meal') else '❌'}")
            st.markdown(f"🥑 שומנים: {log.get('fats_count', 0)} כפות")
            if log.get("notes"):
                st.markdown(f"📝 {log.get('notes')}")


def show_settings(data):
    """Show settings page"""
    st.markdown("## ⚙️ הגדרות")

    settings = data["user_settings"]

    # Week selection
    new_week = st.selectbox(
        "שבוע נוכחי",
        options=list(range(1, 14)),
        index=settings["current_week"] - 1,
        format_func=lambda x: f"שבוע {x}"
    )

    # Track selection (only for week 9+)
    new_track = settings.get("track")
    if new_week >= 9:
        st.markdown("#### 🛤️ מסלול:")
        new_track = st.radio(
            "מסלול",
            options=["fast", "cleanse", "moderate"],
            index=["fast", "cleanse", "moderate"].index(settings.get("track") or "fast"),
            format_func=lambda x: {
                "fast": "🚀 מהיר",
                "cleanse": "✨ ניקוי",
                "moderate": "🍚 מתון"
            }.get(x),
            label_visibility="collapsed",
            horizontal=True
        )

    if st.button("💾 שמור הגדרות", use_container_width=True):
        settings["current_week"] = new_week
        settings["track"] = new_track if new_week >= 9 else None
        save_data(data)
        st.success("✅ ההגדרות נשמרו!")
        st.rerun()

    st.markdown("---")

    # Reset data
    st.markdown("### 🗑️ איפוס נתונים")
    if st.button("🔄 התחל מחדש", use_container_width=True):
        if st.session_state.get("confirm_reset"):
            os.remove(DATA_FILE) if DATA_FILE.exists() else None
            st.session_state.clear()
            st.rerun()
        else:
            st.session_state["confirm_reset"] = True
            st.warning("לחץ/י שוב לאישור איפוס")


def main():
    """Main application entry point"""
    # Load data
    data = load_data()

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

    # Motivational footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        💧 הצפת לפטין | ✨ התקדמות, לא שלמות | 💪 יום אחד בכל פעם
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
