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

# === 「高榮-出國經費導航員」優雅深紫區塊 ===
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


# --- 4. 內嵌式「會議條件篩選條件面板🧪」 ---
# 終極精準狙擊 CSS：直接對準 stBlock 與其變體，只要裝有我們自訂藍標題的盒子，就強制變身！
st.markdown(
    """
    <style>
    /* 多重保險鎖定器：精準捕捉內含 .custom-filter-title 的 Block 容器外盒 */
    div[data-testid="stBlock"]:has(.custom-filter-title),
    div[data-testid="stBorderedContainer"]:has(.custom-filter-title),
    div[data-testid="stVerticalBlockBorderedWrapper"]:has(.custom-filter-title),
    div[class*="BorderedWrapper"]:has(.custom-filter-title) {
        background-color: #1e222b !important; /* 換上深石墨黑 */
        border: 1px solid #2d323f !important;
        border-left: 5px solid #38bdf8 !important; /* 科技藍左邊條強制歸位！ */
        border-radius: 12px !important;
        padding: 22px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        margin-bottom: 25px !important;
    }
    
    /* 雙區塊標題字體大小完美等大對齊（17.5px粗體），並指定明亮科技藍 */
    .custom-filter-title {
        color: #38bdf8 !important;
        font-family: 'Microsoft JhengHei', sans-serif !important;
        font-weight: bold !important;
        font-size: 17.5px !important;
        margin: 0 0 15px 0 !important;
        display: block !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 啟動帶邊框容器（將被上方的精準 CSS 徹底重塑外觀）
with st.container(border=True):
    # 渲染出大小與上方完全對齊、顏色也是科技藍的漂亮標題
    st.markdown('<h4 class="custom-filter-title">會議條件篩選條件面板 🧪</h4>', unsafe_allow_html=True)
    
    # 搜尋元件並排且完美包覆在內部
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

# TIMESTAMPMARK 2026-06-09 01:22:00
