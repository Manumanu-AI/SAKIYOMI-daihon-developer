# pages/5_インサイトデータ表示.py

import streamlit as st
import pandas as pd
from application.insight_service import InsightService
from domain.insight import Insight

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
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

            # 編集可能な表の表示
            edited_df = st.data_editor(df)

            if st.button("保存"):
                # 変更されたデータの保存
                for index, row in edited_df.iterrows():
                    insight = Insight(**row.to_dict())
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
