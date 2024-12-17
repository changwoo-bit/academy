import streamlit as st
import pandas as pd
import plotly.express as px

st.title("학원 정보 제공 플랫폼")

# 사이드바 카테고리
menu = st.sidebar.selectbox(
    "카테고리를 선택하세요",
    ["홈", "학원 검색", "지역별 학원 통계", "FAQ"]
)

academy = "academy.csv"

try:
    academy_df = pd.read_csv(academy, encoding='cp949')
except FileNotFoundError:
    st.error("학원 데이터 파일을 찾을 수 없습니다. 파일 경로를 확인해 주세요.")
    st.stop()

# 데이터 전처리: 결측치 제거
academy_df.dropna(subset=['학원명', '도로명주소'], inplace=True)

# 중복 데이터 처리: 학원명과 도로명주소 기준으로 중복 제거
academy_df.drop_duplicates(subset=['학원명', '도로명주소'], inplace=True)

# 카테고리별 출력
if menu == "홈":
    st.write("여기서 학원 정보를 검색하고, 통계를 확인하고, 자주 묻는 질문을 볼 수 있습니다.")
    st.write("사이드에 있는 탭을 참고하여 원하는 정보를 확인하세요.")

    st.image("156.jpeg", caption="학원 정보 제공 플랫폼", use_column_width=True)  # 이미지 경로와 캡션을 설정

    
elif menu == "학원 검색":
    st.subheader("학원 검색")
    region = st.text_input("지역을 입력하세요 (예: 강남구, 안동시)").strip()

    if st.button("검색", key="search_button_unique"):
        if region:
            filtered_data = academy_df[academy_df["행정구역명"].str.contains(region, na=False)]

            if not filtered_data.empty:
                st.success(f"{len(filtered_data)}개의 학원을 찾았습니다.")
                for _, row in filtered_data.iterrows():
                    st.subheader(row["학원명"])
                    st.write(f"교습과정: {row['분야명']}")
                    st.write(f"주소: {row['도로명주소']}")
                    st.write(f"전화번호: {row['전화번호']}")
                    st.write(f"개설일자: {row['개설일자']}")
                    st.write("---")
            else:
                st.warning("검색 결과가 없습니다.")
        else:
            st.warning("지역명을 입력하세요.")

elif menu == "지역별 학원 통계":
    st.subheader("지역별 학원 통계")

    g_data = academy_df.groupby(['시도교육청명', '행정구역명']).size().reset_index(name='학원 수')

    edu_office = st.selectbox("시도교육청명을 선택하세요", academy_df['시도교육청명'].unique())
    f_data = g_data[g_data['시도교육청명'] == edu_office]

    if not f_data.empty:
        fig = px.bar(
            f_data,
            x='행정구역명',
            y='학원 수',
            title=f"{edu_office} 내 행정구역별 학원 수 비교",
            labels={"행정구역명": "행정구역명", "학원 수": "학원 수"},
            color='학원 수',
            height=500
        )
        st.plotly_chart(fig)
    else:
        st.warning("선택한 시도교육청명에 대한 데이터가 없습니다.")

elif menu == "FAQ":
    st.subheader("자주 묻는 질문")

    st.write("1. 이 플랫폼은 어떤 데이터를 기반으로 하나요?")
    st.write("   - 이 플랫폼은 시도교육청에서 제공하는 공공 데이터를 기반으로 학원 정보를 제공합니다. 학원명, 교습과정, 주소, 개설일자 등 다양한 정보를 포함하고 있습니다.")
    
    st.write("2. 학원 정보는 얼마나 자주 업데이트되나요?")
    st.write("   - 데이터는 공공 데이터 소스를 기반으로 제공되기 때문에, 제공 기관의 업데이트 주기에 따라 변경됩니다.")
    
    st.write("3. 학원 정보 검색 시 결과가 없는 이유는 무엇인가요?")
    st.write("   - 입력한 지역명에 해당하는 학원이 없을 수 있습니다. 또한 학원 이름이나 행정구역명 입력 시 철자가 맞는지 다시 확인해 주세요.")
    
    st.write("4. 제공되는 학원 데이터에는 어떤 항목이 포함되나요?")
    st.write("   - 학원명, 교습 과정, 주소, 전화번호, 개설일자 등 학원 운영에 대한 주요 항목들이 제공됩니다.")
    


