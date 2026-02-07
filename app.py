import streamlit as st
import json
import requests

# הגדרות דף Mobile-First
st.set_page_config(page_title="LeptinVibe", layout="wide")

# --- מנגנון אימות סיסמה מה-Secrets ---
def check_password():
    if st.session_state.get("authenticated", False):
        return True

    st.title("🥗 LeptinVibe")
    correct_password = st.secrets["PASSWORD"]
    
    password_input = st.text_input("סיסמה", type="password", key="password_input")

    if st.button("כניסה", use_container_width=True):
        if password_input == correct_password:
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

if not check_password():
    st.stop()

# --- טעינת נתונים מה-Gist ---
@st.cache_data(ttl=300)
def load_data_from_gist():
    try:
        token = st.secrets["GITHUB_TOKEN"]
        gist_id = st.secrets["GIST_ID"]
        headers = {"Authorization": f"token {token}"}
        url = f"https://api.github.com/gists/{gist_id}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        files = response.json().get('files', {})
        
        # טעינת שלושת הקבצים שלך
        recipes = json.loads(files['recapise.json']['content'])['recipes']
        not_allowed = json.loads(files['not allowed.json']['content'])
        vibes = json.loads(files['vibes.json']['content'])['vibes']
        
        return recipes, not_allowed, vibes
    except Exception as e:
        st.error(f"שגיאה בטעינת הנתונים: {e}")
        return None, None, None

recipes, not_allowed, vibes = load_data_from_gist()

if not recipes or not not_allowed or not vibes:
    st.stop()

# --- סינון מחמיר (חוקי הלפטין) ---
def is_approved(recipe, forbidden_data):
    # איסוף מילות מפתח בעברית לסינון
    forbidden_keywords = []
    for cat in forbidden_data['forbidden_items_leptin_method'].values():
        for item in cat['items']:
            forbidden_keywords.extend(item.get('hebrew_keywords', []))

    ing_text = " ".join(recipe['ingredients'])
    return not any(kw in ing_text for kw in forbidden_keywords)

# --- ממשק המשתמש ---
st.header("מה ה-Vibe שלך?")
vibe_names = [v['display_name'] for v in vibes]
selected_vibe_name = st.radio("בחר תחושה:", vibe_names, horizontal=True)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

# סינון והצגה
approved_recipes = [r for r in recipes if str(r['id']) in selected_vibe['recipe_ids'] and is_approved(r, not_allowed)]

for recipe in approved_recipes:
    with st.container(border=True):
        st.subheader(recipe['name'])
        st.caption(f"📅 {recipe['diet_phase']}")
        
        # Visual Meter (50/25/25)
        st.write("**איזון צלחת לפטיני:**")
        is_main = "מנה עיקרית" in recipe['category']
        
        if is_main:
            st.write("🟢 50% ירקות מנקים | 🔴 25% חלבון | 🟡 25% פחמימה")
            st.progress(0.5)
            st.warning("זכור להוסיף 50% ירקות מנקים טריים!")
        else:
            st.write("🟢 100% ירקות מנקים")
            st.progress(1.0)
            st.success("מעולה! זה ירק מנקה חופשי.")

        with st.expander("רכיבים והוראות"):
            for ing in recipe['ingredients']:
                st.write(f"• {ing}")
            st.write(f"**הוראות:** {recipe['instructions']}")
            if 'notes' in recipe:
                st.info(recipe['notes'])

st.divider()
st.link_button("חיפוש השראה נוספת ב-Tasty", "https://tasty.co/ingredient")
