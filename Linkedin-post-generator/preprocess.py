import json
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw_posts.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed_posts.json")

def clean_text(text):
    """Remove non-UTF-8-safe characters (like broken emojis)."""
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")


def process_posts(raw_file_path, processed_file_path=OUTPUT_PATH):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)        
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

            unified_tags = get_unified_tags(enriched_posts)


        for post in enriched_posts:
            current_tags = post['tags']
            #new_tags = {unified_tags[tag] for tag in current_tags}
            new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
            post['tags'] = list(new_tags)

        os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
        with open(processed_file_path, encoding='utf-8', mode='w') as outfile:
            json.dump(enriched_posts, outfile, indent=4)

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])
    
    unique_tags_list = ', '.join(unique_tags)
    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list.
    Example 1: "Jobseekers", "Job Hunting" can all be merged into a single tag "Job Search"
    Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
    Example 3: "Personal Growth", "Personal Development", "Self Imporvement" can be mapped to "Self Improvement"
    Example 4: "Scam Alert", "Job Scam" etc, can be mapped to Scams

    2. Each tag should follow title case convention. example : "Motivation", "Job Search"
    3. Output should be JSON object, No preamble
    4. Output should have the mapping of original tag and the unified tag.
    For example : {{"Jobseekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}

    Here is the list of tags:
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. unable to parse jobs.")
    
    return res


def extract_metadata(post):
    template = '''
    You are given a linkedin post. you need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly 3 keys : line_count, language and tags.
    3. Tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Tanglish (Tanglish means tamil + english)

    Here is the actual post on which you should perform this task:
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    cleaned_post = clean_text(post)
    response = chain.invoke(input={'post': cleaned_post})

    try:
        json_parser = JsonOutputParser()
        resp = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. unable to parse jobs.")
    return resp

    # return {
    #     'line_count': 10,
    #     'language': 'English',
    #     'tags': ['Mental Health', 'Motivation']

    # }


if __name__ == "__main__":
    process_posts(DATA_PATH, "./data/processed_posts.json")
    
