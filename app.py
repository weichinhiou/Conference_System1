import streamlit as st
import pandas as pd
from io import BytesIO
import os
import re

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="高榮無界任意門", layout="wide")

# --- [新增] 醒目公告區 ---
st.error("""
### 🚀 系統遷移重要公告
正式版網頁已全面啟用，功能更穩定、速度更快！請同仁移步至正式版頁面使用：
[👉 點我前往：高榮無界任意門 (正式版)](https://ksvgh-anywhere-door.vercel.app/)
""", icon="📢")
st.divider() # 畫一條線區隔

# --- 2. 資料讀取 ---
@st.cache_data
def load_data(file_path, mtime):
    df = pd.read_excel(file_path)
    
    # 智慧偵測：尋找名稱包含「日期」或「時間」的欄位進行格式優化
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
try:
    file_mtime = os.path.getmtime(target_file)
except:
    file_mtime = 0

df = load_data(target_file, file_mtime)

# 智慧偵測：尋找名稱包含「類別」或「分類」的欄位作為篩選依據
category_col = next((col for col in df.columns if '類別' in str(col) or '分類' in str(col)), None)

# 拆解標籤，並自動過濾「與、及、and」等無效連接詞
all_categories = []
if category_col:
    cat_set = set()
    for items in df[category_col]:
        if pd.notna(items) and str(items).strip():
            # 自動識別並切開各式分隔符號
            tokens = re.split(r'[.,、\/;；，\s]+', str(items))
            for token in tokens:
                t = token.strip()
                if t and t not in ['與', '及', 'and', '&']:
                    cat_set.add(t)
    all_categories = sorted(list(cat_set))

# --- 3. 標題區 (全新升級：高榮無界任意門) ---
st.write("")
col_t1, col_t2, col_t3 = st.columns([1, 8, 1])
with col_t2:
    st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold; color: #f1f5f9;'>高榮無界任意門</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 20px; color: #94a3b8;'>KSVGH Borderless Anywhere Door 🚪✨</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 14px; color: #64748b;'>GLOBAL MEDICAL EDUCATION PLATFORM</div>", unsafe_allow_html=True)
st.write("")

st.caption("🔄 更新日期: 2026 / 06 / 15")

# --- 4. CSS ---
st.markdown("""
    <style>
    /* 基礎外觀 */
    div[data-testid="stExpander"] { background-color: #1e222b; border: 1px solid #2d323f; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #64748b; }
    
    /* 調整主要功能大標題的字型大小與內距 */
    div[data-testid="stExpander"] summary { padding-top: 12px !important; padding-bottom: 12px !important; }
    div[data-testid="stExpander"] summary p { font-size: 20px !important; font-weight: bold; color: #94a3b8; line-height: 1.4 !important; }
    
    /* 出國資源法規導航員顏色 (紫) */
    div[data-testid="stExpander"]:has(a[href*="18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA"]) { border-left: 5px solid #a855f7 !important; }
    div[data-testid="stExpander"]:has(a[href*="18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA"]) summary p { color: #d8b4fe !important; }
    
    /* 出國進修知識大腦顏色 (優雅淡褐色) */
    div[data-testid="stExpander"]:has(a[href*="1Hmt10muecDgjKXs0dNU9kaasEdFpPRhU"]) { border-left: 5px solid #c
