# 🧠 AI Trip Planner ✈️  
Plan your dream journey in seconds using a LLaMA-powered AI assistant!

> An intelligent, interactive travel itinerary generator built using **LangChain**, **Streamlit**, and **local/offline LLMs (LLaMA 3.2)**.  
> Supports PDF download, custom interests, and multi-day planning with real attractions, food, and culture tips.

---

## 🌟 Features

- 💡 Smart multi-day itinerary planning based on location, days, and interests
- 🗺️ Real places, famous restaurants, hidden gems, and travel suggestions
- ⌛ Time slots (Morning, Afternoon, Evening) for better planning
- 🧾 Downloadable **PDF itinerary**
- 🎨 Beautiful, animated UI using Streamlit + custom CSS
- 🔌 Works **offline with Ollama** or online via **OpenAI API**

---

## 📸 Demo

<img width="1907" height="876" alt="Screenshot 2025-08-07 172749" src="https://github.com/user-attachments/assets/413cbfc5-3454-4109-9b76-d6cf956340ec" />

---

## 🚀 Getting Started

You can run this app with **either a local LLaMA 3.2 model (via Ollama)** or using **OpenAI API**.

---

### 📦 Requirements

- Python 3.10+
- pip
- `ollama` (for local LLaMA)
- Optional: `.env` file with OpenAI key

Install dependencies:

pip install -r requirements.txt

---

### 🧠 Option 1: Using Offline `llama3.2` via Ollama

1. **Install Ollama**  
   [https://ollama.com/download](https://github.com/ollama/ollama)

2. run this command in your terminal

  `ollama run llama3.2`

3. **Test it works**:
  
 ` ollama run llama3.2`

### Option 2: Use OpenAI GPT-4 via API Key
1. Create a .env File in the Project Root
 `OPENAI_API_KEY=your_openai_key_here`

2. Modify trip_backend.py

    Replace this:
 `from langchain_community.llms import Ollama
   llm = Ollama(model="llama3.2")`

   With this:

   `from langchain.chat_models import ChatOpenAI
    from dotenv import load_dotenv
    import os
    load_dotenv()
    llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key=os.getenv("OPENAI_API_KEY")
) `

3. Run the App

   `streamlit run app.py`


