import streamlit as st
import streamlit.components.v1 as components
import re

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

    # InstagramのURLのリスト
    instagram_urls = [
        'https://www.instagram.com/p/C5az-xYv_8v',
        'https://www.instagram.com/p/C5k1fixvMIP/?img_index=1',
        'https://www.instagram.com/p/C5az-xYv_8v/?img_index=1',
        'https://www.instagram.com/p/C5OJTpEvZ9v/?img_index=1',
        'https://www.instagram.com/p/C5AwrsqOy_g/?img_index=1',
        'https://www.instagram.com/p/C4xfOTDvHbV/?img_index=1',
        'https://www.instagram.com/p/C4h3MGrJkaS/?img_index=1',
        'https://www.instagram.com/p/C4c_DLNv5A6/?img_index=1',
        'https://www.instagram.com/p/C4P4KrZvCFu/?img_index=1'
    ]

    # 3列に分けて表示
    col1, col2, col3 = st.columns(3)

    # リストの値を繰り返し表示
    for i, url in enumerate(instagram_urls):
        # /?\以降を削除
        cleaned_url = re.sub(r'/\?.*', '', url)
        
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
            "embed_url": "https://www.canva.com/design/DAGFLSPbwsQ/JCvjuwoBa9gW5eYfokggWg/view",
            "button_url": "https://www.canva.com/design/DAFf5KnMSsI/0jYScCGQ_Pj83v2RAm_36w/view?utm_content=DAFf5KnMSsI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLSQm_oU/mbsnhOo2z5XW6Krr1I3PGg/view",
            "button_url": "https://www.canva.com/design/DAFO1ftprAA/Zpj4rNVqB4gy8UZ2SgvgMQ/view?utm_content=DAFO1ftprAA&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLcSuR_o/cbbDm_ymB3mFB7eTXpvXZA/view",
            "button_url": "https://www.canva.com/design/DAFf5KnMSsI/0jYScCGQ_Pj83v2RAm_36w/view?utm_content=DAFf5KnMSsI&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLR9H73s/HrPfu9sJdDxIlD0-vTXdbg/view",
            "button_url": "https://www.canva.com/design/DAFDxk5uaf0/B82mafUpqiKlYvPG2pC3eg/view?utm_content=DAFDxk5uaf0&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLQzcfOI/5kxozzhURKAoCEag4I4m8A/view",
            "button_url": "https://www.canva.com/design/DAFQmbG2Z_s/ZHkevvfxb-qGAWBq7dpWhw/view?utm_content=DAFQmbG2Z_s&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLUYw144/zdrcK7Wl2ldP_nJ-KEOMwQ/view",
            "button_url": "https://www.canva.com/design/DAFQmAjpl6M/7sOsbIPjmQ4-aPlHw5nZbQ/view?utm_content=DAFQmAjpl6M&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        },
        {
            "embed_url": "https://www.canva.com/design/DAGFLTf9-tg/ZiZEnnWiqacBwIXy_EQe0g/view",
            "button_url": "https://www.canva.com/design/DAFDxRJf4gc/qZKcaRU2gBuuVH0m0r8TyA/view?utm_content=DAFDxRJf4gc&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink&mode=preview"
        }
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
