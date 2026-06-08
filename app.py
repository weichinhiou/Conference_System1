import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="醫學教育與國際會議查詢系統", layout="wide")

# --- 2. 資料讀取與處理 ---
@st.cache_data
def load_data():
    # 讀取資料夾裡的 WHO2026.xlsx
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


# --- 3. 主畫面標題與導航員專區 ---
st.title("🌐 醫學教育與國際會議查詢系統")
st.caption("🔄 目前更新版本日期: 2026 / 05 / 25") 

# === 「高榮-出國經費導航員」優雅深紫（文字精準微調版） ===
st.markdown(
    """
    <div style="background-color: #262b36; padding: 22px; border-radius: 12px; border: 1px solid #3b4254; border-left: 5px solid #a855f7; box-shadow: 0 4px 12px rgba(0,0,0,0.4); margin-bottom: 25px;">
        <h4 style="margin: 0 0 10px 0; color: #c084fc; font-family: 'Microsoft JhengHei', sans-serif; font-weight: bold; font-size: 17.5px;">
            高榮-出國經費導航員 🚀
        </h4>
        <p style="margin: 0; color: #f1f5f9; font-size: 14.5px; line-height: 1.6;">
            出國補助申請、流程與相關規定諮詢線上問AI小助手：<br>
            👉 <a href="https://gemini.google.com/gem/18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA?usp=sharing" target="_blank" style="color: #60a5fa; font-weight: bold; text-decoration: underline;">戳我一下，看看有哪些經費補助可以申請~</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --- 4. 主畫面「摺疊式」篩選面板 ---
with st.expander("📂 🔍 點擊展開 / 隱藏篩選條件面板", expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        search_keyword = st.text_input("🔎 輸入關鍵字 (如: 組織名稱、國家或城市)")
    with col2:
        selected_categories = st.multiselect(
            "🏷️ 選擇感興趣的專業類別 (可多選)", 
            options=all_categories
        )


# --- 5. 資料過濾邏輯 ---
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


# --- 6. 查詢結果呈現與下載 ---
st.write(f"共找到 **{len(filtered_df)}** 筆符合的會議資料：")

# 將 DataFrame 顯示在網頁上
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# 下載 Excel 功能
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

# TIMESTAMPMARK 2026-06-09 00:20:00
