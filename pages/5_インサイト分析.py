# pages/5_インサイト分析.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight

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

    # デバッグ情報
    st.write(f"User ID: {user_id}")

    # インサイトデータの取得
    insights = service.get_insights_by_user(user_id)
    
    # デバッグ情報
    st.write(f"取得したインサイトデータの数: {len(insights)}")

    if insights:
        # DataFrameの作成
        df = pd.DataFrame([insight.dict() for insight in insights])
        
        # デバッグ情報
        st.write("データフレームの内容:")
        st.write(df)

        # 日時列の形式を調整
        df['created_at'] = pd.to_datetime(df['created_at'])

        # 編集可能な表の表示
        edited_df = st.data_editor(
            df,
            column_config={
                "post_id": st.column_config.TextColumn("Post ID", disabled=True),
                "user_id": st.column_config.TextColumn("User ID", disabled=True),
                "created_at": st.column_config.DatetimeColumn("Created At", format="YYYY-MM-DD HH:mm:ss", step=60),
                "followers_reach_count": st.column_config.NumberColumn("Followers Reach Count", min_value=0, step=1),
                "like_count": st.column_config.NumberColumn("Like Count", min_value=0, step=1),
                "new_reach_count": st.column_config.NumberColumn("New Reach Count", min_value=0, step=1),
                "reach_count": st.column_config.NumberColumn("Reach Count", min_value=0, step=1),
                "save_count": st.column_config.NumberColumn("Save Count", min_value=0, step=1),
            },
            hide_index=True,
            num_rows="dynamic",
        )

        if st.button("行を挿入"):
            try:
                new_insight = service.create_new_insight(user_id)
                new_row = pd.DataFrame([new_insight.dict()])
                df = pd.concat([df, new_row], ignore_index=True)
                st.success(f"新しい行が追加されました。Post ID: {new_insight.post_id}")
            except Exception as e:
                st.error(f"行の挿入中にエラーが発生しました: {str(e)}")

        if st.button("保存"):
            for index, row in edited_df.iterrows():
                insight_dict = row.to_dict()
                insight_dict['created_at'] = insight_dict['created_at'].to_pydatetime()
                insight = Insight.from_dict(insight_dict)
                result = service.update_insight(insight)
                if result["status"] == "success":
                    st.success(f"Post {insight.post_id} updated successfully")
                else:
                    st.error(f"Failed to update post {insight.post_id}")
            
            df = edited_df

    else:
        st.info("インサイトデータがありません。")

if __name__ == "__main__":
    main()
