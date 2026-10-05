# Edge Cases & Mitigation Strategies: AI-Powered Discovery Engine

Based on the system architecture and phase-wise implementation plan for the 2x2 Visual Choice Grid, this document outlines potential edge cases, system vulnerabilities, and their corresponding mitigation strategies.

---

## 1. Data Sparsity & Insufficient Candidate Pool
**Scenario:** 
A user has a very small photo library, or their specific vague query (e.g., "blue unicycle") returns fewer than 4 relevant images in the Vector DB.
**Impact:** 
The K-Means clustering algorithm ($K=4$) will fail, throw an error, or duplicate images to fill the 2x2 grid, leading to a broken UI experience.
**Mitigation:** 
*   **Dynamic K-Sizing:** The Visual Search Orchestrator must evaluate the size of the retrieved candidate pool before clustering. If `pool_size < 4`, bypass the clustering engine entirely and gracefully degrade to the legacy linear search UI.
*   **Thresholding:** Only trigger the 2x2 grid if the Approximate Nearest Neighbor (ANN) search returns a minimum confidence threshold of at least 15-20 viable candidates.

## 2. The Homogeneous Pool (Low Visual Variance)
**Scenario:** 
A user searches for "beach", but their top 100 candidate images are a burst of 100 nearly identical photos taken within 10 seconds of the exact same wave. 
**Impact:** 
The clustering engine will successfully create 4 clusters, but the 4 centroid images will look visually identical to the user, rendering the choice grid useless.
**Mitigation:** 
*   **Minimum Distance Constraints:** Implement a minimum cosine-distance check between the 4 chosen centroids. 
*   **Diversity Injection:** If the initial K-Means output lacks variance, dynamically expand the candidate pool to N=300 and re-cluster with a penalty for temporal proximity (e.g., force the system to pick photos from different dates).

## 3. The "Infinite Pivot" Trap
**Scenario:** 
The user clicks the "None of these (Show others)" button repeatedly because the system keeps surfacing incorrect clusters.
**Impact:** 
Applying continuous negative vector weights will eventually push the query vector into a "noise" space, returning completely random or blank results. It also wastes heavy compute resources and frustrates the user.
**Mitigation:** 
*   **Pivot Capping:** Enforce a strict "Pivot Depth Limit" (e.g., maximum 3 dynamic pivots per session). 
*   **Graceful Exit:** If the user hits the pivot limit, remove the 2x2 grid, display a helpful message ("We're having trouble finding this exact memory"), and present the standard chronological search results or suggest query rephrasing.

## 4. Adversarial or Non-Sensical Queries
**Scenario:** 
The user enters gibberish ("asdfasdf") or abstract concepts impossible to photograph ("the meaning of life").
**Impact:** 
The Query Embedding Model generates a low-confidence or random vector, retrieving completely irrelevant photos. Presenting a 2x2 grid of random photos makes the AI look incompetent.
**Mitigation:** 
*   **Confidence Scoring:** The Query Analyzer / Intent Router must measure the confidence score of the generated text embedding. If the query maps poorly to known visual concepts, bypass the 2x2 grid and instantly return a "No results found" state.

## 5. Latency Spikes During Dynamic Pivots
**Scenario:** 
Under peak server load, the recalculation of negative weights, the subsequent secondary ANN search, and the re-clustering take 800ms instead of the budgeted 200ms.
**Impact:** 
The UI hangs after the user clicks "None of these", breaking the illusion of instantaneous, millisecond visual recognition and causing perceived friction.
**Mitigation:** 
*   **Optimistic UI / Skeleton States:** Display shimmering placeholder skeletons in the grid immediately upon click.
*   **Strict Timeouts:** If the Visual Search Orchestrator does not return new centroids within 400ms, fail gracefully by rendering the standard search list beneath the grid rather than keeping the user waiting indefinitely.

## 6. Sensitive Content Surfacing
**Scenario:** 
A user types a vague query like "documents" or "private". The clustering engine inadvertently selects a highly sensitive image (e.g., a photo of a passport, medical records, or explicit content) as the representative centroid for a cluster.
**Impact:** 
User discomfort and privacy concerns, especially if the user is searching in a public setting or sharing their screen.
**Mitigation:** 
*   **Safe-Search Centroid Penalties:** During the offline Ingestion Pipeline (Phase 1), flag images containing PII, documents, or sensitive content.
*   **Centroid Filtering:** Instruct the Centroid Representative Selector (Phase 2) to strongly heavily penalize or exclude flagged sensitive images from being chosen as the anchor image for a cluster, picking the second-closest "safe" image instead.

## 7. Multi-Lingual and Cultural Nuance Failures
**Scenario:** 
A user inputs a query using cultural slang (e.g., "Diwali vibes" or colloquial terms in Hindi/Spanish) that the primary embedding model does not map accurately to visual concepts.
**Impact:** 
The vector mapping fails to capture the semantic meaning, resulting in poor image retrieval.
**Mitigation:** 
*   **Language Fallback:** If the query is detected as a language/dialect with low embedding confidence, the Query Analyzer should route the request to the standard keyword search, which leverages localized EXIF data and metadata tags better than the visual vector space.
