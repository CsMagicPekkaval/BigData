import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# ----------------------------------------
# 讀取資料（假設 CSV 欄位包含：chinese, english, true_cluster）
# ----------------------------------------
df = pd.read_csv("students_200.csv")

X = df[["chinese", "english"]].values   # 只有兩欄

# ----------------------------------------
# 1. 原始資料 K-means 分群
# ----------------------------------------
kmeans_raw = KMeans(n_clusters=3, random_state=0)
raw_labels = kmeans_raw.fit_predict(X)

raw_silhouette = silhouette_score(X, raw_labels)

print("========== 原始資料（未降維） ==========")
print(f"Silhouette score = {raw_silhouette:.4f}\n")

# ----------------------------------------
# 2. PCA 降維（測試 1、2、3 維）
# ----------------------------------------
dimensions = [1, 2]   # <-- 你的資料只有兩個欄位，所以最多只能降到 2 維

best_dim = None
best_score = -1
results = {}

for dim in dimensions:
    pca = PCA(n_components=dim)
    X_reduced = pca.fit_transform(X)

    kmeans_pca = KMeans(n_clusters=3, random_state=0)
    labels_pca = kmeans_pca.fit_predict(X_reduced)

    score = silhouette_score(X_reduced, labels_pca)
    results[dim] = score

    print(f"PCA {dim} 維 → Silhouette score = {score:.4f}")

    # 找最佳維度
    if score > best_score:
        best_dim = dim
        best_score = score

print("\n========== 最佳 PCA 維度 ==========")
print(f"最佳維度：{best_dim} 維(Silhouette = {best_score:.4f})")