#embedding for testing


from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer("all-MiniLM-L6-v2")



sentence1= "Machine Learning is used in hospitals."

sentence2= "AI helps doctors treat patients."

sentence3 = "I like pizza."

embedding1 = model.encode(sentence1)
embedding2= model.encode(sentence2)
embedding3 = model.encode(sentence3)

print("Sentence1 vs Sentence2: ")
print(cos_sim(embedding1, embedding2))


print("\nSentence1 vs Sentence3: ")
print(cos_sim(embedding1, embedding3))


