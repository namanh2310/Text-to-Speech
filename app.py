import streamlit as st
import requests
import re
import json
from PIL import Image

st.title("Chuyển đổi văn bản thành giọng nói!")

# sidebar
with st.sidebar:
        
        st.title("Tùy chỉnh")
        api_token = st.sidebar.text_input("Nhập API Token (Enter 2 lần  )", placeholder="Chỉ nhập khi hết API Token")
        text_color = st.color_picker("Chọn màu văn bản", "#000000")
        font_size = st.slider("Chọn cỡ chữ", min_value=12, max_value=36, value=16)
        selected_type = st.sidebar.radio("Chọn định dạng âm thanh", ["mp3", "wma", "wav", "aac", "flac"])
        image = Image.open('Logo.png')
        new_image = image.resize((400, 300))
        st.image(new_image)
# custom styles
custom_styles = f"""
        <style>
        .css-hxt7ib {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}
        .css-15tx938, p, input, textarea {{
            font-size: {font_size}px;
        }} 

        .css-15tx938, p, input, textarea, span {{
            color: {text_color};
        }} 
        img {{
            border: 1px solid transparent;
            border-radius: 8px;
            transition: all ease 0.5s;
        }}
        img:hover {{
            border: 1px solid green;
        }}
        </style>
    """
def selected_voice(voice):
    if voice ==  "Nữ miền Bắc - Quỳnh Anh":
        return 'hn-quynhanh'
    elif voice == "Nữ miền Nam - Diễm My":
        return 'hcm-diemmy'
    elif voice == "Nữ miền Trung - Mai Ngọc":
        return 'hue-maingoc'
    elif voice == "Nữ miền Bắc - Phương Trang":
        return 'hn-phuongtrang'
    elif voice == "Nữ miền Bắc - Thảo Chi":
        return 'hn-thaochi'
    elif voice == "Nữ miền Bắc - Thanh Hà":
        return 'hn-thanhha'
    elif voice == "Nữ miền Nam - Phương Ly":
        return 'hcm-phuongly'
    elif voice == "Nữ miền Nam - Thùy Dung":
        return 'hcm-thuydung'
    elif voice == "Nam miền Bắc - Thanh Tùng":
        return 'hn-thanhtung'
    elif voice == "Nam miền Trung - Bảo Quốc":
        return 'hue-baoquoc'
    elif voice == "Nam miền Nam - Minh Quân":
        return 'hcm-minhquan'
    elif voice == "Nữ miền Bắc - Thanh Phương":
        return 'hn-thanhphuong'
    elif voice == "Nam miền Bắc - Nam Khánh":
        return 'hn-namkhanh'
    elif voice == "Nữ miền Nam - Lê Yến":
        return 'hn-leyen'
    elif voice == "Nam miền Bắc - Tiến Quân":
        return 'hn-tienquan'
    elif voice == "Nữ miền Nam - Thùy Dương":
        return 'hcm-thuyduyen'
    else:
        return None

def endecode(dict):
    decoded_text = dict.decode('utf-8')
    parsed_data = json.loads(decoded_text)
    return parsed_data

st.markdown(custom_styles, unsafe_allow_html=True)

title = st.text_input('Nhập tiêu đề đầu ra: ') # audio file title
text = st.text_area('Nhập văn bản cần chuyển đổi: ', height=150) # text2speech

voice_options = ["- - - ", 
                "Nữ miền Bắc - Quỳnh Anh", 
                "Nữ miền Nam - Diễm My", 
                "Nữ miền Trung - Mai Ngọc",
                "Nữ miền Bắc - Phương Trang",
                "Nữ miền Bắc - Thảo Chi",
                "Nữ miền Bắc - Thanh Hà",
                "Nữ miền Nam - Phương Ly",
                "Nữ miền Nam - Thùy Dung",
                "Nam miền Bắc - Thanh Tùng",
                "Nam miền Trung - Bảo Quốc",
                "Nam miền Nam - Minh Quân",
                "Nữ miền Bắc - Thanh Phương",
                "Nam miền Bắc - Nam Khánh",
                "Nữ miền Nam - Lê Yến",
                "Nam miền Bắc - Tiến Quân",
                "Nữ miền Nam - Thùy Dương"]
                
selected_voice_raw = st.selectbox("Chọn giọng nói:", voice_options) # voice_options
speed = st.slider("Chọn tốc độ đọc:", min_value=0.7, max_value=1.3, value=1.0, step=0.1) # audio speed

url = "https://viettelai.vn/tts/speech_synthesis"

# current api_token
if not api_token:
        api_token = 'eb30fe739c5795a4440ae34531ba2ac0'

payload = json.dumps({
"text": text,
"voice": selected_voice(selected_voice_raw),
"speed": speed,
"tts_return_option": 3,
"token": api_token,
"without_filter": False
})

headers = {
'accept': '*/*',
'Content-Type': 'application/json'
}

if st.button("TẠO ÂM THANH"):
        if text and selected_voice:
                response = requests.request("POST", url, headers=headers, data=payload)

                with open(f"{title}.{selected_type}", "wb") as audio_file:
                    audio_file.write(response.content)
                
                st.audio(response.content, format=f"audio/{selected_type}")
                st.download_button(
                label="Download Audio",
                data=response.content,
                file_name=f"{title}.{selected_type}",
                mime=f"audio/{selected_type}")
        else:
            st.warning("Vui lòng nhập đầy đủ thông tin!")
