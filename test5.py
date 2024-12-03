from PIL import Image

# Create a new blank image (RGB mode, 100x100 pixels, white color)
image = Image.new('RGB', (100, 100), color='white')

# Save the image
image.save('test_image.png')

# Open and show the image
image = Image.open('test_image.png')
image.show()

# Print out the image format and size
print(f"Image format: {image.format}")
print(f"Image size: {image.size}")
