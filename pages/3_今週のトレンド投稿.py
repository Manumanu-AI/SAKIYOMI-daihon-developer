import streamlit as st
import streamlit.components.v1 as components
from application.instagram_trend_post_service import InstagramTrendPostService
from application.canva_template_service import CanvaTemplateService
import re

instagram_trend_post_service = InstagramTrendPostService()
canva_template_service = CanvaTemplateService()

instagram_trend_posts = instagram_trend_post_service.get_weekly_trend_posts()
canva_templates = canva_template_service.list_canva_templates()

# ページの設定
st.set_page_config(
    page_title="デザイン提案",
    page_icon='🤖',
    layout='wide',
)
st.sidebar.title('メニュー')

# ページタイトル
st.title('デザイン提案')

# タブの作成
tab1, tab2 = st.tabs(["今週のトレンド投稿", "Canvaデザイン"])

with tab1:
    st.header('今週のトレンド投稿')

    # 3列に分けて表示
    col1, col2, col3 = st.columns(3)

    # リストの値を繰り返し表示
    for i, instagram_trend_post in enumerate(instagram_trend_posts):
        # /?\以降を削除
        cleaned_url = re.sub(r'/\?.*', '', instagram_trend_post["image_url"])

        # 最短の埋め込みコードを生成
        embed_code = f'<blockquote class="instagram-media" data-instgrm-permalink="{cleaned_url}/" data-instgrm-version="14"><a href="{cleaned_url}/">この投稿をInstagramで見る</a></blockquote><script async src="//www.instagram.com/embed.js"></script>'

        if i % 3 == 0:
            with col1:
                components.html(embed_code, height=600)
        elif i % 3 == 1:
            with col2:
                components.html(embed_code, height=600)
        else:
            with col3:
                components.html(embed_code, height=600)

with tab2:
    st.header('Canvaデザイン')

    # CanvaのURLのリストとボタンのリンク
    canva_items = [
    {
        "embed_url": template["embed_url"],
        "button_url": template["button_url"]
    }
    for template in canva_templates
    ]

    # 3列に分けて表示
    col1, col2, col3 = st.columns(3)

    # Canvaの埋め込みコードとボタンを生成して表示
    for i, item in enumerate(canva_items):
        canva_embed_code = f'''
        <div style="position: relative; width: 100%; height: 0; padding-top: 125.0000%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0;" src="{item['embed_url']}?embed" allowfullscreen="allowfullscreen" allow="fullscreen"></iframe>
        </div>
        '''

        button_code = f'''
        <div style="text-align: center; margin-top: 10px;">
          <a href="{item['button_url']}" target="_blank" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px;">テンプレを使用する</a>
        </div>
        '''

        if i % 3 == 0:
            with col1:
                components.html(canva_embed_code + button_code, height=500)
        elif i % 3 == 1:
            with col2:
                components.html(canva_embed_code + button_code, height=500)
        else:
            with col3:
                components.html(canva_embed_code + button_code, height=500)
