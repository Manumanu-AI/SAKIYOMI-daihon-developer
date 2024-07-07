# pages/5_インサイト分析.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight

def main():
    st.title("インサイトデータ表示")

    # ログイン状態のチェック
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.warning("ログインしていません。先にログインしてください。")
        return

    # ユーザーIDの取得
    user_id = st.session_state.get('user_info', {}).get('localId')
    if not user_id:
        st.error("ユーザー情報が見つかりません。再度ログインしてください。")
        return

    service = InsightService()

    if 'insights_df' not in st.session_state:
        insights = service.get_insights_by_user(user_id)
        st.session_state.insights_df = pd.DataFrame([insight.dict() for insight in insights])

    # 以下、既存のコードと同様...

    if not st.session_state.insights_df.empty:
        st.session_state.insights_df['created_at'] = pd.to_datetime(st.session_state.insights_df['created_at'])

        edited_df = st.data_editor(
            st.session_state.insights_df,
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
                st.session_state.insights_df = pd.concat([st.session_state.insights_df, new_row], ignore_index=True)
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
            
            st.session_state.insights_df = edited_df

    else:
        st.info("インサイトデータがありません。")

if __name__ == "__main__":
    main()
