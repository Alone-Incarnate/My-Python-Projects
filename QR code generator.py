import qrcode
from PIL import Image

# The URL you want to encode in the QR code
url = "https://www.facebook.com/profile.php?id=100027034642492"

# Create the QR code without the logo
qr = qrcode.QRCode(
    version=1,  # QR code version (adjust as needed)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
)
qr.add_data(url)
qr.make(fit=True)

# Create the QR code image
qr_img = qr.make_image(fill_color="black", back_color="white")

# Open and resize the logo image
logo_path = "facebook1.png"
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((50, 50))  # Adjust the size as needed

# Calculate the position to center the logo in the QR code
position = ((qr_img.size[0] - logo_img.size[0]) // 2, (qr_img.size[1] - logo_img.size[1]) // 2)

# Paste the logo on the QR code
qr_img.paste(logo_img, position)

# Save the image with the logo
qr_img.save("facebook qr.png")
