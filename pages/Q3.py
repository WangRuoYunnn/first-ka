import streamlit as st
from models import cbow_model, most_similar_words, sentence_similarity_rank

st.set_page_config(page_title="Q3 · CBOW")
st.title("Q3 · CBOW")

user_text = st.chat_input("Enter a word or a sentence")
if not user_text:
    st.info("下方輸入文字來看結果")
    st.stop()

if len(user_text.split()) == 1:
    sims = most_similar_words(cbow_model, user_text)
    st.write(f"Top-10 words similar to **{user_text}**:")
    st.table(sims)
else:
    rank = sentence_similarity_rank(cbow_model, user_text)
    st.write("最類似的原始句子：")
    for s, score in rank[:3]:
        st.markdown(f"- {s}  _(cos = {score:.2f})_")
