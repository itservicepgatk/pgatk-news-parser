import requests
from bs4 import BeautifulSoup
import json
import os
import re
import shutil
from datetime import datetime

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

if os.environ.get("GITHUB_ACTIONS"):
    TARGET_IMG_DIR = "images/news"
    URL_PREFIX = "https://raw.githubusercontent.com/itservicepgatk/pgatk-news-parser/main/images/news/"
else:
    TARGET_IMG_DIR = r"d:\Workspace\Web\PGATK Website\public\images\news"
    URL_PREFIX = "/images/news/"

if not os.path.exists(TARGET_IMG_DIR):
    os.makedirs(TARGET_IMG_DIR, exist_ok=True)

def smart_crop_16_9(image_path):
    if not HAS_CV2:
        return False
    
    img = cv2.imread(image_path)
    if img is None:
        return False
        
    h, w = img.shape[:2]
    
    target_ratio = 16.0 / 9.0
    current_ratio = w / h
    
    if abs(current_ratio - target_ratio) < 0.01:
        return True # already 16:9
        
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
        
    cv2.imwrite(image_path, cropped)
    return True

def download_image(url, local_filename):
    if not os.path.exists(local_filename):
        try:
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                
                # Apply smart crop if possible
                smart_crop_16_9(local_filename)
                
                return True
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
        response = requests.get(current_url)
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

            # Останавливаем парсинг, если дошли до дат раньше 1 января 2026
            if dt.year < 2026:
                reached_old_dates = True
                break

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
                        local_filename = os.path.join(TARGET_IMG_DIR, f"{post_id}_{img_idx}.jpg")
                        local_url = f"{URL_PREFIX}{post_id}_{img_idx}.jpg"
                        
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
                            local_filename = os.path.join(TARGET_IMG_DIR, f"{post_id}_{img_idx}.jpg")
                            local_url = f"{URL_PREFIX}{post_id}_{img_idx}.jpg"
                            
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
                    
            # Определение категорий
            categories_dict = {
                'Профориентация': ['профориентац', 'абитуриент', 'поступай', 'профессия'],
                'Профилактика': ['профилактик', 'безопасност', 'мчс', 'гаи', 'наркоти', 'преступлен', 'кибер', 'мошенник'],
                'Достижения': ['победител', 'награжд', 'диплом', 'чемпион', 'заняли', 'конкурс', 'олимпиад', 'успеш', 'достижен'],
                'Год белорусской женщины': ['женщин', 'девушк', r'\bматери\b', r'\bмать\b'],
                'Жизнь колледжа': ['праздник', 'мероприяти', 'акция', 'выставк', 'колледж', 'экскурси', 'соревновани', 'концерт', 'конференци', 'преподавател', 'встреч', 'студент', 'учащи'],
                'Общежитие': ['общежити'],
                'БРСМ': ['брсм', 'молодеж', 'волонтер'],
                'ВПВ': ['впв', 'военно-патриотическ', 'патриотическ', 'патриот', 'военн'],
                'Спорт': ['спорт', 'соревнован', 'турнир', 'чемпионат', 'матч', 'атлет', 'физкультур', 'эстафет']
            }
            
            post_categories = []
            clean_text_lower = clean_text.lower()
            for cat, keywords in categories_dict.items():
                if any(re.search(kw, clean_text_lower) if '\\b' in kw else kw in clean_text_lower for kw in keywords):
                    post_categories.append(cat)
                    
            if not post_categories:
                post_categories = ['Telegram']

            page_posts.append({
                'id': post_id,
                'title': title,
                'summary': summary,
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
    # Парсим новые (или старые до 2026 года)
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
    
    # Также копируем файл в папку сайта для надежности
    website_json = r"d:\Workspace\Web\PGATK Website\public\telegram_news.json"
    try:
        shutil.copy2(output_file, website_json)
        print(f"Successfully copied to {website_json}")
    except Exception as e:
        print(f"Failed to copy json to website directory: {e}")
        
    print(f"Successfully saved {len(final_posts)} total posts to {output_file}")
