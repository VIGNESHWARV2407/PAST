from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
import openpyxl

def llm_model(input_data):
    # Define the LLM and template
    llm = OllamaLLM(model="llama3.1:latest")

    template = """You are a priority analyzer for support tickets at an Information Technology company. Your task is to examine each ticket description to determine its priority level based on urgency and impact. 
    Your role is to prioritize the tickets based on the tickets, and don't analyse the greetings or anything other than ticket that related to technical and service issues.


    if the ticket is without technical or service issues which is related to computer issue only no other issue should not be taken, just  say "Ticket invalid (must be related to technical/service issues)" and don't do anything else.

    The priority levels are classified as:


    High: Critical issues requiring immediate attention.
    Mid: Important but not urgent.
    Low: Low impact or minor concerns.

    just return the priority label as High / Low / Mid only. no need of reason for categorize
    Ticket Description: {ticket_description}
    """

    # Create the PromptTemplate with the variable `ticket_description`
    prompt = PromptTemplate.from_template(template)

    # Define a chain that takes a dictionary input
    chain = prompt | llm

    # Chatbot loop to ask for input
    res = chain.invoke(input_data)
        
    return res