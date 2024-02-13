import cv2
import mediapipe as mp
from ultralytics import YOLO
import torch
from models import hand_LSTM
from dataset import MyDataset
from utilities import putText_korean, grab_release, detect_and_process, overlay_text
from config import best_model, step_best_model, model_path, font_path, hand_cls, length, position, font_size, color

def main():
    # 장치 설정 (CPU 또는 GPU)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    
    # 모델 초기화
    yolo_model = YOLO(best_model)
    step_model = YOLO(step_best_model)
    lstm_model = hand_LSTM().to(device)
    lstm_model.load_state_dict(torch.load(model_path, map_location=device))
    lstm_model.eval()

    # mediapipe 손 감지 모듈 초기화
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.3)
    mp_drawing = mp.solutions.drawing_utils

    hand_list = [mp_hands, hands, mp_drawing]

    cap_device = 0
    cap = cv2.VideoCapture(cap_device)  # for Mac
    # cap = cv2.VideoCapture(0)  # for Windows
    lstm_model.eval()
    status_num = -1
    step = 0
    wait_frames = 60
    cnt_frames = 0
    xyz_list_list = []
    detect_list = [0, 13, 4, 5, 3] #객체 번호인 detect_list추가
    
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        image =cv2.resize(frame, (640, 640))
        if step <= len(detect_list) -1: #step이 5이상이면 list index out of range오류 발생
            image, xyz_list_list, status_num, x1, y1, x2, y2 = detect_and_process(
            image, step_model, yolo_model, hand_list, lstm_model, step, detect_list ,hand_cls, length, xyz_list_list, status_num) # detect_cls삭제, step, detect_list추가
    
        # 각 단계별 텍스트 지정 로직
        if step == 0:
            text = '파란 다리를 집어 올리세요.' if status_num != 1 else '빨간 원 위에 파란 다리를 올려놓으세요.'
        elif step == 1:
            text = '노란 다리를 집어 올리세요.' if status_num != 1 else '파란색 다리의 왼쪽에 노란색 다리를 놓으세요.'
        elif step == 2:
            text = '초록색 원을 집어 올리세요.' if status_num != 1 else '노란색 다리 밑에 초록색 원을 넣어주세요.'
        elif step == 3:
            text = '초록색 큐브를 집어 올리세요.' if status_num != 1 else '노란색 다리의 오른쪽 위에 초록색 큐브를 놓으세요.'
        elif step == 4:
            text = '파란색 부채꼴을 집어 올리세요.' if status_num != 1 else '초록색 큐브의 왼쪽에 파란색 부채꼴을 놓으세요.'
        else:
            x1, y1, x2, y2 = 0, 0, 0, 0 # 초기화
            text = '완료!'
                    
        if x1 != 0 and y1 != 0 and x2 != 0 and y2 != 0:
            text = '참 잘했어요!'
            if cnt_frames < wait_frames:
                cnt_frames += 1
            else:
                step += 1
                cnt_frames = 0
                status_num = -1
        
        image = overlay_text(image, text, position, font_path, font_size, color)

        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey()
        
if __name__ == "__main__":
    main()
