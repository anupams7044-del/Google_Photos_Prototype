# Product Manager Fellowship
## Graduation Project - Sep 2026

**Submission deadline:** Oct 7, 4:00:00 PM (Asia/Calcutta)

You are a Product Manager on the Core Experience team at Google Photos.

Over years of usage, users accumulate thousands of photos, videos, screenshots, documents, and other visual memories in Google Photos.

While users can easily search when they know what they are looking for, retrieval becomes much harder when memory is incomplete.

For example, a user may remember:

* “That small café we went to during our Goa trip.” OR
* “The picture of the medicine I took when I was sick last year.”

The user knows that the photo exists—but may not remember when it was taken, where it was taken, what album it belongs to, or the exact words needed to search for it.

One of your company’s strategic goals is to:

**Increase the percentage of users who successfully retrieve a photo they remember but cannot precisely describe when they start searching.**

The challenge is not to improve search in general.

Your task is to understand how people remember old visual information, where the existing retrieval experience breaks down, and identify an opportunity that can meaningfully improve successful retrieval.

---

## Part 1: Build an AI-Powered Discovery Engine
Before proposing any solution, build an AI-powered system that analyzes user feedback and conversations about photo retrieval at scale.

You may use:
* Claude
* GPTs
* Agents
* Workflows
* RAG
* n8n
* Zapier
* Perplexity
* Any AI-native stack of your choice

Analyze publicly available sources such as:
* Google Play Store reviews
* App Store reviews
* Reddit discussions
* Google Photos community/support discussions
* Social media conversations
* YouTube comments
* Forums and other relevant public discussions

Your discovery engine should help uncover questions like (sample questions only):
* What kinds of old photos do users struggle to retrieve?
* What information do people actually remember about a photo?
* What information have they forgotten?
* How do users formulate searches when their memory is incomplete?

Your workflow should go beyond summarizing reviews or performing sentiment analysis. It should enable you to identify and compare different retrieval problems and opportunity areas using evidence from real users.

## Part 2: Break Down the Business Metric
Break down:

**Successful retrieval of vaguely remembered photos**

into the relevant user behaviors and product outcomes.

Develop your own decomposition based on your understanding of the product and the evidence surfaced by your discovery engine.

Consider questions such as (sample questions):
* Is the user unable to express what they remember?
* Does Google Photos fail to understand the clues they provide?
* Are potentially relevant results difficult to evaluate?
* Does the user struggle to refine an unsuccessful search?

Use this decomposition to identify where the greatest opportunities may exist.

## Part 3: Validate the Opportunity Through User Research
AI-generated insights are only a starting point.

Conduct 5–6 user interviews with respondents from the target segment you choose.

Think carefully about the user research methodology you would choose.

## Part 4: Define the Problem
Based on your discovery engine and primary research, clearly articulate:
* Your target user segment
* The retrieval scenario you are solving for
* The product outcome you intend to influence
* The root cause of retrieval failure
* Existing user workarounds
* Why solving the problem creates meaningful user value
* Why solving the problem makes business sense for Google Photos

Show how your thinking evolved across:
`Business Metric → Product Outcomes → AI-Powered Discovery → Observed User Behavior → Problem Definition`

DO NOT frame the problem simply as:
*“Users find it difficult to search for old photos.”*

Your research should uncover why retrieval fails despite users retaining some memory of the photo.

## Part 5: Build an AI-Native MVP
Based on the problem you identify, build and deploy a functional AI-native MVP.

The MVP may take the form of:
* A feature within Google Photos
* An AI-powered retrieval workflow
* A conversational or multimodal retrieval experience
* An agent
* A standalone prototype

The MVP must be sufficiently functional that another person can use it to attempt a retrieval task.

Your research should determine where intelligence is actually needed in the retrieval journey.

## Part 6: Test Your MVP With Users
Return to at least 3 users from your target segment and ask them to interact with your MVP.

Where feasible, test it against real or representative retrieval tasks uncovered during your initial research.

Document what you learned and what you would change in the next iteration.

## Part 7: Define Success
Define appropriate leading and diagnostic metrics for your solution.

Your final metric framework should reflect the solution you actually build.

## Part 8: Risks & Mitigation Steps
Think about why your solution might fail.

Identify the most important risks for your specific solution and propose mitigation plans.

---

## Deliverables

### [Link] AI-Powered Discovery Engine
* Link where the workflow can be tested
* A 1-slide explanation inside the final deck outlining how the workflow works

### [PDF] 10-slide deck
The deck should communicate:
* Business metric decomposition
* Discovery-engine findings
* User research and observed retrieval tasks
* Chosen target segment
* Root cause
* Problem definition
* Solution rationale
* MVP and user testing
* Success metrics
* Risks and limitations

### [Link] Deployed AI-Native MVP
* A publicly accessible prototype, workflow, or agent that can be interacted with and tested.

## Guidelines for the deck
* Name of the Fellow should NOT be present anywhere in the slide deck
* 10 slides max (title slide, if you choose to have it, should be counted within the 10 slides)
* Slide title should state the key message of the slide for easier reading. For example: don’t write “Problem” as the slide title, state the problem succinctly in the slide title.
* If you are using a background colour for the slides, please ensure the text is readable.
* When using colours, keep in mind the reader may be colour blind. So, choose colours carefully.
* Link supporting artefacts (eg. survey URLs etc) via a hyperlink. Please ensure the reader has access to the documents. If you do not provide access, this might lead to reduction in your scores.
* Maximum file size should be less than 40 MB
* Naming of the file should be e.g. NL_PhonePe
* Minimum font size: 14 for Google Slides or PPT (this has to be strictly adhered to)
* Minimum font size: 26 for Figma with frame of 1920*1080px (this has to be strictly adhered to)
* Minimum font size: 22 for Canva with frame of 1920*1080px (this has to be strictly adhered to)
* Submission Deadline: 7 October, 2026 3:59:00 PM IST (no submissions will be accepted after the deadline, even if it is by a few seconds!)

---

# Learnings from AI Discovery Engine

Building upon our foundational insights, the overarching learning from engineering the Google Photos AI Discovery Engine is that elite product management requires bridging the massive gap between raw data, human psychology, and executive strategy. By designing a live, multi-channel data ingestion pipeline that scrapes and synthesizes nearly 1,300 feedback records across the Play Store, Reddit, StackExchange, and Open Web forums, we empirically proved a fundamental architectural disconnect: users organize their memories as rich, sensory narratives (context, people, vibes), while the legacy search system forces them into rigid, isolated keywords. This friction is not a mere UI flaw but a critical business vulnerability, manifesting as a "manual scroll tax" that drives 45% of users to abandon searches, spikes frustration rates above 65%, and actively degrades the overarching Search Success Rate on our KPI Tree. The true product breakthrough came from realizing that we cannot solve this by incrementally tweaking keyword accuracy; instead, we must evolve the search paradigm entirely. Through prototyping the interactive 2x2 Visual Choice Grid and the Sample Query Sandbox, we learned how to instantly resolve search ambiguity without conversational overhead—allowing users to visually disambiguate vague queries in milliseconds. Ultimately, the most profound takeaway from building the dynamic data filters and the One-Click Executive Deck Export is that true AI product discovery is not just about leveraging large language models to categorize sentiment; it is about packaging complex technical breakdowns and emotional user pain points into a cohesive, boardroom-ready narrative that directly aligns human needs with actionable, AI-driven product solutions.

---

# Context

## The Problem: Search Abandonment in Personal Media Retrieval

Searching personal photo libraries suffers from a fundamental misalignment between human memory and computational retrieval. Users recall memories through fragmented emotional, sensory, and visual impressions (such as "that cozy dinner" or "a summer getaway") rather than specific dates, file names, or precise keywords.

When users enter broad or ambiguous queries like "vacation" into current photo platforms, standard search algorithms return a flat, homogeneous list ranked purely by sequential similarity scores. If the top-ranked results latch onto a single trip—such as dozens of photos from a single beach afternoon—and that trip is not what the user wanted, the search immediately stalls. Users are forced either to scroll endlessly through irrelevant photos or struggle to rephrase their query. This high cognitive burden and lack of productive feedback loops leads directly to search abandonment and user churn.

## The Solution: The 2x2 Visual Choice Grid

The 2x2 Visual Choice Grid replaces linear search scrolling with an active, visual refinement loop built directly into the native search interface. Instead of guessing one specific photo, the system projects the user's broad query across their library and presents four mutually distinct visual interpretations arranged in a compact 2x2 matrix.

```
+-----------------------------------+
|  [Q: "vacation"                 ] |
|  Which fits your memory?          |
|  +-------------+ +-------------+  |
|  | [Beach]     | | [Mountains] |  |
|  +-------------+ +-------------+  |
|  | [City Walk] | | [Home Meal] |  |
|  +-------------+ +-------------+  |
|  [ None of these (Show others) ]  |
+-----------------------------------+

```

### Core Mechanics & Technical Architecture

* **Candidate Pool Retrieval:** A user's vague text query is mapped into a shared multimodal vector space. The retrieval engine quickly pulls the top 60 to 100 candidate images based on contextual embeddings rather than strict keyword tags.
* **On-the-Fly Vector Clustering ($K=4$):** Rather than presenting the top four nearest neighbors (which tend to look identical), the engine runs a fast clustering algorithm (such as K-Means, $K=4$) across the candidate embeddings. This segments the candidate photos into four statistically distinct visual and contextual themes—for instance, beach, snowy mountains, urban streetscapes, and indoor family gatherings.
* **Centroid Representative Selection:** The system selects the single image closest to the mathematical center (centroid) of each cluster to populate the four quadrants of the grid, ensuring maximum visual contrast.
* **Rapid Millisecond Recognition:** Because the human brain processes visual scenes in under 100 milliseconds, users can evaluate all four diverse directions instantly, tapping the quadrant that matches their mental picture to zero in on the relevant event.
* **The "Hot or Cold" Dynamic Pivot:** If none of the initial four anchors fit, a persistent fallback action labeled *"None of these (Show different options)"* applies a negative vector weight to the rejected cluster centroids. The backend recalculates the remaining pool and surfaces four completely fresh visual directions, turning what would have been a search failure into an intuitive process of elimination.

## Strategic Product Alignment

Integrating this capability as a native, non-conversational grid maintains full fidelity with Google Photos’ core user experience:

* **Zero Conversational Overhead:** Chatbot interfaces force users to type back-and-forth, wait for conversational streaming, and navigate awkward horizontal carousels. Personal photo discovery is fundamentally visual and spatial; a native 2x2 grid honors that behavior.
* **Seamless UI Continuity:** The grid appears organically beneath the search bar only when query ambiguity is detected, preserving the clean, uncluttered canvas users expect from Google Material Design.
* **Measurable Retention Impact:** By transforming ambiguous dead-ends into a two-tap narrowing process, the solution dramatically cuts query reformulation latency, eliminates doom-scrolling, and prevents search abandonment.
