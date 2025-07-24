import streamlit as st
import random
import time

# 설정
st.set_page_config(page_title="🃏 같은 그림 맞히기 게임", layout="centered")

# 제목
st.title("🃏 같은 그림 맞히기 게임")
st.caption("30초 안에 모든 그림을 맞혀보세요!")

# 초기 세션 상태
if "cards" not in st.session_state:
    emojis = ["🐶", "🐱", "🐸", "🐵", "🐰", "🐼", "🐯", "🦊"]
    cards = emojis * 2
    random.shuffle(cards)
    st.session_state.cards = cards
    st.session_state.revealed = [False] * 16
    st.session_state.matched = [False] * 16
    st.session_state.selected = []
    st.session_state.flips = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False

# 타이머 계산
elapsed = int(time.time() - st.session_state.start_time)
remaining_time = max(0, 30 - elapsed)

# 게임 종료 처리
if remaining_time == 0 and not st.session_state.game_over:
    st.session_state.game_over = True
    st.warning("⏰ 시간 초과! 게임이 끝났습니다.")

# 타이머 표시
st.subheader(f"⏱ 남은 시간: {remaining_time}초")
st.write(f"🔁 뒤집은 횟수: {st.session_state.flips}")

# 게임판 구성 (4x4)
cols = st.columns(4)
for i in range(16):
    col = cols[i % 4]
    with col:
        if st.session_state.matched[i] or st.session_state.revealed[i]:
            st.button(st.session_state.cards[i], key=f"card{i}", disabled=True)
        else:
            if st.button("❓", key=f"card{i}"):
                if not st.session_state.game_over and len(st.session_state.selected) < 2:
                    st.session_state.revealed[i] = True
                    st.session_state.selected.append(i)
                    st.session_state.flips += 1

# 두 장 선택됐을 때 매칭 처리
if len(st.session_state.selected) == 2:
    idx1, idx2 = st.session_state.selected
    if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
        st.session_state.matched[idx1] = True
        st.session_state.matched[idx2] = True
    else:
        time.sleep(1)
        st.session_state.revealed[idx1] = False
        st.session_state.revealed[idx2] = False
    st.session_state.selected = []

# 모든 매칭 완료 시 게임 승리
if all(st.session_state.matched) and not st.session_state.game_over:
    st.success("🎉 축하합니다! 모든 그림을 맞혔어요!")
    st.session_state.game_over = True

# 게임 다시 시작 버튼
if st.session_state.game_over:
    if st.button("🔄 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
