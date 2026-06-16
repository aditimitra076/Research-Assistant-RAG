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

chunk_size = 1000

#creating overlapping chunks
overlap = 200

chunks = []

for i in range(0, len(full_text), chunk_size-overlap):
    chunk = full_text[i:i+chunk_size]
    chunks.append(chunk)




#################################################################
#embedding

from sentence_transformers import SentenceTransformer

load_dotenv()

login(token=os.getenv("HF_TOKEN"))


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("Number of chunks : ", len(chunks))
print("Number of embeddings: ", len(embeddings))

print("\nShape of embeddings : \n")
print(embeddings.shape)



##################################################################
#retrieval

#RETRIVER ->to find relevant infromation

from sentence_transformers.util import cos_sim

#user input question
#query = input("Ask a question: ") #user input of question

while True:
    query = input("\nAsk a question( or type exit): ")

    if query.lower()=="exit":
        break



query_embedding = model.encode(query)

scores = []


#stroing chunk embedding values
for i in range(len(chunks)):
    score = cos_sim(query_embedding, embeddings[i]).item() #item () converts pytorch tensor object to a normal number for ease of sorting
    scores.append((score, chunks[i]))

scores.sort(key=lambda x: x[0], reverse=True)

top_3 = scores[:3]


context=""

for score, chunk in top_3:
    context+= chunk+ "\n\n"

print("\n----CONTEXT----\n")
print(context[:1500])


#######################################################3
#connecting to LLM

#load token

client = InferenceClient(
    api_key = os.getenv("HF_TOKEN")
)

prompt = f"""
Answer the question using ONLY the provided context.

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