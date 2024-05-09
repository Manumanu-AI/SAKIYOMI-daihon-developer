import streamlit as st
import streamlit.components.v1 as components
import re

# ページの設定
st.set_page_config(
    page_icon='🤖',
    layout='wide',
)

st.title('おすすめ投稿一覧(ベータ版)')
st.markdown('#')
st.header('最新の投稿')


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
