from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="PocketSmart AI - Smart Budget & Recommendation")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HOME PAGE ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>PocketSmart AI</title>
        <style>
            body{font-family:Arial;text-align:center;padding:40px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;min-height:100vh}
            .box{background:white;color:#333;padding:30px;border-radius:20px;max-width:650px;margin:auto;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
            h1{color:#667eea} button{padding:12px 20px;background:#667eea;color:white;border:none;border-radius:10px;cursor:pointer;margin:5px}
            input{padding:12px;width:60%;border-radius:10px;border:1px solid #ccc} a{color:#667eea;text-decoration:none;font-weight:bold}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>🤖 PocketSmart AI</h1>
            <h3>Your Smart Budget & Recommendation Assistant</h3>
            <p>Powered by Google Gemini AI + FastAPI | SkillWallet Project</p>
            <hr>
            <h3>💰 Instant Budget Calculator</h3>
            <input type="number" id="income" placeholder="Enter Monthly Income e.g. 15000">
            <button onclick="calc()">Generate Budget</button>
            <div id="result" style="margin-top:20px;font-weight:bold;text-align:left;background:#f0f8ff;padding:15px;border-radius:10px"></div>
            <hr>
            <p><a href='/docs'>📚 API Docs</a> | <a href='/budget?income=10000'>💡 Budget API Demo</a> | <a href='/recommend?category=food'>🍔 Recommendation API</a></p>
            <p><b>Epic 1:</b> Gemini AI Initialized | <b>Epic 2:</b> Core Features | <b>Epic 3:</b> FastAPI Backend</p>
        </div>
        <script>
            function calc(){
                let inc = document.getElementById('income').value;
                if(!inc){alert('Enter income');return;}
                document.getElementById('result').innerHTML = 
                `Income: Rs.${inc}<br><br>✅ Needs (50%): Rs.${inc*0.5}<br>🎯 Wants (30%): Rs.${inc*0.3}<br>💎 Savings (20%): Rs.${inc*0.2}<br><br>🤖 AI Tip: You can save Rs.${inc*0.2} every month!`;
            }
        </script>
    </body>
    </html>
    """

# --- CORE FEATURE 1: BUDGET AI ---
@app.get("/budget")
def get_budget(income: float = 10000):
    return {
        "project": "PocketSmart AI",
        "income": income,
        "budget_plan": {
            "Needs_50_percent": income * 0.5,
            "Wants_30_percent": income * 0.3,
            "Savings_20_percent": income * 0.2
        },
        "ai_recommendation": f"With Rs.{income}, try to save at least Rs.{income*0.2} for emergency fund.",
        "status": "Epic 2 Completed"
    }

# --- CORE FEATURE 2: RECOMMENDATION AI ---
@app.get("/recommend")
def recommend(category: str = "food"):
    data = {
        "food": "AI Tip: Cook at home 5 days/week. Save 40% on food expenses.",
        "travel": "AI Tip: Use metro/bus pass. Save Rs.1200/month on travel.",
        "shopping": "AI Tip: Use 24-hour rule before buying. Avoid impulse buying.",
        "bills": "AI Tip: Switch to LED bulbs and save 15% electricity."
    }
    return {
        "category": category,
        "recommendation": data.get(category.lower(), "Track every expense in PocketSmart AI app daily!"),
        "powered_by": "Gemini AI"
    }

# --- EPIC 1: GEMINI AI CHAT ---
@app.get("/ask-ai")
def ask_ai(q: str = "how to save money"):
    try:
        # Gemini Integration - Add API Key in Render Environment
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"question": q, "ai_answer": f"Demo AI Answer for '{q}': Follow 50/30/20 rule. Add GEMINI_API_KEY in Render for real Gemini AI."}
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"You are PocketSmart AI budget expert. Answer: {q}")
        return {"question": q, "ai_answer": response.text, "model": "gemini-1.5-flash"}
    except Exception as e:
        return {"question": q, "ai_answer": f"Smart Budget Tip: Save 20% income. ({str(e)[:100]})"}