import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="醫學教育與國際會議查詢系統", layout="wide")

# --- 2. 資料讀取與處理 ---
@st.cache_data
def load_data():
    # 根據你的診斷清單，直接讀取資料夾裡的 WHO2026.xlsx
    df = pd.read_excel("WHO2026.xlsx")
    
    # 處理 Excel 內建的日期格式
    def fix_date(val):
        if pd.isna(val):
            return "待公布"
        if isinstance(val, (int, float)):
            return pd.to_datetime(val, unit='D', origin='1899-12-30').strftime('%Y-%m-%d')
        if hasattr(val, 'strftime'): 
            return val.strftime('%Y-%m-%d')
        return str(val)
            
    df['2026 研討會日期'] = df['2026 研討會日期'].apply(fix_date)
    df = df.fillna("") 
    return df

df = load_data()

# 自動抓取所有的「專業類別」，並去除重複
all_categories = set()
for items in df['專業類別分類']:
    if items:
        for item in str(items).split('.'):
            all_categories.add(item.strip())
all_categories = sorted(list(all_categories))

# --- 3. 側邊欄 (使用者操作區) ---
st.sidebar.header("🔍 篩選條件")

# 關鍵字搜尋
search_keyword = st.sidebar.text_input("輸入關鍵字 (如: 組織名稱、國家或城市)")

# 多選分類下拉選單
selected_categories = st.sidebar.multiselect(
    "選擇感興趣的專業類別 (可多選)", 
    options=all_categories
)

# --- 4. 資料過濾邏輯 ---
filtered_df = df.copy()

# 邏輯A: 關鍵字過濾
if search_keyword:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)
    filtered_df = filtered_df[mask]

# 邏輯B: 專業類別過濾 (部分符合)
if selected_categories:
    def check_category(row_cat):
        row_tags = [tag.strip() for tag in str(row_cat).split('.')]
        return any(tag in selected_categories for tag in row_tags)
    
    mask = filtered_df['專業類別分類'].apply(check_category)
    filtered_df = filtered_df[mask]

# --- 5. 主畫面呈現 ---
st.title("🌐 醫學教育與國際會議查詢系統")
st.caption("🔄 目前更新版本日期: 2026 / 05 / 25") 

st.write(f"共找到 **{len(filtered_df)}** 筆符合的會議資料：")

# 將 DataFrame 顯示在網頁上
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# --- 6. 下載 Excel 功能 ---
def convert_df_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='查詢結果')
    processed_data = output.getvalue()
    return processed_data

if not filtered_df.empty:
    excel_data = convert_df_to_excel(filtered_df)
    st.download_button(
        label="📥 下載本次查詢結果 (Excel格式)",
        data=excel_data,
        file_name="會議查詢結果_導出.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )