import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()
GOOGLE_API_KEY = os.getenv("api_key")

genai.configure(api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
class program_inspector:
    def respond(self, usr_inp):
        base_prompt = "you are a code inspector. based on the input if there is an error you will write the corrections for the error. note that you will write only the corrections, that is the corrected code snippet, if there is no error, you will pass without any generations."
        response = model.generate_content(base_prompt)
        response_txt = response.text
        return response_txt