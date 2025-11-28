import streamlit as st
import requests
from PIL import Image
import os
from io import BytesIO
import base64

st.title("🩺 Breast Cancer Prediction with Grad-CAM")

st.markdown("""
Upload an image or choose a sample. (You can search for 'breast cancer histopathology images' on the internet for the images.) 
The backend will classify the tissue and generate a Grad-CAM heatmap.
""")

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000") + "/predict/"   #uses latter url if not former

# Check backend connection
try:
    requests.get(API_URL) 
    st.sidebar.success("Backend Connected")
except:
    st.sidebar.error("Backend Not Reachable")


uploaded_file = st.file_uploader("Upload Histopathology Image", type=["jpg", "jpeg", "png"])

st.markdown("### Or Try Sample Images:")

sample_dir = os.path.join(os.path.dirname(__file__), "samples")
sample_images = [
    img for img in os.listdir(sample_dir)
    if img.lower().endswith((".jpg", ".jpeg", ".png"))
]

cols = st.columns(4)
selected_sample = None

for i, img_name in enumerate(sample_images):
    with cols[i % 4]:
        img_path = os.path.join(sample_dir, img_name)
        img = Image.open(img_path)
        st.image(img, caption=img_name, width='stretch')

        if st.button(f"Use {img_name}", key=img_name):
            selected_sample = img_path



img_bytes = None
img_display = None

if uploaded_file is not None:
    img_bytes = uploaded_file.read()
    img_display = Image.open(BytesIO(img_bytes))
    st.success("Using uploaded image")

elif selected_sample is not None:
    with open(selected_sample, "rb") as f:
        img_bytes = f.read()
    img_display = Image.open(BytesIO(img_bytes))
    st.success(f"Using sample image: {os.path.basename(selected_sample)}")


# SEND IMAGE TO BACKEND
if img_bytes is not None:
    with st.spinner("Processing image... Please wait"):
        response = requests.post(API_URL, files={"file": img_bytes})

    if response.status_code == 200:
        result = response.json()

        st.subheader("Prediction Result")
        st.write(f"**Prediction:** {result['Prediction']}")
        st.write(f"**Malignant Probability:** {result['Malignant Probability']}")
        st.write(f"**Benign Probability:** {result['Benign Probability']}")

        # Decode Grad-CAM
        gradcam_image = Image.open(BytesIO(base64.b64decode(result["GradCAM"])))

        col1, col2 = st.columns(2)
        with col1:
            st.image(img_display, caption="Original Image", width='stretch')
        with col2:
            st.image(gradcam_image, caption="Grad-CAM Visualization", width='stretch')

    else:
        st.error("Backend returned an error. Check FastAPI logs.")

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align:center;'>
            Visit My:
<a href='https://unstableme.github.io' target='_blank'>Website</a> |
<a href='https://linkedin.com/in/unstableme/' target='_blank'>LinkedIn</a> |
<a href='https://github.com/unstableme/' target='_blank'>GitHub</a>
</div>
""", unsafe_allow_html=True)
