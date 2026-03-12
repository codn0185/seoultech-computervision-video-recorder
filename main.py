# 서울과학기술대학교 컴퓨터비전 2주차 과제
# Video Recorder

# === Import Libraries ===
import numpy as np
import cv2 as cv
import os
from datetime import datetime

print("---Version---")
print("numpy: " + np.__version__)  # 2.4.3
print("cv2: " + cv.__version__)  # 4.13.0
print("-------------")


# === Config ===
# Video Config
VIDEO_URL = "rtsp://210.99.70.120:1935/live/cctv001.stream"  # CCTV001	127.1504447	36.8625719	세집매 삼거리	충청남도 천안시 서북구 신당동 482-22
WINDOW_TITLE: str = "CCTV - 충청남도 천안시 서북구 신당동 482-22 세집매 삼거리"
WIDTH: int
HEIGHT: int
FPS: int
# File Config
VIDEO_RECORD_DIRECTORY: str = "./records"
VIDEO_RECORD_FILENAME_FORMAT: str = "%Y-%m-%d %H-%M-%S"
VIDEO_FORMAT: str = "avi"
VIDEO_FOURCC: str = "XVID"
# Mod Config
PREVIEW_MOD: int = 1
RECORDER_MOD: int = 2
CURRENT_MOD: int = PREVIEW_MOD  # 현재 모드
# key Config
SWITCH_MOD_KEYCODE: int = 32  # Space
EXIT_PROGRAM_KEYCODE: int = 27  # ESC


# === Utilities ===
# 모드 변경
def switch_mod() -> None:
    global CURRENT_MOD
    if CURRENT_MOD == PREVIEW_MOD:
        print("Mod Changed: Preview -> Recorder")
        CURRENT_MOD = RECORDER_MOD
    elif CURRENT_MOD == RECORDER_MOD:
        print("Mod Changed: Recorder -> Preview")
        CURRENT_MOD = PREVIEW_MOD


# === Main Function ===
def main():
    video = cv.VideoCapture(VIDEO_URL)

    # 비디오가 정상인지 확인
    if not video.isOpened():
        print(f"Video is Unavailable: {VIDEO_URL}")
        return

    # 녹화 파일 저장 디렉토리 생성
    if not os.path.exists(VIDEO_RECORD_DIRECTORY):
        os.makedirs(VIDEO_RECORD_DIRECTORY)

    # 비디오 정보
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    fps = min(video.get(cv.CAP_PROP_FPS), 30)  # 최대 30fps
    wait_msec = int(1000 / fps)
    print(f"Resolution: {width}x{height}, FPS: {fps}fps({wait_msec}ms)")

    # 프로그램 시작
    print("Start Program")
    record: cv.VideoWriter = None
    isRecording: bool = False
    while True:
        valid, frame = video.read()

        if not valid:
            print("Video is not Valid")
            break

        # 키 입력
        keycode = cv.waitKey(wait_msec)
        if keycode == EXIT_PROGRAM_KEYCODE:
            print("Exit Program")
            break
        elif keycode == SWITCH_MOD_KEYCODE:
            if isRecording:  # Record -> Preview
                print("Mod Changed: Recorder -> Preview")
                isRecording = False
                # 녹화 저장 종료
                record.release()
                record = None
            else:  # Preview -> Record
                print("Mod Changed: Preview -> Recorder")
                isRecording = True
                # 녹화 저장 경로 설정
                file_path = f"{VIDEO_RECORD_DIRECTORY}/{datetime.now().strftime(VIDEO_RECORD_FILENAME_FORMAT)}.{VIDEO_FORMAT}"
                print(f"Video Recorded at: {file_path}")
                # VideoWriter 생성
                record = cv.VideoWriter(
                    file_path,
                    cv.VideoWriter_fourcc(*VIDEO_FOURCC),
                    fps,
                    (width, height),
                    isColor=frame.ndim >= 3 and frame.shape[2] > 1,
                )
                if not record.isOpened():
                    print("VideoWriter 생성 실패")

        # 녹화 저장
        if isRecording and record:
            record.write(frame)

        # 화면에 녹화 표시
        if isRecording:
            cv.putText(  # 좌상단에 빨강 Record 텍스트 출력
                img=frame,
                text="Record",
                org=(10, 15),
                fontFace=cv.FONT_HERSHEY_DUPLEX,
                fontScale=0.5,
                color=(0, 0, 255),
            )

        # 프레임 출력
        cv.imshow(WINDOW_TITLE, frame)

    # 녹화 중일 때 종료 시 저장 후 종료
    if isRecording:
        record.release()
        record = None

    video.release()
    cv.destroyAllWindows()


# === Run ===
if __name__ == "__main__":
    main()
