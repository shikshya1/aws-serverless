from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


model = SentenceTransformer('/mnt/tmp/paraphrase-MiniLM-L6-v2')

def hello(event, context):

    documents=event['documents']
    query=event['query']

    embeddings= model.encode(documents)
    query_embeddings= model.encode(query)
    embeddings.shape

    scores = cos_sim(query_embeddings, embeddings).flatten()
    results = zip(documents, scores)
    results = sorted(results, key=lambda x: x[1], reverse=True)
    final_result=[]

    for idx, distance in results[0:len(documents)]:
        final_result.append({'sentence': idx, 'similarity_score': distance.item()})

    return {"query": query, "sentences": final_result}

