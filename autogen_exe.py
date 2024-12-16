import tempfile
import os

from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor

from gemma_ini import usr_inp
from gemma_programmer import program_response
#from gemma_inspector import program_inspector
from gemma_insights import insights_response
from data_opener import data_handler


import nbformat
from nbformat.v4 import new_notebook, new_code_cell
from nbformat import write
from jupyter_client import KernelManager
import asyncio

''' 
current workflow 
flowchart LR
    A[User Input (Path)] --> B{Data Handler}
    B --> C[User Input (Requirement)]
    C --> D{Program Response}
    D --> E{Code Execution}
    E --> F{Code Executor Agent}
    F --> G{Insights Generation}
    G --> H[Output]
'''


data_path = input(r'Input your path:').strip('"')
data_path = rf"{data_path}" 
absolute_path = os.path.abspath(data_path)
print(absolute_path)
handler = data_handler()
data = data_handler.handle_external_dataset(absolute_path)
metadata = data['metadata']

#eddited 1.39 am 15-12. Here we have a metadata extraction part for the dataset. We further need to attach the metadata, as well as the dataset in itself with the program executor/ programmer

user_input = input("Please type your requirements: ")

# Use the program_response module to generate the response
program_response_obj = program_response()
response_text = program_response_obj.respond(user_input, data_path)


'''inspector = CodeInspector(verbose=True)
result = inspector.comprehensive_inspection(response_text)
print(result)'''


print("Generated Code:\n", response_text)

# Create a temporary directory to store the code files.
temp_dir = tempfile.TemporaryDirectory()


# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=100,  # Timeout for each code execution in seconds.
    work_dir=temp_dir.name,  # Use the temporary directory to store the code files.
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    llm_config=False,  # Turn off LLM for this agent.
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="NEVER",  # Always take human input for this agent for safety.
)

reply = code_executor_agent.generate_reply(messages=[{"role": "user", "content": response_text}])

#inspection model
'''program_inspetor_obj = program_inspector()
inspector_suggets = program_inspetor_obj.respond(reply + response_text)'''

#visualization model
'''code_response_obj = code_response()
visual_insight = code_response_obj.code_respond(reply)'''

insights_response_obj = insights_response()
insight_text = insights_response_obj.respond(user_input, str(reply), str(metadata))

print("the path for the file is : " ,os.listdir(temp_dir.name))
print(reply, insight_text)