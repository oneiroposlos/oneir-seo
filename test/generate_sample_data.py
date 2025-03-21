import random

import numpy as np
import pandas as pd
from faker import Faker

from src import config as cf
from src.utils import save

# Initialize Faker for generating random data
fake = Faker()

num_mood_ids = 58  # Number of unique mood IDs

dates = pd.date_range(start="2024-12-01", end="2024-12-23", freq="D")
for date in dates:
    num_samples = random.randint(5000, 10000)  # Random number of samples between 5000 and 10000
    # Generate random sample data
    data = {
        "user_id": np.random.randint(1000, 2000, size=num_samples),
        "timestamp": [fake.date_time_this_year() for _ in range(num_samples)],  # Random timestamps from this year
        "location": [fake.city() for _ in range(num_samples)],  # Random city names as locations
        "event_type": [fake.word(ext_word_list=["view", "like", "apply", "comment", "save", "report"]) for _ in
                       range(num_samples)],
        "mood_id": np.random.randint(1, num_mood_ids, size=num_samples)  # Random mood_id between 1 and 10
    }

    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Optionally write the data to a CSV file
    output_file = f"{cf.DATA_DIR}/users/raw/{date.strftime('%Y-%m-%d')}.gz"
    save(df, output_file)
    print(f"{num_samples} samples has been generated and saved to {output_file}")

# Define mood categories
categories = sorted([
    "Relaxation",
    "Focus",
    "Motivation",
    "Playfulness",
    "Euphoria",
    "Calm Confidence",
    "Sensory Enhancement",
    "Inspiration"
])

# Generate mood information
mood_data = []
for mood_id in range(1, num_mood_ids + 1):
    mood_name = fake.sentence()  # Generate a simple mood name based on the ID
    scores = [round(random.uniform(0.0, 1.0), 5) for _ in range(len(categories))]  # Random scores between 0 and 1

    mood_data.append({
        "id": mood_id,
        "mood_name": mood_name,
        "mood_description": fake.text(),  # Generate a random mood description
        "mode_config": {
            "data": [{
                "mode": {
                    "curve": {},
                    "quick": {},

                },
                "type": fake.word(ext_word_list=["PCC", "FLAVOR"]),
                "position": i,
                "currentMode": fake.word(ext_word_list=["QUICK", "CURVE"]),

            } for i in range(3)]
        },
        "categories": categories,
        "scores": scores
    })

# Convert to a DataFrame for pretty visualization
moods_df = pd.DataFrame(mood_data)
output_file = f"{cf.DATA_DIR}/moods/mood_information.gz"
save(moods_df, output_file)

print(f"Mood information has been generated and saved to {output_file}")

# For display purposes
print(moods_df)
