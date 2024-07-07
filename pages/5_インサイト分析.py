# pages/5_インサイトデータ表示.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight

def main():
    st.title("インサイトデータ表示")

    service = InsightService()

    # データの取得
    insights = service.get_all_insights()

    # DataFrameの作成
    df = pd.DataFrame([insight.dict() for insight in insights])

    # 編集可能な表の表示
    edited_df = st.data_editor(df)

    if st.button("保存"):
        # 変更されたデータの保存
        for index, row in edited_df.iterrows():
            insight = Insight(**row.to_dict())
            result = service.update_insight(insight)
            if result["status"] == "success":
                st.success(f"Post {insight.post_id} updated successfully")
            else:
                st.error(f"Failed to update post {insight.post_id}")

if __name__ == "__main__":
    main()
