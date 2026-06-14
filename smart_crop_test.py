import cv2
import os

def smart_crop_16_9(image_path):
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
            # find center of faces
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
        
    cv2.imwrite(image_path + "_cropped.jpg", cropped)
    return True

img_path = r"d:\Workspace\Web\PGATK Website\public\images\news\11987_0.jpg"
print(smart_crop_16_9(img_path))
