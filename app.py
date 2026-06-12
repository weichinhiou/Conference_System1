import streamlit as st
import pandas as pd
from io import BytesIO
import os
import re

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="高榮國際任意門", layout="wide")

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

# --- 3. 標題區 ---
st.write("")
col_t1, col_t2, col_t3 = st.columns([1, 8, 1])
with col_t2:
    st.markdown("<div style='text-align: center; font-size: 32px; font-weight: bold; color: #f1f5f9;'>高榮國際任意門</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 20px; color: #94a3b8;'>KSVGH Abroad Anywhere Door</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 14px; color: #64748b;'>GLOBAL MEDICAL EDUCATION PLATFORM</div>", unsafe_allow_html=True)
st.write("")

st.caption("🔄 更新日期: 2026 / 06 / 12")

# --- 4. CSS ---
st.markdown("""
    <style>
    /* 基礎外觀 */
    div[data-testid="stExpander"] { background-color: #1e222b; border: 1px solid #2d323f; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #64748b; }
    div[data-testid="stExpander"] summary p { font-weight: bold; color: #94a3b8; }
    
    /* 經費導航員顏色 (紫) */
    div[data-testid="stExpander"]:has(a[href*="18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA"]) { border-left: 5px solid #a855f7 !important; }
    div[data-testid="stExpander"]:has(a[href*="18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA"]) summary p { color: #d8b4fe !important; }
    
    /* 出國進修知識大腦顏色 (優雅淡褐色) */
    div[data-testid="stExpander"]:has(a[href*="1Hmt10muecDgjKXs0dNU9kaasEdFpPRhU"]) { border-left: 5px solid #c5a880 !important; background-color: #24211c !important; }
    div[data-testid="stExpander"]:has(a[href*="1Hmt10muecDgjKXs0dNU9kaasEdFpPRhU"]) summary p { color: #e6dfd5 !important; }
    
    /* 篩選條件面板最外層 (蘋果綠) */
    div[data-testid="stExpander"]:has(input), div[data-testid="stExpander"]:has(select) { border-left: 5px solid #66CC66 !important; }
    div[data-testid="stExpander"]:has(input) summary p, div[data-testid="stExpander"]:has(select) summary p { color: #66CC66 !important; }
    
    /* 🛠️ 核心優化：讓「內嵌子區塊（第二層）」強制維持精緻灰色框，建立漂亮層次感 */
    div[data-testid="stExpander"] div[data-testid="stExpander"] { 
        border-left: 5px solid #64748b !important; 
        background-color: #1a1d24 !important;
    }
    div[data-testid="stExpander"] div[data-testid="stExpander"] summary p { 
        color: #94a3b8 !important; 
    }
    
    /* 輸入框與下拉選單底色 */
    div[data-testid="stTextInput"] div[data-baseweb="input"], 
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
        background-color: #3e4756 !important;
        border-color: #566175 !important;
    }
    div[data-testid="stTextInput"] input { color: #ffffff !important; }
    
    /* GO 按鈕外觀與間距 */
    div[data-testid="stButton"] {
        margin-bottom: 10px;
    }
    div[data-testid="stButton"] button {
        background-color: #66CC66 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        height: 40px !important;
        font-weight: bold !important;
        font-size: 14px !important;
        transition: background-color 0.2s ease;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #4da64d !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. 功能區 ---
with st.expander("💡 有關本系統", expanded=False):
    st.markdown("<p style='font-size: 14.5px; margin: 0;'>系統維護：教學研究部 醫學教學科 魏今秀</p>", unsafe_allow_html=True)

with st.expander("🚀 出國經費導航員", expanded=False):
    st.markdown("<p style='font-size: 14.5px; margin: 0;'><a href='https://gemini.google.com/gem/18x5GMgjMdXG5Ume9-ySxoECpU7qS4mzA?usp=sharing' style='color: #d8b4fe; font-weight: bold; text-decoration: underline;'>戳我一下，看看有哪些經費補助可以申請~</a></p>", unsafe_allow_html=True)

with st.expander("🏈 出國進修知識大腦", expanded=False):
    st.markdown("<p style='font-size: 14.5px; margin: 0;'><a href='https://gemini.google.com/gem/1Hmt10muecDgjKXs0dNU9kaasEdFpPRhU?usp=sharing' style='color: #f3e8ee; font-weight: bold; text-decoration: underline;'>點擊這裡，讓出國進修知識大腦為您解答所有公費公假、法規與申請流程疑問！</a></p>", unsafe_allow_html=True)

# 🌍 主區塊：世衛&醫教主題會議捕手 (高榮國際任意門核心功能)
with st.expander("🌍 世衛&醫教主題會議捕手", expanded=False):
    
    # 🤖 AI 智慧推薦狀態初始化
    if "ai_suggested_cats" not in st.session_state:
        st.session_state.ai_suggested_cats = []

    # 子區塊 A：AI 智慧媒合 (預設內縮灰色框)
    with st.expander("🧪 AI 論文摘要/研究主題智慧媒合 (免盲搜)", expanded=False):
        user_abstract = st.text_area(
            "貼上您的英文論文摘要 (Abstract) 或研究大綱：", 
            placeholder="例如：We aim to investigate the impact of portfolio systems on medical faculty evaluation workflows...",
            height=100
        )
        
        if st.button("🪄 讓 AI 幫我推薦專業類別", use_container_width=True):
            if not user_abstract.strip():
                st.warning("請先輸入摘要內容喔！")
            else:
                with st.spinner("AI 正在研讀您的摘要並媒合全球會議類別..."):
                    try:
                        from openai import OpenAI
                        
                        openai_key = st.secrets.get("OPENAI_API_KEY")
                        gemini_key = st.secrets.get("GEMINI_API_KEY")
                        
                        if gemini_key:
                            client = OpenAI(
                                api_key=gemini_key,
                                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
                            )
                            model_to_use = "gemini-2.5-flash"
                        else:
                            client = OpenAI(api_key=openai_key)
                            model_to_use = "gpt-4o-mini"
                        
                        prompt = f"""
                        你是一位資深的國際醫學會議召集人。請閱讀以下使用者的論文摘要，並從「可選類別清單」中，
                        挑選出最符合、最相關的 1 到 3 個類別標籤。
                        
                        【使用者的論文摘要】
                        {user_abstract}
                        
                        【可選類別清單】
                        {all_categories}
                        
                        【嚴格輸出規則】
                        請只回傳一個標準的 JSON 陣列，裡面包含挑選出的類別字串，絕對不要包含 Markdown 語法標記。
                        範例：["人權", "性別"]
                        """
                        
                        response = client.chat.completions.create(
                            model=model_to_use,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.2
                        )
                        
                        import json
                        raw_reply = response.choices[0].message.content.strip()
                        
                        raw_reply = raw_reply.lstrip("`").rstrip("`")
                        if raw_reply.lower().startswith("json"):
                            raw_reply = raw_reply[4:].strip()
                            
                        suggested_tags = json.loads(raw_reply)
                        valid_tags = [tag for tag in suggested_tags if tag in all_categories]
                        
                        if valid_tags:
                            st.session_state.ai_suggested_cats = valid_tags
                            st.success(f"💡 AI 替您精選了標籤：{', '.join(valid_tags)}！已自動為您勾選下方選單。")
                            st.rerun()
                        else:
                            st.info("AI 研讀了摘要，但目前現有會議分類中沒有完美契合的標籤，建議使用關鍵字搜尋。")
                            
                    except Exception as e:
                        st.error(f"AI 媒合失敗，請確認 st.secrets 中已配置正確的 API 密鑰。錯誤訊息: {str(e)}")
                        
    # 子區塊 B：傳統會議條件篩選 (已修正為預設內縮灰色框，完美保持階層感)
    with st.expander("🧪 會議條件篩選", expanded=False):
        col1, col2 = st.columns(2)
        
        # 關鍵字搜尋區 (底部對齊，完美支援手機排版)
        sub_col_input, sub_col_btn = col1.columns([5, 1], vertical_alignment="bottom")
        search_keyword = sub_col_input.text_input("🔎 關鍵字搜尋")
        sub_col_btn.button("GO", use_container_width=True, help="點擊套用關鍵字搜尋")
        
        if category_col:
            selected_categories = col2.multiselect(
                "🏷️ 專業類別 (可複選)", 
                options=all_categories,
                default=st.session_state.ai_suggested_cats
            )
        else:
            selected_categories = []
            col2.write("\n*(未偵測到帶有「類別」或「分類」關鍵字之欄位)*")

    # 主區塊底部的組織公告說明
    st.markdown("<p style='font-size: 14px; color: #94a3b8; margin-top: 15px; margin-bottom: 5px;'>關於系統收錄的 223 個國際組織：以下匯集 WHO 及國際重要醫學教育機構資料，供同仁交流參考，最新會期與變更狀況請以官網為準。</p>", unsafe_allow_html=True)

# --- 6. 呈現 ---
filtered_df = df.copy()
if search_keyword:
    mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_keyword, case=False)).any(axis=1)
    filtered_df = filtered_df[mask]
    
if selected_categories and category_col:
    filtered_df = filtered_df[filtered_df[category_col].apply(lambda x: any(cat in str(x) for cat in selected_categories))]

st.write(f"共找到 **{len(filtered_df)}** 筆資料：")
st.write("*(提示：點擊標題列可進行排序，如月份，表格支援左右滑動以檢視完整欄位)*")

# --- 全自動偵測內容包含網址的欄位並美化成超連結與置中配置 ---
table_column_config = {}
for idx, col in enumerate(filtered_df.columns):
    sample_series = filtered_df[col].astype(str)
    is_link = sample_series.str.contains('http://|https://|www\.', case=False, regex=True).any()
    
    align_center = idx in [2, 3, 4]
    
    if is_link:
        table_column_config[col] = st.column_config.LinkColumn(
            col, 
            display_text="🔗 點擊前往", 
            alignment="center" if align_center else None
        )
    elif align_center:
        table_column_config[col] = st.column_config.Column(alignment="center")

st.dataframe(
    filtered_df, 
    use_container_width=True, 
    hide_index=True,
    column_config=table_column_config
)

# --- 7. 下載 ---
if not filtered_df.empty:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_df.to_excel(writer, index=False)
    st.download_button("📥 下載本次查詢結果", data=output.getvalue(), file_name="會議查詢結果.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
