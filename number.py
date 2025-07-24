import streamlit as st
import random

st.set_page_config(page_title="숫자 맞히기 게임", page_icon="🎯")
st.title("🎯 숫자 맞히기 게임")
st.markdown("0부터 100 사이의 숫자 중 제가 하나를 골랐어요. **기회는 5번**! 맞혀보세요!")

# 초기화
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(0, 100)
    st.session_state.tries = 0
    st.session_state.max_tries = 5
    st.session_state.game_over = False
    st.session_state.success = False

# 게임 종료가 아닐 때만 입력 받기
if not st.session_state.game_over:
    user_input = st.number_input("숫자를 입력하세요:", min_value=0, max_value=100, step=1)

    if st.button("제출"):
        st.session_state.tries += 1
        remaining = st.session_state.max_tries - st.session_state.tries

        if user_input < st.session_state.secret_number:
            st.warning(f"너무 작아요! 🔽 (남은 기회: {remaining}번)")
        elif user_input > st.session_state.secret_number:
            st.warning(f"너무 커요! 🔼 (남은 기회: {remaining}번)")
        else:
            st.success(f"🎉 정답입니다! {st.session_state.tries}번 만에 맞췄어요!")
            st.session_state.success = True
            st.session_state.game_over = True

        # 기회 소진 시
        if st.session_state.tries >= st.session_state.max_tries and not st.session_state.success:
            st.error(f"😢 아쉽네요. 기회를 모두 소진했어요. 정답은 {st.session_state.secret_number}였습니다.")
            st.session_state.game_over = True

# 다시 시작 버튼
if st.session_state.game_over:
    if st.button("🔄 다시 시작하기"):
        st.session_state.secret_number = random.randint(0, 100)
        st.session_state.tries = 0
        st.session_state.game_over = False
        st.session_state.success = False
