import streamlit as st
import json
import requests
import plotly.graph_objects as go

# הגדרות דף Mobile-First
st.set_page_config(page_title="LeptinVibe", layout="wide", initial_sidebar_state="collapsed")

# --- פונקציית אימות (Login) המסתמכת על Secrets ---
def check_password():
    if st.session_state.get("authenticated", False):
        return True

    st.title("🥗 LeptinVibe")
    
    # שימוש בתיבת טקסט עם מפתח ייחודי
    password = st.text_input("סיסמה", type="password", key="password_input")

    if st.button("כניסה", use_container_width=True):
        # משיכת הסיסמה מה-Secrets (כולל ערך ברירת מחדל לגיבוי)
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

if not check_password():
    st.stop()

# --- טעינת נתונים מ-GitHub Gist באמצעות Secrets ---
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
    except Exception as e:
        st.error(f"שגיאה בטעינת נתונים: וודא ש-GITHUB_TOKEN ו-GIST_ID מוגדרים ב-Secrets")
        return [], {}, []

# טעינת המאגרים
recipes_data, not_allowed, vibes = load_all_data()

# --- לוגיקת סינון מחמירה (חוקי השיטה) ---
def is_approved_by_leptin(recipe):
    forbidden_items = []
    for cat in not_allowed['forbidden_items_leptin_method'].values():
        forbidden_items.extend([i['name'].lower() for i in cat['items']])
    
    ingredients_str = " ".join(recipe['ingredients']).lower()
    return not any(item in ingredients_str for item in forbidden_items)

# --- ממשק ה-App ---
st.header("מה ה-Vibe שלך?")

# סליידר בחירה (Pills)
vibe_display_names = [v['display_name'] for v in vibes]
selected_vibe_name = st.pills("בחר תחושה:", vibe_display_names, index=0)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

# סינון מתכונים
approved_recipes = [
    r for r in recipes_data 
    if str(r['id']) in selected_vibe['recipe_ids'] and is_approved_by_leptin(r)
]

# תצוגת כרטיסיות (Grid)
if not approved_recipes:
    st.info("לא נמצאו מתכונים מתאימים ל-Vibe הזה שתואמים את חוקי השיטה.")
else:
    for recipe in approved_recipes:
        with st.container(border=True):
            col_img, col_info = st.columns([1, 1.2])
            
            with col_img:
                # שימוש בחיפוש רכיבים של Tasty לצורך תמונה
                main_ing = recipe['ingredients'][0].split()[-1]
                st.image(f"https://source.unsplash.com/400x300/?{main_ing},healthy-food", use_container_width=True)
                st.subheader(recipe['name'])
                st.caption(f"🏆 {recipe['diet_phase']}")

            with col_info:
                # Visual Meter (50/25/25)
                is_main = "מנה עיקרית" in recipe['category']
                labels = ['ירקות מנקים', 'חלבון', 'פחמימה']
                # אם זו מנה עיקרית נניח איזון, אם לא נניח ירקות
                vals = [50, 25, 25] if is_main else [100, 0, 0]
                
                fig = go.Figure(data=[go.Pie(labels=labels, values=vals, hole=.6, 
                                            marker_colors=['#2ecc71', '#e74c3c', '#f1c40f'])])
                fig.update_layout(showlegend=False, height=140, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
                
                if not is_main:
                    st.success("🥗 ירקות מנקים - מצוין!")
                else:
                    st.warning("☝️ זכור להוסיף 50% ירקות מנקים")

            with st.expander("לצפייה ברכיבים והוראות"):
                st.write("**רכיבים:**")
                for ing in recipe['ingredients']:
                    st.write(f"• {ing}")
                st.write(f"**הוראות:** {recipe['instructions']}")
                if 'notes' in recipe:
                    st.info(recipe['notes'])

st.divider()
st.markdown(f"🔗 [חפש עוד השראה ב-Tasty](https://tasty.co/ingredient)")
