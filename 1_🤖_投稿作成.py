import streamlit as st
import scraping_helper as sh
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

st.set_page_config(
    page_icon='🤖',
    layout='wide',
)

st.title('SAKIYOMI 投稿作成AI')

st.sidebar.title('メニュー')

# タブセット1: "Input / Generated Script" を含むタブ
tab1, tab2 = st.tabs(["プロット生成", "データ登録"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        user_input = st.text_area("生成指示 : 作りたいプロットのイメージを入力", value="""以下の内容で台本を書いてください。\nテーマ：\n\nターゲット：\n\nその他の指示：""", height=300)
        url = st.text_input("参考URL")
        submit_button = st.button('送信')

        if submit_button:
            if 'last_url' not in st.session_state or st.session_state['last_url'] != url:
                index = sh.initialize_pinecone()
                try:
				# ns1のデータを削除しようと試みる
                    sh.delete_all_data_in_namespace(index, "ns1")
                except Exception:
            # エラーが発生しても何もせずに処理を続行する
                    pass

                st.session_state['last_url'] = url
                scraped_data = sh.scrape_url(url)
                combined_text, metadata_list = sh.prepare_text_and_metadata(sh.extract_keys_from_json(scraped_data))
                chunks = sh.split_text(combined_text)
                embeddings = sh.make_chunks_embeddings(chunks)
                sh.store_data_in_pinecone(index, embeddings, chunks, metadata_list, "ns1")
                time.sleep(10)
                st.success("ウェブサイトを読み込みました！")
            else:
                st.info("同じウェブサイトのデータを使用")


    with col2:
        if submit_button:
            namespaces = ["ns1", "ns2", "ns3", "ns4", "ns5"]
            index = sh.initialize_pinecone()
            response = sh.generate_response_with_llm_for_multiple_namespaces(index, user_input, namespaces)
            if response:  # responseがNoneでないことを確認
                response_text = response.get('text')
                st.session_state['response_text'] = response_text  # セッション状態にresponse_textを保存
            else:
                st.session_state['response_text'] = "エラー: プロットを生成できませんでした。"

        # セッション状態からresponse_textを取得、存在しない場合はデフォルトのメッセージを表示
        displayed_value = st.session_state.get('response_text', "生成結果 : プロットが表示されます")
        st.text_area("生成結果", value=displayed_value, height=400)
  




# タブ2: パラメーター設定
with tab2:
    st.header('データを登録')
    # 2カラムを作成
    col1, col2, col3, col4 = st.columns(4)

    with col1:  
        index = sh.initialize_pinecone()
        st.subheader("URLの登録")

        # URL入力
        url = st.text_input("登録URLを入力してください")

        # 登録ボタン
        register_button1 = st.button("URL登録")

        if register_button1:
            # スクレイピング
            scraped_data = sh.scrape_url(url)


            combined_text, metadata_list = sh.prepare_text_and_metadata(sh.extract_keys_from_json(scraped_data))


            chunks = sh.split_text(combined_text)

            embeddings = sh.make_chunks_embeddings(chunks)

            # Pineconeにデータを保存
            sh.store_data_in_pinecone(index, embeddings, chunks, metadata_list, "ns2")

            st.success("データをPineconeに登録しました！")

        # 全データ削除ボタン
        delete_all_button1 = st.button("URL全データ削除")

        if delete_all_button1:
            sh.delete_all_data_in_namespace(index, "ns2")  # 全データを削除する関数を呼び出し
            st.success("全データが削除されました！")


    with col2:
        index = sh.initialize_pinecone()  # Pineconeを初期化
        st.subheader("過去プロットの登録")

        # PDFファイルアップロード
        pdf_file1 = st.file_uploader("PDFファイルをアップロード", type=["pdf"], key="pdf_file1")

        # 登録ボタン
        register_button2 = st.button("PDF登録")

        if register_button2 and pdf_file1 is not None:
            # PDFファイルからテキストを抽出
            pdf_text = sh.extract_text_from_pdf(pdf_file1)
            
            # テキストをチャンクに分割
            chunks = sh.split_text(pdf_text)
            
            # チャンクの埋め込みを生成
            embeddings = sh.make_chunks_embeddings(chunks)


            # Pineconeにデータを保存
            sh.store_pdf_data_in_pinecone(index, embeddings, pdf_file1.name, "ns3")
            st.success("データをPineconeに登録しました！")

        # 全データ削除ボタン
        delete_all_button2 = st.button("全データ削除")

        if delete_all_button2:
            # 全データを削除する関数を呼び出し
            sh.delete_all_data_in_namespace(index, "ns3")
            st.success("全データが削除されました！")


    with col3:
        index = sh.initialize_pinecone()  # Pineconeを初期化
        st.subheader("競合データの登録")

        # PDFファイルアップロード
        pdf_file2 = st.file_uploader("PDFファイルをアップロード", type=["pdf"], key="pdf_file2")   

        # 登録ボタン
        register_button3 = st.button("PDF登録", key="register_button3")

        if register_button3 and pdf_file2 is not None:
            # PDFファイルからテキストを抽出
            pdf_text = sh.extract_text_from_pdf(pdf_file2)
            
            # テキストをチャンクに分割
            chunks = sh.split_text(pdf_text)
            
            # チャンクの埋め込みを生成
            embeddings = sh.make_chunks_embeddings(chunks)


            # Pineconeにデータを保存
            sh.store_pdf_data_in_pinecone(index, embeddings, pdf_file2.name, "ns4")
            st.success("データをPineconeに登録しました！")

        # 全データ削除ボタン
        delete_all_button3 = st.button("全データ削除", key="delete_all_3")

        if delete_all_button3:
            # 全データを削除する関数を呼び出し
            sh.delete_all_data_in_namespace(index, "ns4")
            st.success("全データが削除されました！")

    with col4:
        index = sh.initialize_pinecone()  # Pineconeを初期化
        st.subheader("SAKIYOMIデータの登録")

        # PDFファイルアップロード
        pdf_file3 = st.file_uploader("PDFをアップロード", type=["pdf"], key="pdf_file3")

        # 登録ボタン
        register_button4 = st.button("PDF登録", key="register_button4")

        if register_button4 and pdf_file3 is not None:
            # PDFファイルからテキストを抽出
            pdf_text = sh.extract_text_from_pdf(pdf_file3)
            
            # テキストをチャンクに分割
            chunks = sh.split_text(pdf_text)
            
            # チャンクの埋め込みを生成
            embeddings = sh.make_chunks_embeddings(chunks)


            # Pineconeにデータを保存
            sh.store_pdf_data_in_pinecone(index, embeddings, pdf_file3.name, "ns5")
            st.success("データをPineconeに登録しました！")

        # 全データ削除ボタン
        delete_all_button4 = st.button("全データ削除", key="delete_all_4")

        if delete_all_button4:
            # 全データを削除する関数を呼び出し
            sh.delete_all_data_in_namespace(index, "ns5")
            st.success("全データが削除されました！")
