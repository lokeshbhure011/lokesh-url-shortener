import os
def cleanup_qr_codes():
    folder = "static"
    for file in os.listdir(folder):
        if file.endswith(".png"):
            os.remove(os.path.join(folder, file))