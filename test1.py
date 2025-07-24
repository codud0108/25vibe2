import streamlit as st
import pandas as pd

st.set_page_config(page_title="학교 시간표 앱", layout="wide")
st.title("📚 학교 시간표 작성기")

# 설정
DAYS = ['월', '화', '수', '목', '금']
PERIODS = [f'{i+1}교시' for i in range(7)]  # 7교시까지

# 학년/반 선택
grade = st.selectbox("학년 선택", options=["1학년", "2학년", "3학년"])
class_num = st.selectbox("반 선택", options=["1반", "2반", "3반"])

st.markdown("---")

# 시간표 입력
st.subheader("✏️ 시간표 입력")

timetable = {}  # 시간표 딕셔너리

for period in PERIODS:
    cols = st.columns(len(DAYS)+1)
    cols[0].markdown(f"**{period}**")
    timetable[period] = []
    for i, day in enumerate(DAYS):
        subject = cols[i+1].text_input(f"{day}요일 {period}", key=f"{day}_{period}")
        timetable[period].append(subject)

# 데이터프레임으로 변환
df = pd.DataFrame(timetable, index=DAYS).T

# 출력
st.markdown("---")
st.subheader("📅 시간표 결과")
st.dataframe(df, use_container_width=True)

# 저장 기능 (옵션)
csv = df.to_csv(index=True).encode('utf-8-sig')
st.download_button(
    label="📥 시간표 CSV 다운로드",
    data=csv,
    file_name=f"{grade}_{class_num}_시간표.csv",
    mime='text/csv',
)
