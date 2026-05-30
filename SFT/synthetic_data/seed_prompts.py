"""
Seed prompts and topic generators for synthetic instruction dataset.

Provides diverse seed topics across multiple categories to generate
instruction-following examples with broad coverage.
"""

# ============================================================================
# Category-specific seed topics
# ============================================================================

CODING_TOPICS = [
    "Implement binary search in Python",
    "Explain Big-O notation with examples",
    "Write a function to detect palindromes",
    "Implement a linked list from scratch",
    "Explain the difference between mutable and immutable types",
    "Write a Python decorator for timing functions",
    "Implement quicksort with explanation",
    "Explain how Python's GIL affects threading",
    "Write a recursive function to traverse a binary tree",
    "Implement a simple cache with LRU eviction",
    "Explain async/await in JavaScript",
    "Write a function to parse JSON safely",
    "Implement a basic REST API with FastAPI",
    "Explain the difference between SQL and NoSQL databases",
    "Write a regex to validate email addresses",
    "Implement a stack using two queues",
    "Explain dependency injection with examples",
    "Write a function to flatten nested arrays",
    "Implement a basic event emitter",
    "Explain the SOLID principles in OOP",
    "Write a Python generator for Fibonacci numbers",
    "Implement merge sort with detailed steps",
    "Explain TypeScript generics with examples",
    "Write a function to deep clone objects",
    "Implement a basic state machine",
    "Explain CORS and how to handle it",
    "Write SQL to find duplicate records",
    "Implement debouncing in JavaScript",
    "Explain memoization with examples",
    "Write a function to validate Sudoku boards",
]

MATH_REASONING_TOPICS = [
    "Solve a quadratic equation step by step",
    "Calculate compound interest with examples",
    "Explain probability with a coin flip example",
    "Solve a system of linear equations",
    "Calculate the area of irregular shapes",
    "Explain calculus derivatives with examples",
    "Solve a geometry problem with triangles",
    "Calculate statistical mean, median, and mode",
    "Explain exponential growth with examples",
    "Solve a permutation problem",
    "Calculate matrix multiplication",
    "Explain logarithms with practical examples",
    "Solve a word problem about distance and time",
    "Calculate standard deviation step by step",
    "Explain Bayes' theorem with examples",
    "Solve a problem involving ratios",
    "Calculate Fibonacci sequence values",
    "Explain prime factorization",
    "Solve a trigonometry problem",
    "Calculate volume of 3D shapes",
    "Explain conditional probability",
    "Solve a problem involving percentages",
    "Calculate the slope of a line",
    "Explain sequences and series",
    "Solve a problem about combinations",
    "Calculate the area under a curve",
    "Explain mathematical induction",
    "Solve a problem involving vectors",
    "Calculate eigenvalues of a matrix",
    "Explain group theory basics",
]

CREATIVE_WRITING_TOPICS = [
    "Write a short story about time travel",
    "Create a poem about the changing seasons",
    "Write dialogue for a tense negotiation scene",
    "Create a character description for a detective",
    "Write a mystery story opening paragraph",
    "Create a haiku about technology",
    "Write a fantasy story about a hidden kingdom",
    "Create a sci-fi scenario about first contact",
    "Write a humorous story about a misunderstanding",
    "Create a poem about resilience",
    "Write a romance scene without cliches",
    "Create a horror story atmosphere",
    "Write a story from an unusual perspective",
    "Create dialogue between historical figures",
    "Write a story that begins with a phone call",
    "Create a poem using extended metaphors",
    "Write a story exploring a moral dilemma",
    "Create a children's story with a lesson",
    "Write a mystery with a twist ending",
    "Create a poem about urban life",
    "Write a story set in a futuristic city",
    "Create dialogue revealing character through speech",
    "Write a story about an unexpected friendship",
    "Create a fairy tale with a modern twist",
    "Write a story about overcoming fear",
    "Create a poem about silence",
    "Write flash fiction in 100 words",
    "Create a character with conflicting motivations",
    "Write a story exploring loneliness",
    "Create a poem about memory",
]

TECHNICAL_EXPLANATION_TOPICS = [
    "Explain how the internet works",
    "Describe how CPUs execute instructions",
    "Explain DNS and how it resolves domains",
    "Describe how SSL/TLS encryption works",
    "Explain how blockchain achieves consensus",
    "Describe how machine learning models learn",
    "Explain how databases handle transactions",
    "Describe how operating systems manage memory",
    "Explain how compilers translate code",
    "Describe how computer networks route packets",
    "Explain how garbage collection works",
    "Describe how Git tracks changes",
    "Explain how containers differ from VMs",
    "Describe how OAuth authentication works",
    "Explain how WebSockets enable real-time communication",
    "Describe how CDNs improve performance",
    "Explain how load balancers distribute traffic",
    "Describe how microservices architecture works",
    "Explain how caching improves performance",
    "Describe how regex engines work",
    "Explain how neural networks process data",
    "Describe how compression algorithms work",
    "Explain how cryptocurrency wallets work",
    "Describe how search engines index the web",
    "Explain how recommendation systems work",
    "Describe how message queues enable async processing",
    "Explain how cookies enable web sessions",
    "Describe how computer graphics rendering works",
    "Explain how databases use indexes",
    "Describe how virtual memory works",
]

PROFESSIONAL_COMMUNICATION_TOPICS = [
    "Write a professional email requesting a meeting",
    "Draft a project status update for stakeholders",
    "Write a polite email declining an invitation",
    "Create a clear bug report",
    "Write a follow-up email after an interview",
    "Draft a project proposal summary",
    "Write a polite email about a missed deadline",
    "Create meeting notes from a discussion",
    "Write a thank-you email after a meeting",
    "Draft a request for clarification",
    "Write a professional resignation letter",
    "Create a code review comment that's constructive",
    "Write an email introducing yourself to a team",
    "Draft a brief executive summary",
    "Write an apology email for an error",
    "Create a one-page project pitch",
    "Write a request for budget approval",
    "Draft a professional LinkedIn message",
    "Write feedback for a colleague's work",
    "Create a clear technical specification",
    "Write a status report for upper management",
    "Draft an out-of-office auto-reply",
    "Write an email asking for help politely",
    "Create a decision memo with recommendations",
    "Write a professional networking message",
    "Draft a customer support response",
    "Write a kickoff email for a new project",
    "Create a risk assessment summary",
    "Write a thank-you note for mentorship",
    "Draft a professional bio for a conference",
]

GENERAL_KNOWLEDGE_TOPICS = [
    "Explain the causes of the French Revolution",
    "Describe the water cycle in detail",
    "Explain photosynthesis in plants",
    "Describe how vaccines work",
    "Explain the theory of evolution",
    "Describe the structure of an atom",
    "Explain why the sky is blue",
    "Describe how human memory works",
    "Explain the history of the printing press",
    "Describe the layers of Earth's atmosphere",
    "Explain economic supply and demand",
    "Describe how ecosystems maintain balance",
    "Explain the importance of biodiversity",
    "Describe how climate change affects oceans",
    "Explain the basics of quantum mechanics",
    "Describe how the human immune system works",
    "Explain different types of government systems",
    "Describe how renewable energy works",
    "Explain the structure of DNA",
    "Describe how earthquakes occur",
    "Explain different psychological theories",
    "Describe how the brain processes information",
    "Explain the history of artificial intelligence",
    "Describe how genetics affects traits",
    "Explain the principles of nutrition",
    "Describe how stars are formed",
    "Explain how vaccines have changed medicine",
    "Describe how the food chain works",
    "Explain the impact of social media on society",
    "Describe how musical instruments produce sound",
]

# ============================================================================
# Category configuration
# ============================================================================

CATEGORIES = {
    "coding": {
        "topics": CODING_TOPICS,
        "weight": 0.25,
        "system_prompt": "You are creating training data for a language model. Generate ONE clear, natural-sounding user instruction or question. Output ONLY the instruction itself - no headers, no markdown, no explanations, no preamble. Make it sound like a real user asking for help.",
        "instruction_template": "Generate a single user question or instruction about: {topic}\n\nOutput format: Just the instruction as a natural sentence(s). No headers like '### Title'. Start directly with the question or task.\n\nExample format: 'Can you write a Python function that...' or 'I'm trying to understand... Could you explain...'",
    },
    "math_reasoning": {
        "topics": MATH_REASONING_TOPICS,
        "weight": 0.20,
        "system_prompt": "You are creating training data. Generate ONE clear, natural math question. Output ONLY the question - no headers, no markdown, no preamble.",
        "instruction_template": "Generate a single user question about: {topic}\n\nOutput format: Just the question as a natural sentence. No headers. Start directly with the question.\n\nExample: 'How do I solve...' or 'What is the difference between...' or 'Can you walk me through...'",
    },
    "creative_writing": {
        "topics": CREATIVE_WRITING_TOPICS,
        "weight": 0.15,
        "system_prompt": "You are creating training data. Generate ONE creative writing request. Output ONLY the request - no headers, no markdown, no preamble.",
        "instruction_template": "Generate a single creative writing request about: {topic}\n\nOutput format: Just the request as a natural sentence. No headers. Start directly with the request.\n\nExample: 'Write a short story about...' or 'Create a poem that...' or 'I need help writing...'",
    },
    "technical_explanation": {
        "topics": TECHNICAL_EXPLANATION_TOPICS,
        "weight": 0.20,
        "system_prompt": "You are creating training data. Generate ONE clear question asking for a technical explanation. Output ONLY the question - no headers, no markdown, no preamble.",
        "instruction_template": "Generate a single user question asking to explain: {topic}\n\nOutput format: Just the question as a natural sentence. No headers. Start directly with the question.\n\nExample: 'Can you explain how... works?' or 'I'd like to understand...'",
    },
    "professional_communication": {
        "topics": PROFESSIONAL_COMMUNICATION_TOPICS,
        "weight": 0.10,
        "system_prompt": "You are creating training data. Generate ONE professional communication request. Output ONLY the request - no headers, no markdown, no preamble.",
        "instruction_template": "Generate a single user request about: {topic}\n\nOutput format: Just the request as a natural sentence. No headers. Start directly with the request.\n\nExample: 'Help me write an email to...' or 'I need to draft a...'",
    },
    "general_knowledge": {
        "topics": GENERAL_KNOWLEDGE_TOPICS,
        "weight": 0.10,
        "system_prompt": "You are creating training data. Generate ONE educational question. Output ONLY the question - no headers, no markdown, no preamble.",
        "instruction_template": "Generate a single user question about: {topic}\n\nOutput format: Just the question as a natural sentence. No headers. Start directly with the question.\n\nExample: 'What causes...' or 'How does... work?' or 'Why is...'",
    },
}


def get_category_distribution(num_examples: int) -> dict:
    """Calculate number of examples per category based on weights."""
    return {
        cat: int(num_examples * config["weight"])
        for cat, config in CATEGORIES.items()
    }


def get_all_topics_with_categories():
    """Return all topics with their category labels."""
    result = []
    for category, config in CATEGORIES.items():
        for topic in config["topics"]:
            result.append({
                "topic": topic,
                "category": category,
                "system_prompt": config["system_prompt"],
                "instruction_template": config["instruction_template"],
            })
    return result
