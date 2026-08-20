# Task 2 — FAQ Chatbot

## CodeAlpha AI Internship

A professional NLP-based FAQ chatbot built with Python and Streamlit.

### AI/NLP Approach
1. Store a small FAQ knowledge base.
2. Normalize user questions.
3. Convert FAQ questions into TF-IDF vectors.
4. Convert the user's question into the same vector space.
5. Calculate cosine similarity.
6. Return the answer associated with the most similar FAQ.
7. Use a similarity threshold to avoid unreliable answers.

### Features
- Interactive chat interface
- NLP preprocessing
- TF-IDF vectorization
- Cosine similarity matching
- Confidence/similarity score
- Fallback response for unknown questions
- Clean object-oriented implementation
- Cached model for better Streamlit performance

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
streamlit run chatbot.py
```

The browser will open the chatbot interface automatically.
