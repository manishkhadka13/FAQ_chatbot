import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 FAQ Chatbot")
st.caption("Ask me anything — I'll find the most relevant answer for you.")

st.divider()

query = st.text_input("Your question", placeholder="e.g. how do I get my money back?")

if st.button("Search", type="primary"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching..."):
            response = requests.post(
                f"{API_URL}/faq/ask",
                json={"query": query}
            )

        if response.status_code == 200:
            data = response.json()
            results = data["results"]

            if results:
                for r in results:
                    with st.container(border=True):
                        st.write(f"**{r['faq']['question']}**")
                        st.write(r["faq"]["answer"])
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if r["faq"]["category"]:
                                st.caption(f"📂 {r['faq']['category']}")
                        with col2:
                            st.caption(f"✅ {round(r['similarity'] * 100)}% match")
            else:
                st.warning(data["message"])
        else:
            st.error("Could not reach the API. Is uvicorn running?")