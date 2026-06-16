#code to read a file using library pypdf

from pypdf import PdfReader
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from huggingface_hub import login


reader = PdfReader("data/sample.pdf")

#print("Number of pages: ", len(reader.pages))

full_text =""

for page in reader.pages:
    full_text += page.extract_text()

#print(full_text[:2000])

#print(len(full_text))

##############################################################
#chunking

chunk_size = 500

#creating overlapping chunks
overlap = 100

chunks = []

for i in range(0, len(full_text), chunk_size-overlap):
    chunk = full_text[i:i+chunk_size]
    chunks.append(chunk)

print("\n===CHUNK 0===\n")
print(chunks[0])


#################################################################
#embedding

from sentence_transformers import SentenceTransformer

load_dotenv()

#login(token=os.getenv("HF_TOKEN"))


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    chunks,
    normalize_embeddings=True)

print("Number of chunks : ", len(chunks))
print("Number of embeddings: ", len(embeddings))

print("\nShape of embeddings : \n")
print(embeddings.shape)



##################################################################
#retrieval

#RETRIVER ->to find relevant infromation

from sentence_transformers.util import cos_sim


#load token
client = InferenceClient(
        api_key = os.getenv("HF_TOKEN")
    )

#user input question

while True:
    query = input("\nAsk a question( or type exit): ")

    if query.lower()=="exit":
        break

    #query embedding######################################
    query_embedding = model.encode(
        query,
        normalize_embeddings=True)


    scores = []


    #stroing chunk embedding values
    for i in range(len(chunks)):
        score = cos_sim(query_embedding, embeddings[i]).item() #item () converts pytorch tensor object to a normal number for ease of sorting
        scores.append((score,i, chunks[i]))

    scores.sort(key=lambda x: x[0], reverse=True)

    #debug retreval
    print("\nTop 10 scores:\n")

    for score, idx, chunk in scores[:10]:
        print(f"Chunk{idx} : {score:.4f}")

    top_10 = scores[:10]

    print("\nTop Retrived Chunks: \n")

    for score, idx, chunk in top_10:
        print(f"\nChunk Index: {idx}")
        print(f"Score: {score:.4f}")
        print(chunk[:300])

    #context creation####################################
    context=""

    for score,idx, chunk in top_10:
        context+= chunk+ "\n\n"

    # print("\n----CONTEXT----\n")
    # print(context[:1500])

    
    #connecting to LLM##########################################
    

    prompt = f"""
    You are a helpful reserach assistant.

    Answer the question using ONLY the provided context.

    If the answer is not present in the context, say:
    "I could not find the answer in the provided document."

    Context: 
    {context}

    Question:
    {query}

    """

    ##############################################################3
    #generating answer

    response = client.chat_completion(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        max_tokens=300
    )

    print("\n====ANSWER====\n")
    print(response.choices[0].message.content)


    










