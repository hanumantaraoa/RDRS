import os
import secrets
import string

# Combine letters, digits, and punctuation
alphabet = string.ascii_letters + string.digits + string.punctuation

dir_path = path("rdrs/data/sandbox")

# Generate a text string of 1024 random characters
random_text = ''.join(secrets.choice(alphabet) for _ in range(1024))

# Write using standard text mode ('w')
with open("rdrs/data/sandbox/random_text.txt", "w", encoding="utf-8") as file:
    file.write(random_text)
