import google.generativeai as genai
from dotenv import load_dotenv
import os 

load_dotenv()
GOOGLE_API_KEY = os.getenv("api_key")

genai.configure(api_key = GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
class program_response:
    def respond(self, usr_inp, filepath):
        base_prompt = "You are a program expert who is excellent in data anlysis, EDA and visualizations. Strictly Generate Python code and nothig else. If you were to ouput anything else that is not a python code, start each sentence with '#'. Generate a python code to " + usr_inp + "here is the file path of the dataset. take this path and then generate the code over this " + filepath
        response = model.generate_content(base_prompt)
        response_txt = response.text
        return response_txt