from langchain_ollama.llms import OllamaLLM

llm=OllamaLLM(model="llama3.1:latest")
user=input("Enter your query : ")
res=llm.invoke(user)
print(res)