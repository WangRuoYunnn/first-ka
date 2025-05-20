import streamlit as st
from coding.utils import paging 

def save_lang():
    st.session_state["lang_setting"] = st.session_state.get("language_select")

def sidebar(user_image: str = "https://www.w3schools.com/howto/img_avatar.png"):
    with st.sidebar:
        paging()  # 目錄連結
        selected_lang = st.selectbox(
            "Language",
            ["English", "繁體中文"],
            index=0,
            on_change=save_lang,
            key="language_select",
        )

        # 記錄語系，供頁面其他區塊使用
        if "lang_setting" in st.session_state:
            lang_setting = st.session_state["lang_setting"]
        else:
            lang_setting = selected_lang
            st.session_state["lang_setting"] = lang_setting

        # 大頭貼或其他側邊資訊
        st.container(border=True).image(user_image)

    # 回傳目前語系，讓頁面需要時可用
    return st.session_state["lang_setting"]
