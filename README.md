# 📈 Morning Market Assistant (GenAI)

An AI-powered market assistant that accepts **text or voice queries** and returns
a **natural language market summary**, **latest stock data**, **news insights**,
and **voice output**.

The system is designed to handle **real-world user inputs** such as brand names,
subsidiaries, typos, and mixed geography (US + India markets).

---

## 🚀 Features

- 🎙️ **Voice & Text Input**
- 🔊 **Voice Response with Stop Control**
- 🧠 **LLM-based understanding of market queries**
- 📊 **Live stock prices using Yahoo Finance**
- 📰 **Latest news headlines**
- 🌍 **Supports US & Indian markets (NSE / BSE)**
- 🧩 **Handles subsidiaries and brand names (e.g., WhatsApp → Meta)**
- ⚡ **FastAPI backend**
- 🖥️ **Simple, user-friendly Web UI**

---

## 🧠 High-Level Architecture

User (Text / Voice)
↓
Speech-to-Text (Whisper)
↓
LLM (Groq - LLaMA)
↓
Ticker Resolution Engine
↓
Market Data (yfinance)
↓
News Fetching
↓
LLM Summary Generation
↓
Text + Voice Output


---

## 🔍 How Ticker Resolution Works (Important)

User queries often contain:
- brand names (WhatsApp, Jio)
- subsidiaries (Google India)
- abbreviations (TCS, TATA)
- typos

To handle this, the system uses a **hybrid resolution strategy**:

1. **LLM extracts possible tickers**
2. **Market validation using real stock data**
3. **Parent-company inference (fallback only)**
4. **Exchange-aware resolution**
   - India: NSE first (`.NS`), then BSE (`.BO`)
   - US: NASDAQ / NYSE symbols

Only tickers that return **real market data** are used.

This avoids hallucinations and false matches.

---

## 🧪 Example Queries

| User Input | System Behavior |
|----------|----------------|
| `Tesla, Microsoft` | Direct US stock resolution |
| `TCS, Wipro` | NSE/BSE-aware Indian stocks |
| `WhatsApp stock` | Maps to Meta |
| `Reliance Jio share price` | Maps to Reliance Industries |
| `Flipkart share price` | Explained as private company |

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**
- **Groq LLaMA models**
- **Yahoo Finance (yfinance)**
- **Whisper (local speech-to-text)**
- **gTTS (text-to-speech)**

### Frontend
- HTML
- CSS
- Vanilla JavaScript

---

## 📁 Project Structure  

morning_market_assistant/
│
├── app/
│ ├── agents/
│ ├── controllers/
│ ├── services/
│ └── main.py
│
├── frontend/
│ ├── index.html
│ ├── script.js
│ └── style.css
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd morning_market_assistant

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows


3️⃣ Install dependencies
pip install -r requirements.txt


4️⃣ Set environment variables

Create a .env file (DO NOT commit it):

GROQ_API_KEY=your_groq_api_key_here


5️⃣ Run the application
uvicorn app.main:app --reload


Open in browser:

http://127.0.0.1:8000/ui


🎙️ Voice Support Notes

Whisper runs locally (on-premise, free)
Requires FFmpeg installed on the system
Voice response can be stopped mid-playback

⚠️ Known Limitations (Honest & Important)
Private companies do not have stock prices
Parent-company mapping is limited to well-known brands
News is fetched from public sources and may be rate-limited
Market data depends on Yahoo Finance availability

🧭 Future Improvements

Hybrid Company Master Database
Caching for faster responses
Charts & technical indicators
User portfolio tracking
Multilingual support
Better brand-to-parent inference

🌐 Deployment

Planned deployment:
Hugging Face Spaces (FastAPI)
The project is structured to be easily deployable.


📜 License

This project is for educational and demonstration purposes.
