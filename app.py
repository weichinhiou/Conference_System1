import streamlit as st
import pandas as pd
from io import BytesIO
import os
import re

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="高榮無界任意門", layout="wide")

# --- 2. 醒目公告區 ---
st.error("""
### 🚀 系統遷移重要公告
正式版網頁已全面啟用，功能更穩定、速度更快！請同仁移步至正式版頁面使用：
[👉 點我前往：高榮無界任意門 (正式版)](https://ksvgh-anywhere-door.vercel.app/)
""", icon="📢")

# --- 3. 資料讀取 ---
@st.cache_data
def load_data(file_path, mtime):
    df = pd.read_excel(file_path)
    date_cols = [col for col in df.columns if '日期' in str(col) or '時間' in str(col)]
    def fix_date(val):
        if pd.isna(val): return "待公布"
        if isinstance(val, (int, float)): return pd.to_datetime(val, unit='D', origin='1899-12-30').strftime('%Y-%m-%d')
        if hasattr(val, 'strftime'): return val.strftime('%Y-%m-%d')
        return str(val)
    for col in date_cols:
        df[col] = df[col].apply(fix_date)
    return df.fillna("")

target_file = "LIST.xlsx"
try: file_mtime = os.path.getmtime(target_file)
except: file_mtime = 0
df = load_data(target_file, file_mtime)

category_col = next((col for col in df.columns if '類別' in str(col) or '分類' in str(col)), None)
all_categories = []
if category_col:
    cat_set = set()
    for items in df[category_col]:
        if pd.notna(items) and str(items).strip():
            tokens = re.split(r'[.,、\/;；，\s]+', str(items))
            for token in tokens:
                t = token.strip()
                if t and t not in ['與', '及', 'and', '&']: cat_set.add(t)
    all_categories = sorted(list(cat_set))

# --- 4. 標題與 CSS ---
col_t1, col_t2, col_t3 = st.columns([1, 8, 1])
with col_t2:
    st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold; color: #f1f5f9;'>高榮無界任意門</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 20px; color: #94a3b8;'>KSVGH Borderless Anywhere Door 🚪✨</div>", unsafe_allow_html=True)
st.caption("🔄 更新日期: 2026 / 06 / 15")

st.markdown("""<style>
    div[data-testid="stExpander"] { background-color: #1e222b; border: 1px solid #2d323f; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #64748b; }
    div[data-testid="stExpander"] summary p { font-size: 20px !important; font-weight: bold; color: #94a3b8; }
    div[data-testid="stButton"] button { background-color: #66CC66 !important; color: white !important; }
    </style>""", unsafe_allow_html=True)

# --- 5. 功能區 ---
if "user_has_searched" not in st.session_state: st.session_state.user_has_searched = False
if "ai_suggested_cats" not in st.session_state: st.session_state.ai_suggested_cats = []

with st.expander("🐾 有關本系統"):
    st.write("這是專為高榮人打造的學術羅盤，輔助同仁媒合國際會議...")

with st.expander("🚀 出國資源法規導航員"):
    st.markdown("[點我前往資源查詢](https://gemini.google.com/gem/18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA?usp=sharing)")

# 已補回區塊
with st.expander("🏈 出國進修知識大腦"):
    st.markdown("<a href='https://gemini.google.com/gem/1Hmt10muecDgjKXs0dNU9kaasEdFpPRhU?usp=sharing' style='color: #f3e8ee;'>不知道怎麼開始規劃進修嗎，來問問結訓返國有豐富經驗的學長姊吧~</a>", unsafe_allow_html=True)

with st.expander("🌍 世衛&醫教主題會議捕手", expanded=True):
    with st.expander("🧪 AI 智慧媒合"):
        user_abstract = st.text_area("貼上摘要：")
        if st.button("🪄 AI 媒合"): st.session_state.user_has_searched = True
    
    with st.expander("🧪 會議條件篩選"):
        search_keyword = st.text_input("🔎 關鍵字搜尋")
        selected_categories = st.multiselect("🏷️ 專業類別", options=all_categories)
        if st.button("GO"): st.session_state.user_has_searched = True

# --- 6. 結果顯示 ---
if st.session_state.user_has_searched:
    filtered_df = df.copy()
    if search_keyword:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)
        filtered_df = filtered_df[mask]
    st.write(f"共找到 {len(filtered_df)} 筆資料：")
    st.dataframe(filtered_df, use_container_width=True)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False)
    st.download_button("📥 下載查詢結果", data=output.getvalue(), file_name="結果.xlsx")
