# pages/5_インサイト分析.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight
import traceback
from datetime import datetime

def show_add_insight_popup():
    with st.form("add_insight_form"):
        st.subheader("新しい投稿データを追加")
        post_url = st.text_input("投稿URL")
        plot = st.text_area("プロット")
        save_count = st.number_input("保存数", min_value=0, step=1)
        like_count = st.number_input("いいね数", min_value=0, step=1)
        reach_count = st.number_input("リーチ数", min_value=0, step=1)
        new_reach_count = st.number_input("新規リーチ数", min_value=0, step=1)
        followers_reach_count = st.number_input("フォロワーリーチ数", min_value=0, step=1)
        
        submitted = st.form_submit_button("保存")
        return submitted, post_url, plot, save_count, like_count, reach_count, new_reach_count, followers_reach_count

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

                # カラムの順序を変更し、一部のカラムを非表示に
                columns_order = ['post_id', 'post_url', 'plot', 'save_count', 'like_count', 'reach_count', 'new_reach_count', 'followers_reach_count', 'posted_at']
                insights_df = insights_df[columns_order]

                edited_df = st.data_editor(
                    insights_df,
                    column_config={
                        "post_id": st.column_config.TextColumn("Post ID", disabled=True),
                        "post_url": st.column_config.TextColumn("Post URL"),
                        "plot": st.column_config.TextColumn("プロット"),
                        "save_count": st.column_config.NumberColumn("保存数", min_value=0, step=1),
                        "like_count": st.column_config.NumberColumn("いいね数", min_value=0, step=1),
                        "reach_count": st.column_config.NumberColumn("リーチ数", min_value=0, step=1),
                        "new_reach_count": st.column_config.NumberColumn("新規リーチ数", min_value=0, step=1),
                        "followers_reach_count": st.column_config.NumberColumn("フォロワーリーチ数", min_value=0, step=1),
                        "posted_at": st.column_config.DatetimeColumn("投稿日時", format="YYYY-MM-DD HH:mm:ss", step=60),
                    },
                    hide_index=True,
                    num_rows="dynamic",
                )

                col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
                with col1:
                    if st.button("投稿データを追加"):
                        st.info("投稿データを入力して、保存を押してください。")
                        st.session_state.show_popup = True

                with col2:
                    if st.button("保存"):
                        for index, row in edited_df.iterrows():
                            insight_dict = row.to_dict()
                            insight_dict['user_id'] = user_id
                            insight_dict['created_at'] = datetime.now()
                            insight = Insight.from_dict(insight_dict)
                            result = service.update_insight(insight)
                            if result["status"] == "success":
                                st.success(f"Post {insight.post_id} updated successfully")
                            else:
                                st.error(f"Failed to update post {insight.post_id}")
                        st.experimental_rerun()

                with col3:
                    post_id_to_delete = st.text_input("削除する投稿ID")

                with col4:
                    if st.button("削除"):
                        if post_id_to_delete:
                            if st.warning(f"本当に投稿ID {post_id_to_delete} を削除しますか？"):
                                result = service.delete_insight(user_id, post_id_to_delete)
                                if result["status"] == "success":
                                    st.success(f"Post {post_id_to_delete} deleted successfully")
                                    st.experimental_rerun()
                                else:
                                    st.error(f"Failed to delete post {post_id_to_delete}")
                        else:
                            st.error("削除する投稿IDを入力してください")

                if st.session_state.get('show_popup', False):
                    submitted, post_url, plot, save_count, like_count, reach_count, new_reach_count, followers_reach_count = show_add_insight_popup()
                    if submitted:
                        new_insight = Insight(
                            user_id=user_id,
                            post_url=post_url,
                            plot=plot,
                            save_count=save_count,
                            like_count=like_count,
                            reach_count=reach_count,
                            new_reach_count=new_reach_count,
                            followers_reach_count=followers_reach_count,
                            posted_at=datetime.now(),
                            created_at=datetime.now()
                        )
                        result = service.create_new_insight(new_insight)
                        if result["status"] == "success":
                            st.success(f"新しい投稿データが追加されました。Post ID: {new_insight.post_id}")
                            st.session_state.show_popup = False
                            st.experimental_rerun()
                        else:
                            st.error("投稿データの追加に失敗しました")

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
