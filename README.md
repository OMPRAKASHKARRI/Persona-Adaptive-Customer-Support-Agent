# Persona-Adaptive Customer Support Agent

An AI-powered customer support agent that adapts its responses based on customer persona, retrieves relevant knowledge from a support knowledge base using Retrieval-Augmented Generation (RAG), and escalates unresolved or sensitive issues to a human support representative.

Built as part of the Adsparkx AI Engineering Internship Assignment.

---

## Project Overview

This system automatically:

- Detects customer persona
- Retrieves relevant support documentation
- Generates persona-aware responses
- Escalates sensitive or unresolved issues
- Produces structured human handoff summaries

The application supports both:

- Interactive CLI Chatbot
- Streamlit Web Interface

---

## Features

### Persona Detection

Supports three customer personas:

#### Technical Expert

Characteristics:

- Uses technical terminology
- Requests logs, APIs, configurations
- Wants detailed troubleshooting

Example:

```text
Can you explain why my API authentication returns 401?
```

---

#### Frustrated User

Characteristics:

- Emotional language
- Repeated complaints
- Urgent requests

Example:

```text
Nothing works! I've tried resetting my password five times.
```

---

#### Business Executive

Characteristics:

- Outcome-focused
- Interested in business impact
- Prefers concise communication

Example:

```text
How does this issue impact operations and when will it be resolved?
```

---

### Retrieval-Augmented Generation (RAG)

The system:

- Loads support documents
- Chunks documents
- Generates embeddings
- Stores vectors in ChromaDB
- Retrieves top-k relevant chunks

---

### Adaptive Response Generation

Responses change according to detected persona.

| Persona | Response Style |
|----------|---------------|
| Technical Expert | Detailed, technical, troubleshooting-focused |
| Frustrated User | Empathetic, simple, reassuring |
| Business Executive | Concise, impact-focused, outcome-driven |

---

### Escalation Logic

Conversations are escalated when:

- Billing issues occur
- Refund requests occur
- Legal or sensitive requests occur
- Retrieval confidence is low
- User dissatisfaction persists

---

### Human Handoff Summary

Structured escalation summary includes:

- Persona
- User issue
- Conversation history
- Documents used
- Attempted actions
- Recommended next steps

---

## Tech Stack

### Backend

- Python 3.14

### LLM

- Google Gemini 2.5 Flash

### Embeddings

- Sentence Transformers
- all-MiniLM-L6-v2

### Vector Database

- ChromaDB

### Frameworks

- Streamlit
- LangChain Text Splitters

### Document Processing

- PyPDF

---

## Architecture Diagram

```text
┌──────────────────┐
│    User Query    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Persona Detector │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   RAG Pipeline   │
│ ChromaDB + KB    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Response Engine  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Escalation Check │
└─────┬──────┬─────┘
      │      │
      ▼      ▼
 Response  Human Handoff
           Summary
```

---

## Project Structure

```text
persona-support-agent/

├── data/
│   ├── api_authentication.md
│   ├── billing_policy.txt
│   ├── database_sync.md
│   ├── login_issues.md
│   ├── refund_policy.txt
│   ├── password_reset_guide.pdf
│   └── ...

├── src/
│   ├── classifier.py
│   ├── rag_pipeline.py
│   ├── generator.py
│   ├── escalator.py
│   └── config.py

├── app.py
├── cli_chat.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Persona Detection Strategy

A Gemini-powered classifier identifies customer persona based on:

- Technical terminology
- Emotional language
- Business-oriented language

A rule-based fallback classifier is also implemented to ensure reliability when API limits are reached.

---

## RAG Pipeline Design

### Document Loading

Supported formats:

- Markdown
- TXT
- PDF

### Chunking Strategy

- Recursive Character Text Splitter
- Configurable chunk size
- Configurable overlap

### Embeddings

Model:

```text
all-MiniLM-L6-v2
```

### Vector Database

```text
ChromaDB
```

### Retrieval

Top-K semantic retrieval based on query embeddings.

---

## Escalation Logic

The system escalates when:

- Refund requests appear
- Billing issues appear
- Legal issues appear
- Retrieval confidence is low
- Multiple failed attempts occur

---

## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd persona-support-agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```text
.env
```

Add:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Running the Application

### Streamlit UI

```bash
streamlit run app.py
```

### CLI Chatbot

```bash
python cli_chat.py
```

---

## Example Queries

### Technical Expert

```text
Can you explain why my API authentication returns 401?
```

### Frustrated User

```text
Nothing works! I've tried resetting my password five times.
```

### Business Executive

```text
How does this issue impact operations and when will it be resolved?
```

### Escalation Example

```text
I want a refund immediately.
```

---

## Known Limitations

- Gemini API quota limits may affect response generation.
- Retrieval quality depends on knowledge base coverage.
- Limited conversation memory.
- Basic confidence estimation.

---

## Future Improvements

- LangGraph workflow orchestration
- Multi-turn memory
- Sentiment analysis
- Analytics dashboard
- Human approval workflow
- Advanced confidence scoring

---

## Author

Omprakash Karri

Adsparkx AI Engineering Internship Assignment
