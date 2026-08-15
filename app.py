import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

# --- Google Drive 認証関数 ---
@st.cache_resource
def get_drive():
    gauth = GoogleAuth()
    # 自動認証の設定（初回はブラウザが開きます）
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

# --- ファイル一覧取得関数 ---
def list_files_in_drive(folder_id):
    drive = get_drive()
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    return file_list

# --- Streamlit アプリ構成 ---
st.set_page_config(page_title="WorldBuilder Platform", layout="wide")
st.title("🌌 架空世界バーチャル観光プラットフォーム")

# サイドバーでフォルダIDを入力
folder_id = st.sidebar.text_input("Google Drive フォルダIDを入力:")

if folder_id:
    try:
        files = list_files_in_drive(folder_id)
        
        # ファイルの分類
        videos = [f for f in files if 'video' in f['mimeType']]
        images = [f for f in files if 'image' in f['mimeType']]
        texts = [f for f in files if 'text' in f['mimeType']]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("🎥 メインビュー")
            if videos:
                # 実際のWeb公開用リンクを取得（要: 権限設定）
                st.video(videos[0]['alternateLink']) 
            
            st.subheader("🖼️ 風景イメージ")
            for img in images:
                st.image(img['alternateLink'])

        with col2:
            st.subheader("📜 世界観設定")
            for txt in texts:
                content = txt.GetContentString()
                st.write(content)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("左側のサイドバーに、観光地データが入ったGoogleドライブのフォルダIDを入力してください。")
