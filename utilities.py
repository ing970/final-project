import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader
from dataset import MyDataset
from PIL import ImageFont, ImageDraw, Image

def grab_release(image, yolo_model, hand_list , lstm_model, detect_cls, hand_cls, length, xyz_list_list, status_num):
    mp_hands, hands, mp_drawing = hand_list[0], hand_list[1], hand_list[2]
    
    # 장치 설정 (CPU 또는 GPU)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    # YOLO 객체 감지
    box_results = yolo_model.predict(image, conf = 0.6, verbose=False, show = False)
    boxes = box_results[0].boxes.xyxy.cpu()
    box_class = box_results[0].boxes.cls.cpu().tolist()

    x1, y1, x2, y2 = 0, 0, 0, 0
    hx1, hy1, hx2, hy2 = 0,0,0,0
    for idx, cls in enumerate(box_class):
        if int(cls) == detect_cls:
            x1, y1, x2, y2 = boxes[idx]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        elif int(cls) == hand_cls:
            hx1, hy1, hx2, hy2 = boxes[idx]
            hx1, hy1, hx2, hy2 = int(hx1), int(hy1), int(hx2), int(hy2)
            cv2.rectangle(image, (int(hx1), int(hy1)), (int(hx2), int(hy2)), (0, 0, 255), 2)
    
    #mediapipe
    results = hands.process(image)
    xyz_list = []
    if results.multi_hand_landmarks:
        for x_y_z in results.multi_hand_landmarks:
            for landmark in x_y_z.landmark:
                xyz_list.append(landmark.x) # *10 삭제
                xyz_list.append(landmark.y)
                xyz_list.append(landmark.z) 
                

        xyz_list.append(abs(x1-hx1)/640) # /640 추가
        xyz_list.append(abs(x2-hx2)/640)
        xyz_list.append(abs(y1-hy1)/640)
        xyz_list.append(abs(y2-hy2)/640)

        if x1 != 0 and y1 != 0 and x2 != 0 and y2 != 0 and hx1 != 0 and hy1 != 0 and hx2 != 0 and hy2 != 0:
            xyz_list_list.append(xyz_list)# 객체와 손이 인식되면

        for hand_landmarks in results.multi_hand_landmarks:
              with torch.no_grad():
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    if len(xyz_list_list) == length:
        dataset = []
        dataset.append({'key': 0, 'value': xyz_list_list})
        dataset = MyDataset(dataset)
        dataset = DataLoader(dataset)
        xyz_list_list = []
        for data, label in dataset:
            data = data.to(device)
            with torch.no_grad():
                result = lstm_model(data)
                _, out = torch.max(result, 1)
                status_num = out.item()
                # if out.item() == 0: status = 'Release'
                # else: status = 'Grab'

    # cv2.putText(image, status, (0, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0, 225), 2)

    return image, xyz_list_list, status_num


# 한글폰트 출력
def putText_korean(img, text, position, font_path, font_size, color):
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(position, text, font=font, fill=color)
    return np.array(img_pil)

def overlay_text(image, text, position, font_path, font_size, color):
    return putText_korean(image, text, position, font_path, font_size, color)

# 실시간 안내 system 함수화
def detect_and_process(image, step_model, yolo_model, hand_list, lstm_model, step, detect_list, hand_cls, length, xyz_list_list, status_num): # detect_cls삭제, step, detect_list추가
    box_results = step_model.predict(image, conf = 0.6, verbose=False, show = False)
    boxes = box_results[0].boxes.xyxy.cpu()
    box_class = box_results[0].boxes.cls.cpu().tolist()
    
    x1, y1, x2, y2 = 0, 0, 0, 0 # 초기화
    for idx, cls in enumerate(box_class):
        if int(cls) == step: #detect_cls를 step으로 대체
            x1, y1, x2, y2 = boxes[idx]
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (225, 0, 0), 2)

    image, xyz_list_list, status_num = grab_release(image, yolo_model, hand_list, lstm_model, detect_list[step], hand_cls, length, xyz_list_list, status_num) #detect_list[step]추가, detect_cls삭제
    
    return image, xyz_list_list, status_num, x1, y1, x2, y2

def overlay_text(image, text, position, font_path, font_size, color):
    return putText_korean(image, text, position, font_path, font_size, color)