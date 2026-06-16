#code to read a file using library pypdf

from pypdf import PdfReader


reader = PdfReader("data/sample.pdf")

#print("Number of pages: ", len(reader.pages))

full_text =""

for page in reader.pages:
    full_text += page.extract_text()

#print(full_text[:2000])

#print(len(full_text))

#################################
#chunking

chunk_size = 1000

#creating overlapping chunks
overlap = 200

chunks = []

for i in range(0, len(full_text), chunk_size-overlap):
    chunk = full_text[i:i+chunk_size]
    chunks.append(chunk)



#print("Number of chunks: ", len(chunks))

#print("\nLength of first chunk:\n")
#print(len(chunks[0]))


#embedding

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

print("Number of chunks : ", len(chunks))
print("Number of embeddings: ", len(embeddings))

print("\nShape of embeddings : \n")
print(embeddings.shape)


#retrieval

#RETRIVER ->to find relevant infromation

from sentence_transformers.util import cos_sim

query = "What are criticism of fair clustering?"

query_embedding = model.encode(query)

scores = []

#stroing chunk embedding values
for i in range(len(chunks)):
    score = cos_sim(query_embedding, embeddings[i]).item() #item () converts pytorch tensor object to a normal number for ease of sorting
    scores.append((score, chunks[i]))

scores.sort(reverse=True)

top_3 = scores[:3]


#prints the chunk
for i, (score, chunk) in enumerate(top_3):
    print(f"\n---Chunk{i+1}---")
    print("Score: ", score)
    print(chunk[:500])

# best_score= -1
# best_chunk = ""

# for i in range(len(chunks)):
#     score  = cos_sim(query_embedding, embeddings[i])

#     if score> best_score:
#         best_score= score
#         best_chunk = chunks[i]


# print("\nBest similarity score: \n")
# print(best_score)

# print("\nMost relevant chunk: \n")
# print(best_chunk)