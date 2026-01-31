# 💧 שיטת הלפטין - The Leptin Method Tracker

אפליקציית מעקב יומי לתוכנית הרזיה בשיטת הלפטין.

A Hebrew, mobile-friendly daily tracking app for "The Leptin Method" weight loss program.

## Features / תכונות

### 📊 מעקב יומי
- **💧 הצפת לפטין** - מעקב מים (2-4 ליטר ביום) + כפתור "2 כוסות לפני ארוחה"
- **🥗 ירקות וחלבון** - מעקב אחר 50% ירקות מנקים וחלבון בכל ארוחה
- **⏰ חלון אכילה** - מעקב 8-12 שעות
- **🥑 שומנים מרוכזים** - מגבלה של 2-3 כפות ביום

### 🛤️ לוגיקה דינמית לפי שבוע
- **שבועות 1-2 (ההצפה)** - התמקדות במים וירקות בלבד
- **שבועות 3-7 (הניקוי)** - ללא סוכר, קמח ומזון מעובד
- **שבועות 9-12 (המסלולים)** - בחירה בין מסלול מהיר/ניקוי/מתון

### 🆘 תכונות מיוחדות
- **גלגלי הצלה** - פרוטוקול חירום להתאוששות
- **יום פינוק** - מצב מיוחד עם כללים מותאמים
- **היסטוריה** - צפייה ב-14 ימים אחרונים
- **שמירה אוטומטית** - כל הנתונים נשמרים מקומית

## Installation / התקנה

```bash
# Clone the repository
git clone <repository-url>
cd diet

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Running on Mobile / הרצה בנייד

### Option 1: Local Network (Same WiFi)
```bash
# Run with network access
streamlit run app.py --server.address 0.0.0.0 --server.port 8501

# Find your computer's IP address:
# On Linux/Mac: hostname -I
# On Windows: ipconfig

# Open on mobile: http://YOUR_IP:8501
```

### Option 2: Streamlit Cloud (Free Hosting)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Access from anywhere!

### Option 3: Using ngrok (Temporary Public URL)
```bash
# Install ngrok
pip install pyngrok

# Run streamlit
streamlit run app.py &

# Create tunnel
ngrok http 8501
```

## Usage / שימוש

1. **הגדרה ראשונית** - בחר שבוע נוכחי ומסלול (אם רלוונטי)
2. **מעקב יומי** - רשום צריכת מים, ירקות, חלבון וחלון אכילה
3. **סיום יום** - לחץ "סיים יום" לקבלת סיכום
4. **היסטוריה** - צפה בהתקדמות שלך

## Data Storage / אחסון נתונים

הנתונים נשמרים בקובץ `leptin_data.json` בתיקיית האפליקציה.

## Tech Stack

- **Python 3.8+**
- **Streamlit** - Web framework
- **JSON** - Local data persistence

## License

MIT
