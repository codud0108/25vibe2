import streamlit as st
import random

st.set_page_config(page_title="날짜 맞히기 게임", page_icon="📅")
st.title("📅 1월 날짜 맞히기 게임")
st.markdown("1월 1일부터 1월 31일 중 제가 생각한 날짜를 맞혀보세요! 🎯")

# 초기 세션 상태 설정
if "target_date" not in st.session_state:
    st.session_state.target_date = random.randint(1, 31)
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.game_over = False

# 게임 상태
if not st.session_state.game_over:
    user_date = st.number_input("1월 며칠이라고 생각하세요?", min_value=1, max_value=31, step=1)

    if st.button("제출"):
        st.session_state.attempts += 1

        if user_date == st.session_state.target_date:
            st.success(f"정답입니다! 🎉 {user_date}일이 맞습니다!")
            st.session_state.score += 1
            st.session_state.target_date = random.randint(1, 31)  # 새로운 날짜 설정
        else:
            st.warning(f"틀렸어요! 😢 제가 생각한 날짜는 {st.session_state.target_date}일이었어요.")
            st.session_state.target_date = random.randint(1, 31)

        # 시도 횟수 초과 시 게임 종료
        if st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.game_over = True

    st.info(f"현재 점수: **{st.session_state.score}점** / 시도: {st.session_state.attempts}/{st.session_state.max_attempts}")

else:
    st.markdown(f"## 🎮 게임 종료!")
    st.success(f"최종 점수: **{st.session_state.score}점**")
    if st.button("🔁 다시 시작하기"):
        # 초기화
        st.session_state.target_date = random.randint(1, 31)
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.game_over = False
