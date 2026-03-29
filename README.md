# 🦀 TokenPincher

Save tokens like a stingy engineer.

---

## 🚀 Overview

TokenPincher is a lightweight toolkit for analyzing, estimating, and optimizing LLM prompts.

It helps developers reduce token usage, lower cost, and improve prompt efficiency.

---

## ✨ Features

* Token estimation
* Cost estimation
* Prompt optimization
* Suggestion engine
* CLI + Web UI (React)
* Modular architecture

---

## 🧱 Project Structure

```
token-pincher/
├── backend/token_pincher/
├── api/
├── frontend/        # React app
├── cli/
├── pyproject.toml
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
pip install -e .
```

---

## ▶️ Run

### 1. Start backend

```bash
uvicorn api.server:app --reload
```

---

### 2. Start frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Open:

```
http://localhost:5173
```

---

## 🔌 API

### POST `/analyze`

Estimate token usage and cost.

#### Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "請幫我寫一個 Python 爬蟲"
    }
  ]
}
```

#### Response

```json
{
  "tokens": 42,
  "cost": 0.00012,
  "warnings": []
}
```

---

### POST `/optimize`

Optimize prompt to reduce tokens.

#### Request

```json
{
  "prompt": "You are a helpful assistant. Please carefully analyze this problem and explain it."
}
```

#### Response

```json
{
  "optimized": "Analyze this problem and explain it."
}
```



