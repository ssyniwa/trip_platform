import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
# --- 認証設定 ---
# Streamlit CloudのSecretsに設定したJSONの内容を読み込む
def get_drive_service():
    # SecretsからJSON文字列を取得
    creds_dict = json.loads(st.secrets["google_drive"]["credentials"])
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    return build('drive', 'v3', credentials=creds)

# --- ファイル一覧取得 ---
def list_files_in_folder(folder_id):
    service = get_drive_service()
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name, mimeType, webViewLink)").execute()
    return results.get('files', [])
def get_file_content(service, file_id):
    try:
        request = service.files().get_media(fileId=file_id)
        content = request.execute()
        return content.decode('utf-8')
    except Exception as e:
        return f"読み込みエラー: {e}"
# --- UI構築 ---
st.title("🌌 架空世界バーチャル観光プラットフォーム")
folder_id = st.text_input("Google Drive フォルダIDを入力:")

if folder_id:
    try:
        service = get_drive_service()
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name, mimeType, webViewLink)").execute()
        files = results.get('files', [])
        
        videos = [f for f in files if 'video' in f['mimeType']]
        images = [f for f in files if 'image' in f['mimeType']]
        # テキストファイル、または拡張子が .md / .txt のものを対象にする
        texts = [f for f in files if 'text' in f['mimeType'] or f['name'].endswith(('.txt', '.md'))]

        col1, col2 = st.columns([2, 1])
        with col1:
            if videos:
                st.video(videos[0]['webViewLink'])
            for img in images:
                st.image(img['webViewLink'])
                
        with col2:
            st.subheader("📜 世界観設定")
            for txt in texts:
                st.markdown(f"**📄 {txt['name']}**")
                # 中身を取得して表示する
                file_content = get_file_content(service, txt['id'])
                st.markdown(file_content)
                st.write("---")

    except Exception as e:
        st.error(f"接続エラー: {e}")
