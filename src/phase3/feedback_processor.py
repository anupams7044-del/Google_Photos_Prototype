import numpy as np

class FeedbackProcessor:
    def __init__(self, negative_weight_factor=0.3):
        # Defines how aggressively we push away from rejected images
        self.negative_weight_factor = negative_weight_factor
        
    def apply_negative_feedback(self, original_query_vector, rejected_centroid_embeddings):
        """
        Takes the current query vector and pushes it mathematically AWAY from the rejected concepts.
        Simplified Rocchio Algorithm variant.
        Math: New_Q = Old_Q - (Weight * Average(Rejected_Vectors))
        """
        if not rejected_centroid_embeddings:
            return original_query_vector
            
        q_vec = np.array(original_query_vector)
        
        # Calculate the central direction of the concepts the user rejected
        rejected_matrix = np.array(rejected_centroid_embeddings)
        rejected_mean = np.mean(rejected_matrix, axis=0)
        
        # Push the query vector away from the rejected mean
        new_q_vec = q_vec - (self.negative_weight_factor * rejected_mean)
        
        # Re-normalize the vector to keep it on the unit hypersphere (critical for cosine similarity accuracy)
        norm = np.linalg.norm(new_q_vec)
        if norm > 0:
            new_q_vec = new_q_vec / norm
            
        return new_q_vec.tolist()
