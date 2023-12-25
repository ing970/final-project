import cv2
import os
import glob

def save_movie(image_directory, output_directory, fps=30):
    """
    지정된 디렉토리에서 PNG 이미지들을 읽어 비디오 파일로 저장하는 함수.

    Args:
    image_directory (str): 이미지 파일들이 있는 디렉토리 경로.
    output_directory (str): 생성된 비디오를 저장할 디렉토리 경로.
    fps (int, optional): 초당 프레임 수. 기본값은 30.

    이 함수는 image_directory에서 모든 PNG 이미지를 찾아 정렬한 후,
    이 이미지들을 사용하여 비디오 파일을 생성하고 output_directory에 저장합니다.
    """

    print(f"Processing images from: {image_directory}")
    # .png 파일을 찾아 정렬
    image_files = sorted(glob.glob(os.path.join(image_directory, '*.png')))
    print(f"Found {len(image_files)} images.")

    # 출력 디렉토리가 없으면 생성
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")

    # 출력 비디오 파일 이름 결정
    video_file_name = os.path.basename(image_directory) + '.mov'
    output_video_path = os.path.join(output_directory, video_file_name)
    print(f"Output video will be saved as: {output_video_path}")

    # 비디오 작성자 초기화
    frame_size = None
    video_writer = None

    # 이미지 순회
    for image_file in image_files:
        image = cv2.imread(image_file)
        if image is None:
            print(f"Failed to load image: {image_file}")
            continue

        if frame_size is None:
            frame_size = (image.shape[1], image.shape[0])
            # 코덱 정의 및 VideoWriter 객체 생성
            fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 'XVID'는 일반적인 코덱입니다. 필요에 따라 변경하세요.
            video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)
            print("Initialized video writer.")

        # 비디오에 프레임 작성
        video_writer.write(image)

        # 이미지 표시
        cv2.imshow('Frame', image)

        # 1/fps 초 기다림
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    # 비디오 작성자 및 디스플레이 창 해제
    if video_writer is not None:
        video_writer.release()
    cv2.destroyAllWindows()
    print("Completed processing.")

# 사용 예시
# image_directory2 = '/path/to/images'  # 이미지 디렉토리 경로를 설정하세요.
# output_directory2 = '/path/to/output'  # 출력 파일 경로를 설정하세요.
# save_movie(image_directory2, output_directory2, fps=30)
