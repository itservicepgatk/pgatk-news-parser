import json
import os
import re
import shutil
import pymorphy3

# File paths
input_file = 'telegram_news.json'
latest_file = 'telegram_news_latest.json'

website_json = r"d:\Workspace\Web\PGATK Website\public\telegram_news.json"
website_latest = r"d:\Workspace\Web\PGATK Website\public\telegram_news_latest.json"

if not os.path.exists(input_file):
    print(f"Error: {input_file} not found!")
    exit(1)

with open(input_file, 'r', encoding='utf-8') as f:
    posts = json.load(f)

morph = pymorphy3.MorphAnalyzer()

# Define lemma-based categories dict
categories_dict = {
    'Профориентация': ['профориентация', 'абитуриент', 'поступать', 'поступление', 'профессия', 'специальность', 'день открытых дверей', 'приемная комиссия', 'приёмная комиссия', 'приемная кампания', 'приёмная кампания', 'профориентационный'],
    'Профилактика': ['профилактика', 'профилактический', 'безопасность', 'безопасный', 'мчс', 'гаи', 'наркотик', 'наркотический', 'наркобизнес', 'наркомания', 'преступление', 'преступник', 'преступность', 'кибербезопасность', 'киберпреступность', 'мошенник', 'мошенничество', 'мошеннический', 'дорожный', 'пожарный', 'вейп', 'курение', 'курить', 'алкоголь', 'алкогольный', 'правонарушение'],
    'Достижения': ['победитель', 'победить', 'победа', 'наградить', 'награждение', 'награда', 'диплом', 'чемпион', 'занять', 'конкурс', 'олимпиада', 'успешный', 'достижение', 'гордиться', 'лауреат', 'призер', 'призёр', 'первое место', 'второе место', 'третье место', '1 место', '2 место', '3 место', 'грамота'],
    'Год белорусской женщины': ['женщина', 'девушка', r'\bматери\b', r'\bмать\b'],
    'Жизнь колледжа': ['праздник', 'праздничный', 'мероприятие', 'акция', 'выставка', 'колледж', 'экскурсия', 'соревнование', 'концерт', 'конференция', 'преподаватель', 'встреча', 'встретиться', 'студент', 'учащийся', 'директор', 'администрация', 'выпускной', 'выпускник', 'творчество', 'творческий', 'челлендж', 'библиотека', 'субботник', 'семинар', 'педагог', 'педагогический'],
    'Общежитие': ['общежитие', 'заселение', 'заселиться'],
    'БРСМ': ['брсм', 'молодежь', 'молодёж', 'молодежный', 'молодёжный', 'волонтер', 'волонтёр', 'волонтерский', 'волонтёрский', 'активист', 'студотряд', 'мооп'],
    'ВПВ': ['впв', 'военный', 'военно-патриотический', 'патриотический', 'патриот', 'патриотизм', 'исторический', 'история', 'память', 'памятник', 'памятный', 'вов', 'отечественный', 'геноцид', 'хатынь', 'пограничный', 'пограничник', 'граница', 'кинолог', 'зарница', 'мемориал'],
    'Спорт': ['спорт', 'спортивный', 'соревнование', 'турнир', 'чемпионат', 'матч', 'атлет', 'физкультура', 'физкультурный', 'физкультминутка', 'эстафета', 'волейбол', 'баскетбол', 'футбол', 'теннис', 'легкоатлетический', 'легкоатлет', 'кросс', 'лыжи', 'спартакиада'],
    'Официально': ['депутат', 'собрание', 'министр', 'заседание', 'власть', 'государство', 'государственный', 'республика', 'республиканский', 'закон', 'парламент', 'исполком', 'горисполком', 'облисполком', 'конституция', 'информирование', 'выборы']
}

def get_lemmas(text):
    words = re.findall(r'\b[а-яёa-z0-9-]+\b', text.lower())
    return [morph.parse(w)[0].normal_form for w in words]

def count_phrase_occurrences(phrase, doc_lemmas):
    is_regex = any(char in phrase for char in ['\\', '?', '<', '!', '(', '[', '^', '$'])
    if is_regex:
        lemma_str = ' '.join(doc_lemmas)
        return len(re.findall(phrase, lemma_str))
        
    phrase_lemmas = get_lemmas(phrase)
    if not phrase_lemmas:
        return 0
    
    count = 0
    n = len(phrase_lemmas)
    for i in range(len(doc_lemmas) - n + 1):
        if doc_lemmas[i:i+n] == phrase_lemmas:
            count += 1
    return count

def classify(title, summary):
    category_scores = {cat: 0 for cat in categories_dict}
    title_lemmas = get_lemmas(title)
    body_lemmas = get_lemmas(summary)
    
    for cat, keywords in categories_dict.items():
        for kw in keywords:
            title_matches = count_phrase_occurrences(kw, title_lemmas)
            body_matches = count_phrase_occurrences(kw, body_lemmas)
            
            category_scores[cat] += (title_matches * 3) + body_matches
            
    post_categories = []
    if any(score > 0 for score in category_scores.values()):
        sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        best_cat, best_score = sorted_cats[0]
        if best_score > 0:
            post_categories.append(best_cat)
        
        if len(sorted_cats) > 1:
            second_cat, second_score = sorted_cats[1]
            if second_score >= 3 and second_score >= best_score * 0.4:
                post_categories.append(second_cat)
                
    if not post_categories:
        post_categories = ['Новости']
    return post_categories

print(f"Loaded {len(posts)} posts for morphological migration...")

# Migrate
change_count = 0
for i, p in enumerate(posts):
    if i % 500 == 0 and i > 0:
        print(f"Processed {i} posts...")
    old_cats = p.get('category', ['Новости'])
    new_cats = classify(p['title'], p['summary'])
    if old_cats != new_cats:
        p['category'] = new_cats
        change_count += 1

print(f"Recategorized {change_count} posts using lemmatization.")

# Save main file
with open(input_file, 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
print(f"Saved changes to {input_file}.")

# Save latest 15 file
latest_posts = posts[:15]
with open(latest_file, 'w', encoding='utf-8') as f:
    json.dump(latest_posts, f, ensure_ascii=False, indent=2)
print(f"Saved changes to {latest_file}.")

# Copy to website directory
try:
    shutil.copy2(input_file, website_json)
    shutil.copy2(latest_file, website_latest)
    print(f"Successfully copied morphologically updated JSON files to website public dir.")
except Exception as e:
    print(f"Error copying JSON files to website: {e}")
