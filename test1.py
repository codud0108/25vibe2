import streamlit as st
import pandas as pd

st.set_page_config(page_title="학교 시간표 앱", layout="wide")
st.title("📚 학교 시간표 작성기")

# 설정
DAYS = ['월', '화', '수', '목', '금']
NUM_PERIODS = 7
PERIODS = [f'{i+1}교시' for i in range(NUM_PERIODS)]

# 학년/반 선택
grade = st.selectbox("학년 선택", options=["1학년", "2학년", "3학년"])
class_num = st.selectbox("반 선택", options=["1반", "2반", "3반","4반", "5반", "6반", "7반","8반", "9반", "10반"])

st.markdown("---")

# 교시별 수업 시간 입력
st.subheader("⏰ 교시별 수업 시간 입력")

period_times = []
cols_header = st.columns([1, 2, 2])
cols_header[0].markdown("**교시**")
cols_header[1].markdown("**시작 시간 (예: 09:00)**")
cols_header[2].markdown("**종료 시간 (예: 09:45)**")

for i, period in enumerate(PERIODS):
    cols = st.columns([1, 2, 2])
    cols[0].markdown(f"{period}")
    start_time = cols[1].text_input(f"{period}_start", value="", label_visibility="collapsed", key=f"start_{period}")
    end_time = cols[2].text_input(f"{period}_end", value="", label_visibility="collapsed", key=f"end_{period}")
    period_times.append(f"{period} ({start_time}~{end_time})")

st.markdown("---")

# 시간표 입력
st.subheader("✏️ 시간표 입력 (과목 / 교실)")

timetable = {}

for i, period in enumerate(PERIODS):
    display_name = period_times[i]
    cols = st.columns(len(DAYS)+1)
    cols[0].markdown(f"**{display_name}**")
    timetable[display_name] = []
    for j, day in enumerate(DAYS):
        subject = cols[j+1].text_input(f"{day}_{period}_subject", label_visibility="collapsed", placeholder="과목", key=f"{day}_{period}_subj")
        classroom = cols[j+1].text_input(f"{day}_{period}_room", label_visibility="collapsed", placeholder="교실", key=f"{day}_{period}_room")
        combined = f"{subject} ({classroom})" if subject and classroom else subject or ""
        timetable[display_name].append(combined)

# 데이터프레임 생성 및 출력
df = pd.DataFrame(timetable, index=DAYS).T

st.markdown("---")
st.subheader("📅 최종 시간표 (과목 + 교실)")
st.dataframe(df, use_container_width=True)

# 저장
csv = df.to_csv(index=True).encode('utf-8-sig')
st.download_button(
    label="📥 시간표 CSV 다운로드",
    data=csv,
    file_name=f"{grade}_{class_num}_시간표.csv",
    mime='text/csv',
)
