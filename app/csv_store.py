import csv
from pathlib import Path
from datetime import datetime

class CSVStore:
    def __init__(self, influencers_path, comments_path):
        self.inf_path = Path(influencers_path)
        self.com_path = Path(comments_path)
        # Asegurar cabeceras
        if not self.inf_path.exists():
            with open(self.inf_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'name', 'last_scrape'])
        if not self.com_path.exists():
            with open(self.com_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'influencer_id', 'platform', 'date', 'text', 'sentiment', 'score'])

    def append_influencer(self, inf):
        with open(self.inf_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([inf.id, inf.name, inf.last_scrape.isoformat()])

    def append_comment(self, com):
        with open(self.com_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                com.id,
                com.influencer_id,
                com.platform,
                com.date.isoformat(),
                com.text,
                com.sentiment,
                com.score
            ])