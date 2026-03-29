## 🧪 Prompt Examples

### ❌ Token-wasting prompt

```
You are a helpful assistant. Please carefully analyze the following request and provide a detailed explanation.

請幫我寫一個 Python 爬蟲。
```

---

### ✅ Optimized prompt

```
寫一個 Python 爬蟲。
```

---

### ❌ Over-engineered prompt

```
You are a professional software engineer. Please carefully read and fully understand the following request and provide a complete answer.

請幫我寫一個 REST API。
```

---

### ✅ Optimized

```
用 FastAPI 寫一個 REST API。
```

---

### 🔥 Extreme case

```
You are a helpful assistant. You must always explain everything step by step in detail.

請幫我寫一個排序演算法。
```

Expected suggestions:

```json
[
  "remove_generic_instruction",
  "remove_politeness_words"
]
```

---

## 🖥 CLI

```bash
python cli/main.py chat.json
```

Example:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello world"
    }
  ]
}
```

---

## 🧠 Philosophy

Less tokens, less money, same result.

---

## 🛣 Roadmap

* VSCode extension
* Multi-model support (Claude / GPT)
* Real tokenizer integration
* Prompt auto-rewrite using LLM
* Token heatmap visualization

---

---

# 🦀 TokenPincher（摳門工程師工具）

讓你用最少的 token，達到最好的效果。

---

## 🚀 專案介紹

TokenPincher 是一個用來分析與優化 LLM prompt 的工具。

目標是：

* 降低 token 使用量
* 節省成本
* 維持輸出品質

---

## ✨ 功能

* Token 計算
* 成本估算
* Prompt 優化
* 建議提示
* CLI + Web UI（React）
* 模組化架構

---

## ▶️ 執行方式

### 1️⃣ 啟動後端

```bash
uvicorn api.server:app --reload
```

---

### 2️⃣ 啟動前端

```bash
cd frontend
npm install
npm run dev
```

打開：

```
http://localhost:5173
```

---

## 🔌 API

### `/analyze`

分析 token 使用量

### `/optimize`

優化 prompt

---

## 🧪 Prompt 範例

### ❌ 浪費 token

```
You are a helpful assistant. Please carefully analyze the request.

請幫我寫一個 Python 爬蟲。
```

---

### ✅ 優化後

```
寫一個 Python 爬蟲。
```

---

### ❌ 過度描述

```
你是一個非常專業的工程師，請仔細閱讀需求並提供完整解答。

請寫一個 API。
```

---

### ✅ 優化

```
寫一個 API。
```

---

## 🧠 核心理念

少一點 token，多一點智慧。

---

## 🛣 未來規劃

* VSCode 插件
* 多模型支援
* 精準 tokenizer
* 自動 prompt 重寫
* Token 視覺化分析
