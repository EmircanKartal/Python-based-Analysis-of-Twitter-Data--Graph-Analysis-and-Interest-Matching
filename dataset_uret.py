import json
from faker import Faker
import random

fake = Faker()

def generate_user(unique_usernames, common_usernames):
    username = fake.user_name()
    name = fake.name()
    followers_count = random.randint(30, 200)
    following_count = random.randint(30, 200)

    # Ensure common usernames are present in both followers and followings for some users
    if random.choice([True, False]):
        user_followers = random.sample(common_usernames, min(random.randint(10, 30), len(common_usernames)))
        user_followings = random.sample(common_usernames, min(random.randint(10, 30), len(common_usernames)))
    else:
        user_followers = []
        user_followings = []

    # Generate some unique usernames
    unique_followers = random.sample(unique_usernames, min(followers_count - len(user_followers), len(unique_usernames)))
    unique_followings = random.sample(unique_usernames, min(following_count - len(user_followings), len(unique_usernames)))

    user_followers.extend(unique_followers)
    user_followings.extend(unique_followings)

    return {
        "username": username,
        "name": name,
        "followers_count": followers_count,
        "following_count": following_count,
        "language": fake.language_code(),
        "region": fake.country_code(),
        "tweets": [fake.sentence() for _ in range(random.randint(10, 50))],
        "followers": user_followers,
        "following": user_followings
    }

def generate_dataset(num_users):
    # Generate common usernames
    common_usernames = [fake.user_name() for _ in range(50)]  # Adjust the number as needed

    # Generate unique usernames
    unique_usernames = set()
    while len(unique_usernames) < num_users:
        unique_usernames.add(fake.user_name())

    dataset = []

    for _ in range(num_users):
        user_data = generate_user(unique_usernames, common_usernames)
        dataset.append(user_data)

    return dataset

if __name__ == "__main__":
    num_users = 50

    dataset = generate_dataset(num_users)

    # Convert the dataset to JSON format
    json_dataset = json.dumps(dataset, indent=4)

    # Save the dataset to a file
    with open("Similarity_Dataset.json", "w") as file:
        file.write(json_dataset)
