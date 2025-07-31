from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2")

def run_trip_planner(destination, days, interests):
    task1 = f"""
You are a professional travel planner.

Plan a rich and immersive {days}-day trip to {destination} for someone who enjoys {interests}.
Your output should be creative and detailed. Include 1–2 general highlights per day, using warm and inspiring language.
Avoid times or specific locations — just themes for each day.

Make it at least 6–8 lines long.
"""
    task1_result = llm.invoke(task1)

    task2 = f"""
Expand this high-level plan into a full itinerary with real places, famous restaurants, travel suggestions, and hidden gems in {destination}:

{task1_result}

⚠️ STRICT INSTRUCTIONS:
- ONLY include real, well-known places, neighborhoods, or restaurants in {destination}.
- If unsure, use general terms like “local café” or “popular market”.
- For each activity block, include realistic **time ranges** in the format:
  - Morning (9:00 AM – 11:30 AM)
  - Lunch (12:00 PM – 1:30 PM)
  - Afternoon (2:00 PM – 5:00 PM)
  - Evening (6:00 PM – 8:00 PM)

Mention:
- Specific attractions
- Best local restaurants
- Travel modes (walk/train/etc.)
- Cultural tips or etiquette

Make it engaging and vivid. Length: 10–12+ lines.
"""
    task2_result = llm.invoke(task2)

    task3 = f"""
Optimize this itinerary so it’s realistic, well-paced, and delightful for a {days}-day visit to {destination}:

{task2_result}

✅ Ensure:
- NO overlapping or conflicting times
- Smooth transitions between activities with realistic timing
- Balanced mix of experiences: food, culture, nature
- Use time blocks like: "Morning (9:00 AM – 11:00 AM): Visit XYZ"

🚫 Do NOT invent unknown locations. Be specific only when confident.
✅ Add closing remarks and cultural or travel tips at the end.

Make it a polished version a traveler could follow. Length: 12+ lines.
"""
    task3_result = llm.invoke(task3)

    return task3_result
