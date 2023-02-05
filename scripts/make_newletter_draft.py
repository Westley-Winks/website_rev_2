import os
import requests
import frontmatter

from dotenv import load_dotenv
load_dotenv(".env")

BD_TOKEN = os.environ["BD_TOKEN"]
# POST_PATH = os.environ["INPUT_POST_PATH"]
POST_PATH = input('What is the folder name?')
# POST_PATH = "2022-01-19"

def make_draft(post_path):

    headers = {
        "Authorization": f"Token {BD_TOKEN}"
    }

    payload = {}

    with open(f"content/peace-corps/{post_path}/index.md") as f:
        body = frontmatter.loads(f.read())

    # get title from front matter
    subject = body["title"]

    # get slug from front matter
    slug = body["slug"]

    # get description from front matter
    description = body["description"]

    # remove front matter
    body = body.content

    # add View In Browser link
    header_text = f"[View in Browser](https://westleywinks.com/peace-corps/{slug}/)\n\n"

    # create payload
    payload["subject"] = subject
    payload["body"] = header_text + f"# {subject}\n\n" + f"*{description}*\n\n" + body
    payload["status"] = "draft"

    r = requests.post("https://api.buttondown.email/v1/emails", headers=headers, json=payload)

    return r

response = make_draft(POST_PATH)

if response.status_code != 201:
    print("Problem with api\n", response.status_code, response.text)
else:
    print("Draft Posted!")