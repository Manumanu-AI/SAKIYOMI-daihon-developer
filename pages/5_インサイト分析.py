@st.experimental_dialog("投稿データを削除", width="large")
def delete_insight_dialog():
    service = InsightService()
    user_id = st.session_state.get('user_info', {}).get('localId')
    insights = service.get_insights_by_user(user_id)
    insights_df = pd.DataFrame([insight.dict() for insight in insights])
    
    post_id = st.selectbox("削除する投稿を選択", options=insights_df['post_id'].tolist())
    
    if 'delete_state' not in st.session_state:
        st.session_state.delete_state = 'initial'

    if st.session_state.delete_state == 'initial':
        if st.button("削除"):
            st.session_state.delete_state = 'confirm'
            st.rerun()
    
    elif st.session_state.delete_state == 'confirm':
        st.warning("本当に削除しますか？操作は取り消せません。")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("キャンセル"):
                st.session_state.delete_state = 'initial'
                st.rerun()
        with col2:
            if st.button("はい"):
                st.session_state.delete_state = 'delete'
                st.rerun()

    if st.session_state.delete_state == 'delete':
        result = service.delete_insight(user_id, post_id)
        if result["status"] == "success":
            st.success(f"Post {post_id} deleted successfully")
            st.session_state.need_update = True
            st.session_state.delete_state = 'initial'
            st.rerun()
        else:
            st.error(f"Failed to delete post {post_id}")
            st.session_state.delete_state = 'initial'
