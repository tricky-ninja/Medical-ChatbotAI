from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.vectorstores import Chroma

main_prompt = """
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Only return the helpful detailed answer below and nothing else. If the user asks for medication, only recomend them
medicine if you know it, and always provide a discliamer that the user should see a doctor before taking any medicine

Context: {context}
{question}

Helpful answer:
"""

class LLM:
    def __init__(self, save_directory, system_prompt, debug=False) -> None:
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectordb = Chroma(persist_directory=save_directory,embedding_function=self.embeddings)
        self.prompt = system_prompt
        self.prev_context = ""
        self.debug = debug

    def respond(self, question):
        question =  "Question: " + question
        PROMPT=PromptTemplate(template=self.prompt, input_variables=["context", "question"])
        chain_type_kwargs={"prompt": PROMPT}
        llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})
        
        qa=RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=self.vectordb.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True, 
        chain_type_kwargs=chain_type_kwargs)
        result=qa({"query": question})
        # self.prev_context += question + "\nHelpful answer: " + result["result"] + "\n"
        if self.debug:
            print("Memory: " + self.prev_context) 
        return result
    

def main():
    model = LLM("db", main_prompt, debug=False)
    while True:
        question = input("Question: ")
        print(model.respond(question)["result"])

if __name__ == "__main__":
    main()