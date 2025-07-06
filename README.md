# Math Tutor Chatbot

A chat-based math tutor that combines Retrieval-Augmented Generation (RAG) over a curated math Q&A set with conversational logic, confidence support, and a local LLM for re-explanation and motivational feedback. The system is designed to mimic a friendly, knowledgeable human teacher.

---

## Features

- **Retrieval-Augmented Generation (RAG):**
  - Retrieves relevant Q&A pairs from a curated math dataset using vector search (FAISS).
- **Stepwise Explanations:**
  - Splits solutions into logical steps and checks for understanding after each step.
- **Confidence & Motivation Layer:**
  - Detects low confidence or negative sentiment and injects motivational messages.
- **LLM-Powered Re-explanation:**
  - Uses a local LLM (Ollama) to re-explain steps or handle unknown inputs, with context from recent conversation.
- **No Repeat Questions:**
  - Tracks which questions have been asked and avoids repeats until all are completed.
- **Session-Aware:**
  - Maintains conversation state, history, and context for each user session.
- **Streamlit UI:**
  - Simple, modern chat interface with the input bar at the bottom.

---

## Architecture

```
User (Streamlit UI)
   |
   |  (POST /chat)
   v
FastAPI Backend (api.py)
   |
   |  (HTTP API)
   v
Ollama Local LLM (deepseek-r1:1.5b or other)
```

- **Frontend:** Streamlit app for chat UI.
- **Backend:** FastAPI app for all chat logic, session management, and LLM orchestration.
- **LLM:** Local model served by Ollama, used for re-explanation, unknown input handling, and motivational feedback.

---

## Setup

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install Python Dependencies
```
pip install -r requirements.txt
```

### 3. Install and Run Ollama
- [Download and install Ollama](https://ollama.com/download)
- Pull and run the model (e.g., deepseek-r1:1.5b):
```
ollama pull deepseek-r1:1.5b
ollama serve
```

### 4. Prepare the Math Q&A Dataset
- Place your curated Q&A pairs in `data/math_qa.json` (see the provided sample format).

---

## Running the App

### 1. Start the FastAPI Backend
```
uvicorn api:app --reload --port 8001
```

### 2. Start the Streamlit Frontend
```
streamlit run streamlit_app.py
```

### 3. Open the App
- Go to [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage
- Type your math question or respond to the tutor's prompts.
- Say "yes" to proceed to the next step, "no" to get a re-explanation, or "exit" to end the chat.
- Any other input will be handled by the LLM with full context and motivational support.
- The tutor will avoid repeating questions until all have been asked.

---

## Component Explanations

### **1. RAG Pipeline (`tutor/rag.py`)**
- Loads Q&A pairs from `data/math_qa.json`.
- Embeds questions using SentenceTransformers.
- Stores embeddings in a FAISS index for fast similarity search.
- Retrieves top-k most relevant Q&A pairs for a user query.

### **2. Tutor Flow Manager (`tutor/flow_manager.py`)**
- Splits answers into steps.
- Provides prompts for each step.
- Offers rephrasing and encouragement.

### **3. Confidence Layer (`tutor/confidence.py`)**
- Detects low-confidence phrases and negative sentiment using keywords and a HuggingFace sentiment model.

### **4. Messaging Templates (`tutor/templates.py`)**
- Stores and manages tutor personality, encouragement, and prompts.

### **5. LLM Orchestration (`tutor/llm_rephrase.py`)**
- All LLM calls use `tutor_llm_response`, which:
  - Receives the current question, previous explanation, user input, and recent conversation context.
  - Uses a detailed, conversational prompt to generate a supportive, human-like response.
  - Calls the local LLM via Ollama's HTTP API.

**Prompt Example:**
```
Explain in a way that sounds like a person is talking out loud, like a teacher or tutor explaining it to a student in real time. Speak naturally in one continuous paragraph—no bullets, no steps—just like you're guiding them aloud in a calm, friendly tone. Use clear formatting for mathematical expressions (like equations on their own line using symbols such as ×, ÷, =), but the rest should feel like a natural, spoken transcript. You're a warm, emotionally-aware, and highly dedicated math tutor. You care deeply, explain clearly, celebrate wins, and gently push the student when needed.

Current math question: '{question}'
Your last explanation: '{previous_output}'
Student's latest reply: '{user_input}'
Recent student messages: {last_user_inputs}
Your recent replies: {last_tutor_outputs}

Now respond in a way that:
- If the student said 'No' or seems confused, **do not repeat** the same explanation word-for-word—rephrase it in simpler terms.
- Add a basic **real-world analogy** or **small example** if helpful.
- If they got it right, celebrate! Say things like 'Yes! That's exactly right!' or 'You nailed it!'
- If they're trying but struggling, encourage them and go slower.
- If they seem checked out or giving up, gently but firmly call it out—use phrases like 'You're better than this' or 'Come on, I know you've got this.'
- Ask 'Does this make sense so far? (Yes/No)' after each logical checkpoint unless they're too overwhelmed.
- If they said 'No', end with a warm check-in like: 'Is that clearer now?' or 'Want to try a simpler example together?'

Above all, make the student feel supported, safe to ask questions, and confident they can learn this—you're a real teacher, not a script.
```

### **6. FastAPI Backend (`api.py`)**
- Exposes a `/chat` endpoint for all chat logic.
- Handles session state, stepwise explanations, branching, and LLM orchestration.
- Avoids repeating questions until all have been asked.

### **7. Streamlit Frontend (`streamlit_app.py`)**
- Provides a chat UI with the input bar at the bottom.
- Tracks session state, history, and conversation context.
- Hides any `<think>...</think>` blocks from LLM output before displaying to the user.

---

## File Structure

```
├── api.py                # FastAPI backend
├── streamlit_app.py      # Streamlit frontend
├── requirements.txt      # Python dependencies
├── data/
│   └── math_qa.json      # Math Q&A dataset
├── tutor/
│   ├── rag.py            # RAG pipeline
│   ├── flow_manager.py   # Stepwise flow logic
│   ├── confidence.py     # Confidence/sentiment detection
│   ├── templates.py      # Messaging templates
│   └── llm_rephrase.py   # LLM orchestration and prompt
└── README.md             # This file
```

---

## License
MIT # Math-Tutor-AI
