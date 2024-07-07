# pages/5_インサイトデータ表示.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight
from datetime import datetime

def main():
    st.title("インサイトデータ表示")

    service = InsightService()

    # ユーザー選択
    user_ids = service.get_user_ids()
    selected_user_id = st.selectbox("ユーザーを選択してください", user_ids)

    if selected_user_id:
        # データの取得
        insights = service.get_insights_by_user(selected_user_id)

        if insights:
            # DataFrameの作成
            df = pd.DataFrame([insight.dict() for insight in insights])

            # 日時列の形式を調整
            df['created_at'] = pd.to_datetime(df['created_at'])

            # 編集可能な表の表示
            edited_df = st.data_editor(
                df,
                column_config={
                    "created_at": st.column_config.DatetimeColumn(
                        "Created At",
                        format="YYYY-MM-DD HH:mm:ss",
                        step=60,
                    ),
                    "followers_reach_count": st.column_config.NumberColumn(
                        "Followers Reach Count",
                        min_value=0,
                        step=1,
                    ),
                    "like_count": st.column_config.NumberColumn(
                        "Like Count",
                        min_value=0,
                        step=1,
                    ),
                    "new_reach_count": st.column_config.NumberColumn(
                        "New Reach Count",
                        min_value=0,
                        step=1,
                    ),
                    "reach_count": st.column_config.NumberColumn(
                        "Reach Count",
                        min_value=0,
                        step=1,
                    ),
                    "save_count": st.column_config.NumberColumn(
                        "Save Count",
                        min_value=0,
                        step=1,
                    ),
                },
                hide_index=True,
            )

            if st.button("保存"):
                # 変更されたデータの保存
                for index, row in edited_df.iterrows():
                    insight_dict = row.to_dict()
                    insight_dict['created_at'] = insight_dict['created_at'].timestamp()
                    insight = Insight.from_dict(insight_dict)
                    result = service.update_insight(selected_user_id, insight)
                    if result["status"] == "success":
                        st.success(f"Post {insight.post_id} updated successfully")
                    else:
                        st.error(f"Failed to update post {insight.post_id}")
        else:
            st.info("選択されたユーザーのインサイトデータがありません。")
    else:
        st.info("ユーザーを選択してください。")

if __name__ == "__main__":
    main()
