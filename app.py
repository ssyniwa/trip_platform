import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
def local_css():
    st.markdown("""
    <style>
    /* 全体のカード枠 */
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #6c5ce7; /* パープルのアクセント */
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    /* 全体説明エリア */
    .desc-box {
        background-color: #fdf6e3;
        padding: 15px;
        border-radius: 10px;
        color: #5d4037;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
    /* スポットカード */
    .spot-card {
        background-color: #e1f5fe;
        padding: 15px;
        border-radius: 10px;
        border-top: 5px solid #03a9f4;
        height: 100%;
    }
    .spot-text { color: #0277bd; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
# --- 認証とURL変換 ---
def get_gspread_client():
    creds_dict = json.loads(st.secrets["google_drive"]["credentials"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    return gspread.authorize(creds)

def convert_drive_url(url):
    if "drive.google.com/file/d/" in url:
        file_id = url.split("/d/")[1].split("/")[0]
        return f"https://lh3.googleusercontent.com/d/{file_id}"
    return url

# --- 登録機能 ---
with st.sidebar.expander("🚀 新しい観光地の登録"):
    user_name = st.text_input("ユーザー名:")
    location_name = st.text_input("観光地名:")
    desc_all = st.text_area("観光地全体の説明:")
    img_all = st.text_input("全体画像URL:")
    
    st.write("--- 人気スポット ---")
    spot1_desc = st.text_input("スポット1説明:")
    spot1_img = st.text_input("スポット1画像URL:")
    spot2_desc = st.text_input("スポット2説明:")
    spot2_img = st.text_input("スポット2画像URL:")
    spot3_desc = st.text_input("スポット3説明:")
    spot3_img = st.text_input("スポット3画像URL:")
    
    if st.button("登録"):
        client = get_gspread_client()
        sheet = client.open("観光地管理シート").sheet1
        sheet.append_row([user_name, location_name, desc_all, img_all, spot1_desc, spot1_img, spot2_desc, spot2_img, spot3_desc, spot3_img])
        st.success("登録完了！")

# --- 表示機能 ---
st.set_page_config(page_title="バーチャル観光プラットフォーム", layout="wide")
local_css()

# --- 表示機能 (カード型デザイン) ---
st.title("🌌 架空世界バーチャル観光プラットフォーム")
st.markdown("---")

if st.button("観光地リストを更新"):
    client = get_gspread_client()
    sheet = client.open("観光地管理シート").sheet1
    data = sheet.get_all_records()
    
    for row in data:
        # st.expanderで観光地ごとにグループ化
        with st.expander(f"📍 {row['観光地名']}  |  投稿者: {row['ユーザー名']}", expanded=False):
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            # 全体情報
            st.image(convert_drive_url(row['全体画像URL']), use_container_width=True)
            st.markdown("### 🌍 観光地全体の説明")
            st.markdown(f"<div class='desc-box'>{row['全体説明']}</div>", unsafe_allow_html=True)
            
            # 人気スポット 3選
            st.markdown("### 🌟 人気スポット TOP3")
            cols = st.columns(3)
            for i, col in enumerate(cols, 1):
                with col:
                    
                    st.image(convert_drive_url(row[f'スポット{i}画像URL']), use_container_width=True)
                    st.markdown(f"<p class='spot-text'>SPOT {i}</p>", unsafe_allow_html=True)
                    st.write(row[f'スポット{i}説明'])
                    st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
