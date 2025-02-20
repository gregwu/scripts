# Remember to install Pillow and ghostscript first
# In Mac, to install GhostScript, run: brew install ghostscript
# In Mac, to install Pillow

# TODO
# - Cannot handle directory name with space
# - If directory did not contains any *.pdg file, it will throw error (e.g. a directory within a directory)

# Directory Structure
# ./books
# ├── book1
# │   ├── *.pdg
# │   ├── *.pdg
# │   └── *.pdg
# ├── book2
# │   ├── *.pdg
# │   ├── *.pdg
# │   └── *.pdg
# /img_to_pdf.py

from PIL import Image, ImageFile
import os

# https://stackoverflow.com/a/23575424/1802483
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Get the list of directory in ./books
files = os.listdir("./books")

# Each directory is a book directory containing a list of *.pdg file
# Rename all *.pdg file to *.jpg file
for file in files:

    # Bypass file if it is not a directory
    if not os.path.isdir(f"./books/{file}"):
        continue

    for f in os.listdir(f"./books/{file}"):
        if f.endswith(".pdg"):
            os.rename(f"./books/{file}/{f}", f"./books/{file}/{f[:-4]}.jpg")

    # Read the directory name as book name and
    # read all *.jpg files in `data` dir as string, order by file name
    dir = f"./books/{file}"

    files = sorted([f for f in os.listdir(dir) if f.endswith(".jpg")], key=lambda x: x)

    # The logic here is:
    # 1. Read first image
    # 2. Save it as PDF
    # 3. Read remaining images and append it to this PDF file
    # 4. Compress the PDF file using ps2pdf command
    # 5. Rename the compressed PDF file to original file name

    img = Image.open(os.path.join(dir, files[0]))
    img.save(f"{file}.pdf", "PDF",
             resolution=80.0,
             save_all=True,
             append_images=[Image.open(os.path.join(dir, f)) for f in files[1:]])

    # Use ps2pdf command to compress the PDF file and append _compressed.pdf to the file name
    os.system(f"ps2pdf {file}.pdf {file}_compressed.pdf")

    # Remove the large file
    os.remove(f"{file}.pdf")

    # Removing _compressed in filename
    os.rename(f"{file}_compressed.pdf", f"{file}.pdf")
