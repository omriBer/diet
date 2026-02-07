import streamlit as st
import json
import requests
import plotly.graph_objects as go

# הגדרות סודיות (בפרודקשן כדאי להשתמש ב-st.secrets)
PASSWORD = "***************"
GITHUB_TOKEN = "*************"
GIST_ID = ""

# --- מנגנון הגנת סיסמה ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("🔐 כניסה למערכת LeptinVibe")
    pwd = st.text_input("הזן סיסמה:", type="password")
    if st.button("התחבר"):
        if pwd == PASSWORD:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("סיסמה שגויה. נסה שוב.")
    return False

if not check_password():
    st.stop()

# --- טעינת נתונים מ-GitHub Gist ---
@st.cache_data(ttl=600)  # רענון כל 10 דקות
def load_data_from_gist():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
    if response.status_code == 200:
        files = response.json()['files']
        # טעינת הקבצים הספציפיים שלך
        recipes = json.loads(files['recapise.json']['content'])['recipes']
        not_allowed = json.loads(files['not allowed.json']['content'])
        vibes = json.loads(files['vibes.json']['content'])['vibes']
        return recipes, not_allowed, vibes
    else:
        st.error("שגיאה בחיבור ל-GitHub Gist. בדוק את ה-Token וה-ID.")
        return [], {}, []

# טעינת הנתונים
recipes_data, not_allowed, vibes = load_data_from_gist()

# --- פונקציות עזר (סינון ומד צלחת) ---
def is_leptin_approved(recipe):
    forbidden_list = []
    # השיטה אוסרת על קמחים, סוכר ומזונות טחונים
    for category in not_allowed['forbidden_items_leptin_method'].values():
        forbidden_list.extend([item['name'].lower() for item in category['items']])
    
    ingredients_str = " ".join(recipe['ingredients']).lower()
    return not any(forbidden in ingredients_str for forbidden in forbidden_list)

# --- ממשק המשתמש (UI) ---
st.title("🥗 LeptinVibe")
st.sidebar.success("מחובר בהצלחה")

# בורר ה-Vibe (Horizontal Pills)
selected_vibe_name = st.pills("איך המרגש עכשיו?", [v['display_name'] for v in vibes], index=0)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

# סינון והצגה
approved_recipes = [r for r in recipes_data if str(r['id']) in selected_vibe['recipe_ids'] and is_leptin_approved(r)]

for recipe in approved_recipes:
    with st.container(border=True):
        col1, col2 = st.columns([1, 1])
        with col1:
            # משיכת תמונה מ-Tasty
            main_ingredient = recipe['ingredients'][0].split()[-1]
            st.image(f"https://source.unsplash.com/400x300/?food,{main_ingredient}", use_container_width=True)
            st.subheader(recipe['name'])
            st.caption(f"📍 {recipe['diet_phase']}")
        
        with col2:
            # מד הצלחת (50% ירקות מנקים, 25% חלבון, 25% פחמימה)
            labels = ['ירקות מנקים', 'חלבון', 'פחמימה']
            values = [50, 25, 25] if "מנה עיקרית" in recipe['category'] else [100, 0, 0]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=['#2ecc71', '#e74c3c', '#f1c40f'])])
            fig.update_layout(showlegend=False, height=150, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        with st.expander("הוראות ורכיבים"):
            for ing in recipe['ingredients']:
                st.write(f"- {ing}")
            st.info(recipe.get('notes', 'אין הערות נוספות'))

# קישור חיצוני ל-Tasty
st.divider()
st.link_button("חיפוש רכיבים ב-Tasty", "https://tasty.co/ingredient")
