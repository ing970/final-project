import cv2
import os
import glob
import time

def display_images_as_movie(image_directory, fps=30):
    """
    지정된 디렉토리의 이미지들을 영화처럼 디스플레이합니다.

    이 함수는 주어진 디렉토리에서 모든 JPEG 이미지를 읽어서 정렬한 후,
    지정된 프레임 속도로 순차적으로 화면에 표시합니다. 이 시퀀스는
    창에서 표시되며 'q'를 누르면 종료됩니다.

    매개변수:
    image_directory (str): JPEG 이미지가 포함된 디렉토리 경로.
    fps (int, optional): 디스플레이 시퀀스의 프레임 속도. 기본값은 30입니다.

    함수는 각 이미지를 읽고 'Frame'이라는 창에 표시한 다음,
    다음 이미지를 표시하기 전에 1/fps초 동안 기다립니다. 'q'가 눌리면,
    디스플레이 시퀀스가 중단되고 창이 닫힙니다.
    """

    # .jpg 파일을 찾아 정렬
    image_files = sorted(glob.glob(os.path.join(image_directory, '*.jpg')))

    # 이미지들을 순회하며 디스플레이
    for image_file in image_files:
        image = cv2.imread(image_file)
        if image is None:
            continue

        # 이미지 디스플레이
        cv2.imshow('Frame', image)

        # 1/fps 초 기다림
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    # 디스플레이 창 해제
    cv2.destroyAllWindows()

# 사용 예시
# image_directory = '/path/to/your/image/directory'  # 이미지 디렉토리 경로로 교체하세요.
# display_images_as_movie(image_directory, fps=30)
