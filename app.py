from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from pinecone import Pinecone
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
INDEX_NAME = os.environ.get('INDEX_NAME')

print(f"PINECONE_API_KEY {PINECONE_API_KEY}")
print(f"INDEX_NAME {INDEX_NAME}")


embeddings = download_hugging_face_embeddings()

# #Initializing the Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)  
# index = pc.Index(INDEX_NAME)

#Loading the llm
llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})


def retriver_results(query, top_res):
    #Initializing the Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)  
    index = pc.Index(INDEX_NAME)
    # create the query vector
    xq = embeddings.embed_query(query)
    print(f"embeddings length: {len(xq)}")
    # now query
    xc = index.query(vector=xq, top_k=top_res, include_metadata=True, namespace="real", include_values=True)

    contexts = []
    contexts = contexts + [
            x['metadata']['text'] for x in xc['matches']
        ]
    
    querydocs = []
    from langchain.docstore.document import Document

    for eachcont in contexts:
        doc =  Document(page_content=eachcont, metadata={"source": "local"})
        querydocs.append(doc)

    return querydocs, "".join(contexts)

def retrieve_answers(query):
    querydocs,context = retriver_results(query,2)
    input_prompts = PROMPT.format(context=context,question=query)
    # response=chain.run(input_documents=querydocs,question=input_prompts)
    response=llm(input_prompts)
    return response



@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(f"Input {input}")
    result = retrieve_answers(input)
    print("Response : ", result)
    return result

@app.route("/question/<inpquery>", methods=["GET"])
def question(inpquery):
    print(f"inpquery for {inpquery}")
    from pinecone import Pinecone
    from dotenv import load_dotenv
    import os

    load_dotenv()

    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    INDEX_NAME = os.environ.get('INDEX_NAME')
    #Initializing the Pinecone
    pc = Pinecone(api_key=PINECONE_API_KEY)  
    index = pc.Index(INDEX_NAME)
    print(index.describe_index_stats())



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= False)


