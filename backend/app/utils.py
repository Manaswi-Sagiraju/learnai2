import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
import pandas as pd

def recommend_topics(user_scores: pd.DataFrame, all_topics: pd.DataFrame, top_n=3):
    if user_scores.empty:
        return all_topics.head(top_n).to_dict('records')
    
    topic_vectors = all_topics[['difficulty']].values
    user_vector = np.array(user_scores[['score']].values.flatten()).reshape(1, -1)
    similarities = cosine_similarity(user_vector, topic_vectors)
    all_topics['similarity'] = similarities.flatten()
    return all_topics.sort_values(by='similarity', ascending=False).head(top_n).to_dict('records')

def detect_knowledge_gap(user_history: pd.DataFrame):
    if len(user_history) < 2:
        return pd.DataFrame()
    X = user_history[['score', 'attempts', 'difficulty']]
    y = (user_history['score'] < 50).astype(int)
    model = LogisticRegression()
    model.fit(X, y)
    user_history['fail_prob'] = model.predict_proba(X)[:,1]
    weak_topics = user_history[user_history['fail_prob'] > 0.5]
    return weak_topics
