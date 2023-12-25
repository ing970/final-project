import cv2
import os
import glob


def extract_frames_from_videos(video_paths, num_frames_per_video=300):
    """여러 비디오에서 지정된 개수만큼 프레임을 추출합니다.
    Args:
        video_paths (list): 비디오 파일 경로 리스트
        num_frames_per_video (int): 각 비디오에서 추출할 프레임 수
    Returns:
        dict: 각 비디오 경로를 키로 하고, 해당 비디오에서 추출된 프레임 리스트를 값으로 하는 딕셔너리
    """
    frames_dict = {}

    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"비디오 파일을 열 수 없습니다: {video_path}")
            continue

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = total_frames // (num_frames_per_video - 1)
        frames = []

        for i in range(0, total_frames, interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            if len(frames) == num_frames_per_video:
                break

        cap.release()
        frames_dict[video_path] = frames

    return frames_dict

def save_extracted_frames(frames_dict, base_save_path):
    """추출된 프레임들을 이미지 파일로 저장합니다.
    Args:
        frames_dict (dict): 비디오 경로를 키로 하고 프레임 리스트를 값으로 하는 딕셔너리
        base_save_path (str): 저장할 기본 경로
    """
    for video_path, frames in frames_dict.items():
        video_name = os.path.basename(video_path).split('.')[0]
        save_path = os.path.join(base_save_path, video_name)
        os.makedirs(save_path, exist_ok=True)

        for i, frame in enumerate(frames):
            frame_number = f'{i:02d}'  # Format the frame number to be two digits
            frame_path = os.path.join(save_path, f'frame_{frame_number}.jpg')
            cv2.imwrite(frame_path, frame)

# ".mov" 확장자를 가진 모든 비디오 파일의 경로
base_dir = '/Users/sdc/Documents/ds_study/DeepLearning/dl_project/hand_movement/wrapup/yolo/test/IMG_6312.mov'
video_paths = glob.glob(base_dir)  # 디렉토리 변경

# 프레임 추출 및 저장
frames_dict = extract_frames_from_videos(video_paths)
save_extracted_frames(frames_dict, '/Users/sdc/Documents/ds_study/DeepLearning/dl_project/hand_movement/wrapup/yolo/test/extracted_frames/')