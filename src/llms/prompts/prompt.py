system_prompt = (
    "Act as an expert emotion classifier for multiple languages."
)

extract_mood_prompt_template = (
    """
	Act as an expert emotion classifier. Analyze the user's input below and follow these steps:
    1. **Mood Identification**: Classify the user's primary mood from this list:
       [Happy, Sad, Anxious, Angry, Calm, Excited, Stressed, Lonely, Neutral].
       If none fit, choose the closest option or add a new mood (e.g., "Bored").
    2. **Confidence Score**: Rate your confidence in the classification (1-10, 10=highest).
    3. **Reasoning**: Explain key phrases, tone, or context that led to your conclusion.
       Highlight metaphors, emojis, or linguistic cues (e.g., sarcasm).
    
    **User Input**: "{user_answering}"
    
    **Output Format**:
    - Mood: [Detected Mood]
    - Confidence: [Score]/10
    - Reasoning: [1-2 sentences]
    
    **Examples**:
    1.
    User Input: "I can’t handle this anymore. Everything is going wrong."
    Output:
    - Mood: Anxious
    - Confidence: 9
    - Reasoning: Phrases like "can’t handle this" and "everything is going wrong" indicate overwhelm and anxiety.
    
    2.
    User Input: "Just got promoted! 🎉 Time to celebrate!"
    Output:
    - Mood: Excited
    - Confidence: 10
    - Reasoning: The celebratory emoji and words like "promoted" and "celebrate" reflect excitement.
    
    Now analyze and return the information in a structured format that matches the following Python Pydantic Model:
    {format_instructions}
    """
)

suggest_keywords_prompt_template = (
    """
	Act as a mental health keyword analyst. Analyze the conversation below and suggest relevant keywords to categorize the interaction. Follow these rules:

    1. **Keyword Types** (include at least 1 from each category):
       - **Mood**: Primary emotions (e.g., "anxiety", "joy", "loneliness").
       - **Theme**: Broader context (e.g., "work stress", "relationship issues", "self-care").
       - **Topic**: Specific subjects discussed (e.g., "sleep problems", "meditation", "career goals").
       - **Activity**: Actions or solutions mentioned (e.g., "exercise", "journaling", "therapy").
    
    2. **Guidelines**:
       - Extract keywords directly from the text or infer them from context.
       - Prioritize specificity (e.g., "social anxiety" instead of "anxiety").
       - Avoid generic terms (e.g., "feel", "help").
       - Limit to 5-8 keywords total.
    
    **Conversation**:
    {conversation}
    
    **Output Format**:
    - Mood: [keyword1], [keyword2]
    - Theme: [keyword3], [keyword4]
    - Topic: [keyword5], [keyword6]
    - Activity: [keyword7], [keyword8]
    
    **Examples**:
    1.
    **Conversation**:
    User: "I can’t sleep because I’m overwhelmed with deadlines."
    Assistant: "Let’s try a breathing exercise. Would you like a guided session?"
    
    **Output**:
    - Mood: Overwhelm, Anxiety
    - Theme: Work Pressure, Time Management
    - Topic: Insomnia, Deadlines
    - Activity: Breathing Exercises, Guided Meditation
    
    2.
    **Conversation**:
    User: "I’m lonely since moving cities. Any tips to meet people?"
    Assistant: "Volunteering or joining clubs can help. Want local event suggestions?"
    
    **Output**:
    - Mood: Loneliness, Isolation
    - Theme: Relocation, Social Connection
    - Topic: New Environment, Community Building
    - Activity: Volunteering, Social Events
    Now analyze and return the information in a structured format that matches the following Python Pydantic Model:
    {format_instructions}
    """
)
