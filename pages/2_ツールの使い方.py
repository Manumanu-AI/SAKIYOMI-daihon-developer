import streamlit as st
st.set_page_config(
    page_icon='🤖',
    layout='wide',
)

st.sidebar.title('メニュー')

custom_css = """
<style>
    .tighter {
        line-height: 1.3; /* 行間を狭めるための値。適宜調整してください */
    }
</style>
"""

# カスタムCSSを適用する
st.markdown(custom_css, unsafe_allow_html=True)


st.title('ツールの使い方')
st.markdown('#')

st.header('ツールの使い方 - 24/7/31更新')

st.video('https://youtu.be/qCmEa33JKSA')

st.header('新バージョンの概要')

st.video('https://youtu.be/TnEDGd1SKA0')


st.markdown('##')

st.subheader('よくある質問')
# カスタムCSSを適用したテキストを表示
text3 = '''
<p class="tighter">
<b>Q. 生成指示の参考例はありますか？</b><br>
A.<br>
こちらをご参照ください。
（<a href="https://www.notion.so/SAKIYOMI-AI-for-12-25-2924739ce4a84017a90384e01c7b00b5?pvs=21" target="_blank">生成指示の参考例</a>）<br><br>
<b>Q. 参考URLは1個しか登録出来ないですか？または、参考URL0個は可能？</b><br>
A.<br>
現時点では1個のみです。<br>
LP、ブログ、Note等のURLを読み込むことができます。<br>

<b>Q. 参考URLに動画・画像・Instagramの投稿は登録可能？</b><br>
A.<br>
登録不可となります。<br>
画像素材サイト等もご使用いただけません。<br>
</p>
'''

# カスタムCSSを適用したテキストを表示
text2 = '''
<p class="tighter">
	<b>注意点</b> <br>
	生成中にPCがスリープモードに入ると、生成がストップします。<br>
	スリープモードを1〜2分で設定してる人は、5分へ設定変更してください。
</p>
'''

st.markdown(text3, unsafe_allow_html=True)

st.markdown(text2, unsafe_allow_html=True)



