import streamlit as st
from models import sentences, sentence_to_vec, pca_2d, pca_3d, add_point_to_fig

st.set_page_config(page_title="Q1-1 · 2D & 3D")
st.title("Q1-1 · Word2Vec、PCA")

# 頁面說明
st.markdown("""  
- 先用 Skip-gram Word2Vec 將十句話變 50 維向量  
- 再用 PCA 壓到 2D / 3D 畫散佈圖  
- 點越靠近 → 語意越相似  
- 輸入新句子，紅點會顯示它在語意空間的位置
""")

# 顯示十句原始句子
with st.expander("點我看 10 句原始句子"):
    for i, s in enumerate(sentences, 1):
        st.markdown(f"**S{i}**．{s}")

# 畫原始 10 句
fig2d = pca_2d()
fig3d = pca_3d()

# 使用者輸入
new_sent = st.chat_input("Type a sentence to project 👇")
if new_sent:
    vec = sentence_to_vec(new_sent)
    add_point_to_fig(fig2d, vec, label="You")
    add_point_to_fig(fig3d, vec, label="You")

st.subheader("2-D view")
st.plotly_chart(fig2d, use_container_width=True)

st.subheader("3-D view")
st.plotly_chart(fig3d, use_container_width=True)
