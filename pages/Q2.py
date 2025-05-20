import streamlit as st
from models import sentences, skipgram_model, most_similar_words, sentence_similarity_rank

st.set_page_config(page_title="Q2 · Skip-gram")
st.title("Q2 · Skip-gram")

# 頁面說明
st.markdown("""  
1. 輸入單字 → 看最相似單字  
2. 輸入\四句子 → 看最像的三句原始句子  
""")

# 顯示十句原始句子
with st.expander("點我看 10 句原始句子"):
    for i, s in enumerate(sentences, 1):
        st.markdown(f"**S{i}**．{s}")

# user prompt
user_text = st.chat_input("Enter a word or a sentence")
if not user_text:
    st.info("下方輸入文字來看結果")
    st.stop()

if len(user_text.split()) == 1:
    # 當成單字
    sims = most_similar_words(skipgram_model, user_text)
    st.write(f"Top-10 words similar to **{user_text}**:")
    st.table(sims)
else:
    # 當成一句話
    rank = sentence_similarity_rank(skipgram_model, user_text)
    st.write("最類似的原始句子：")
    for s, score in rank[:3]:
        st.markdown(f"- {s}  _(cos = {score:.2f})_")
