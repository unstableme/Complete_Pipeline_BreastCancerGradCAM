import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image
import base64
import cv2

from tensorflow.keras.models import load_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = r"Model/IDC_CNN_GRAD_CAM.h5"
model = load_model(MODEL_PATH, compile=False, safe_mode=False)

LAST_CONV_LAYER = "separable_conv2d_1" 


#GENERATE GRADCAM
def generate_gradcam_cv2(img_array, model, last_conv_layer_name):

    grad_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=[
            model.get_layer(last_conv_layer_name).output,
            model.output
        ]
    )

    # cast & expand dims
    img_tensor = tf.cast(tf.expand_dims(img_array, axis=0), tf.float32)

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_tensor)
        loss = predictions[0]  # binary classification

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))    
    conv_outputs = conv_outputs[0]      # remove batch

    heatmap = tf.tensordot(conv_outputs, pooled_grads, axes=[2, 0])
    heatmap = tf.nn.relu(heatmap)

    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)
    heatmap = heatmap.numpy()

    return heatmap


#CREATE COLORED OVERLAY
def create_overlay_with_cv2(original_img_pil, heatmap):
    original = np.array(original_img_pil)
    original_rgb = original.astype("uint8")

    heatmap_resized = cv2.resize(heatmap, (original_rgb.shape[1], original_rgb.shape[0]))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)

    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    blended = cv2.addWeighted(original_rgb, 0.6, heatmap_color, 0.4, 0)

    return Image.fromarray(blended)


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        img_bytes = await file.read()
        original_img = Image.open(BytesIO(img_bytes)).convert("RGB")

        resized = original_img.resize((128, 128))
        img_array = np.array(resized).astype("float32") / 255.0

        preds = model.predict(np.expand_dims(img_array, axis=0))
        malignant_prob = float(preds[0][0])
        benign_prob = 1 - malignant_prob
        result = "Malignant" if malignant_prob > 0.5 else "Benign"

        # ---- GRADCAM ----
        heatmap = generate_gradcam_cv2(img_array, model, LAST_CONV_LAYER)
        overlay_img = create_overlay_with_cv2(resized, heatmap)
        overlay_img = overlay_img.resize(original_img.size, Image.BILINEAR)

        # Convert GradCAM to base64
        buf = BytesIO()
        overlay_img.save(buf, format="PNG")
        gradcam_b64 = base64.b64encode(buf.getvalue()).decode()

        return {
            "Prediction": result,
            "Malignant Probability": round(malignant_prob, 3),
            "Benign Probability": round(benign_prob, 3),
            "GradCAM": gradcam_b64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "IDC Detection API Running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
