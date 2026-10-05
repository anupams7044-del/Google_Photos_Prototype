class QueryAnalyzer:
    def __init__(self):
        # A simple list of specific keywords/patterns for MVP
        # In a real production system, this would be an NLP intent classification model
        self.specific_markers = ['.jpg', '.png', 'img_', 'dsc_', 'screenshot', '2020', '2021', '2022', '2023', '2024']
        
    def analyze_intent(self, query: str):
        """
        Classifies if a query is highly specific (returns 'specific') 
        or relies on vague memory/vibes (returns 'vague').
        """
        lower_query = query.lower()
        
        # Check for specific file names or dates
        for marker in self.specific_markers:
            if marker in lower_query:
                return 'specific'
                
        # If it's short, descriptive, or emotional, treat as a vague memory search
        return 'vague'
