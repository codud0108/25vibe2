import streamlit as st
import random

st.set_page_config(page_title="비겨야 이기는 가위바위보", page_icon="✊", layout="centered")
st.title("✊ 비겨야 이기는 가위바위보")

# 선택지
choices = ["가위", "바위", "보"]

# 사용자 선택
user_choice = st.radio("당신의 선택은?", choices, horizontal=True)

# 게임 시작 버튼
if st.button("결과 보기"):
    # 컴퓨터 랜덤 선택
    ai_choice = random.choice(choices)

    st.write(f"🤖 챗GPT의 선택: **{ai_choice}**")
    st.write(f"🙂 당신의 선택: **{user_choice}**")

    # 결과 판정: 비기면 승리
    if user_choice == ai_choice:
        st.success("🎉 비겼습니다! 당신의 승리입니다!")
    else:
        st.error("😢 비기지 못했네요. 당신의 패배입니다.")

