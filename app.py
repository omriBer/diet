import streamlit as st
import json
import requests

st.set_page_config(page_title="LeptinVibe", layout="wide")

# --- אימות סיסמה ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 LeptinVibe Login")
    pwd = st.text_input("סיסמה", type="password")
    if st.button("כניסה"):
        if pwd == st.secrets.get("PASSWORD", "wTn6bLdrZT7gEHu"):
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("סיסמה שגויה")
    st.stop()

# --- טעינת נתונים מרוחקת ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        headers = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}
        response = requests.get(f"https://api.github.com/gists/{st.secrets['GIST_ID']}", headers=headers)
        
        if response.status_code != 200:
            st.error(f"GitHub Error {response.status_code}: {response.text}")
            return None, None, None
            
        files = response.json().get('files', {})
        
        # בדיקה אם שמות הקבצים קיימים ב-Gist
        # שים לב: שמות הקבצים ב-Gist חייבים להיות בול כמו כאן
        if 'recapise.json' not in files or 'vibes.json' not in files:
            st.error(f"קבצים חסרים ב-Gist! נמצאו רק: {list(files.keys())}")
            return None, None, None

        recipes = json.loads(files['recapise.json']['content'])['recipes']
        not_allowed = json.loads(files['not allowed.json']['content'])
        vibes = json.loads(files['vibes.json']['content'])['vibes']
        return recipes, not_allowed, vibes
    except Exception as e:
        st.error(f"שגיאה כללית: {str(e)}")
        return None, None, None

recipes_data, not_allowed, vibes = load_all_data()

# --- מניעת קריסה אם הנתונים לא נטענו ---
if not vibes:
    st.warning("המערכת מחכה לנתונים מ-GitHub...")
    st.stop()

# --- המשך הלוגיקה (Vibes וסינון) ---
st.header("מה ה-Vibe שלך?")
vibe_names = [v['display_name'] for v in vibes]
selected_vibe_name = st.radio("בחר תחושה:", vibe_names, horizontal=True)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

# סינון מחמיר (קמח/סוכר/פירות אסורים)
forbidden = []
for cat in not_allowed['forbidden_items_leptin_method'].values():
    forbidden.extend([i['name'].lower() for i in cat['items']])

def is_approved(recipe):
    ing_text = " ".join(recipe['ingredients']).lower()
    return not any(f in ing_text for f in forbidden)

approved_recipes = [r for r in recipes_data if str(r['id']) in selected_vibe['recipe_ids'] and is_approved(r)]

for recipe in approved_recipes:
    with st.container(border=True):
        st.subheader(recipe['name'])
        # מד צלחת 50/25/25
        st.write("🟢 ירקות מנקים: 50% | 🔴 חלבון: 25% | 🟡 פחמימה: 25%")
        st.progress(0.5) 
        with st.expander("רכיבים והוראות"):
            st.write(recipe['instructions'])

st.divider()
st.caption("💧 הצפת לפטין | התקדמות, לא שלמות")
