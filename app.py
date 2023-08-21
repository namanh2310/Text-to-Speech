import streamlit as st
import requests
import re
import json

st.title("Chuyển đổi văn bản thành giọng nói!")

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
        st.title("Customization")
        theme_color = st.color_picker("Choose a theme color", "#ffffff")
        font_size = st.slider("Choose font size", min_value=12, max_value=36, value=16)

input_rgb = f"rgb{tuple(int(theme_color[i:i+2], 16) for i in (1, 3, 5))}"
rgb_values = re.findall(r'\d+', input_rgb)

r, g, b = map(int, rgb_values)
print(r)
text_color = '#000000'
if int(r) < 150:
    text_color = '#ffffff'

opposite_r = 495 - r
opposite_g = 497 - g
opposite_b = 501 - b

opposite_rgb = f'rgb({opposite_r}, {opposite_g}, {opposite_b})'

    # Apply custom styles
custom_styles = f"""
        <style>
            .css-k1vhr4 {{
                background-color: {theme_color};
            }}
            .css-10trblm {{
                color: {text_color}
            }}
            .stTextArea > .css-15tx938, 
            .stSelectbox > .css-15tx938, 
            .stSlider > .css-15tx938,
            .css-15uh7qh > .element-container {{
                font-size: {font_size}px;
                color: {text_color};
            }}
            .st-cu {{
                font-size: {font_size}px;
                background-color: {opposite_rgb};
                color: {text_color};
            }}
        </style>
    """
st.markdown(custom_styles, unsafe_allow_html=True)

title = st.text_input('Nhập tiêu đề đầu ra: ')
text = st.text_area('Nhập văn bản cần chuyển đổi: ', height=150)

voice_options = ["Chọn giọng nói", 
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
                
selected_voice_raw = st.selectbox("Chọn giọng nói:", voice_options)

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
    


speed = st.slider("Chọn tốc độ đọc:", min_value=0.7, max_value=1.3, value=1.0, step=0.1)

url = "https://viettelai.vn/tts/speech_synthesis"

payload = json.dumps({
"text": text,
"voice": selected_voice(selected_voice_raw),
"speed": speed,
"tts_return_option": 3,
"token": "eb30fe739c5795a4440ae34531ba2ac0",
"without_filter": False
})

headers = {
'accept': '*/*',
'Content-Type': 'application/json'
}

if st.button("Gửi đi"):
        if text and selected_voice:
            response = requests.request("POST", url, headers=headers, data=payload)

            with open(f"{title}.wav", "wb") as audio_file:
                audio_file.write(response.content)
            
            st.audio(response.content, format="audio/wav")
            st.download_button(
            label="Download Audio",
            data=response.content,
            file_name=f"{title}.wav",
            mime="audio/wav"
        )
        else:
            st.warning("Please enter data before submitting")
