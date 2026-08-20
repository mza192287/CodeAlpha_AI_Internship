import re
from pathlib import Path

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


FAQS = [
    {
        "question": "What is CodeAlpha?",
        "answer": "CodeAlpha is a software development company that provides internship and technology learning opportunities."
    },
    {
        "question": "What is the AI internship about?",
        "answer": "The AI internship provides hands-on experience in AI model development, machine learning workflows, and real-time data processing."
    },
    {
        "question": "How many AI tasks must I complete?",
        "answer": "According to the internship instructions, interns must complete a minimum of two or three tasks, depending on the program requirement."
    },
    {
        "question": "How do I submit my project?",
        "answer": "Complete the assigned project, upload the source code to GitHub using the required repository naming format, and submit the completed task through the provided submission form."
    },
    {
        "question": "What should the GitHub repository be called?",
        "answer": "The internship instructions specify the repository format: CodeAlpha_ProjectName."
    },
    {
        "question": "Do I need to post my project on LinkedIn?",
        "answer": "Yes. The instructions ask interns to share internship status on LinkedIn and post a video explanation of the project with the GitHub repository link."
    },
    {
        "question": "What is a language translation tool?",
        "answer": "It is an application that accepts text, lets the user select source and target languages, sends the text to a translation service, and displays the translated result."
    },
    {
        "question": "What is an FAQ chatbot?",
        "answer": "An FAQ chatbot matches a user's question with the most similar question in a prepared FAQ knowledge base and returns the corresponding answer."
    },
    {
        "question": "Which NLP technique is used in this chatbot?",
        "answer": "This chatbot uses TF-IDF vectorization and cosine similarity to compare the user's question with the stored FAQ questions."
    },
    {
        "question": "What happens if no FAQ matches my question?",
        "answer": "The chatbot returns a helpful fallback message instead of pretending that it knows the answer."
    },
]


def clean_text(text: str) -> str:
    """Normalize text for better similarity matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class FAQChatbot:
    def __init__(self, faqs, threshold=0.25):
        self.faqs = faqs
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        questions = [clean_text(item["question"]) for item in faqs]
        self.matrix = self.vectorizer.fit_transform(questions)

    def get_response(self, user_question: str):
        cleaned = clean_text(user_question)

        if not cleaned:
            return "Please type a question.", 0.0

        query_vector = self.vectorizer.transform([cleaned])
        scores = cosine_similarity(query_vector, self.matrix)[0]

        best_index = scores.argmax()
        best_score = float(scores[best_index])

        if best_score < self.threshold:
            return (
                "I'm sorry, I couldn't find a reliable answer in my FAQ knowledge base. "
                "Please try asking the question in a different way."
            ), best_score

        return self.faqs[best_index]["answer"], best_score


@st.cache_resource
def create_chatbot():
    return FAQChatbot(FAQS)


def main():
    st.set_page_config(
        page_title="CodeAlpha FAQ Chatbot",
        page_icon="🤖",
        layout="centered"
    )

    st.title("🤖 CodeAlpha AI FAQ Chatbot")
    st.caption("NLP-powered FAQ matching using TF-IDF and cosine similarity.")

    chatbot = create_chatbot()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! Ask me anything about the AI internship tasks and submission process."
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_question = st.chat_input("Type your question...")

    if user_question:
        st.session_state.messages.append(
            {"role": "user", "content": user_question}
        )

        answer, score = chatbot.get_response(user_question)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            st.write(answer)

        if score > 0:
            st.caption(f"FAQ similarity score: {score:.2f}")


if __name__ == "__main__":
    main()
