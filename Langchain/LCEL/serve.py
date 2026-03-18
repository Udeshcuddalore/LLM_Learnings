from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

#0. Import the model 
model = ChatGroq(model = "llama-3.3-70b-versatile",groq_api_key = groq_api_key)

#1. create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template),("user","{text}")]
)

#2. parser
parser = StrOutputParser()

#3. create chain
chain = prompt_template|model|parser

#4. App definition
app = FastAPI(title = "Langchain server", version = "1.0",description = "A simple API Server using Langchain runnable interfaces")

#5. Add the routes to FastAPI

add_routes(
    app, chain,
    path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host = "localhost", port = 8000)