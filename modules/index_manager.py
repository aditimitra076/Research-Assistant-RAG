import faiss
import pickle
import os


INDEX_PATH = "storage/index.faiss"
CHUNKS_PATH = "storage/chunks.pkl"


def save_index(index, chunks):

    os.makedirs(
        "storage",
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        CHUNKS_PATH,
        "wb"
    ) as file:
        
        pickle.dump(
            chunks,
            file
        )

def load_index():
    if(
        not os.path.exists(INDEX_PATH)
        or 
        not os.path.exists(CHUNKS_PATH)
    ):
        
        return None, None
    
    index= faiss.read_index(
        INDEX_PATH
    )

    with open(
        CHUNKS_PATH,
        "rb"
    ) as file:
        
        chunks = pickle.load(file)

    return index, chunks