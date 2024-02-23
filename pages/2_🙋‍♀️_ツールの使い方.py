import streamlit as st
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

st.header('台本の生成方法')

st.video('https://youtu.be/SZjbQvWrXYA?si=iI3j92OLbI5YiXfl')

st.markdown('#')
st.subheader('操作方法')
text1 = '''
<p class="tighter">
<b>1. 「生成指示」に下記の3項目を入力する</b><br>
- テーマ<br>
- ターゲット<br>
- その他の指示<br>
（<a href="https://www.notion.so/SAKIYOMI-AI-for-12-25-2924739ce4a84017a90384e01c7b00b5?pvs=21" target="_blank">参考例</a>）<br>


<b>2. 「参考URL」にAIに参照させたいサイトのURLを必ず1つ入力する</b><br>
＊InstagramのURLやYouTube、画像素材サイトは使用不可<br>    
<b>3. 「送信」を押す</b>
</p>
'''

st.markdown(text1, unsafe_allow_html=True)

st.markdown('#')


# カスタムCSSを適用したテキストを表示
text2 = '''
<p class="tighter">
	<b>注意点</b> <br>
	生成中にPCがスリープモードに入ると、生成がストップします。<br>
	スリープモードを1〜2分で設定してる人は、5分へ設定変更してください。
</p>
'''

st.markdown(text2, unsafe_allow_html=True)

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
0個だとエラーになるため、最低でも1個は必要となります。<br>

<b>Q. 参考URLに動画・画像・Instagramの投稿は登録可能？</b><br>
A.<br>
登録不可です。<br>
また画像素材サイトも使用出来ません。<br>
</p>
'''

st.markdown(text3, unsafe_allow_html=True)
