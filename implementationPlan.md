# Phase-Wise Implementation Plan: 2x2 Visual Choice Grid

This document outlines the strategic, phase-wise implementation plan for the AI-Powered Discovery Engine and 2x2 Visual Choice Grid, based on the established system architecture.

---

## Phase 1: Foundation & Data Pipeline (Weeks 1-4)
**Objective:** Establish the foundational AI infrastructure and ensure all user photos are accurately embedded and stored in a scalable vector database.

*   **1.1 Multimodal Embedding Model Setup:** 
    *   Deploy the underlying foundation model (e.g., a variant of CLIP or internal multimodal model) capable of understanding both images and text in a shared vector space.
*   **1.2 Vector Database Provisioning:** 
    *   Initialize the Vector DB (e.g., Google ScaNN) with strict multi-tenant partitioning by User ID to ensure privacy and security.
*   **1.3 Offline Ingestion Pipeline:** 
    *   Build the asynchronous background worker to process new photo uploads.
    *   Extract vision features, objects, vibes, and EXIF metadata (time, location).
    *   Generate and index embeddings into the Vector DB.
*   **Milestone:** A scalable pipeline that successfully ingests photos, converts them to vectors, and indexes them securely.

---

## Phase 2: Core AI & Retrieval Engine (Weeks 5-8)
**Objective:** Build the core logic capable of retrieving candidates and organizing them into distinct visual categories in real-time.

*   **2.1 Query Embedding Service:** 
    *   Develop the API endpoint that converts natural language text queries into dense mathematical vectors.
*   **2.2 Candidate Pool Retrieval (ANN):** 
    *   Implement Approximate Nearest Neighbor (ANN) search to rapidly fetch the top 60-100 image embeddings matching the query vector.
*   **2.3 Real-Time Clustering Engine:** 
    *   Implement a highly optimized, low-latency K-Means clustering algorithm ($K=4$) tailored for small datasets (N=100 vectors).
*   **2.4 Centroid Selection:** 
    *   Build the logic to identify and extract the single most representative image (centroid) for each of the 4 generated clusters.
*   **Milestone:** A backend API that accepts a text query and returns 4 highly distinct centroid images representing different conceptual directions.

---

## Phase 3: Orchestration & Dynamic Feedback Loop (Weeks 9-11)
**Objective:** Connect the routing logic and build the "Hot or Cold" feedback mechanism to allow users to pivot their search.

*   **3.1 Query Analyzer & Router:** 
    *   Build a lightweight intent classifier to determine if a query is "specific" (route to legacy search) or "vague" (route to the Visual Search Orchestrator).
*   **3.2 Visual Search Orchestrator:** 
    *   Implement session state management to track a user's search refinement journey without requiring conversational chat history.
*   **3.3 Dynamic Pivot / Feedback Processor:** 
    *   Develop the negative weight algorithm. When a user rejects the 4 options, apply negative vectors to the rejected centroids, recalculate the query vector, and fetch a new set of candidates.
*   **Milestone:** A complete stateful backend flow that supports initial vague queries and subsequent dynamic pivots ("None of these").

---

## Phase 4: Client-Side Integration (Frontend) (Weeks 12-14)
**Objective:** Build the native UI components and integrate them seamlessly into the Google Photos client applications.

*   **4.1 Native Component Development:** 
    *   Develop the 2x2 Visual Choice Grid component for iOS, Android, and Web platforms.
    *   Ensure the design strictly adheres to Google Material Design principles (uncluttered, native feel beneath the search bar).
*   **4.2 Interaction Handlers:** 
    *   Wire up the positive reinforcement tap (clicking a quadrant to fetch that cluster's full results).
    *   Wire up the negative reinforcement tap ("None of these" button to trigger the dynamic pivot).
*   **4.3 UI Animations & Transitions:** 
    *   Implement smooth, sub-100ms UI transitions to make the grid feel instantaneous and interactive.
*   **Milestone:** Fully functional end-to-end feature accessible in staging client builds.

---

## Phase 5: Telemetry, Optimization, & NFRs (Weeks 15-17)
**Objective:** Harden the system for Google-scale production, focusing on latency, security, and measurable business impact.

*   **5.1 Latency Optimization:** 
    *   Profile the entire round-trip (Query -> ANN -> Clustering -> Render). Move clustering to edge-compute or WebAssembly if necessary to hit the strict 200-300ms latency budget.
*   **5.2 Telemetry Integration:** 
    *   Implement logging for the key success metrics: Search Abandonment Rate, Time to Disambiguation, Pivot Depth, and Manual Scroll Tax (pixels scrolled).
*   **5.3 Security & Load Testing:** 
    *   Conduct rigorous security audits on the multi-tenant Vector DB isolation. 
    *   Simulate high-concurrency peak load testing on the clustering microservices.
*   **Milestone:** Production-ready system that meets all strict non-functional requirements.

---

## Phase 6: User Testing, MVP Launch & Iteration (Weeks 18-20)
**Objective:** Validate the solution with real users, measure the impact on the core business metric, and iterate.

*   **6.1 Internal Dogfooding & QA:** 
    *   Roll out to internal Google employees. Conduct exploratory testing to catch edge cases in vague queries.
*   **6.2 A/B Testing & Phased Rollout:** 
    *   Launch the MVP to a small target segment (e.g., 1-5% of live users). A/B test against the legacy keyword search.
*   **6.3 Data Analysis & Tuning:** 
    *   Analyze the telemetry data to see if successful retrieval of vaguely remembered photos has increased.
    *   Tune the embedding weights, cluster sizes (K), or candidate pool size based on real-world interaction depth.
*   **Milestone:** Successful MVP validation and a documented case study proving the impact on the core product metric, ready for global rollout.
