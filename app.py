from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load all environment variables from .env
load_dotenv()

# Configure the API key for the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision model and get response
def get_gemini_response(input_text, image, prompt):
    # Loading the Gemini Pro Vision model
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to process the uploaded image file
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Create the image_part dictionary
        image_part = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_part
    else:
        # Raise an error if no file is uploaded
        raise FileNotFoundError("No file uploaded")

# Streamlit page configuration
st.set_page_config(page_title="Minor Project (Invoice Extractor)")

st.header("Gemini Application")

# Input for user prompt
input_text = st.text_input("Input Prompt: ", key="input")

# File uploader for images
uploaded_file = st.file_uploader("Choose an image..", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Submit button
submit = st.button("Tell me about the invoice")

# Input prompt for the Gemini AI model
input_prompt = """
You are an expert in understanding invoices. You will 
receive input images as invoices, and you will have to 
answer questions based on the input images.
"""

# If submit button is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)

        st.subheader("The Response is:")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
