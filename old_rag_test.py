from pypdf import PdfReader
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
#from huggingface_hub import login

import faiss #vector database
import numpy as np #needed as faiss requires numpy arrays

#############################################################
#reading the pdf
reader = PdfReader("data/sample.pdf")
full_text =""

for page in reader.pages:
    text= page.extract_text()

    if text:
        full_text +=text




##############################################################
#chunking

chunk_size = 1000
overlap = 200

chunks = []

for i in range(0, len(full_text), chunk_size-overlap):
    chunk = full_text[i:i+chunk_size]
    chunks.append({
        "text":chunk,
        "chunk_id": len(chunks)
    })

chunk_texts = [chunk["text"]for chunk in chunks] #converting to string as sentence transformers expects strings




###############################################################
#embedding

from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    chunk_texts,
    normalize_embeddings=True
    )
#normalize_embeddings= True makes vector unit length, useful as cosine similarity becomes dot product which FAISS IndexFlatIP uses.

embeddings = np.array(embeddings).astype("float32") #faiss requires float32 not float64

print("Number of chunks : ", len(chunks))
print("Number of embeddings: ", len(embeddings))

print("\nShape of embeddings : \n")
print(embeddings.shape)




##############################################################
#faiss index
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print("\nFAISS index created\n")
print("Vectors stored: ", index.ntotal)


###############################################################
#load token
client = InferenceClient(
        api_key = os.getenv("HF_TOKEN")
    )


###############################################################
#user question

while True:
    query = input("\nAsk a question( or type exit): ")

    if query.lower()=="exit":
        break

###############################################################
#query embedding

    query_embedding =np.array(
        model.encode(
            query,
            normalize_embeddings= True
        )
    ).astype("float32")
    

    query_embedding = query_embedding.reshape(1, -1)


#################################################################
#retrieval
    scores, indices = index.search(query_embedding, 10)

    print("\nTop 10 scores: \n")
    for score, idx in zip(scores[0], indices[0]):
        print(f"Chunk{idx}: {score:.4f}")

    print("\nTop Retrived Chunks\n")

    for score, idx in zip(scores[0], indices[0]):
        print(f"\nChunk INdex: {idx}")
        print(f"Score: {score:.4f}")
        print(chunks[idx]["text"][:300])

##################################################################
#context creation
    
    context=""

    context = "\n\n".join(
        chunks[idx]["text"]
        for idx in indices[0]
    )
   
    
    
##################################################################
#connecting to LLM (actual RAG step)
    

    prompt = f"""
    You are a helpful research assistant.

    Answer the question using ONLY the provided context.

    If authors, title, abstract, affiliations, publication
    information, or metadata are present in the context,
    use them directly.

    If the answer is not found, say:
    "I could not find the answer in the provided document."

    Context: 
    {context}

    Question:
    {query}

    """

#####################################################################
#generating answer using LLama 3.1

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


    










