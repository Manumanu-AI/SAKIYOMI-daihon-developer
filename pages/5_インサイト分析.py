# pages/5_インサイト分析.py

import streamlit as st
import pandas as pd
import numpy as np
from application.insight_service import InsightService
from domain.insight import Insight
import traceback
from datetime import datetime, timedelta

@st.experimental_dialog("投稿データを追加", width="large")
def add_insight_dialog():
    with st.form("new_insight_form"):
        post_url = st.text_input("Post URL")
        plot = st.text_area("Plot")
        save_count = st.number_input("Save Count", min_value=0, step=1)
        like_count = st.number_input("Like Count", min_value=0, step=1)
        reach_count = st.number_input("Reach Count", min_value=0, step=1)
        new_reach_count = st.number_input("New Reach Count", min_value=0, step=1)
        followers_reach_count = st.number_input("Followers Reach Count", min_value=0, step=1)
        posted_at = st.date_input("Posted At")

        submitted = st.form_submit_button("保存")
        if submitted:
            service = InsightService()
            user_id = st.session_state.get('user_info', {}).get('localId')
            new_insight = Insight(
                user_id=user_id,
                post_url=post_url,
                plot=plot,
                save_count=save_count,
                like_count=like_count,
                reach_count=reach_count,
                new_reach_count=new_reach_count,
                followers_reach_count=followers_reach_count,
                posted_at=posted_at,
                created_at=datetime.now()
            )
            result = service.create_new_insight(new_insight)
            if result["status"] == "success":
                st.success("新しい投稿データが追加されました")
                st.rerun()
            else:
                st.error("投稿データの追加に失敗しました")

@st.experimental_dialog("投稿データを編集", width="large")
def edit_insight_dialog():
    service = InsightService()
    user_id = st.session_state.get('user_info', {}).get('localId')
    insights = service.get_insights_by_user(user_id)
    insights_df = pd.DataFrame([insight.dict() for insight in insights])
    
    post_id = st.selectbox("編集する投稿を選択", options=insights_df['post_id'].tolist())
    insight_to_edit = insights_df[insights_df['post_id'] == post_id].iloc[0]

    with st.form("edit_insight_form"):
        post_url = st.text_input("Post URL", value=insight_to_edit['post_url'])
        plot = st.text_area("Plot", value=insight_to_edit['plot'])
        save_count = st.number_input("Save Count", value=insight_to_edit['save_count'], min_value=0, step=1)
        like_count = st.number_input("Like Count", value=insight_to_edit['like_count'], min_value=0, step=1)
        reach_count = st.number_input("Reach Count", value=insight_to_edit['reach_count'], min_value=0, step=1)
        new_reach_count = st.number_input("New Reach Count", value=insight_to_edit['new_reach_count'], min_value=0, step=1)
        followers_reach_count = st.number_input("Followers Reach Count", value=insight_to_edit['followers_reach_count'], min_value=0, step=1)
        posted_at = st.date_input("Posted At", value=pd.to_datetime(insight_to_edit['posted_at']).date())

        submitted = st.form_submit_button("更新")
        if submitted:
            updated_insight = Insight(
                post_id=post_id,
                user_id=user_id,
                post_url=post_url,
                plot=plot,
                save_count=save_count,
                like_count=like_count,
                reach_count=reach_count,
                new_reach_count=new_reach_count,
                followers_reach_count=followers_reach_count,
                posted_at=posted_at,
                created_at=insight_to_edit['created_at']
            )
            result = service.update_insight(updated_insight)
            if result["status"] == "success":
                st.success(f"Post {post_id} updated successfully")
                st.rerun()
            else:
                st.error(f"Failed to update post {post_id}")

def main():
    st.markdown("## インサイト分析")  # タイトルを変更し、サイズを小さく

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
            insights_df['posted_at'] = pd.to_datetime(insights_df['posted_at'])

            # サマリーセクション
            st.markdown("### サマリ")  # サマリの文字を小さく

            # 日付範囲選択
            col1, col2 = st.columns(2)
            with col1:
                end_date = st.date_input("終了日", value=datetime.now().date())
            with col2:
                start_date = st.date_input("開始日", value=end_date - timedelta(days=6))

            # 選択された期間のデータをフィルタリング
            mask = (insights_df['posted_at'].dt.date >= start_date) & (insights_df['posted_at'].dt.date <= end_date)
            filtered_df = insights_df.loc[mask]

            # サマリーデータの計算
            summary_data = {
                "保存数": filtered_df['save_count'].sum(),
                "リーチ数": filtered_df['reach_count'].sum(),
                "保存率": np.round(filtered_df['save_count'].sum() / filtered_df['reach_count'].sum() * 100, 2) if filtered_df['reach_count'].sum() > 0 else 0,
                "フォロワーリーチ数": filtered_df['followers_reach_count'].sum(),
                "新規リーチ数": filtered_df['new_reach_count'].sum(),
                "ホーム率": 0,  # この値の計算方法が不明なため、0としています
                "いいね数": filtered_df['like_count'].sum(),
                "フォロワー数": 0,  # この値はデータフレームに含まれていないため、0としています
            }

            # サマリーの表示（1行8列に）
            cols = st.columns(8)
            metrics = [
                ("保存数", f"{summary_data['保存数']:,}"),
                ("リーチ数", f"{summary_data['リーチ数']:,}"),
                ("保存率", f"{summary_data['保存率']}%"),
                ("フォロワーリーチ数", f"{summary_data['フォロワーリーチ数']:,}"),
                ("新規リーチ数", f"{summary_data['新規リーチ数']:,}"),
                ("ホーム率", f"{summary_data['ホーム率']}%"),
                ("いいね数", f"{summary_data['いいね数']:,}"),
                ("フォロワー数", f"{summary_data['フォロワー数']:,}")
            ]
            for col, (label, value) in zip(cols, metrics):
                col.metric(label, value)

            st.sidebar.write("データフレーム作成成功")
            st.sidebar.write(f"データフレームの行数: {len(insights_df)}")

            # 表の上に「投稿データ」と記載
            st.markdown("### 投稿データ")

            # カラムの順序を指定
            column_order = ['post_id', 'post_url', 'plot', 'save_count', 'like_count', 'reach_count', 'new_reach_count', 'followers_reach_count', 'posted_at']
            insights_df = insights_df[column_order]

            st.dataframe(
                insights_df,
                column_config={
                    "post_id": st.column_config.TextColumn("投稿ID"),
                    "post_url": st.column_config.TextColumn("投稿URL"),
                    "plot": st.column_config.TextColumn("プロット"),
                    "save_count": st.column_config.NumberColumn("保存数"),
                    "like_count": st.column_config.NumberColumn("いいね数"),
                    "reach_count": st.column_config.NumberColumn("リーチ数"),
                    "new_reach_count": st.column_config.NumberColumn("新規リーチ数"),
                    "followers_reach_count": st.column_config.NumberColumn("フォロワーリーチ数"),
                    "posted_at": st.column_config.DatetimeColumn("投稿日時", format="YYYY-MM-DD HH:mm:ss"),
                },
                hide_index=True,
            )
        else:
            st.info("インサイトデータがありません。下のボタンからデータを追加してください。")

        # 区切り線とスペーサーを追加
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)

        # データ操作セクション
        st.markdown("### データ操作")

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("投稿データを追加", use_container_width=True):
                add_insight_dialog()
            if st.button("投稿データを編集", use_container_width=True):
                edit_insight_dialog()

        with col2:
            if insights:
                post_id_to_delete = st.selectbox("削除する投稿を選択", options=insights_df['post_id'].tolist())
                if st.button("削除", use_container_width=True):
                    result = service.delete_insight(user_id, post_id_to_delete)
                    if result["status"] == "success":
                        st.success(f"投稿 {post_id_to_delete} が正常に削除されました")
                        st.rerun()
                    else:
                        st.error(f"投稿 {post_id_to_delete} の削除に失敗しました")
            else:
                st.info("削除するデータがありません。先にデータを追加してください。")

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.sidebar.write("エラーの詳細:")
        st.sidebar.code(traceback.format_exc())

if __name__ == "__main__":
    main()
