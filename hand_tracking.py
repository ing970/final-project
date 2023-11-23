import cv2
import mediapipe as mp

# mediapipe 손 감지 모듈 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 카메라 초기화
cap = cv2.VideoCapture(1) # for mac
# cap = cv2.VideoCapture(0) # for windows

def is_hand_closed(hand_landmarks):
    # 각 손가락의 끝점과 중간점 사이의 각도를 계산하여 손가락이 구부러졌는지 판단
    # 엄지, 집게손가락, 중지의 끝점과 중간점을 사용
    finger_tips = [4, 8, 12]  # 엄지, 집게손가락, 중지의 끝점 랜드마크 인덱스
    finger_middles = [3, 7, 11]  # 엄지, 집게손가락, 중지의 중간점 랜드마크 인덱스
    closed_count = 0

    for tip, middle in zip(finger_tips, finger_middles):
        tip_pos = hand_landmarks.landmark[tip]
        middle_pos = hand_landmarks.landmark[middle]
        distance = ((tip_pos.x - middle_pos.x) ** 2 + (tip_pos.y - middle_pos.y) ** 2) ** 0.5
        if distance < 0.03:  # 임계값은 실험을 통해 조정
            closed_count += 1

    # 대부분의 손가락이 구부러진 것으로 판단되면 손을 쥐었다고 간주
    return closed_count >= 2

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # BGR 이미지를 RGB로 변환
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 좌우반전
    image = cv2.flip(frame, 1)
    
    # 손 감지
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # 손의 상태를 판단
            hand_state = 'Grab' if is_hand_closed(hand_landmarks) else 'Release'
            hand_label = handedness.classification[0].label
            label = f'{hand_label} Hand: {hand_state}'

            # 랜드마크 그리기 및 라벨 표시
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(image, label, (20, 60 if hand_label == 'Right' else 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if hand_state == 'Grab' else (0, 0, 255), 3)

    cv2.imshow('Hand Tracking', image)

    # q를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
