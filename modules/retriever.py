import re
import numpy as np

from rapidfuzz import process, fuzz

from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def correct_query(
        query,
        chunks
):

    vocabulary = set()

    for chunk in chunks:

        words = re.findall(
            r"[A-Za-z]+",
            chunk["text"].lower()
        )

        vocabulary.update(words)

    corrected_words = []

    for word in query.split():

        clean_word = re.sub(
            r"[^A-Za-z]",
            "",
            word.lower()
        )

        if (
            len(clean_word) < 4
            or clean_word in vocabulary
        ):

            corrected_words.append(word)

            continue

        match = process.extractOne(
            clean_word,
            vocabulary,
            scorer=fuzz.ratio
        )

        if (
            match
            and match[1] >= 85
        ):

            corrected_words.append(
                match[0]
            )

        else:

            corrected_words.append(
                word
            )

    return " ".join(
        corrected_words
    )


#reranker
def rerank_chunks(
        query,
        chunks,
        scores,
        indices
):

    query_words = set(
        re.findall(
            r"[A-Za-z]+",
            query.lower()
        )
    )

    reranked = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx == -1:
            continue

        chunk = chunks[idx]

        chunk_words = set(
            re.findall(
                r"[A-Za-z]+",
                chunk["text"].lower()
            )
        )

        keyword_overlap = len(
            query_words.intersection(
                chunk_words
            )
        )

        page_bonus = 0

        if chunk["page"] <= 2:
            page_bonus = 2

        final_score = (

            float(score) * 0.6 +

            keyword_overlap * 0.3 +

            page_bonus * 0.1
        )

        reranked.append(

            (
                final_score,
                idx
            )
        )

    reranked.sort(
        reverse=True
    )

    return [
        idx
        for _, idx in reranked
    ]




def retrieve_chunks(
        query,
        index,
        chunks,
        top_k=5
):

    query = correct_query(
        query,
        chunks
    )

    print(
        f"\nCorrected Query: {query}"
    )

    query_embedding = np.array(
        model.encode(
            query,
            normalize_embeddings=True
        )
    ).astype("float32")

    query_embedding = query_embedding.reshape(
        1,
        -1
    )

    metadata_keywords = [
        "author",
        "authors",
        "title",
        "abstract",
        "keyword",
        "keywords",
        "affiliation",
        "affiliations",
        "published",
        "publication",
        "conference",
        "journal"
    ]

    metadata_query = any(
        word in query.lower()
        for word in metadata_keywords
    )

    search_k = 10 if metadata_query else top_k

    scores, indices = index.search(
        query_embedding,
        search_k
    )

    reranked_indices = rerank_chunks(
    query,
    chunks,
    scores,
    indices
    )

    filtered_chunks = []

    selected_indices = []

    added = set()

    if metadata_query:

        for idx, chunk in enumerate(chunks):

            if chunk["page"] <= 2:

                filtered_chunks.append(
                    chunk["text"]
                )

                selected_indices.append(
                    idx
                )

                added.add(idx)

    score_lookup = {
        idx: score
        for score, idx in zip(
            scores[0],
            indices[0]
        )
    }

    for idx in reranked_indices:
        score = score_lookup[idx]

        if idx == -1:
            continue

        if idx in added:
            continue

        if score < 0.45:
            continue

        filtered_chunks.append(
            chunks[idx]["text"]
        )

        selected_indices.append(
            idx
        )

        added.add(idx)

    if len(filtered_chunks) == 0:

        for idx in reranked_indices:

            if idx == -1:
                continue

            filtered_chunks.append(
                chunks[idx]["text"]
            )

            selected_indices.append(
                idx
            )

            if len(filtered_chunks) == top_k:
                break

    context = ""

    for idx in selected_indices:

        context += (
            "\n=====DOCUMENT=====\n"
            f"Filename: {chunks[idx]['pdf_name']}\n"
            f"Page: {chunks[idx]['page']}\n\n"
            f"{chunks[idx]['text']}\n\n"
        )

    return (
        context,
        scores,
        np.array([selected_indices])
    )