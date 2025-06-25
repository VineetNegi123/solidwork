import streamlit as st
import numpy as np
import cv2
from PIL import Image
import ezdxf
import io

st.set_page_config(page_title="Sketch to SolidWorks DXF", layout="centered")
st.title("🛠️ Image to SolidWorks DXF Converter")
st.write("Upload a sketch image, and we'll generate a DXF file you can import into SolidWorks.")

uploaded_file = st.file_uploader("Upload a Sketch Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("L")  # Convert to grayscale
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to numpy array and detect edges
    img_array = np.array(image)
    edges = cv2.Canny(img_array, 100, 200)

    st.subheader("Edge Detection Preview")
    st.image(edges, clamp=True, channels="GRAY")

    # Generate DXF with small circles at edge points
    st.subheader("Generating DXF file...")
    doc = ezdxf.new()
    msp = doc.modelspace()

    points = np.argwhere(edges > 0)
    for y, x in points[::10]:  # Sample every 10th point to reduce DXF size
        msp.add_circle((x, -y), radius=0.5)

    dxf_stream = io.BytesIO()
    doc.write(dxf_stream)
    dxf_stream.seek(0)

    st.download_button(
        label="📥 Download DXF File",
        data=dxf_stream,
        file_name="sketch_output.dxf",
        mime="application/dxf"
    )

    st.markdown("""
    ✅ **Next Step:** Open the DXF in SolidWorks → Extrude to create `.SLDPRT`

    ⚠️ Note: This is a simplified DXF with point circles. For cleaner CAD, consider uploading cleaner sketches or use AI recognition tools for detailed parts.
    """)
