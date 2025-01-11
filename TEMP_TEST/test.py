import os

# Example path
temporary_image_path = "your\\imagefile.jpg"

# Get the file name without the extension
file_name = os.path.splitext(os.path.basename(temporary_image_path))[0]

print(file_name)
