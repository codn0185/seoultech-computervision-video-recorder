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
def switch_mod() -> None:  # 모드 변경
    global CURRENT_MOD, RECORDER_MOD, PREVIEW_MOD
    if CURRENT_MOD == PREVIEW_MOD:
        print("Mod Changed: Preview -> Recorder")
        CURRENT_MOD = RECORDER_MOD
    elif CURRENT_MOD == RECORDER_MOD:
        print("Mod Changed: Recorder -> Preview")
        CURRENT_MOD = PREVIEW_MOD


# === Main Function ===
def main():
    pass


# === Run ===
if __name__ == "__main__":
    main()
