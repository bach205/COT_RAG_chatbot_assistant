from huggingface_hub import InferenceClient
from langchain_core.prompts.base import BasePromptTemplate
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline
import os

huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
huggingface_model_name = "meta-llama/Llama-3.2-1B-Instruct"
pipe = pipeline("text-generation", model=huggingface_model_name)
pipe_runnable = HuggingFacePipeline(pipeline=pipe)
client = InferenceClient(
    provider="sambanova",
    api_key=huggingface_api_key,
)
def llm (messages :BasePromptTemplate,type:str = "inference"):
    try:
        if(type == ""):
            pass
        elif(type == "local"):
            return pipe_runnable.invoke(messages)
        else:
            if(not messages):
                print("type something.....")
                return "type something ...."
            formatted_messages = [{"role":m.type ,"content": m.content} for m in messages]
            return client.chat.completions.create(
            model=huggingface_model_name,
            messages=[formatted_messages]
        ) 
    except Exception as e:
        print(e)
        return e
