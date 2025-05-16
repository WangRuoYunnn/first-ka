# models.py
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import numpy as np
import plotly.express as px

# ---- 資料 ----
sentences = [
    'Support Talent Acquisition Advisors talent sourcing, screening, project execution',
    'Provide administrative support recruitment function.',
    'Input employee personal data into human resources information computer system database.',
    'Manage job posting on platform',
    'Send interview invitation both candidates hiring managers',
    'Search potential candidates in company databases public job board',
    'Manage pre-screening interview Mandarin English',
    'Provide functional system expertise',
    'Provide recruitment project support',
    'Bachelor Master'
]
tokenized = [s.lower().split() for s in sentences]

# Skip-gram
skipgram_model = Word2Vec(
    tokenized,
    vector_size=50,
    window=4,
    min_count=1,
    sg=1,          # sg=1 → Skip-gram
    epochs=30,
    seed=42
)
w2v = skipgram_model

# CBOW
cbow_model = Word2Vec(
    tokenized,
    vector_size=50,
    window=4,
    min_count=1,
    sg=0,          # sg=0 → CBOW
    epochs=30,
    seed=42
)

# ---- 把句子變向量 ----
def sentence_to_vec(sent: str, model=w2v) -> np.ndarray:
    words = sent.lower().split()
    vecs = [model.wv[w] for w in words if w in model.wv]
    return np.mean(vecs, axis=0) if vecs else np.zeros(model.vector_size)

# ---- 生成 2D / 3D 圖 ----
def pca_2d(model=w2v):
    X = np.vstack([sentence_to_vec(s, model) for s in sentences])
    coords = PCA(n_components=2, random_state=42).fit_transform(X)
    fig = px.scatter(
        x=coords[:, 0], y=coords[:, 1], text=[f"S{i}" for i in range(len(sentences))]
    )
    fig.update_traces(textposition="top center")
    return fig

def pca_3d(model=w2v):
    X = np.vstack([sentence_to_vec(s, model) for s in sentences])
    coords = PCA(n_components=3, random_state=42).fit_transform(X)
    fig = px.scatter_3d(
        x=coords[:, 0], y=coords[:, 1], z=coords[:, 2],
        text=[f"S{i}" for i in range(len(sentences))]
    )
    fig.update_traces(textposition="top center")
    return fig

# ---- 在圖上加點 ----
def add_point_to_fig(fig, vec, label="new"):
    if vec.ndim == 1:  # 2D
        fig.add_scatter(x=[vec[0]], y=[vec[1]], mode="markers+text",
                        marker=dict(size=10, color="red"),
                        text=[label], textposition="bottom center")
    else:  # 3D；這裡其實用不到
        pass

# ---- 近義詞 & 句子相似度 ----
def most_similar_words(model, word, topn=10):
    return model.wv.most_similar(word, topn=topn)

def sentence_similarity_rank(model, sent):
    vec = sentence_to_vec(sent, model)
    sims = []
    for s in sentences:
        sims.append((s, cosine(vec, sentence_to_vec(s, model))))
    return sorted(sims, key=lambda x: -x[1])

def cosine(a, b):
    if a.dot(a) == 0 or b.dot(b) == 0:
        return 0
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))
