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

# --- UI構築 ---
st.title("🌌 架空世界バーチャル観光プラットフォーム")
folder_id = st.text_input("Google Drive フォルダIDを入力:")

if folder_id:
    try:
        files = list_files_in_folder(folder_id)
        
        # ファイル種別ごとに分類（mimeTypeで判定）
        videos = [f for f in files if 'video' in f['mimeType']]
        images = [f for f in files if 'image' in f['mimeType']]
        texts = [f for f in files if 'text' in f['mimeType']]

        col1, col2 = st.columns([2, 1])
        with col1:
            if videos:
                st.video(videos[0]['webViewLink'])
            for img in images:
                st.image(img['webViewLink'])
        with col2:
            for txt in texts:
                # サービスアカウントによる内容取得は別途権限が必要なため、
                # まずはwebViewLinkでファイル内容を確認するのが無難です
                st.markdown(f"[{txt['name']}]({txt['webViewLink']})")

    except Exception as e:
        st.error(f"接続エラー: {e}")
