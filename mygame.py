import streamlit as st
import random
from datetime import datetime

# 별자리 정보
ZODIAC_SIGNS = [
    ("염소자리", (12, 22), (1, 19)),
    ("물병자리", (1, 20), (2, 18)),
    ("물고기자리", (2, 19), (3, 20)),
    ("양자리",   (3, 21), (4, 19)),
    ("황소자리", (4, 20), (5, 20)),
    ("쌍둥이자리", (5, 21), (6, 21)),
    ("게자리",   (6, 22), (7, 22)),
    ("사자자리", (7, 23), (8, 22)),
    ("처녀자리", (8, 23), (9, 22)),
    ("천칭자리", (9, 23), (10, 22)),
    ("전갈자리", (10, 23), (11, 22)),
    ("사수자리", (11, 23), (12, 21)),
]

# 별자리 판단 함수
def get_zodiac(month, day):
    for sign, (start_m, start_d), (end_m, end_d) in ZODIAC_SIGNS:
        if start_m > end_m:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
                return sign
        elif (month == start_m and day >= start_d) or (month == end_m and day <= end_d):
            return sign
    return None

# 랜덤 날짜 생성
def generate_random_date():
    while True:
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        try:
            datetime(2024, month, day)
            return (month, day)
        except:
            continue

# 페이지 설정
st.set_page_config(page_title="별자리 날짜 맞히기 게임", page_icon="🌟")
st.title("🌟 별자리로 날짜 맞히기 게임")
st.write('20번의 기회동안 최대한 많이 맞춰보세요')

# 세션 초기화
if "answer_date" not in st.session_state:
    st.session_state.answer_date = generate_random_date()
    st.session_state.zodiac = get_zodiac(*st.session_state.answer_date)
    st.session_state.tries = 0
    st.session_state.max_tries = 20  # 여기서 기회를 20번으로 설정
    st.session_state.score = 0
    st.session_state.game_over = False

# 게임 진행
if not st.session_state.game_over:
    st.subheader(f"⭐ 힌트: 이 날짜는 **{st.session_state.zodiac}**에 해당합니다!")
    user_month = st.number_input("몇 월인가요?", min_value=1, max_value=12, step=1)
    user_day = st.number_input("몇 일인가요?", min_value=1, max_value=31, step=1)

    if st.button("제출"):
        try:
            datetime(2024, user_month, user_day)
            st.session_state.tries += 1

            if (user_month, user_day) == st.session_state.answer_date:
                st.success("🎉 정답입니다! 날짜를 정확히 맞히셨어요!")
                st.session_state.score += 1
                st.session_state.answer_date = generate_random_date()
                st.session_state.zodiac = get_zodiac(*st.session_state.answer_date)
            else:
                st.warning("❌ 틀렸습니다! 다시 시도해보세요.")

            if st.session_state.tries >= st.session_state.max_tries:
                st.session_state.game_over = True
        except:
            st.error("유효하지 않은 날짜입니다.")

    st.info(f"현재 점수: **{st.session_state.score}점** | 시도: {st.session_state.tries}/{st.session_state.max_tries}")

else:
    st.markdown("## 🎮 게임 종료!")
    answer = st.session_state.answer_date
    st.markdown(f"정답 날짜는 **{answer[0]}월 {answer[1]}일** 이었습니다!")
    st.success(f"최종 점수: **{st.session_state.score}점**")
    if st.button("🔁 다시 시작하기"):
        st.session_state.answer_date = generate_random_date()
        st.session_state.zodiac = get_zodiac(*st.session_state.answer_date)
        st.session_state.tries = 0
        st.session_state.score = 0
        st.session_state.game_over = False

# 별자리표 아래에 출력
st.markdown("---")
st.markdown("### 🗓️ 별자리 날짜표")
for sign, start, end in ZODIAC_SIGNS:
    st.markdown(f"- **{sign}**: {start[0]}월 {start[1]}일 ~ {end[0]}월 {end[1]}일")
