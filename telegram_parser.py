import requests
from bs4 import BeautifulSoup
import json
import os
import re
import shutil
from datetime import datetime
import pymorphy3
import time

def safe_requests_get(url, stream=False, max_retries=3, backoff_factor=2, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for attempt in range(max_retries):
        try:
            return requests.get(url, headers=headers, stream=stream, timeout=timeout)
        except (requests.RequestException, Exception) as e:
            if attempt == max_retries - 1:
                print(f"Failed to fetch URL {url} after {max_retries} attempts. Error: {e}")
                raise e
            sleep_time = backoff_factor ** (attempt + 1)
            print(f"Request failed ({e}). Retrying in {sleep_time}s (attempt {attempt + 1}/{max_retries})...")
            time.sleep(sleep_time)


morph = pymorphy3.MorphAnalyzer()

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

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

TARGET_IMG_DIR = "images/news"
URL_PREFIX = "https://raw.githubusercontent.com/itservicepgatk/pgatk-news-parser/main/images/news/"

if not os.path.exists(TARGET_IMG_DIR):
    os.makedirs(TARGET_IMG_DIR, exist_ok=True)

def smart_crop_16_9(image_path, target_webp_path):
    if not HAS_CV2:
        return False
    
    img = cv2.imread(image_path)
    if img is None:
        return False
        
    h, w = img.shape[:2]
    
    target_ratio = 16.0 / 9.0
    current_ratio = w / h
    
    cropped = img
    
    if abs(current_ratio - target_ratio) > 0.01:
        # Load cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if current_ratio < target_ratio:
            # Image is taller than 16:9, crop vertically
            target_w = w
            target_h = int(w / target_ratio)
            
            if len(faces) > 0:
                min_y = min([y for x,y,fw,fh in faces])
                max_y = max([y+fh for x,y,fw,fh in faces])
                faces_center_y = (min_y + max_y) // 2
            else:
                faces_center_y = h // 2
                
            y1 = faces_center_y - target_h // 2
            y2 = y1 + target_h
            
            if y1 < 0:
                y1 = 0
                y2 = target_h
            elif y2 > h:
                y2 = h
                y1 = h - target_h
                
            cropped = img[y1:y2, 0:target_w]
            
        else:
            # Image is wider than 16:9, crop horizontally
            target_h = h
            target_w = int(h * target_ratio)
            
            if len(faces) > 0:
                min_x = min([x for x,y,fw,fh in faces])
                max_x = max([x+fw for x,y,fw,fh in faces])
                faces_center_x = (min_x + max_x) // 2
            else:
                faces_center_x = w // 2
                
            x1 = faces_center_x - target_w // 2
            x2 = x1 + target_w
            
            if x1 < 0:
                x1 = 0
                x2 = target_w
            elif x2 > w:
                x2 = w
                x1 = w - target_w
                
            cropped = img[0:target_h, x1:x2]
            
    cv2.imwrite(target_webp_path, cropped, [cv2.IMWRITE_WEBP_QUALITY, 85])
    return True

def download_image(url, target_webp_path):
    if not os.path.exists(target_webp_path):
        try:
            temp_jpg = target_webp_path.replace('.webp', '_temp.jpg')
            r = safe_requests_get(url, stream=True)
            if r.status_code == 200:
                with open(temp_jpg, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                
                # Apply smart crop and convert to webp
                success = smart_crop_16_9(temp_jpg, target_webp_path)
                
                if os.path.exists(temp_jpg):
                    os.remove(temp_jpg)
                    
                return success
        except Exception as e:
            print(f"Failed to download image {url}: {e}")
    return False

def is_valid_post(clean_text, has_media=False):
    text_lower = clean_text.lower()
    
    # 1. Пропускаем расписания и замены
    skip_keywords = ['расписание', 'замен', 'замена', 'замены']
    if any(keyword in text_lower for keyword in skip_keywords):
        return False
        
    # 2. Пропускаем посты без описания (короткие, меньше 50 символов)
    # Если пост состоит из 3-4 слов, это скорее всего просто фото без текста, НО если есть медиа, оставляем!
    if not has_media and len(clean_text.strip()) < 50:
        return False
        
    return True

def parse_telegram_channel(url, existing_ids, max_pages=100):
    current_url = url
    all_posts = []
    reached_old_dates = False

    for page_num in range(max_pages):
        print(f"Fetching page {page_num + 1}...")
        try:
            response = safe_requests_get(current_url, timeout=15)
        except Exception:
            break
        if response.status_code != 200:
            print(f"Failed to fetch {current_url}: Status {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        messages = soup.find_all('div', class_='tgme_widget_message_wrap')
        page_posts = []

        # Telegram отдаёт посты сверху вниз (от старых к новым на странице)
        # Мы переворачиваем, чтобы обрабатывать от новых к старым
        for msg in reversed(messages):
            # Дата и ссылка
            date_node = msg.find('a', class_='tgme_widget_message_date')
            link = 'https://t.me/pgatkk'
            date_str = datetime.now().strftime('%d.%m.%Y')
            dt = datetime.now()
            
            if date_node:
                if date_node.has_attr('href'):
                    link = date_node['href']
                time_node = date_node.find('time')
                if time_node and time_node.has_attr('datetime'):
                    try:
                        dt = datetime.fromisoformat(time_node['datetime'].replace('Z', '+00:00'))
                        date_str = dt.strftime('%d.%m.%Y')
                    except Exception:
                        pass

            # Больше не ограничиваем по году, так как мы хотим полную историю!

            # ID поста
            id_match = re.search(r'/(\d+)$', link)
            post_id = id_match.group(1) if id_match else str(datetime.now().timestamp())

            # Поскольку теперь мы скачиваем картинки, ссылки больше не протухают.
            # Поэтому мы останавливаем парсинг сразу, как только дошли до уже спарсенного поста,
            # чтобы не перекачивать все посты заново и не вешать GitHub Actions.
            if str(post_id) in existing_ids:
                reached_old_dates = True
                break

            text_node = msg.find('div', class_='tgme_widget_message_text')
            if not text_node:
                continue

            # Очищаем текст
            raw_html = str(text_node)
            clean_text = re.sub(r'<br\s*/?>', '\n', raw_html, flags=re.IGNORECASE)
            clean_text = re.sub(r'<[^>]*>', '', clean_text).strip()

            if not clean_text:
                continue

            # Сохраняем безопасный HTML для отображения ссылок и эмодзи
            content_html = text_node.decode_contents()
            content_html = re.sub(r'href="\?q=', r'href="https://t.me/pgatkk?q=', content_html)



            # Фото
            photo_nodes = msg.find_all('a', class_='tgme_widget_message_photo_wrap')
            images = []
            img_idx = 0
            for node in photo_nodes:
                if node.has_attr('style'):
                    style = node['style']
                    match = re.search(r"background-image:url\('([^']+)'\)", style)
                    if match:
                        img_url = match.group(1)
                        local_filename = os.path.join(TARGET_IMG_DIR, f"{post_id}_{img_idx}.webp")
                        local_url = f"{URL_PREFIX}{post_id}_{img_idx}.webp"
                        
                        download_image(img_url, local_filename)
                        images.append(local_url)
                        img_idx += 1
            
            # Если фоток нет, пытаемся найти превью видео (чтобы всегда была картинка)
            if not images:
                video_nodes = msg.find_all('i', class_='tgme_widget_message_video_thumb')
                for node in video_nodes:
                    if node.has_attr('style'):
                        style = node['style']
                        match = re.search(r"background-image:url\('([^']+)'\)", style)
                        if match:
                            img_url = match.group(1)
                            local_filename = os.path.join(TARGET_IMG_DIR, f"{post_id}_{img_idx}.webp")
                            local_url = f"{URL_PREFIX}{post_id}_{img_idx}.webp"
                            
                            download_image(img_url, local_filename)
                            images.append(local_url)
                            img_idx += 1
                            
            image_url = images[0] if images else None
                    
            # Check for video
            has_video = bool(msg.find('video')) or bool(msg.find('a', class_='tgme_widget_message_video_player')) or bool(msg.find('i', class_='tgme_widget_message_video_thumb'))

            has_media = bool(image_url) or has_video
            
            # Проверяем пост на валидность
            if not is_valid_post(clean_text, has_media=has_media):
                continue

            # Заголовок и summary
            title = 'Новости колледжа'
            summary = clean_text

            first_line_break = clean_text.find('\n')

            if first_line_break > 0:
                title = clean_text[:first_line_break].strip()
                summary = clean_text[first_line_break:].strip()
                if not summary:
                    summary = clean_text
            else:
                title = clean_text
                summary = clean_text
                    
            # Определение категорий: умный скоринг на основе лемм
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
            
            category_scores = {cat: 0 for cat in categories_dict}
            title_lemmas = get_lemmas(title)
            body_lemmas = get_lemmas(clean_text)
            
            for cat, keywords in categories_dict.items():
                for kw in keywords:
                    title_matches = count_phrase_occurrences(kw, title_lemmas)
                    body_matches = count_phrase_occurrences(kw, body_lemmas)
                    
                    # Слова в заголовке дают 3 балла, в теле - 1 балл
                    category_scores[cat] += (title_matches * 3) + body_matches
                    
            post_categories = []
            if any(score > 0 for score in category_scores.values()):
                # Сортируем по убыванию очков
                sorted_cats = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
                
                best_cat, best_score = sorted_cats[0]
                if best_score > 0:
                    post_categories.append(best_cat)
                
                # Добавляем вторую категорию, только если у нее достаточно много баллов (>= 3)
                if len(sorted_cats) > 1:
                    second_cat, second_score = sorted_cats[1]
                    if second_score >= 3 and second_score >= best_score * 0.4:
                        post_categories.append(second_cat)
                        
            if not post_categories:
                post_categories = ['Новости']

            page_posts.append({
                'id': post_id,
                'title': title,
                'summary': summary,
                'content_html': content_html,
                'imageUrl': image_url,
                'date': date_str,
                'category': post_categories,
                'link': link,
                'hasVideo': has_video,
                'images': images
            })

        all_posts.extend(page_posts)

        if reached_old_dates:
            break

        more_link = soup.find('a', class_='tme_messages_more')
        if more_link and more_link.has_attr('href'):
            next_path = more_link['href']
            current_url = f"https://t.me{next_path}"
        else:
            break

    return all_posts

if __name__ == '__main__':
    channel_url = 'https://t.me/s/pgatkk'
    output_file = 'telegram_news.json'
    
    # Загружаем существующие новости, чтобы просто дополнять их
    existing_posts = []
    existing_ids = set()
    
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_posts = json.load(f)
                existing_ids = {str(p['id']) for p in existing_posts}
                print(f"Loaded {len(existing_posts)} existing posts.")
        except Exception as e:
            print(f"Error loading existing JSON: {e}")

    print(f"Fetching new posts from {channel_url}...")
    # Парсим новые посты (при регулярном запуске хватит и 100 страниц, так как мы останавливаемся при нахождении старого ID)
    new_posts = parse_telegram_channel(channel_url, existing_ids, max_pages=100)
    
    print(f"Fetched {len(new_posts)} valid new posts.")

    # Объединяем. Новые посты добавляем в начало.
    # Так как new_posts собирались от свежих к старым, они уже в правильном порядке.
    # Но мы должны исключить дубликаты.
    merged_dict = {}
    
    # Сначала кладем старые посты
    for p in existing_posts:
        merged_dict[str(p['id'])] = p
        
    # Затем перезаписываем/добавляем новые
    for p in new_posts:
        merged_dict[str(p['id'])] = p
        
    # Превращаем словарь обратно в список и сортируем по ID (самые новые сверху)
    final_posts = list(merged_dict.values())
    try:
        final_posts.sort(key=lambda x: int(x['id']), reverse=True)
    except:
        pass

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_posts, f, ensure_ascii=False, indent=2)
    
    # Сохраняем последние 15 новостей в отдельный легкий файл
    latest_file = 'telegram_news_latest.json'
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(final_posts[:15], f, ensure_ascii=False, indent=2)
    
    # Также копируем файл в папку сайта для надежности
    website_json = r"d:\Workspace\Web\PGATK Website\public\telegram_news.json"
    website_latest = r"d:\Workspace\Web\PGATK Website\public\telegram_news_latest.json"
    try:
        shutil.copy2(output_file, website_json)
        shutil.copy2(latest_file, website_latest)
        print(f"Successfully copied JSON to {website_json} and {website_latest}")
    except Exception as e:
        print(f"Failed to copy json to website directory: {e}")

    # Также копируем картинки в папку сайта для надежности
    website_img_dir = r"d:\Workspace\Web\PGATK Website\public\images\news"
    if os.path.exists(website_img_dir):
        try:
            copied_count = 0
            for filename in os.listdir(TARGET_IMG_DIR):
                src_file = os.path.join(TARGET_IMG_DIR, filename)
                dest_file = os.path.join(website_img_dir, filename)
                if os.path.isfile(src_file) and not os.path.exists(dest_file):
                    shutil.copy2(src_file, dest_file)
                    copied_count += 1
            if copied_count > 0:
                print(f"Successfully copied {copied_count} new images to {website_img_dir}")
        except Exception as e:
            print(f"Failed to copy images to website directory: {e}")
        
    print(f"Successfully saved {len(final_posts)} total posts to {output_file} and top 15 to {latest_file}")

    # Автоматический git commit и push для локального запуска
    if not os.environ.get('GITHUB_ACTIONS'):
        print("Running git commit and push locally...")
        try:
            import subprocess
            # Проверяем, есть ли измененные или неотслеживаемые файлы
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
            if not status.stdout.strip():
                print("No changes to commit.")
            else:
                # Добавляем файлы
                subprocess.run(["git", "add", "telegram_news.json", "telegram_news_latest.json", "images/"], check=True)
                # Проверяем, есть ли проиндексированные изменения для фиксации
                staged = subprocess.run(["git", "diff", "--cached", "--quiet"])
                if staged.returncode == 0:
                    print("No news changes to commit (only unstaged script or config modifications).")
                else:
                    # Делаем коммит
                    subprocess.run(["git", "commit", "-m", "Auto-update Telegram news (local execution)"], check=True)
                    # Делаем пуш
                    subprocess.run(["git", "push"], check=True)
                    print("Successfully committed and pushed changes to GitHub!")
        except Exception as e:
            print(f"Failed to commit and push changes: {e}")
