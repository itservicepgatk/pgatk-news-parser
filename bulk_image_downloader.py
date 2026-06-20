import requests
from bs4 import BeautifulSoup
import os
import re
import cv2
import concurrent.futures
import time

TARGET_IMG_DIR = "images/news"
TEMP_IMG_DIR = "images/temp"

if not os.path.exists(TARGET_IMG_DIR):
    os.makedirs(TARGET_IMG_DIR, exist_ok=True)
if not os.path.exists(TEMP_IMG_DIR):
    os.makedirs(TEMP_IMG_DIR, exist_ok=True)

def fetch_page_for_images(before_id):
    url = f"https://t.me/s/pgatkk?before={before_id}"
    tasks = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            messages = soup.find_all('div', class_='tgme_widget_message_wrap')
            
            for msg in messages:
                link_node = msg.find('a', class_='tgme_widget_message_date')
                if not link_node:
                    continue
                    
                link = link_node.get('href', '')
                id_match = re.search(r'/(\d+)$', link)
                if not id_match:
                    continue
                    
                post_id = int(id_match.group(1))
                
                images = []
                photo_nodes = msg.find_all('a', class_='tgme_widget_message_photo_wrap')
                for node in photo_nodes:
                    if node.has_attr('style'):
                        style = node['style']
                        match = re.search(r"background-image:url\('([^']+)'\)", style)
                        if match:
                            images.append(match.group(1))
                
                if not images:
                    video_nodes = msg.find_all('i', class_='tgme_widget_message_video_thumb')
                    for node in video_nodes:
                        if node.has_attr('style'):
                            style = node['style']
                            match = re.search(r"background-image:url\('([^']+)'\)", style)
                            if match:
                                images.append(match.group(1))
                                
                for idx, img_url in enumerate(images):
                    tasks.append((post_id, img_url, idx))
    except Exception as e:
        pass
    return tasks

def download_raw_image(task):
    post_id, img_url, idx = task
    target_webp_path = os.path.join(TARGET_IMG_DIR, f"{post_id}_{idx}.webp")
    
    if os.path.exists(target_webp_path):
        return None # Уже существует
        
    temp_jpg = os.path.join(TEMP_IMG_DIR, f"{post_id}_{idx}.jpg")
    if os.path.exists(temp_jpg):
        return temp_jpg
        
    try:
        r = requests.get(img_url, stream=True, timeout=15)
        if r.status_code == 200:
            with open(temp_jpg, 'wb') as f:
                for chunk in r.iter_content(1024*64):
                    f.write(chunk)
            return temp_jpg
    except Exception as e:
        pass
    return None

def smart_crop_16_9(image_path, target_webp_path):
    img = cv2.imread(image_path)
    if img is None:
        return False
        
    h, w = img.shape[:2]
    target_ratio = 16.0 / 9.0
    current_ratio = w / h
    
    cropped = img
    
    if abs(current_ratio - target_ratio) > 0.01:
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if current_ratio < target_ratio:
            target_w = w
            target_h = int(w / target_ratio)
            
            if len(faces) > 0:
                min_y = min([y for x,y,fw,fh in faces])
                max_y = max([y+fh for x,y,fw,fh in faces])
                faces_center_y = (min_y + max_y) // 2
            else:
                faces_center_y = h // 2
                
            y1 = max(0, faces_center_y - target_h // 2)
            y2 = min(h, y1 + target_h)
            if y2 - y1 < target_h:
                y1 = h - target_h
                y2 = h
                
            cropped = img[y1:y2, 0:target_w]
        else:
            target_h = h
            target_w = int(h * target_ratio)
            
            if len(faces) > 0:
                min_x = min([x for x,y,fw,fh in faces])
                max_x = max([x+fw for x,y,fw,fh in faces])
                faces_center_x = (min_x + max_x) // 2
            else:
                faces_center_x = w // 2
                
            x1 = max(0, faces_center_x - target_w // 2)
            x2 = min(w, x1 + target_w)
            if x2 - x1 < target_w:
                x1 = w - target_w
                x2 = w
                
            cropped = img[0:target_h, x1:x2]
            
    cv2.imwrite(target_webp_path, cropped, [cv2.IMWRITE_WEBP_QUALITY, 85])
    return True

def process_image(temp_jpg_path):
    if not temp_jpg_path:
        return False
        
    filename = os.path.basename(temp_jpg_path)
    target_webp_path = os.path.join(TARGET_IMG_DIR, filename.replace('.jpg', '.webp'))
    
    if os.path.exists(target_webp_path):
        try: os.remove(temp_jpg_path)
        except: pass
        return True
        
    success = smart_crop_16_9(temp_jpg_path, target_webp_path)
    if success:
        try: os.remove(temp_jpg_path)
        except: pass
    return success

if __name__ == '__main__':
    START_ID = 3
    END_ID = 12050
    
    print("Этап 1: Быстрый сбор ссылок на картинки со всех страниц...")
    
    # Чтобы собрать все страницы, делаем запросы с шагом 20 
    # (Telegram выдает по 20 постов на страницу)
    page_ids = list(range(END_ID, START_ID, -20))
    
    all_download_tasks = set()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_id = {executor.submit(fetch_page_for_images, pid): pid for pid in page_ids}
        
        for future in concurrent.futures.as_completed(future_to_id):
            tasks = future.result()
            for t in tasks:
                all_download_tasks.add(t) # Используем set чтобы избежать дубликатов из-за пересечений
                
    all_download_tasks = list(all_download_tasks)
    print(f"Найдено {len(all_download_tasks)} уникальных картинок для скачивания.")
    
    print("\nЭтап 2: Многопоточное скачивание (50 потоков)...")
    downloaded_files = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_task = {executor.submit(download_raw_image, task): task for task in all_download_tasks}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_task)):
            result = future.result()
            if result:
                downloaded_files.append(result)
            if (i+1) % 100 == 0:
                print(f"Скачано {i+1} / {len(all_download_tasks)}")
                
    print(f"\nЭтап 3: Конвертация {len(downloaded_files)} картинок в WebP (10 потоков)...")
    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(process_image, file): file for file in downloaded_files}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_file)):
            if future.result():
                success_count += 1
            if (i+1) % 50 == 0:
                print(f"Сконвертировано {i+1} / {len(downloaded_files)}")
                
    print(f"\nГотово! Успешно обработано {success_count} картинок.")
