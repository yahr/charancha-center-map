import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Streamlit 앱 설정
st.set_page_config(layout="wide")  # 전체 화면으로 설정

# Streamlit 앱 제목
st.title("지점 위치 지도")

# 데이터 구간 표시
st.sidebar.header("마커 색상 기준")

# 색상 아이콘 표시
color_legend = {
    "Blue": "0 ~ 99 횟수",
    "Green": "100 ~ 4999 횟수",
    "Orange": "5000 ~ 9999 횟수",
    "Red": "10000 이상 횟수"
}

for color, range_text in color_legend.items():
    st.sidebar.markdown(f"<i style='display: inline-block; width: 12px; height: 12px; background-color: {color.lower()}; border-radius: 50%; margin-right: 8px;'></i>**{color}**: {range_text}", unsafe_allow_html=True)

# 예시 CSV 파일 다운로드 버튼
with open("data/example.csv", "rb") as f:
    st.sidebar.download_button(
        label="예시 CSV 파일 다운로드",
        data=f,
        file_name="example.csv",
        mime="text/csv"
    )

# CSV 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    # CSV 데이터 로드
    df = pd.read_csv(uploaded_file)

    # 횟수 기준 내림차순 정렬
    df = df.sort_values(by="횟수", ascending=True)

    # 지도 초기화
    m = folium.Map(location=[df["위도"].mean(), df["경도"].mean()], zoom_start=10)

    # 마커 색상 설정 함수
    def get_marker_color(count):
        if count < 100:
            return 'blue'
        elif count < 5000:
            return 'green'
        elif count < 10000:
            return 'orange'
        else:
            return 'red'

    # 데이터 기반 마커 추가
    for index, row in df.iterrows():
        color = get_marker_color(row["횟수"])
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=f"{row['지점명']}<br>{row['지점주소']}<br>횟수: {row['횟수']}",
            tooltip=row["지점명"],
            icon=folium.Icon(color=color)
        ).add_to(m)

    # 지도 표시 (화면 전체)
    st_folium(m, use_container_width=True, height=800)
else:
    st.info("CSV 파일을 업로드하세요.")
