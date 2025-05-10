# from langchain.prompts import ChatPromptTemplate
# # from src.model.llm_model import pipe_runnable
# from langchain_core.output_parsers import StrOutputParser
# import os

# from transformers import pipeline
# from langchain_huggingface import HuggingFacePipeline

# huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
# huggingface_model_name = "meta-llama/Llama-3.2-1B-Instruct"
# pipe = pipeline("text-generation", model=huggingface_model_name)
# pipe_runnable = HuggingFacePipeline(pipeline=pipe)
# # Decomposition
# template = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
# The goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \n
# Generate multiple search queries related to: {question} \n
# Output (3 queries):"""
# prompt_decomposition = ChatPromptTemplate.from_template(template)

# # LLM
# llm = pipe_runnable

# # Chain
# generate_queries_decomposition = ( prompt_decomposition | llm | StrOutputParser() | (lambda x: x.split("\n")))

# # Run
# question = "What are the main components of an LLM-powered autonomous agent system?"
# questions = generate_queries_decomposition.invoke({"question":question})
# print(questions)