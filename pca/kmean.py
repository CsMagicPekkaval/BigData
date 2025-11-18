import csv
import random
import itertools

DATA_FILE = "students_200.csv"
K = 3
MAX_ITER = 100


# ---------- 讀資料 ----------
def load_data(path):
    students = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "id": row["student_id"],
                "chinese": float(row["chinese"]),
            "english": float(row["english"]),
            "true": row["true_cluster"].strip()
        })
    return students


# ---------- 共用工具 ----------
def euclidean_sq(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def cluster_means(students, labels):
    sums = {}
    counts = {}
    for s, lbl in zip(students, labels):
        if lbl not in sums:
            sums[lbl] = [0.0, 0.0]
            counts[lbl] = 0
        sums[lbl][0] += s["chinese"]
        sums[lbl][1] += s["english"]
        counts[lbl] += 1

    results = {}
    for lbl in sums:
        c = counts[lbl]
        results[lbl] = (sums[lbl][0] / c, sums[lbl][1] / c, c)
    return results


def best_accuracy(true_labels, pred_labels):
    cluster_ids = sorted(set(pred_labels))
    true_ids = sorted(set(true_labels))

    best_acc = 0.0
    best_map = None

    for perm in itertools.permutations(true_ids, len(cluster_ids)):
        mapping = {cluster_ids[i]: perm[i] for i in range(len(cluster_ids))}
        correct = 0
        for t, p in zip(true_labels, pred_labels):
            if mapping.get(p) == t:
                correct += 1
        acc = correct / float(len(true_labels))
        if acc > best_acc:
            best_acc = acc
            best_map = mapping

    return best_acc, best_map


# ---------- K-means 主體 ----------
def kmeans(students, k=K, max_iter=MAX_ITER):
    points = [(s["chinese"], s["english"]) for s in students]
    n = len(points)

    indices = list(range(n))
    random.shuffle(indices)
    centroids = [points[i] for i in indices[:k]]

    labels = [None] * n

    for _ in range(max_iter):
        changed = False

        # 指派群
        for i, p in enumerate(points):
            best_c = None
            best_d = None
            for c_idx, c in enumerate(centroids):
                d = euclidean_sq(p, c)
                if best_d is None or d < best_d:
                    best_d = d
                    best_c = c_idx
            if labels[i] != best_c:
                labels[i] = best_c
                changed = True

        if not changed:
            break

        # 更新中心
        new_centroids = []
        for c_idx in range(k):
            xs = ys = 0.0
            count = 0
            for lbl, p in zip(labels, points):
                if lbl == c_idx:
                    xs += p[0]
                    ys += p[1]
                    count += 1
            if count == 0:
                new_centroids.append(points[random.randrange(n)])
            else:
                new_centroids.append((xs / count, ys / count))
        centroids = new_centroids

    return labels, centroids


# ---------- 主程式 ----------
def main():
    students = load_data(DATA_FILE)

    # K-means 分群
    kmeans_labels, kmeans_centers = kmeans(students)

    true_labels = [s["true"] for s in students]
    kmeans_acc, kmeans_map = best_accuracy(true_labels, kmeans_labels)


    print(f"最佳準確率：{kmeans_acc:.4f} （約 {kmeans_acc*100:.2f}% ）")
    print("最佳標籤對應（分群結果 → 真實群）：", kmeans_map)
    print("====================================\n")

    print("各群的平均成績：")
    for lbl, (m_c, m_e, cnt) in sorted(cluster_means(students, kmeans_labels).items()):
        print(f"  群 {lbl}：人數 = {cnt}，國文平均 = {m_c:.2f}，英文平均 = {m_e:.2f}")



if __name__ == "__main__":
    main()