import praw
import time
from textblob import TextBlob
import pandas as pd
import re

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(client_id="YOUR_CLIENT_ID",
                     client_secret="YOUR_CLIENT_SECRET",
                     user_agent="YOUR_USER_AGENT")

# List of academic disciplines
academic_disciplines = [
    ("Business School", "Accounting", "acct"),
    ("Business School", "Economics", "econ"),
    ("Business School", "Finance", "finance"),
    ("Business School", "Property", "property"),
    ("Business School", "Global Studies", "global study"),
    ("Faculty of Education and Social Work", "Early Childhood Studies", "ecs"),
    ("Faculty of Education and Social Work", "Education", "edu"),
    ("Faculty of Education and Social Work", "Social Work", "sw"),
    ("Faculty of Education and Social Work", "Sport, Health and Physical Education", "shpe"),
    ("Faculty of Engineering", "Biomedical Engineering", "bme"),
    ("Faculty of Engineering", "Chemical and Materials Engineering", "cme"),
    ("Faculty of Engineering", "Civil Engineering", "civil"),
    ("Faculty of Engineering", "Computer Systems Engineering", "cse"),
    ("Faculty of Engineering", "Electrical and Electronic Engineering", "eee"),
    ("Faculty of Engineering", "General Engineering", "ge"),
    ("Faculty of Engineering", "Mechanical Engineering", "mechanical"),
    ("Faculty of Engineering", "Mechatronics Engineering", "mech"),
    ("Faculty of Engineering", "Software Engineering", "se"),
    ("Faculty of Engineering", "Structural Engineering", "struct"),
    ("Faculty of Creative Arts and Industries", "Fine Arts", "fine art"),
    ("Faculty of Creative Arts and Industries", "Architectural Studies", "architecture"),
    ("Faculty of Creative Arts and Industries", "Design", "design"),
    ("Faculty of Creative Arts and Industries", "Dance Studies", "dance"),
    ("Faculty of Creative Arts and Industries", "Urban Planning", "urban"),
    ("Faculty of Creative Arts and Industries", "Music", "music"),
    ("Faculty of Medical and Health Sciences", "Health Sciences", "health science"),
    ("Faculty of Medical and Health Sciences", "Biomedical Science", "biomed"),
    ("Faculty of Medical and Health Sciences", "Medicine", "med"),
    ("Faculty of Medical and Health Sciences", "Surgery", "surg"),
    ("Faculty of Medical and Health Sciences", "Nursing", "nurs"),
    ("Faculty of Medical and Health Sciences", "Optometry", "opt"),
    ("Faculty of Medical and Health Sciences", "Pharmacy", "pharm"),
    ("Faculty of Science", "Biology", "bio"),
    ("Faculty of Science", "Life Science", "life science"),
    ("Faculty of Science", "Chemistry", "chem"),
    ("Faculty of Science", "Physics", "phy"),
    ("Faculty of Science", "Geography", "geog"),
    ("Faculty of Science", "Earth Science", "earth science"),
    ("Faculty of Science", "Environmental Science", "environmental"),
    ("Faculty of Art", "Human Science", "human"),
    ("Faculty of Art", "Social Science", "sosci"),
    ("Faculty of Science", "Computational Biology", "compbio"),
    ("Faculty of Science", "Computer Science", "compsci"),
    ("Faculty of Science", "Data Science", "data"),
    ("Faculty of Science", "Information and Technology", "information and technology"),
    ("Faculty of Science", "Mathematics", "math"),
    ("Faculty of Science", "Statistics", "stat")
]

# Function to use praw and manipulate the result
def search_reddit_mentions(subreddit_name, total_limit=1000):
    posts = []
    seen_ids = set()
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.new(limit=total_limit):  # Get new posts up to total_limit
            if submission.id in seen_ids:
                continue
            
            seen_ids.add(submission.id) # Take out potential repeated posts
            
            combined_text = submission.title + " " + submission.selftext # Combine topic and text
            clean_text = re.sub(r'[^\w\s]', '', combined_text).lower() # Take out punctuation and make all in lower case
            sentiment_score = TextBlob(clean_text).sentiment.polarity # Sentimental score

            discipline_faculty = [ # Compare to match faculty or discipline
                (faculty, discipline) 
                for faculty, discipline, abbrev in academic_disciplines 
                if discipline.lower() in clean_text or abbrev.lower() in clean_text
            ]
            
            # Include general category
            discipline_faculty.append(("General", "General"))

            posts.append({
                'clean_text': clean_text,
                'sentiment_score': sentiment_score,
                'discipline_faculty': discipline_faculty
            })

        time.sleep(1)  # Sleep to avoid hitting rate limits
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)  # Wait a minute before retrying

    return posts

# Main execution
query = "universityofauckland"
total_post_limit = 1000000

posts = search_reddit_mentions(query, total_limit=total_post_limit)

# Convert to dataframe and save as CSV
df = pd.DataFrame(posts)
csv_filename = f"sentiment_analysis.csv"
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
print(f"Total unique posts collected: {len(posts)}")
