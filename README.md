# Math Tutor Chatbot

A sophisticated chat-based math tutor that combines Retrieval-Augmented Generation (RAG) over a curated math Q&A dataset with conversational AI, confidence detection, and motivational support. The system mimics a friendly, knowledgeable human teacher who adapts explanations based on student understanding and emotional state.

## 👥 Contributors

- [Kushal Makkar](https://github.com/kushal06-makkar)
- [Aayush Vij](https://github.com/aayushvij04)


## 🎯 Project Overview

This project implements an intelligent math tutoring system that:
- **Retrieves** relevant math problems from a curated dataset using semantic search
- **Explains** solutions step-by-step with interactive checkpoints
- **Detects** student confidence and emotional state
- **Adapts** explanations using a local LLM for personalized learning
- **Motivates** students with encouraging, human-like responses
- **Tracks** session progress to avoid repetition

---

## ✨ Key Features

### 🤖 **Retrieval-Augmented Generation (RAG)**
- **Semantic Search**: Uses FAISS vector database with SentenceTransformers embeddings
- **Curated Dataset**: 100+ high-quality math Q&A pairs with detailed explanations
- **Context-Aware Retrieval**: Finds most relevant problems based on user queries

### 📚 **Stepwise Learning System**
- **Progressive Explanations**: Breaks complex solutions into digestible steps
- **Interactive Checkpoints**: "Does this make sense? (Yes/No)" after each logical unit
- **Adaptive Pacing**: Slows down or speeds up based on student responses

### 🧠 **Intelligent Response System**
- **Confidence Detection**: Identifies low confidence and negative sentiment
- **LLM-Powered Re-explanation**: Uses local Ollama model for personalized responses
- **Context Preservation**: Maintains conversation history for coherent interactions
- **Motivational Support**: Injects encouragement and emotional support

### 🎮 **User Experience**
- **No Repeat Questions**: Tracks asked questions until all are completed
- **Session Persistence**: Maintains state across browser sessions
- **Modern UI**: Clean Streamlit interface with bottom input bar
- **Real-time Responses**: Fast API-based communication

---

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    HTTP API    ┌─────────────────┐
│   Streamlit UI  │ ──────────────► │  FastAPI Backend│ ──────────────► │  Ollama LLM     │
│   (Frontend)    │                 │   (api.py)      │                 │ (deepseek-r1)   │
└─────────────────┘                 └─────────────────┘                 └─────────────────┘
         │                                   │                                   │
         │                                   │                                   │
         ▼                                   ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐                 ┌─────────────────┐
│ Session State   │                 │ RAG Pipeline    │                 │ Local Model     │
│ Chat History    │                 │ FAISS Index     │                 │ HTTP Endpoint   │
│ Progress Track  │                 │ Embeddings      │                 │ 11434 Port      │
└─────────────────┘                 └─────────────────┘                 └─────────────────┘
```

### **Component Breakdown**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Chat UI, session management |
| **Backend** | FastAPI | API endpoints, business logic |
| **RAG Engine** | FAISS + SentenceTransformers | Semantic search, embeddings |
| **LLM** | Ollama (deepseek-r1:1.5b) | Re-explanation, unknown input handling |
| **Confidence** | HuggingFace Transformers | Sentiment analysis, confidence detection |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB+ RAM (for LLM)
- Git

### 1. **Clone and Setup**
```bash
git clone <your-repo-url>
cd math-tutor-chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. **Install Ollama**
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### 3. **Download LLM Model**
```bash
ollama pull deepseek-r1:1.5b
# Alternative models: llama3.2:3b, mistral:7b, codellama:7b
```

### 4. **Start Services**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start FastAPI Backend
uvicorn api:app --reload --port 8001 --host 0.0.0.0

# Terminal 3: Start Streamlit Frontend
streamlit run streamlit_app.py --server.port 8501
```

### 5. **Access the Application**
- Open [http://localhost:8501](http://localhost:8501) in your browser
- Start chatting with the math tutor!

---

## 📖 Detailed Usage Guide

### **Basic Interaction Flow**

1. **Ask a Math Question**
   ```
   User: "How do I solve quadratic equations?"
   Tutor: "Great question! Let me help you understand quadratic equations step by step..."
   ```

2. **Step-by-Step Explanation**
   ```
   Tutor: "First, let's look at the standard form: ax² + bx + c = 0
          Does this make sense so far? (Yes/No)"
   
   User: "Yes"
   Tutor: "Perfect! Now let's talk about the quadratic formula..."
   ```

3. **Handling Confusion**
   ```
   User: "No"
   Tutor: "No worries! Let me explain this differently. Think of it like..."
   ```

4. **Unknown Inputs**
   ```
   User: "I'm feeling frustrated"
   Tutor: "I understand math can be challenging sometimes. Let's take a step back..."
   ```

### **Response Types**

| Input | Response Type | Example |
|-------|---------------|---------|
| `"yes"` | Continue to next step | "Great! Let's move on..." |
| `"no"` | LLM re-explanation | "Let me explain this differently..." |
| `"exit"` | End session | "Thanks for learning with me!" |
| Other text | LLM with context | Personalized motivational response |

---

## ⚙️ Configuration

### **Environment Variables**
Create a `.env` file for customization:

```env
# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:1.5b
LLM_TIMEOUT=30

# RAG Configuration
RAG_TOP_K=3
EMBEDDING_MODEL=all-MiniLM-L6-v2

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
STREAMLIT_PORT=8501

# Confidence Detection
CONFIDENCE_THRESHOLD=0.6
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
```

### **Model Selection**
Different Ollama models offer various trade-offs:

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `deepseek-r1:1.5b` | 1.5B | Fast | Good | Recommended |
| `llama3.2:3b` | 3B | Medium | Better | Higher quality |
| `mistral:7b` | 7B | Slow | Best | Maximum quality |
| `codellama:7b` | 7B | Slow | Best | Math-focused |

### **Customizing the Dataset**
Edit `data/math_qa.json` to add your own problems:

```json
{
  "question": "How do I find the derivative of x²?",
  "answer": "To find the derivative of x², we use the power rule...",
  "steps": [
    "Step 1: Identify the power rule applies",
    "Step 2: Apply d/dx(x^n) = n*x^(n-1)",
    "Step 3: Calculate 2*x^(2-1) = 2x"
  ],
  "difficulty": "beginner",
  "topic": "calculus"
}
```

---

## 🔧 API Documentation

### **Chat Endpoint**
```http
POST /chat
Content-Type: application/json

{
  "message": "How do I solve quadratic equations?",
  "session_id": "user_123",
  "last_user_inputs": ["yes", "no"],
  "last_tutor_outputs": ["Step 1 explanation...", "Step 2 explanation..."]
}
```

**Response:**
```json
{
  "response": "Let me help you with quadratic equations...",
  "session_state": {
    "current_question": "quadratic equations",
    "current_step": 1,
    "asked_indices": [0, 1, 2],
    "total_questions": 100
  },
  "confidence_level": "high",
  "needs_llm": false
}
```

### **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "llm_available": true,
  "rag_loaded": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🛠️ Troubleshooting

### **Common Issues**

#### 1. **Ollama Connection Error**
```
Error: Connection refused to Ollama
```
**Solution:**
```bash
# Check if Ollama is running
ollama list

# Restart Ollama
ollama serve

# Verify port 11434 is open
curl http://localhost:11434/api/tags
```

#### 2. **Model Not Found**
```
Error: Model 'deepseek-r1:1.5b' not found
```
**Solution:**
```bash
# Pull the model
ollama pull deepseek-r1:1.5b

# Or use an alternative
ollama pull llama3.2:3b
```

#### 3. **Memory Issues**
```
Error: CUDA out of memory
```
**Solution:**
- Use smaller models (1.5B instead of 7B)
- Increase system RAM
- Use CPU-only mode: `OLLAMA_HOST=0.0.0.0:11434`

#### 4. **Port Conflicts**
```
Error: Port 8001 already in use
```
**Solution:**
```bash
# Find process using port
lsof -i :8001

# Kill process or use different port
uvicorn api:app --port 8002
```

#### 5. **Import Errors**
```
Error: No module named 'sentence_transformers'
```
**Solution:**
```bash
pip install -r requirements.txt
# Or install individually
pip install sentence-transformers faiss-cpu transformers
```

### **Performance Optimization**

#### **For Faster Responses:**
```python
# Use smaller embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Instead of larger models

# Reduce RAG search scope
RAG_TOP_K = 2  # Instead of 5

# Use faster LLM
OLLAMA_MODEL = "deepseek-r1:1.5b"  # Instead of 7B models
```

#### **For Better Quality:**
```python
# Use larger models
OLLAMA_MODEL = "mistral:7b"

# Increase context window
MAX_CONTEXT_LENGTH = 4096

# Use more sophisticated embeddings
EMBEDDING_MODEL = "all-mpnet-base-v2"
```

---

## 🧪 Testing

### **Unit Tests**
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/ -v
```

### **Integration Tests**
```bash
# Test API endpoints
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "session_id": "test"}'

# Test LLM connection
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-r1:1.5b", "prompt": "Hello"}'
```

### **Load Testing**
```bash
# Install locust
pip install locust

# Run load test
locust -f load_test.py --host=http://localhost:8001
```

---

## 📊 Monitoring and Logging

### **Application Logs**
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### **Performance Metrics**
- **Response Time**: Average LLM response time
- **RAG Hit Rate**: Percentage of successful retrievals
- **User Satisfaction**: Based on "yes/no" responses
- **Session Duration**: Average chat session length

### **Health Monitoring**
```bash
# Check system health
curl http://localhost:8001/health

# Monitor Ollama status
curl http://localhost:11434/api/tags

# Check memory usage
ps aux | grep ollama
```

---

## 🔒 Security Considerations

### **API Security**
- **Rate Limiting**: Implement request throttling
- **Input Validation**: Sanitize user inputs
- **CORS Configuration**: Restrict cross-origin requests
- **Authentication**: Add user authentication if needed

### **Data Privacy**
- **Local Processing**: All data processed locally
- **No External APIs**: No data sent to third parties
- **Session Cleanup**: Automatic session data cleanup
- **Log Rotation**: Implement log file rotation

---

## 🤝 Contributing

### **Development Setup**
```bash
# Fork and clone
git clone https://github.com/your-username/math-tutor-chatbot.git
cd math-tutor-chatbot

# Create feature branch
git checkout -b feature/new-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Format code
black .
isort .

# Submit pull request
```

### **Code Style**
- Follow PEP 8 for Python code
- Use type hints for function parameters
- Add docstrings for all functions
- Write unit tests for new features

### **Pull Request Process**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ollama** for providing the local LLM infrastructure
- **HuggingFace** for the transformer models and embeddings
- **FAISS** for efficient similarity search
- **FastAPI** for the modern web framework
- **Streamlit** for the interactive UI components

---


## 🔄 Changelog

### **v1.0.0** (2024-01-15)
- Initial release
- RAG pipeline with FAISS
- Ollama LLM integration
- Streamlit UI
- Confidence detection
- Session management

### **v0.9.0** (2024-01-10)
- Beta release
- Basic chat functionality
- Template-based responses

---
