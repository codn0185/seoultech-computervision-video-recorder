# 서울과학기술대학교 컴퓨터비전 2주차 과제
# Video Recorder

# === Import Libraries ===
import numpy as np
import cv2 as cv

print("---Version---")
print("numpy: " + np.__version__)  # 2.4.3
print("cv2: " + cv.__version__)  # 4.13.0
print("-------------")


# === Config ===
# Config
WINDOW_TITLE: str = "CCTV - 충청남도 천안시 서북구 신당동 482-22 세집매 삼거리"
# Video Config
VIDEO_URL = "rtsp://210.99.70.120:1935/live/cctv001.stream"  # CCTV001	127.1504447	36.8625719	세집매 삼거리	충청남도 천안시 서북구 신당동 482-22
WIDTH: int
HEIGHT: int
FPS: int
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

    if not video.isOpened():
        print(f"Video is Unavailable: {VIDEO_URL}")
        return

    fps = min(video.get(cv.CAP_PROP_FPS), 1000)  # 최대 1000fps
    wait_msec = int(1000 / fps)
    print(f"{fps}fps ({wait_msec}ms)")

    print("Start Program")
    while True:
        valid, frame = video.read()
        if not valid:
            print("Video is not Valid")
            break

        if CURRENT_MOD == RECORDER_MOD:  # Recorder Mod
            cv.putText(  # 좌상단에 빨강 Record 글자 표시
                img=frame,
                text="Record",
                org=(10, 15),
                fontFace=cv.FONT_HERSHEY_DUPLEX,
                fontScale=0.5,
                color=(0, 0, 255),
            )

        cv.imshow(WINDOW_TITLE, frame)

        keycode = cv.waitKey(wait_msec)
        if keycode == EXIT_PROGRAM_KEYCODE:
            print("Exit Program")
            break
        elif keycode == SWITCH_MOD_KEYCODE:
            switch_mod()

    video.release()
    cv.destroyAllWindows()


# === Run ===
if __name__ == "__main__":
    main()
