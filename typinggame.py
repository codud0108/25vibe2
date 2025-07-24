import streamlit as st
import random
import time

st.set_page_config(page_title="영어 타자 연습", page_icon="⌨️", layout="centered")
st.title("⌨️ 영어 타자 연습 게임")

tab1, tab2 = st.tabs(["📘 문장 연습", "🟦 단어 연습"])

# 예시 문장 & 단어 데이터
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing practice makes you faster and more accurate.",
    "Streamlit is an amazing tool for building apps.",
    "Keep calm and code in Python.",
    "Practice every day to improve your typing speed."
]

words = [
    "apple", "banana", "computer", "streamlit", "python", "keyboard",
    "education", "practice", "developer", "learning", "accuracy", "typing"
]

# ---------------- 문장 연습 ----------------
with tab1:
    st.subheader("📘 문장 연습")
    
    if "sentence" not in st.session_state:
        st.session_state.sentence = random.choice(sentences)
        st.session_state.s_start = None
        st.session_state.s_end = None
        st.session_state.s_finished = False

    if st.button("🔁 새 문장 받기", key="new_sentence"):
        st.session_state.sentence = random.choice(sentences)
        st.session_state.s_start = None
        st.session_state.s_end = None
        st.session_state.s_finished = False
        st.experimental_rerun()

    st.markdown("**💬 아래 문장을 정확히 입력하세요:**")
    st.code(st.session_state.sentence)

    s_input = st.text_area("✍️ 여기에 입력하세요:", key="sentence_input", height=100)

    if s_input and st.session_state.s_start is None:
        st.session_state.s_start = time.time()

    if st.button("✅ 제출", key="submit_sentence") and s_input:
        st.session_state.s_end = time.time()
        st.session_state.s_finished = True

    if st.session_state.s_finished:
        total_time = round(st.session_state.s_end - st.session_state.s_start, 2)
        correct = sum(1 for a, b in zip(st.session_state.sentence, s_input) if a == b)
        accuracy = round((correct / len(st.session_state.sentence)) * 100, 2)
        typo = sum(1 for a, b in zip(st.session_state.sentence, s_input) if a != b) + abs(len(st.session_state.sentence) - len(s_input))

        st.success("🎉 결과")
        st.write(f"⏱️ 걸린 시간: **{total_time}초**")
        st.write(f"✅ 정확도: **{accuracy}%**")
        st.write(f"❌ 오타 수: **{typo}개**")

# ---------------- 단어 연습 ----------------
with tab2:
    st.subheader("🟦 단어 연습")

    if "word" not in st.session_state:
        st.session_state.word = random.choice(words)
        st.session_state.word_score = 0
        st.session_state.word_total = 0
        st.session_state.word_result = ""

    st.markdown("**🔤 아래 단어를 입력하세요:**")
    st.header(f"`{st.session_state.word}`")

    w_input = st.text_input("✍️ 단어 입력:", key="word_input")

    if st.button("제출", key="submit_word"):
        st.session_state.word_total += 1
        if w_input.strip().lower() == st.session_state.word.lower():
            st.session_state.word_score += 1
            st.session_state.word_result = "✅ 정답입니다!"
        else:
            st.session_state.word_result = f"❌ 오답입니다! 정답은 `{st.session_state.word}`"

        st.session_state.word = random.choice(words)
        st.experimental_rerun()

    if st.session_state.word_result:
        st.info(st.session_state.word_result)
        st.write(f"🏁 점수: **{st.session_state.word_score} / {st.session_state.word_total}**")
