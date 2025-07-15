import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pathlib import Path

class Analyzer:
    def __init__(self, df_comments: pd.DataFrame, output_dir='static/images'):
        self.df = df_comments
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def sentiment_summary(self):
        if 'sentiment' not in self.df.columns:
            return {}
        total = len(self.df)
        counts = self.df['sentiment'].value_counts().to_dict()
        summary = {
            'total': total,
            'positivos': counts.get('positivo', 0),
            'negativos': counts.get('negativo', 0),
            'neutrales': counts.get('neutral', 0),
        }
        return summary

    def generate_wordcloud(self, file_name='wordcloud.png'):
        text_data = ' '.join(self.df['text'].astype(str).tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        file_path = self.output_dir / file_name
        wordcloud.to_file(str(file_path))
        return str(file_path)

    def top_words(self, n=10):
        words = ' '.join(self.df['text'].astype(str)).split()
        freq = Counter(words)
        return freq.most_common(n)