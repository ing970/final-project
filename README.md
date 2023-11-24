# final-project


## 📎 파일 소개
- mediapipe와 OpenCV를 사용하여 실시간으로 손의 움직임을 추적하고, 손이 쥐어지거나 펴지는 상태를 감지하여 화면에 표시합니다. 
- 각 손(왼손과 오른손)이 쥐어지거나 펴지는 상태를 "Grab" 또는 "Release"로 표시하며, 손의 랜드마크도 시각적으로 보여줍니다.

## 🔄 브랜치 변경 안내
- 이 프로젝트의 기능 개발은 주로 feature 브랜치에서 이루어집니다.
- feature 브랜치에서 작업을 시작하려면, 다음의 Git 명령어를 사용하여 브랜치를 변경해 주세요.
`git checkout feature`

## 🔌 설치 방법
- 이 프로젝트를 실행하기 위해서는 Python이 설치되어 있어야 하며, 몇 가지 Python 라이브러리가 필요합니다.
- 필요한 라이브러리는 requirements.txt 파일에 나열되어 있습니다.<br></br>


1. 먼저, 프로젝트 디렉토리로 이동합니다. 
`cd [Your Project Directory]`

2. 프로젝트를 클론합니다.
`git clone https://github.com/ing970/final-project`

3. 필요한 Python 라이브러리를 설치합니다.
`pip install -r requirements.txt`


❗️ 이 프로젝트는 Python **3.9** 이상에서 테스트되었습니다. 해당 버전 이상을 사용하는 것을 **권장**합니다.


## ⚡️ 실행 방법
- 설치가 완료되면, 다음과 같이 스크립트를 실행할 수 있습니다.
`python hand_tracking.py`
- 실행 후, 카메라가 활성화되고 손의 움직임을 추적하기 시작합니다.
- 프로그램은 각 손의 상태를 "Grab" 또는 "Release"로 표시하며, 손의 랜드마크를 화면에 그립니다.

## 👋 종료 방법
- 프로그램을 종료하려면, 'q' 키를 누릅니다.
