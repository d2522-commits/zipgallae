import streamlit as st
import datetime  # ← 이거 반드시 추가
import pandas as pd
import numpy as np
import plotly.express as px

st.title("🌊 산호초 : 나 지금 과로사 중... 🌊")
st.write(
    "😍 해수온이 올라가면 산호가 조말루치라는 조류를 잃어 ‘백화 현상’이 일어납니다. 산호는 색을 잃고 영양도 제대로 얻지 못해 약해집니다. 지구 온난화, 이상 기후, 오염 등이 원인이며, 백화가 오래 지속되면 산호와 그곳에 사는 해양 생물들 모두 위험해집니다. ❤️‍🩹"
)

# ---------------------------
# 사이드바 필터
# ---------------------------
st.sidebar.header("필터")

start_date = datetime.date(1980, 1, 1)
end_date = datetime.date(2020, 8, 31)

selected_date = st.sidebar.date_input(
    "날짜 선택",
    datetime.date(2000, 1, 1),
    min_value=start_date,
    max_value=end_date
)

countries = ["전 지구", "대한민국", "호주", "인도네시아", "필리핀", "일본", "몰디브", "미국 하와이"]
selected_country = st.sidebar.selectbox("나라 선택", countries)

# ---------------------------
# 가짜 데이터 생성 (예시)
# ---------------------------
dates = pd.date_range("1980-01-01", "2020-08-31", freq="Y")
data = {
    "날짜": np.tile(dates, len(countries)),
    "나라": np.repeat(countries, len(dates)),
    "백화현상지수": np.random.rand(len(dates) * len(countries)) * 100
}
df = pd.DataFrame(data)

# ---------------------------
# 선택된 나라 데이터 필터링
# ---------------------------
if selected_country == "전 지구":
    df_filtered = df.groupby("날짜")["백화현상지수"].mean().reset_index()
else:
    df_filtered = df[df["나라"] == selected_country]

# ---------------------------
# 라인 차트
# ---------------------------
st.subheader("📊 연도별 백화현상 지수 변화")
fig_line = px.line(df_filtered, x="날짜", y="백화현상지수", title=f"{selected_country} 백화현상 추세")
st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------
# 지도
# ---------------------------
st.subheader("🌎 지도에서 보는 국가별 백화현상")
latest_year = selected_date.year
df_map = df[df["날짜"].dt.year == latest_year]

country_map = {
    "대한민국": "South Korea",
    "호주": "Australia",
    "인도네시아": "Indonesia",
    "필리핀": "Philippines",
    "일본": "Japan",
    "몰디브": "Maldives",
    "미국 하와이": "United States",
    "전 지구": "World"
}
df_map["country_en"] = df_map["나라"].map(country_map)

fig_map = px.choropleth(
    df_map,
    locations="country_en",
    locationmode="country names",
    color="백화현상지수",
    title=f"{latest_year}년 국가별 산호초 백화현상 지수",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------
# 관련 자료 링크 (전문적인 카드 디자인)
# ---------------------------
st.subheader("📌 참고 자료 및 추가 정보")

st.markdown("""
<style>
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: flex-start;
}

.card {
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    border-radius: 15px;
    padding: 25px;
    width: 320px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
    font-family: 'Arial', sans-serif;
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.2);
}

.card h4 {
    font-size: 18px;
    margin-bottom: 15px;
    color: #1d3557;
}

.card p {
    font-size: 14px;
    color: #457b9d;
    min-height: 40px;
}

.card a {
    text-decoration: none;
    color: white;
    font-weight: bold;
    background-color: #ff4b4b;
    padding: 10px 25px;
    border-radius: 8px;
    display: inline-block;
    margin-top: 10px;
    transition: background-color 0.3s;
}

.card a:hover {
    background-color: #e63946;
}

.card-icon {
    font-size: 40px;
    margin-bottom: 10px;
    color: #ff6b6b;
}
</style>

<div class="card-container">
    <div class="card">
        <div class="card-icon">🎥</div>
        <h4>전 세계 산호초 백화현상 84%</h4>
        <p>유튜브 영상으로 전 세계 산호초 백화현상 현황을 확인해보세요.</p>
        <a href="https://youtu.be/NbGgeIke2rE?si=__YeCz9ngT8rLyaG" target="_blank">동영상 보기</a>
    </div>
    <div class="card">
        <div class="card-icon">🌊</div>
        <h4>바다 온도 상승과 해산물 어획량</h4>
        <p>바다 온도 상승이 해산물 어획량에 미치는 영향 관련 기사입니다.</p>
        <a href="https://www.planet03.com/post/%EC%8B%9D%EB%9F%89%EC%9C%84%EA%B8%B0-%EB%B0%94%EB%8B%A4%EA%B0%80-%EB%B3%B4%EB%82%B4%EB%8A%94-%EA%B2%BD%EA%B3%A0" target="_blank">뉴스 보기</a>
    </div>
</div>
""", unsafe_allow_html=True)