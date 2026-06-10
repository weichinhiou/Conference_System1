import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="世衛&醫教主題會議捕手", layout="wide")

# --- 2. 資料讀取 ---
@st.cache_data
def load_data():
    df = pd.read_excel("WHO2026.xlsx")
    def fix_date(val):
        if pd.isna(val): return "待公布"
        if isinstance(val, (int, float)): return pd.to_datetime(val, unit='D', origin='1899-12-30').strftime('%Y-%m-%d')
        if hasattr(val, 'strftime'): return val.strftime('%Y-%m-%d')
        return str(val)
    df['2026 研討會日期'] = df['2026 研討會日期'].apply(fix_date)
    return df.fillna("")

df = load_data()
all_categories = sorted(list({item.strip() for items in df['專業類別分類'] if items for item in str(items).split('.')}))

# --- 3. 標題區 ---
st.write("")
col_t1, col_t2, col_t3 = st.columns([1, 8, 1])
with col_t2:
    st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold; color: #f1f5f9;'>世衛&醫教主題會議捕手</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 20px; color: #94a3b8;'>WHO & MedEd Thematic Conf Catcher</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 14px; color: #64748b;'>GLOBAL MEDICAL EDUCATION PLATFORM</div>", unsafe_allow_html=True)
st.write("")

col_meta1, col_meta2 = st.columns(2)
col_meta1.caption("🔄 更新日期: 2026 / 05 / 25")
col_meta2.markdown("<p style='text-align: right; color: #868e96; font-size: 14px;'>系統維護：教學研究部 醫學教學科</p>", unsafe_allow_html=True)

# --- 4. CSS ---
st.markdown("""
    <style>
    /* 基礎外觀 */
    div[data-testid="stExpander"] { background-color: #1e222b; border: 1px solid #2d323f; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #64748b; }
    div[data-testid="stExpander"] summary p { font-weight: bold; color: #94a3b8; }
    
    /* 經費導航員顏色 (紫) */
    div[data-testid="stExpander"]:has(a) { border-left: 5px solid #a855f7; }
    div[data-testid="stExpander"]:has(a) summary p { color: #d8b4fe; }
    
    /* 篩選條件面板 (蘋果綠) */
    div[data-testid="stExpander"]:has(input), div[data-testid="stExpander"]:has(select) { border-left: 5px solid #66CC66 !important; }
    div[data-testid="stExpander"]:has(input) summary p, div[data-testid="stExpander"]:has(select) summary p { color: #66CC66 !important; }
    
    /* 輸入框底色 */
    div[data-testid="stTextInput"] div[data-baseweb="input"], 
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
        background-color: #3e4756 !important;
        border-color: #566175 !important;
    }
    div[data-testid="stTextInput"] input { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. 功能區 ---
with st.expander("💡 關於系統收錄的 223 個國際組織"):
    st.markdown("<p style='font-size: 14.5px; margin: 0;'>本系統匯集 WHO 及國際重要醫學教育機構資料，供同仁交流參考。最新會期請以官網為準。</p>", unsafe_allow_html=True)

with st.expander("🚀 高榮-出國經費導航員", expanded=True):
    # 使用 HTML 標籤確保連結與大小皆正確
    st.markdown("<p style='font-size: 14.5px; margin: 0;'>點此開啟：<a href='https://gemini.google.com/gem/18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA?usp=sharing' style='color: #60a5fa; font-weight: bold; text-decoration: underline;'>出國經費補助申請諮詢 AI 小助手</a></p>", unsafe_allow_html=True)

with st.expander("🧪 會議條件篩選", expanded=True):
    col1, col2 = st.columns(2)
    search_keyword = col1.text_input("🔎 關鍵字搜尋")
    selected_categories = col2.multiselect("🏷️ 專業類別", options=all_categories)

# --- 6. 呈現 ---
filtered_df = df.copy()
if search_keyword:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)
    filtered_df = filtered_df[mask]
if selected_categories:
    filtered_df = filtered_df[filtered_df['專業類別分類'].apply(lambda x: any(cat in str(x) for cat in selected_categories))]

st.write(f"共找到 **{len(filtered_df)}** 筆資料：")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

if not filtered_df.empty:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False)
    st.download_button("📥 下載本次查詢結果", data=output.getvalue(), file_name="會議查詢結果.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
