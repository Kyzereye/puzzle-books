import os
from dotenv import load_dotenv
load_dotenv()
from google.generativeai import configure, GenerativeModel
import google.api_core.exceptions

api_key = os.environ["GEMINI_API_KEY"]
configure(api_key=api_key)

try:
    # Try with the original name
    model = GenerativeModel("gemini-1.5-pro")
    chat = model.start_chat()
    response = chat.send_message("what is the most basic definitions of skees.")
    print(response.text)
except google.api_core.exceptions.NotFound as e:
    print(f"Error: {e}")
    print("Trying with a potential alternative model name...")
    try:
        # Try with a potential alternative model name (check documentation!)
        model = GenerativeModel("gemini-1.0-pro") # Example, check documentation
        chat = model.start_chat()
        response = chat.send_message("what is the basic definition of run.")
        print(response.text)
    except google.api_core.exceptions.NotFound as e2:
        print(f"Still encountering error: {e2}")
        print("Please verify the model name in the Google Gemini API documentation.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")