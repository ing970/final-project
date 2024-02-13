# 프로젝트의 설정 값들을 정의합니다.
best_model = './model/best_model.pt'
step_best_model = './model/step_best_model.pt'
model_path = './model/lstm_model.pth'

# 손, dataset길이 설정
hand_cls = 6
length = 5

# 한글 텍스트를 추가할 위치, 폰트경로, 폰트크기, 색상설정
position = (15, 40) # 텍스트를 출력할 위치
font_path = './font/KCC-Ganpan.ttf' # 한글 폰트 파일 경로
font_size = 30 # 폰트 크기
color = (0, 0, 255)