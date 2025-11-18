import csv
import math
import itertools

DATA_FILE = "students_200.csv"
K = 3


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


# ---------- 階層式分群 (average linkage) ----------
def avg_linkage_distance(points, cluster_a, cluster_b):
    total = 0.0
    count = 0
    for i in cluster_a:
        for j in cluster_b:
            total += math.sqrt(euclidean_sq(points[i], points[j]))
            count += 1
    return total / count


def hierarchical_clustering(students, k=K):
    points = [(s["chinese"], s["english"]) for s in students]
    n = len(points)

    # 每個點自己一群
    clusters = {i: [i] for i in range(n)}
    next_cluster_id = n

    # 合併到只剩 k 群
    while len(clusters) > k:
        best_pair = None
        best_dist = None
        ids = list(clusters.keys())

        for i_idx in range(len(ids)):
            for j_idx in range(i_idx + 1, len(ids)):
                ci = ids[i_idx]
                cj = ids[j_idx]
                d = avg_linkage_distance(points, clusters[ci], clusters[cj])
                if best_dist is None or d < best_dist:
                    best_dist = d
                    best_pair = (ci, cj)

        a, b = best_pair
        new_members = clusters[a] + clusters[b]
        del clusters[a]
        del clusters[b]
        clusters[next_cluster_id] = new_members
        next_cluster_id += 1

    # 重新給 0,1,2… 群標籤
    final_ids = list(clusters.keys())
    labels_by_index = [None] * n
    for label, cid in enumerate(final_ids):
        for idx in clusters[cid]:
            labels_by_index[idx] = label

    return labels_by_index


# ---------- 主程式 ----------
def main():
    students = load_data(DATA_FILE)

    hier_labels = hierarchical_clustering(students)

    true_labels = [s["true"] for s in students]
    hier_acc, hier_map = best_accuracy(true_labels, hier_labels)


    print(f"最佳準確率：{hier_acc:.4f} （約 {hier_acc*100:.2f}% ）")
    print("最佳標籤對應（分群結果 → 真實群）：", hier_map)
    print("====================================\n")

    print("各群的平均成績：")
    for lbl, (m_c, m_e, cnt) in sorted(cluster_means(students, hier_labels).items()):
        print(f"  群 {lbl}：人數 = {cnt}，國文平均 = {m_c:.2f}，英文平均 = {m_e:.2f}")



if __name__ == "__main__":
    main()