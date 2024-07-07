import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight

def main():
    st.title("インサイトデータ表示")

    service = InsightService()

    # データの取得
    insights = service.get_all_insights()

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
                "reach_count": st.column_config.TextColumn(
                    "Reach Count",
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
                insight_dict['created_at'] = insight_dict['created_at'].to_pydatetime()
                insight = Insight.from_dict(insight_dict)
                result = service.update_insight(insight_dict['user_id'], insight)
                if result["status"] == "success":
                    st.success(f"Post {insight.post_id} updated successfully")
                else:
                    st.error(f"Failed to update post {insight.post_id}")
    else:
        st.info("インサイトデータがありません。")

if __name__ == "__main__":
    main()
