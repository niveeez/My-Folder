import json
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FILE = os.path.join(BASE_DIR, "data", "processed_posts.json")

class FewShotPosts:
    def __init__(self, file_path=PROCESSED_FILE):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)
        
    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            df = pd.json_normalize(posts)
            self.df = df
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = set(list(all_tags))
            print(self.df)
            print(all_tags)
            print(list(self.unique_tags))

    
    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif  5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"
        
    def get_tags(self):
        return self.unique_tags
    
    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length']== length) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return df_filtered.to_dict(orient="records")

if __name__ == "__main__":
    fs = FewShotPosts()
    post = fs.get_filtered_posts("Short", "English", "Job Search")
    print(post)
    pass



