# #ChatGPT
import os
import cv2
import pytesseract
from PIL import Image
from fpdf import FPDF

# # Set the path to Tesseract OCR executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Change this path accordingly

# # Define paths
# base_path = os.path.dirname(os.path.abspath(__file__))
# blueprint_folder = os.path.join(base_path, 'static', 'blueprints')
# images_folder = os.path.join(base_path, 'static', 'screenshots_unprocessed')

# # Create the 'images' folder if it doesn't exist
# if not os.path.exists(images_folder):
#     os.makedirs(images_folder)

# def process_image(image_path, target_text='566'):
#     try:
#         # Read the image using OpenCV
#         image = cv2.imread(image_path)
        
#         # Convert the image to grayscale
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         # Use pytesseract to extract text from the image
#         extracted_text = pytesseract.image_to_string(gray_image)
        
#         # Check if the target text is present in the extracted text
#         if target_text in extracted_text:
#             # Get the dimensions of the original image
#             height, width, _ = image.shape
            
#             # Draw a rectangle around the detected text
#             h, w = gray_image.shape
#             boxes = pytesseract.image_to_boxes(gray_image)
#             for b in boxes.splitlines():
#                 b = b.split()
#                 x, y, x2, y2 = int(b[1]), h - int(b[2]), int(b[3]), h - int(b[4])
#                 cv2.rectangle(image, (x, y), (x2, y2), (0, 255, 0), 2)
            
#             # Save the modified image with the highlighted target text
#             cv2.imwrite(os.path.join(images_folder, f'highlighted_{os.path.basename(image_path)}'), image)
            
#             # Display a success message
#             print(f"Target text '{target_text}' found in {os.path.basename(image_path)}. Highlighted image saved.")
#         else:
#             # Display a message if the target text is not found
#             print(f"Target text '{target_text}' not found in {os.path.basename(image_path)}.")

#     except Exception as e:
#         # Handle any exceptions that may occur
#         print(f"Error processing image {os.path.basename(image_path)}: {e}")

# # Loop through all PNG images in the 'blueprints' folder
# for file_name in os.listdir(blueprint_folder):
#     if file_name.endswith('.png'):
#         # Create the full path to the image file
#         image_path = os.path.join(blueprint_folder, file_name)
        
#         # Process the image
#         process_image(image_path)


# Path to the input and output files
input_image_path = 'cropped_test.png'
output_pdf_path = 'test.pdf'

# Read the input image using OpenCV
image = cv2.imread(input_image_path)

# Perform preprocessing on the image (e.g., resizing, noise reduction, etc.)
# Replace the following lines with your desired preprocessing steps
# For example, you can convert the image to grayscale and perform thresholding
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, processed_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Use Tesseract OCR to extract text from the processed image
extracted_text = pytesseract.image_to_string(Image.fromarray(processed_image), lang='eng', config='--psm 12')

# Save the extracted text to a PDF file
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=extracted_text, ln=True)
pdf.output(output_pdf_path)

print("Text extracted and saved to", output_pdf_path)