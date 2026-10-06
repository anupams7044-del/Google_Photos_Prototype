from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import numpy as np

class VisualClusteringEngine:
    def __init__(self, k_clusters=4):
        self.k_clusters = k_clusters

    def cluster_and_get_centroids(self, embeddings, metadata_list, ids_list):
        """
        Takes a list of candidate embeddings and clusters them into K groups.
        Returns the 4 centroid images (the most representative image for each group).
        """
        # Edge Case Mitigation: Data Sparsity
        n_samples = len(embeddings)
        if n_samples < self.k_clusters:
            print(f"Warning: Only {n_samples} candidates found. Adjusting K to {n_samples}.")
            actual_k = n_samples
        else:
            actual_k = self.k_clusters
            
        if actual_k == 0:
            return []

        # Convert to numpy array for sklearn
        X = np.array(embeddings)
        
        # 1. Run Fast K-Means Clustering
        kmeans = KMeans(n_clusters=actual_k, random_state=42, n_init='auto')
        kmeans.fit(X)
        
        cluster_centers = kmeans.cluster_centers_
        labels = kmeans.labels_
        
        centroids_info = []
        
        # 2. Centroid Representative Selection
        for i in range(actual_k):
            # Find all points belonging to cluster i
            cluster_indices = np.where(labels == i)[0]
            
            if len(cluster_indices) == 0:
                continue
                
            cluster_points = X[cluster_indices]
            center = cluster_centers[i].reshape(1, -1)
            
            # Calculate distance from each point in the cluster to the cluster center
            distances = pairwise_distances(cluster_points, center, metric='cosine').flatten()
            
            # Find the index of the point closest to the center (the true centroid)
            closest_idx_in_cluster = np.argmin(distances)
            original_idx = cluster_indices[closest_idx_in_cluster]
            
            centroids_info.append({
                "cluster_id": int(i),
                "photo_id": str(ids_list[original_idx]),
                "metadata": metadata_list[original_idx],
                "embedding": [float(x) for x in embeddings[original_idx]], # Stored for Phase 3 dynamic pivoting
                "distance_to_center": float(distances[closest_idx_in_cluster])
            })
            
        return centroids_info
