# pages/5_インサイト分析.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight
import traceback
from datetime import datetime

# 既存のダイアログ関数（add_insight_dialog, edit_insight_dialog）はそのままです

def main():
    st.title("インサイトデータ表示")

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("ログインしていません。先にログインしてください。")
        return

    user_id = st.session_state.get('user_info', {}).get('localId')
    if not user_id:
        st.error("ユーザー情報が見つかりません。再度ログインしてください。")
        return

    service = InsightService()

    st.sidebar.write("デバッグ情報:")
    st.sidebar.write(f"ログイン状態: {st.session_state.get('logged_in', False)}")
    st.sidebar.write(f"ユーザーID: {user_id}")

    try:
        insights = service.get_insights_by_user(user_id)
        st.sidebar.write(f"取得したインサイト数: {len(insights)}")
        
        if insights:
            insights_df = pd.DataFrame([insight.dict() for insight in insights])
            st.sidebar.write("データフレーム作成成功")
            st.sidebar.write(f"データフレームの行数: {len(insights_df)}")

            if not insights_df.empty:
                insights_df['posted_at'] = pd.to_datetime(insights_df['posted_at'])

                # カラムの順序を指定
                column_order = ['post_id', 'post_url', 'plot', 'save_count', 'like_count', 'reach_count', 'new_reach_count', 'followers_reach_count', 'posted_at']
                insights_df = insights_df[column_order]

                st.dataframe(
                    insights_df,
                    column_config={
                        "post_id": st.column_config.TextColumn("Post ID"),
                        "post_url": st.column_config.TextColumn("Post URL"),
                        "plot": st.column_config.TextColumn("Plot"),
                        "save_count": st.column_config.NumberColumn("Save Count"),
                        "like_count": st.column_config.NumberColumn("Like Count"),
                        "reach_count": st.column_config.NumberColumn("Reach Count"),
                        "new_reach_count": st.column_config.NumberColumn("New Reach Count"),
                        "followers_reach_count": st.column_config.NumberColumn("Followers Reach Count"),
                        "posted_at": st.column_config.DatetimeColumn("Posted At", format="YYYY-MM-DD HH:mm:ss"),
                    },
                    hide_index=True,
                )

                # 区切り線とスペーサーを追加
                st.markdown("---")
                st.markdown("<br>", unsafe_allow_html=True)

                # データ操作セクション
                st.header("データ操作")

                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("投稿データを追加", use_container_width=True):
                        add_insight_dialog()

                with col2:
                    if st.button("投稿データを編集", use_container_width=True):
                        edit_insight_dialog()

                with col3:
                    post_id_to_delete = st.selectbox("削除する投稿を選択", options=insights_df['post_id'].tolist())
                    if st.button("削除", use_container_width=True):
                        result = service.delete_insight(user_id, post_id_to_delete)
                        if result["status"] == "success":
                            st.success(f"Post {post_id_to_delete} deleted successfully")
                            st.rerun()
                        else:
                            st.error(f"Failed to delete post {post_id_to_delete}")

            else:
                st.info("インサイトデータがありません。データフレームが空です。")
        else:
            st.info("インサイトデータがありません。get_insights_by_userが空のリストを返しました。")

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.sidebar.write("エラーの詳細:")
        st.sidebar.code(traceback.format_exc())

if __name__ == "__main__":
    main()
