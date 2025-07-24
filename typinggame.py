import streamlit as st
import random
import time

# 설정
st.set_page_config(page_title="🃏 같은 그림 맞히기 게임", layout="wide")

st.title("🃏 같은 그림 맞히기 게임")
st.caption("난이도를 선택하고 2분 안에 모든 그림을 맞혀보세요!")

# 초기 상태 설정
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.game_over = False

# 난이도 선택
if not st.session_state.initialized:
    difficulty = st.selectbox("난이도를 선택하세요", ["하", "중", "상"])

    # 난이도에 따른 쌍 개수 설정
    if difficulty == "하":
        pair_count = 18
    elif difficulty == "중":
        pair_count = 36
    else:
        pair_count = 48

    # 카드 생성 및 섞기
    all_emojis = [
        "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
        "🐧", "🐦", "🦉", "🦄", "🐴", "🐗", "🐍", "🐢", "🐬", "🐳", "🦋", "🐞", "🐝", "🐛", "🕷️", "🦂",
        "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🦓", "🦒", "🦘", "🐘", "🦏", "🐪", "🐫", "🦙", "🦥"
    ]

    if pair_count > len(all_emojis):
        st.error("❗ 사용할 수 있는 이모지 개수를 초과했습니다.")
        st.stop()

    selected_emojis = random.sample(all_emojis, pair_count)
    cards = selected_emojis * 2
    random.shuffle(cards)

    st.session_state.cards = cards
    st.session_state.revealed = [False] * len(cards)
    st.session_state.matched = [False] * len(cards)
    st.session_state.selected = []
    st.session_state.flips = 0
    st.session_state.start_time = time.time()
    st.session_state.initialized = True
    st.session_state.rows = (len(cards) // 6)  # 6개씩 열 구성

# 시간 계산
TIME_LIMIT = 120
elapsed = int(time.time() - st.session_state.start_time)
remaining_time = max(0, TIME_LIMIT - elapsed)

# 게임 종료 처리
if remaining_time == 0 and not st.session_state.game_over:
    st.session_state.game_over = True
    st.warning("⏰ 시간 초과! 게임이 끝났습니다.")

# 정보 표시
st.subheader(f"⏱ 남은 시간: {remaining_time}초")
st.write(f"🔁 뒤집은 횟수: {st.session_state.flips}")

# 게임판 구성
cols_per_row = 6
total_cards = len(st.session_state.cards)
for row_idx in range(0, total_cards, cols_per_row):
    row = st.columns(cols_per_row)
    for i in range(cols_per_row):
        card_idx = row_idx + i
        if card_idx >= total_cards:
            break
        with row[i]:
            if st.session_state.matched[card_idx] or st.session_state.revealed[card_idx]:
                st.button(st.session_state.cards[card_idx], key=f"card{card_idx}", disabled=True)
            else:
                if st.button("❓", key=f"card{card_idx}"):
                    if not st.session_state.game_over and len(st.session_state.selected) < 2:
                        st.session_state.revealed[card_idx] = True
                        st.session_state.selected.append(card_idx)
                        st.session_state.flips += 1

# 두 장 선택됐을 때 비교
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

# 모든 매칭 성공 시
if all(st.session_state.matched) and not st.session_state.game_over:
    st.success("🎉 축하합니다! 모든 그림을 맞혔어요!")
    st.session_state.game_over = True

# 다시 시작 버튼
if st.session_state.game_over:
    if st.button("🔄 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
