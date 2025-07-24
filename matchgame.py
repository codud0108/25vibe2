import streamlit as st
import random
import time

# 설정
st.set_page_config(page_title="🃏 같은 그림 맞히기 게임", layout="wide")
st.title("🃏 같은 그림 맞히기 게임")
st.caption("2분 30초 안에 카드를 모두 맞히세요! 라운드마다 카드 쌍 수가 2배로 증가합니다.")

# 초기 상태 설정
if "pair_count" not in st.session_state:
    st.session_state.pair_count = 4
    st.session_state.initialized = False
    st.session_state.game_over = False
    st.session_state.stage_clear = False
    st.session_state.final_clear = False

# 최대 쌍 수
MAX_PAIRS = 64

# 라운드 초기화 함수
def init_round():
    pair_count = st.session_state.pair_count
    all_emojis = [
        "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔",
        "🐧", "🐦", "🦉", "🦄", "🐴", "🐗", "🐍", "🐢", "🐬", "🐳", "🦋", "🐞", "🐝", "🐛", "🕷️", "🦂",
        "🐙", "🦑", "🦐", "🦞", "🦀", "🐡", "🐠", "🐟", "🦓", "🦒", "🦘", "🐘", "🦏", "🐪", "🐫", "🦙", "🦥",
        "🦧", "🦨", "🦫", "🦈", "🦭", "🦣", "🦌", "🕊️", "🦅", "🦜", "🦚", "🦢", "🦩", "🦤", "🐇", "🐿️"
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
    st.session_state.rows = (len(cards) // 6)
    st.session_state.initialized = True
    st.session_state.game_over = False
    st.session_state.stage_clear = False

# 초기화가 안 되어있다면 초기화
if not st.session_state.initialized:
    init_round()

# 타이머 설정
TIME_LIMIT = 150
elapsed = int(time.time() - st.session_state.start_time)
remaining_time = max(0, TIME_LIMIT - elapsed)

# 타이머 출력
st.subheader(f"⏱ 남은 시간: {remaining_time}초")
st.write(f"🔁 뒤집은 횟수: {st.session_state.flips}")
st.write(f"📦 현재 쌍 수: {st.session_state.pair_count}쌍 ({st.session_state.pair_count * 2}장)")

# 시간 초과 처리
if remaining_time == 0 and not st.session_state.game_over:
    st.session_state.game_over = True
    st.warning("⏰ 시간 초과! 게임이 끝났습니다.")

# 게임판 출력
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

# 두 장 비교
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

# 모든 쌍 맞췄을 때
if all(st.session_state.matched) and not st.session_state.game_over:
    if st.session_state.pair_count == MAX_PAIRS:
        st.balloons()
        st.success("🎉 최종 클리어! 64쌍을 모두 맞혔어요!")
        st.session_state.final_clear = True
        st.session_state.game_over = True
    else:
        st.success("✅ 다음 단계로 진행합니다!")
        st.session_state.stage_clear = True
        st.session_state.game_over = True

# 다음 라운드로 이동
if st.session_state.stage_clear and not st.session_state.final_clear:
    if st.button("▶ 다음 라운드로!"):
        st.session_state.pair_count *= 2
        st.session_state.initialized = False
        st.experimental_rerun()

# 게임 재시작
if st.session_state.game_over and not st.session_state.stage_clear:
    if st.button("🔄 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
