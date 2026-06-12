# ==================== 🤖 AI 摘要智慧媒合區 (新加入) ====================
    # 初始化 session_state，用來控制多選選單的預設值
    if "ai_suggested_cats" not in st.session_state:
        st.session_state.ai_suggested_cats = []

    with st.inner_expander("🤖 AI 論文摘要/研究主題智慧媒合 (免盲搜)"):
        user_abstract = st.text_area(
            "貼上您的英文論文摘要 (Abstract) 或研究大綱：", 
            placeholder="例如：We terms to investigate the impact of AI-driven portfolios on medical faculty evaluation workflows...",
            height=100
        )
        
        if st.button("🪄 讓 AI 幫我推薦專業類別", use_container_width=True):
            if not user_abstract.strip():
                st.warning("請先輸入摘要內容喔！")
            else:
                with st.spinner("AI 正在研讀您的摘要並媒合全球會議類別..."):
                    try:
                        # 這裡使用標準 API 呼叫 (請確保環境變數或 st.secrets 有設定 KEY)
                        # 如果是用 Gemini API，可替換成 genai 的對應寫法
                        from openai import OpenAI
                        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                        
                        prompt = f"""
                        你是一位資深的國際醫學會議召集人。請閱讀以下使用者的論文摘要，並從「可選類別清單」中，
                        挑選出最符合、最相關的 1 到 3 個類別標籤。
                        
                        【使用者的論文摘要】
                        {user_abstract}
                        
                        【可選類別清單】
                        {all_categories}
                        
                        【嚴格輸出規則】
                        請只回傳一個 JSON 陣列，裡面包含挑選出的類別字串，不要任何 Markdown 標記、解釋或說明。
                        範例：["人權", "性別"]
                        """
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini", # 或使用 gemini-2.5-flash
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.2
                        )
                        
                        # 解析 AI 回傳的標籤字串
                        import json
                        raw_reply = response.choices[0].message.content.strip()
                        # 清理可能夾帶的 ```json 標籤
                        cleaned_reply = re.sub(r'
```json|```', '', raw_reply).strip()
                        suggested_tags = json.loads(cleaned_reply)
                        
                        # 過濾掉不在現有清單中的幻覺標籤
                        valid_tags = [tag for tag in suggested_tags if tag in all_categories]
                        
                        if valid_tags:
                            st.session_state.ai_suggested_cats = valid_tags
                            st.success(f"💡 AI 替您精選了標籤：{', '.join(valid_tags)}！已自動為您勾選下方選單。")
                            st.rerun() # 重新整理網頁以套用篩選
                        else:
                            st.info("AI 研讀了摘要，但目前現有會議分類中沒有完美契合的標籤，建議使用關鍵字搜尋。")
                            
                    except Exception as e:
                        st.error(f"AI 媒合失敗，請檢查 API 金鑰設定。錯誤訊息: {str(e)}")
                        
    st.markdown("---") # 分隔線
    # =====================================================================

    # 修改妳原本的 multiselect 欄位，加上 default 參數連動 session_state
    # 原本是：selected_categories = col2.multiselect("🏷️ 專業類別 (可複選)", options=all_categories)
    # 改成下方這樣：
    if category_col:
        selected_categories = col2.multiselect(
            "🏷️ 專業類別 (可複選)", 
            options=all_categories,
            default=st.session_state.ai_suggested_cats # 🔗 讓 AI 的推薦直接變成預設勾選
        )
