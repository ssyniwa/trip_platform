import streamlit as st
import gspread
import json  # ← この行を追加または確認してください
from oauth2client.service_account import ServiceAccountCredentials

# --- 認証設定 ---
def get_gspread_client():
    creds_dict = json.loads(st.secrets["google_drive"]["credentials"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    return gspread.authorize(creds)

# --- スプレッドシート保存処理 ---
def save_to_sheet(user_name, location_name, description, image_url):
    client = get_gspread_client()
    sheet = client.open("観光地管理シート").sheet1 # スプレッドシート名
    sheet.append_row([user_name, location_name, description, image_url])

# --- UI: 登録機能 ---
with st.sidebar.expander("🚀 新しい観光地の登録"):
    user_name = st.text_input("ユーザー名:")
    location_name = st.text_input("観光地名:")
    description = st.text_area("説明文:")
    image_url = st.text_input("画像URL (Google Driveの共有リンクなど):")
    
    if st.button("データベースに保存"):
        save_to_sheet(user_name, location_name, description, image_url)
        st.success("登録完了！")

# --- UI: 表示機能 ---
st.title("🌌 架空世界バーチャル観光プラットフォーム")
if st.button("一覧を表示"):
    client = get_gspread_client()
    sheet = client.open("観光地管理シート").sheet1
    data = sheet.get_all_records()
    
    for row in data:
        st.subheader(f"{row['観光地名']} (投稿者: {row['ユーザー名']})")
        st.write(row['説明文'])
        st.image(row['画像URL'])
        st.write("---")
