import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("api_key")

genai.configure(api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
class insights_response:
    def respond(self, usr_inp, reply, metadata):
        base_prompt = "You are a insights generation model. Based on the data given and the user input you have to generate insights. Generate the insights over " + usr_inp + "the insight generatoin will be guided by  " + reply + "Unless there is any execution error, do not respond with the error. Also ignore the future warnings error. and the metadata for the data is " + metadata
        response = model.generate_content(base_prompt)
        response_txt = response.text
        return response_txt