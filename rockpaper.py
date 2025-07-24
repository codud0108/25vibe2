import streamlit as st
import random

# 이모지 매핑
emoji_map = {
    "가위": "✌️",
    "바위": "✊",
    "보": "🖐️"
}

# 페이지 설정
st.set_page_config(page_title="비겨야 이기는 가위바위보", page_icon="✊", layout="centered")
st.title("✊ 비겨야 이기는 가위바위보")
st.caption("💡 비겨야만 승리! 50점 넘으면 성공, 0점이면 실패!")

# 사용자 이름 입력
username = st.text_input("🙋 사용자 이름을 입력하세요:", value="guest").strip()

if not username:
    st.warning("이름을 입력해주세요.")
    st.stop()

# 사용자별 점수 상태 초기화
if "users" not in st.session_state:
    st.session_state.users = {}

if username not in st.session_state.users:
    st.session_state.users[username] = {
        "score": 15,   # ✅ 초기 점수 15점
        "win": 0,
        "lose": 0,
        "game_over": False  # 게임 종료 여부
    }

user_data = st.session_state.users[username]

# 게임 종료 시 처리
if user_data["game_over"]:
    st.markdown("---")
    if user_data["score"] <= 0:
        st.error("게임 오버! 점수가 0점이 되었습니다. 😭")
        st.write("😢 😭 😢 😭 😢 😭 😢 😭 😢")
    elif user_data["score"] >= 50:
        st.success("축하합니다! 50점 이상으로 클리어! 🎉")
        st.balloons()
    st.stop()

# 게임 선택 UI
choices = ["가위", "바위", "보"]
user_choice = st.radio("🎮 당신의 선택은?", choices, horizontal=True)

if st.button("🎲 결과 보기"):
    ai_choice = random.choice(choices)

    st.markdown("### 📢 결과")
    st.write(f"🤖 챗GPT의 선택: **{ai_choice} {emoji_map[ai_choice]}**")
    st.write(f"🙂 당신의 선택: **{user_choice} {emoji_map[user_choice]}**")

    if user_choice == ai_choice:
        st.success("🎉 비겼습니다! 당신의 승리입니다! (+5점)")
        user_data["score"] += 5
        user_data["win"] += 1
    else:
        st.error("😢 비기지 못했네요. 당신의 패배입니다. (-3점)")
        user_data["score"] -= 3
        user_data["lose"] += 1

    # 게임 종료 조건 확인
    if user_data["score"] <= 0 or user_data["score"] >= 50:
        user_data["game_over"] = True
        st.experimental_rerun()

# 점수 및 기록 출력
st.markdown("---")
st.subheader(f"📊 {username}님의 전적")
st.write(f"✅ 승리 (비긴 횟수): {user_data['win']}회")
st.write(f"❌ 패배: {user_data['lose']}회")
st.write(f"💯 현재 점수: **{user_data['score']}점**")

# 점수 초기화
if st.button("🧹 내 점수 초기화"):
    user_data["score"] = 15
    user_data["win"] = 0
    user_data["lose"] = 0
    user_data["game_over"] = False
    st.info("점수가 초기화되었습니다.")
