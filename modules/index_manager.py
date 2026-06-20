# import faiss
# import pickle
# import os


# INDEX_PATH = "storage/index.faiss"
# CHUNKS_PATH = "storage/chunks.pkl"


# def save_index(index, chunks):

#     os.makedirs(
#         "storage",
#         exist_ok=True
#     )

#     faiss.write_index(
#         index,
#         INDEX_PATH
#     )

#     with open(
#         CHUNKS_PATH,
#         "wb"
#     ) as file:
        
#         pickle.dump(
#             chunks,
#             file
#         )

# def load_index():
#     if(
#         not os.path.exists(INDEX_PATH)
#         or 
#         not os.path.exists(CHUNKS_PATH)
#     ):
        
#         return None, None
    
#     index= faiss.read_index(
#         INDEX_PATH
#     )

#     with open(
#         CHUNKS_PATH,
#         "rb"
#     ) as file:
        
#         chunks = pickle.load(file)

#     return index, chunks


import faiss
import pickle
import os


def save_index(
        index,
        chunks,
        storage_path
):
    os.makedirs(
        storage_path,
        exist_ok=True
    )

    index_path = os.path.join(
        storage_path,
        "index.faiss"
    )

    chunks_path = os.path.join(
        storage_path,
        "chunks.pkl"
    )

    faiss.write_index(
        index,
        index_path
    )

    

    with open(
        chunks_path,
        "wb"
    ) as file:
        pickle.dump(
            chunks,
            file
        )


def load_index(storage_path):

    index_path = os.path.join(
        storage_path,
        "index.faiss"
    )


    chunks_path = os.path.join(
        storage_path,
        "chunks.pkl"
    )

    if(
        not os.path.exists(index_path)
        or
        not os.path.exists(chunks_path)
    ):
        
        return None, None
    
    index = faiss.read_index(
        index_path
    )

    with open(
        chunks_path,
        "rb"
    ) as file:
        
        chunks = pickle.load(file)

    return index, chunks