# pages/5_インサイト分析.py

import streamlit as st
import pandas as pd
import numpy as np
from application.insight_service import InsightService
from domain.insight import Insight
import traceback
from datetime import datetime, timedelta

# ... (前のコードは変更なし)

def main():
    # ... (前のコードは変更なし)

    try:
        insights = service.get_insights_by_user(user_id)
        st.sidebar.write(f"取得したインサイト数: {len(insights)}")
        
        if insights:
            insights_df = pd.DataFrame([insight.dict() for insight in insights])
            insights_df['posted_at'] = pd.to_datetime(insights_df['posted_at'])

            # サマリーセクション
            st.header("サマリ")

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

            # サマリーの表示（st.metricを使用）
            col1, col2, col3, col4 = st.columns(4)
            col5, col6, col7, col8 = st.columns(4)

            col1.metric("保存数", f"{summary_data['保存数']:,}")
            col2.metric("リーチ数", f"{summary_data['リーチ数']:,}")
            col3.metric("保存率", f"{summary_data['保存率']}%")
            col4.metric("フォロワーリーチ数", f"{summary_data['フォロワーリーチ数']:,}")
            col5.metric("新規リーチ数", f"{summary_data['新規リーチ数']:,}")
            col6.metric("ホーム率", f"{summary_data['ホーム率']}%")
            col7.metric("いいね数", f"{summary_data['いいね数']:,}")
            col8.metric("フォロワー数", f"{summary_data['フォロワー数']:,}")

            # ... (残りのコードは変更なし)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        st.sidebar.write("エラーの詳細:")
        st.sidebar.code(traceback.format_exc())

if __name__ == "__main__":
    main()
