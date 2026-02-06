import streamlit as st
import numpy as np
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Linear Algebra Image Compressor", layout="wide")

st.title(" Matrix Decomposition: Image Compression")
st.markdown("""
This tool uses **Singular Value Decomposition (SVD)** to reduce an image matrix to its most important components. 
It’s the bridge between pure Linear Algebra and real-world data storage.
""")

# 2. Sidebar 
st.sidebar.header(" Settings")
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load and Prepare Data
    original_img = Image.open(uploaded_file).convert('L')
    A = np.array(original_img)
    
    # Mathematical Engine (SVD)
    U, s, Vh = np.linalg.svd(A, full_matrices=False)
    max_k = len(s)

    # Dynamic Slider for K
    k = st.sidebar.select_slider(
        "Select Number of Singular Values (k)",
        options=list(range(1, max_k + 1)),
        value=min(50, max_k),
        help="Higher k = better quality but less compression."
    )

    # 3. Calculations
    # Reconstruct the matrix using the top k components
    A_compressed = np.dot(U[:, :k], np.dot(np.diag(s[:k]), Vh[:k, :]))
    A_compressed = np.clip(A_compressed, 0, 255).astype(np.uint8)

    # Information Metric (The 'Energy' of the image)
    variance_explained = np.sum(s[:k]**2) / np.sum(s**2) * 100

    # 4. Display Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Matrix")
        st.image(A, caption=f"Full Rank: {max_k}", use_container_width=True)
        st.write(f"Size: {A.shape[0]} x {A.shape[1]} pixels")

    with col2:
        st.subheader(f"Compressed Matrix (k={k})")
        st.image(A_compressed, caption=f"Approximated Rank: {k}", use_container_width=True)
        st.metric("Information Retained", f"{variance_explained:.2f}%")

    # 5. Download Functionality
    result_img = Image.fromarray(A_compressed)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.sidebar.download_button(
        label="Download Compressed Image",
        data=byte_im,
        file_name=f"compressed_k{k}.png",
        mime="image/png"
    )

    st.info(f"Theory in Action: You are representing this {A.size} pixel image using only {((U.shape[0]*k) + k + (k*Vh.shape[1]))} data points.")

else:
    st.warning(" Please upload an image in the sidebar to begin the transformation.")
