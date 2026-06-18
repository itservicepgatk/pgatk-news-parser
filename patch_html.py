import json
import requests
from bs4 import BeautifulSoup
import re

with open('telegram_news.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# Process only the first 200 posts to save time and API calls
for p in posts[:200]:
    if 'content_html' not in p or not p['content_html']:
        url = p['link']
        try:
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text_node = soup.find('div', class_='tgme_widget_message_text')
                if text_node:
                    content_html = text_node.decode_contents()
                    content_html = re.sub(r'href="\?q=', r'href="https://t.me/pgatkk?q=', content_html)
                    p['content_html'] = content_html
                    print(f"Updated {p['id']}")
        except Exception as e:
            print(f"Error on {p['id']}: {e}")

with open('telegram_news.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

with open('telegram_news_latest.json', 'w', encoding='utf-8') as f:
    json.dump(posts[:15], f, ensure_ascii=False, indent=2)
