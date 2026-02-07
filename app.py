import streamlit as st
import json
import requests

# הגדרות סודיות
PASSWORD = "***************"
GITHUB_TOKEN = "*************"
GIST_ID = ""

# --- בדיקת סיסמה ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔐 כניסה ל-LeptinVibe")
    pwd = st.text_input("הזן סיסמה:", type="password")
    if st.button("התחבר"):
        if pwd == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("סיסמה שגויה")
    st.stop()

# --- טעינת נתונים ---
@st.cache_data(ttl=600)
def load_data():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
    if response.status_code == 200:
        files = response.json()['files']
        return (json.loads(files['recapise.json']['content'])['recipes'],
                json.loads(files['not allowed.json']['content']),
                json.loads(files['vibes.json']['content'])['vibes'])
    return [], {}, []

recipes_data, not_allowed, vibes = load_data()

# --- ממשק משתמש ---
st.title("🥗 LeptinVibe")

selected_vibe_name = st.pills("איך המרגש?", [v['display_name'] for v in vibes], index=0)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

# סינון מחמיר נגד קמח וסוכר
def is_approved(recipe):
    forbidden = []
    for cat in not_allowed['forbidden_items_leptin_method'].values():
        forbidden.extend([i['name'].lower() for i in cat['items']])
    ing_text = " ".join(recipe['ingredients']).lower()
    return not any(f in ing_text for f in forbidden)

approved = [r for r in recipes_data if str(r['id']) in selected_vibe['recipe_ids'] and is_approved(r)]

for recipe in approved:
    with st.container(border=True):
        st.subheader(recipe['name'])
        
        # הצגת מד הצלחת באמצעות Progress Bar צבעוני
        if "מנה עיקרית" in recipe['category']:
            st.write("📊 **איזון צלחת לפטיני:**")
            st.write("🟢 ירקות מנקים (50%)")
            st.progress(0.5)
            st.write("🔴 חלבון (25%)")
            st.progress(0.25)
            st.warning("נראה שחסר ירק מנקה להשלמת ה-50%!")
        else:
            st.write("🟢 ירקות מנקים (100%)")
            st.progress(1.0)
            
        with st.expander("למתכון המלא"):
            st.write(recipe['instructions'])
