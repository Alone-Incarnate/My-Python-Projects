import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(url, logo_path=None, fill_color="black", back_color="white", 
                    qr_version=1, error_correction="L", logo_size=50, border=4):
    """
    Generate QR code with optional logo
    """
    # Map error correction levels
    error_correction_mapping = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H
    }
    
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=error_correction_mapping[error_correction],
        box_size=10,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
    
    if logo_path:
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((logo_size, logo_size))
        
        # Calculate position to center the logo
        pos = (
            (qr_img.size[0] - logo_img.size[0]) // 2,
            (qr_img.size[1] - logo_img.size[1]) // 2
        )
        
        # Paste logo while maintaining transparency
        if logo_img.mode == 'RGBA':
            mask = logo_img.split()[3]
            qr_img.paste(logo_img, pos, mask)
        else:
            qr_img.paste(logo_img, pos)
    
    return qr_img

def main():
    st.set_page_config(
        page_title="QR Code Generator",
        page_icon="🔗",
        layout="centered",
    )
    
    # Custom CSS styling
    st.markdown("""
    <style>
        .header {
            font-size: 36px !important;
            color: #1f77b4;
            text-align: center;
        }
        .stDownloadButton button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)
    
 
    
    # Main content
    st.markdown('<p class="header">Custom QR Code Generator</p>', unsafe_allow_html=True)
    
    with st.form("qr_form"):
        url = st.text_input("Enter URL:", placeholder="https://example.com")
        
        col1, col2 = st.columns(2)
        with col1:
            fill_color = st.color_picker("Foreground Color", "#000000")
        with col2:
            back_color = st.color_picker("Background Color", "#FFFFFF")
        
        col3, col4 = st.columns(2)
        with col3:
            qr_version = st.number_input("QR Version (1-40)", 1, 40, 1)
        with col4:
            error_correction = st.selectbox("Error Correction", ["L", "M", "Q", "H"], index=0)
        
        logo_file = st.file_uploader("Upload Logo (optional)", type=["png", "jpg", "jpeg"])
        logo_size = st.slider("Logo Size", 30, 150, 50)
        border = st.slider("Border Size", 1, 10, 4)
        
        submitted = st.form_submit_button("Generate QR Code")
    
    if submitted and url:
        try:
            qr_img = generate_qr_code(
                url=url,
                logo_path=logo_file,
                fill_color=fill_color,
                back_color=back_color,
                qr_version=qr_version,
                error_correction=error_correction,
                logo_size=logo_size,
                border=border
            )
            
            # Display QR code
            st.image(qr_img, caption="Generated QR Code", use_column_width=True)
            
            # Download button
            img_bytes = io.BytesIO()
            qr_img.save(img_bytes, format="PNG")
            st.download_button(
                label="Download QR Code",
                data=img_bytes.getvalue(),
                file_name="custom_qr.png",
                mime="image/png",
            )
            
        except Exception as e:
            st.error(f"Error generating QR code: {str(e)}")
    elif submitted and not url:
        st.warning("Please enter a URL before generating the QR code")

if __name__ == "__main__":
    main()
