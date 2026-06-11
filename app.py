import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="世衛&醫教主題會議捕手 WHO & MedEd Thematic Conf Catcher", layout="wide")

# --- 2. 資料讀取與處理 ---
@st.cache_data
def load_data():
    # 讀取資料夾裡的 Excel 檔案
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
            
    if '2026 研討會日期' in df.columns:
        df['2026 研討會日期'] = df['2026 研討會日期'].apply(fix_date)
        
    df = df.fillna("") 
    return df

df = load_data()

# 自動抓取所有的「專業類別」，並去除重複
all_categories = set()
if '專業類別分類' in df.columns:
    for items in df['專業類別分類']:
        if items:
            for item in str(items).split('.'):
                all_categories.add(item.strip())
all_categories = sorted(list(all_categories))


# --- 3. 主畫面標題專區 (80% 寬度黃金比例 Banner) ---
col_b1, col_b2, col_b3 = st.columns([1, 8, 1])
with col_b2:
    st.image("banner.png", use_container_width=True)

# 作者與版本資訊
col_meta1, col_meta2 = st.columns(2)
col_meta1.caption("🔄 目前更新版本日期: 2026 / 05 / 25")
col_meta2.markdown("<p style='text-align: right; color: #868e96; font-size: 14px; margin: 0;'>系統維護：魏今秀 (教學研究部 醫學教學科)</p>", unsafe_allow_html=True)


# --- 🎨 智慧三色調 CSS ---
st.markdown(
    """
    <style>
    div[data-testid="stExpander"] {
        background-color: #1e222b !important;
        border: 1px solid #2d323f !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        margin-bottom: 25px !important;
    }
    div[data-testid="stExpander"] summary p {
        font-weight: bold !important;
        font-size: 16px !important; 
        font-family: 'Microsoft JhengHei', sans-serif !important;
    }
    
    /* 莫蘭迪綠篩選面板 */
    div[data-testid="stExpander"]:has(div[data-testid="stTextInput"]),
    div[data-testid="stExpander"]:has(div[data-testid="stMultiSelect"]) {
        border-left: 5px solid #829986 !important;
    }
    div[data-testid="stExpander"]:has(div[data-testid="stTextInput"]) summary p,
    div[data-testid="stExpander"]:has(div[data-testid="stMultiSelect"]) summary p {
        color: #a3bda7 !important;
    }
    
    /* 其他面板顏色 */
    div[data-testid="stExpander"] { border-left: 5px solid #64748b !important; }
    div[data-testid="stExpander"] summary p { color: #94a3b8 !important; }
    div[data-testid="stExpander"]:has(a[href*="gemini.google.com"]) { border-left: 5px solid #a855f7 !important; }
    div[data-testid="stExpander"]:has(a[href*="gemini.google.com"]) summary p { color: #c084fc !important; }
    
    div[data-testid="stTextInput"] div[data-baseweb="input"], 
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
        background-color: #282f3b !important;
        border-color: #3f4857 !important;
    }
    div[data-testid="stTextInput"] input { color: #f1f5f9 !important; }
    div[data-testid="stExpanderDetails"] { padding: 22px !important; }
    </style>
    """,
    unsafe_allow_html=True
)


# --- 4. 功能區域 ---
with st.expander("💡 關於系統收錄的 223 個國際組織", expanded=False):
    st.markdown("""<p style="font-size: 14.5px; line-height: 1.6; color: #cbd5e1; margin: 0; font-family: 'Microsoft JhengHei', sans-serif;">
    本系統之資料庫核心匯集自 WHO 官方認定之轄下機構、NGO，以及全球重要醫學教育標竿機構（共 223 個）。
    本平台旨在提供便利的查閱方向，實際會期請以組織官網最新公告為準。若有建議或更新需求，歡迎與教學研究部醫學教學科（魏今秀）聯繫。
    </p>""", unsafe_allow_html=True)

with st.expander("🚀 高榮-出國經費導航員", expanded=True):
    st.markdown("""<p style="margin: 0; color: #f1f5f9; font-size: 14.5px; line-height: 1.6; font-family: 'Microsoft JhengHei', sans-serif;">
    出國補助相關規定諮詢：<br>
    <a href="https://gemini.google.com/gem/18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA?usp=sharing" target="_blank" style="color: #60a5fa; font-weight: bold; text-decoration: underline;">戳我一下，看看有哪些經費補助可以申請~</a>
    </p>""", unsafe_allow_html=True)

with st.expander("🧪 會議條件篩選條件面板", expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        search_keyword = st.text_input("🔎 輸入關鍵字")
    with col2:
        if all_categories:
            selected_categories = st.multiselect("🏷️ 選擇感興趣的專業類別", options=all_categories)
        else:
            selected_categories = []
            st.caption("⚠️ 未偵測到預設的專業類別欄位")


# --- 5. 邏輯與呈現 ---
filtered_df = df.copy()
if search_keyword:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)
    filtered_df = filtered_df[mask]
if selected_categories and '專業類別分類' in filtered_df.columns:
    mask = filtered_df['專業類別分類'].apply(lambda x: any(tag in selected_categories for tag in str(x).split('.')))
    filtered_df = filtered_df[mask]

st.write(f"共找到 **{len(filtered_df)}** 筆符合的會議資料：")


# --- 🛠️ 核心改動：精緻化超連結欄位設定 (G, H, I 欄) ---
table_column_config = {}

# 檢查並將 Excel 中的 G 欄 (Python 索引 6) 設定為超連結
if len(filtered_df.columns) >= 7:
    col_g_name = filtered_df.columns[6]
    table_column_config[col_g_name] = st.column_config.LinkColumn(col_g_name, display_text="🔗 點擊前往")

# 檢查並將 Excel 中的 H 欄 (Python 索引 7) 設定為超連結
if len(filtered_df.columns) >= 8:
    col_h_name = filtered_df.columns[7]
    table_column_config[col_h_name] = st.column_config.LinkColumn(col_h_name, display_text="🔗 點擊前往")

# 檢查並將 Excel 中的 I 欄 (Python 索引 8) 設定為超連結
if len(filtered_df.columns) >= 9:
    col_i_name = filtered_df.columns[8]
    table_column_config[col_i_name] = st.column_config.LinkColumn(col_i_name, display_text="🔗 點擊前往")


# 將包含全新超連結設定的配置注入表格中
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config=table_column_config
)


# --- 6. 下載功能 ---
if not filtered_df.empty:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False)
    st.download_button("📥 下載本次查詢結果", data=output.getvalue(), file_name="會議查詢結果.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
