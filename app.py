import streamlit as st
import json
import requests

# הגדרות דף Mobile-First
st.set_page_config(page_title="LeptinVibe", layout="wide", initial_sidebar_state="collapsed")

# --- פונקציית אימות (Login) ---
def check_password():
    if st.session_state.get("authenticated", False):
        return True

    st.title("🥗 LeptinVibe")
    password = st.text_input("סיסמה", type="password", key="password_input")

    if st.button("כניסה", use_container_width=True):
        correct_password = st.secrets.get("PASSWORD", "wTn6bLdrZT7gEHu")
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("סיסמה שגויה")
    return False

if not check_password():
    st.stop()

# --- טעינת נתונים ---
@st.cache_data(ttl=600)
def load_all_data():
    try:
        token = st.secrets["GITHUB_TOKEN"]
        gist_id = st.secrets["GIST_ID"]
        headers = {"Authorization": f"token {token}"}
        response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
        response.raise_for_status()
        files = response.json()['files']
        return (
            json.loads(files['recapise.json']['content'])['recipes'],
            json.loads(files['not allowed.json']['content']),
            json.loads(files['vibes.json']['content'])['vibes']
        )
    except:
        st.error("שגיאה בטעינת נתונים מה-Gist")
        return [], {}, []

recipes_data, not_allowed, vibes = load_all_data()

# --- לוגיקת סינון מחמירה ---
def is_approved_by_leptin(recipe):
    forbidden = []
    for cat in not_allowed['forbidden_items_leptin_method'].values():
        forbidden.extend([i['name'].lower() for i in cat['items']])
    ing_str = " ".join(recipe['ingredients']).lower()
    return not any(item in ing_str for item in forbidden)

# --- ממשק ה-App ---
st.header("מה ה-Vibe שלך?")
vibe_names = [v['display_name'] for v in vibes]
# החלפת st.pills ב-st.radio יציב יותר
selected_vibe_name = st.radio("בחר תחושה:", vibe_names, index=0, horizontal=True)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

approved_recipes = [r for r in recipes_data if str(r['id']) in selected_vibe['recipe_ids'] and is_approved_by_leptin(r)]

for recipe in approved_recipes:
    with st.container(border=True):
        st.subheader(recipe['name'])
        st.caption(f"🏆 {recipe['diet_phase']}")
        
        # --- Visual Meter (50/25/25) ללא Plotly ---
        is_main = "מנה עיקרית" in recipe['category']
        
        st.write("**איזון צלחת לפטיני:**")
        # ירקות מנקים (50% או 100%)
        veg_val = 0.5 if is_main else 1.0
        st.write(f"🟢 ירקות מנקים: {int(veg_val*100)}%")
        st.progress(veg_val)
        
        if is_main:
            st.write("🔴 חלבון ופחמימה: 50%")
            st.progress(0.5)
            st.warning("☝️ זכור להוסיף 50% ירקות מנקים טריים לצד המנה")
        
        with st.expander("רכיבים והוראות"):
            for ing in recipe['ingredients']:
                st.write(f"• {ing}")
            st.write(f"**הוראות:** {recipe['instructions']}")

st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    💧 הצפת לפטין | התקדמות, לא שלמות
</div>
""", unsafe_allow_html=True)
