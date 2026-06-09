import streamlit as st
import pandas as pd
from io import BytesIO

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="世衛醫教會議捕手 WHO&MedEd Conf Catcher", layout="wide")

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


# --- 3. 主畫面標題與作者署名專區 ---
st.title("🌐 世衛醫教會議捕手 WHO&MedEd Conf Catcher")

# 作者與版本資訊：一左一右完美對齊
col_meta1, col_meta2 = st.columns([1, 1])
with col_meta1:
    st.caption("🔄 目前更新版本日期: 2026 / 05 / 25")
with col_meta2:
    st.markdown("<p style='text-align: right; color: #868e96; font-size: 14px; margin: 0;'>系統維護：魏今秀 (教學研究部 醫學教學科)</p>", unsafe_allow_html=True)


# 🎨 智慧三色調 CSS 注入：完美統馭灰、紫、藍三種摺疊面板
st.markdown(
    """
    <style>
    /* 🎯 基礎設定：將所有面板外殼設為深黑底色、圓角與立體陰影 */
    div[data-testid="stExpander"] {
        background-color: #1e222b !important;
        border: 1px solid #2d323f !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        margin-bottom: 25px !important;
    }
    
    /* 統一所有折疊面板的標題字級為 16px 粗體 */
    div[data-testid="stExpander"] summary p {
        font-weight: bold !important;
        font-size: 16px !important; 
        font-family: 'Microsoft JhengHei', sans-serif !important;
    }
    
    /* ---------------------------------------------------- */
    /* 🟢 種類 1：預設低調深邃灰（給「💡 223 國際組織宗旨」使用） */
    div[data-testid="stExpander"] {
        border-left: 5px solid #64748b !important;
    }
    div[data-testid="stExpander"] summary p {
        color: #94a3b8 !important;
    }
    
    /* ---------------------------------------------------- */
    /* 🟣 種類 2：智慧偵測優雅紫（給「🚀 出國經費導航員」使用） */
    /* 當偵測到面板內含有 Gemini AI 的連結時，自動重載為紫調 */
    div[data-testid="stExpander"]:has(a[href*="gemini.google.com"]) {
        border-left: 5px solid #a855f7 !important;
    }
    div[data-testid="stExpander"]:has(a[href*="gemini.google.com"]) summary p {
        color: #c084fc !important;
    }
    
    /* ---------------------------------------------------- */
    /* 🔵 種類 3：智慧偵測科技藍（給「🧪 條件篩選面板」使用） */
    /* 當偵測到面板內含有輸入框或多選器時，自動重載為藍調 */
    div[data-testid="stExpander"]:has(div[data-testid="stTextInput"]),
    div[data-testid="stExpander"]:has(div[data-testid="stMultiSelect"]) {
        border-left: 5px solid #38bdf8 !important;
    }
    div[data-testid="stExpander"]:has(div[data-testid="stTextInput"]) summary p,
    div[data-testid="stExpander"]:has(div[data-testid="stMultiSelect"]) summary p {
        color: #38bdf8 !important;
    }
    /* ---------------------------------------------------- */
    
    /* 優雅微調內襯間距 */
    div[data-testid="stExpanderDetails"] {
        padding: 22px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 🛠️ 宗旨小抽屜（低調灰面板，預設不展開）
with st.expander("💡 關於系統收錄的 223 個國際組織", expanded=False):
    st.markdown(
        """
        <p style="font-size: 14.5px; line-height: 1.6; color: #cbd5e1; margin: 0; font-family: 'Microsoft JhengHei', sans-serif;">
        本系統之資料庫核心匯集自 WHO（世界衛生組織）官方認定之轄下機構、非政府組織（NGO），以及全球重要醫學教育標竿機構（共計 223 個權威組織）。部分組織近年雖暫無常態性研討會公告（系統顯示為待公布），但在國際醫學界仍具關鍵影響力。健全的基礎庫不僅呈現當下現況，更具備前瞻追蹤價值，以利同仁未來規劃學術發表或國際交流時參考。
        <br><br>
        📢 <b>系統服務初心與小叮嚀</b>：<br>
        因全球國際研討會數量龐大且資訊變動頻繁，系統較難做到即時隨時更新，各項訊息的變化往往難以完全掌握。本平台建立的初心旨在提供同仁一個便利的查閱方向與規劃參考，實際會議詳情與會期請務必以各組織官網之最新公告為準。若同仁在使用上有任何建議，或發現有需要修正與補充的資訊，非常歡迎隨時與教學研究部醫學教學科（魏今秀）聯繫，讓我們共同維護、完善這個專屬高榮的資料庫。
        </p>
        """,
        unsafe_allow_html=True
    )


# === 🚀 「高榮-出國經費導航員」全新進化可伸縮抽屜 ===
# 改為 st.expander 完美融入一體化設計，預設展開（expanded=True）方便查閱
with st.expander("🚀 高榮-出國經費導航員", expanded=True):
    st.markdown(
        """
        <p style="margin: 0; color: #f1f5f9; font-size: 14.5px; line-height: 1.6; font-family: 'Microsoft JhengHei', sans-serif;">
            出國補助申請流程與相關規定諮詢線上問AI小助手：<br>
            <a href="https://gemini.google.com/gem/18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA?usp=sharing" target="_blank" style="color: #60a5fa; font-weight: bold; text-decoration: underline;">戳我一下，看看有哪些經費補助可以申請~</a>
        </p>
        """,
        unsafe_allow_html=True
    )


# --- 4. 篩選控制台 ---
with st.expander("🧪 會議條件篩選條件面板", expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        search_keyword = st.text_input("🔎 輸入關鍵字 (如: 國際組織/會議名稱、主題)")
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

# 寬度微調平衡
custom_column_config = {}
if len(filtered_df.columns) > 0:
    first_column_name = filtered_df.columns[0]
    custom_column_config[first_column_name] = st.column_config.TextColumn(width="medium")

# 將 DataFrame 顯示在網頁上
st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config=custom_column_config
)

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
