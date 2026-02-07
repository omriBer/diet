import streamlit as st
import json
import plotly.graph_objects as go

# הגדרות דף Mobile-First
st.set_page_config(page_title="LeptinVibe", layout="wide", initial_sidebar_state="collapsed")

# טעינת נתונים בטוחה
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

recipes_data = load_json('recapise.json')['recipes']
not_allowed = load_json('not allowed.json')
vibes = load_json('vibes.json')['vibes'] # בהתבסס על המבנה שהגדרנו

# פונקציית סינון מחמירה
def is_leptin_approved(recipe):
    forbidden_list = []
    for category in not_allowed['forbidden_items_leptin_method'].values():
        forbidden_list.extend([item['name'].lower() for item in category['items']])
    
    ingredients_str = " ".join(recipe['ingredients']).lower()
    for forbidden in forbidden_list:
        if forbidden in ingredients_str:
            return False
    return True

# כותרת ואווירה
st.title("🥗 LeptinVibe")
st.markdown("##### בחירת מתכון לפי Vibe ואיזון צלחת")

# 1. Vibe Selector (סליידר אופקי של Pills)
selected_vibe_name = st.pills("איך המרגש עכשיו?", [v['display_name'] for v in vibes], index=0)
selected_vibe = next(v for v in vibes if v['display_name'] == selected_vibe_name)

# 2. סינון המתכונים לפי ה-Vibe והחוקים
approved_recipes = [r for r in recipes_data if str(r['id']) in selected_vibe['recipe_ids'] and is_leptin_approved(r)]

# 3. תצוגת המתכונים (Grid)
for recipe in approved_recipes:
    with st.container(border=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # תמונה מ-Tasty (מבוסס על רכיב ראשון)
            main_ingredient = recipe['ingredients'][0].split()[-1]
            tasty_img = f"https://tasty.co/ingredient/{main_ingredient}"
            st.image(f"https://source.unsplash.com/400x300/?food,{main_ingredient}", use_column_width=True) # דוגמה ויזואלית
            st.subheader(recipe['name'])
            st.caption(f"📍 {recipe['diet_phase']}")
            
        with col2:
            # 4. ה-Visual Meter (50/25/25)
            # לוגיקה פשוטה: אם המתכון הוא 'מנה עיקרית' נניח שהוא חלבון, אם 'סלט' הוא ירק
            labels = ['ירקות מנקים', 'חלבון', 'פחמימה לפטינית']
            values = [0, 0, 0]
            
            if "סלט" in recipe['category'] or "ירק" in recipe['category']:
                values = [50, 0, 0]
            elif "מנה עיקרית" in recipe['category']:
                values = [0, 25, 25]
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, 
                                        marker_colors=['#2ecc71', '#e74c3c', '#f1c40f'])])
            fig.update_layout(showlegend=False, height=150, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            
            # התרעה חכמה
            if values[0] == 0:
                st.warning("⚠️ חסרים ירקות מנקים להשלמת הצלחת!")

        # Tap expander (במקום gesture מורכב ב-Streamlit)
        with st.expander("הוראות הכנה ורכיבים"):
            st.write("**רכיבים:**")
            for ing in recipe['ingredients']:
                st.write(f"- {ing}")
            st.write(f"**הוראות:** {recipe['instructions']}")
            if 'notes' in recipe:
                st.info(recipe['notes'])

# 5. קישור ל-Tasty
st.divider()
st.link_button("חפש השראה נוספת ב-Tasty", "https://tasty.co/ingredient")
