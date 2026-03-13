import numpy as np
import cv2 as cv
import os
from datetime import datetime

from fsm import VideoFSM

# === 상수 ===
FPS_LIST: list[float] = [12.0, 24.0, 30.0, 60.0, 120.0]
CODEC_LIST: list[str] = [
    "avi",
    "mp4",
    "mov",
]
CODEC_TO_FOURCC_DICT: dict[str, str] = {
    "avi": "XVID",
    "mp4": "mp4v",
    "mov": "MJPG",
}
VIDEO_RECORD_DIRECTORY: str = "./records"
VIDEO_RECORD_FILENAME_FORMAT: str = "%Y-%m-%d %H-%M-%S"
KEYCODE_DICT: dict[str, int] = {
    #  프로그램 종료
    "esc": 27,
    # 녹화 시작/종료
    "space": 32,
    # 코덱 변경 모드 토글
    "c": 99,
    "C": 67,
    # FPS 변경 모드 토글
    "f": 102,
    "F": 70,
    # 이전 값
    "-": 45,
    "_": 95,
    # 다음 값
    "=": 61,
    "+": 43,
    # 일시정지 모드 토글
    "p": 112,
    "P": 80,
    # 단축키 가이드
    "/": 47,
    "?": 191,
}


class VideoController:
    fsm: VideoFSM = None

    window_title: str = "Title"
    source_video: cv.VideoCapture = None
    source_video_data = {
        "width": 0,  # 너비
        "height": 0,  # 높이
        "fps": 0,  # 주사율
        "channel": 0,  # color 채널 수
    }
    frame: np.ndarray = None

    record_video: cv.VideoWriter = None
    target_video_data = {
        "width": 0,  # 너비
        "height": 0,  # 높이
        "fps": 0,  # 주사율
        "wait_msec": 0,  # 프레임 간 대기시간 (ms)
        "channel": 0,  # color 채널 수
        "fps_index": 2,  # 주사율 인덱스
        "codec_index": 0,  # 코덱 인덱스
    }

    def __init__(self):
        self.fsm = VideoFSM(self)

        # 녹화 폴더 생성
        if not os.path.exists(VIDEO_RECORD_DIRECTORY):
            os.makedirs(VIDEO_RECORD_DIRECTORY)

    # 비디오 초기 설정
    def initializeSourceVideo(self, source_link: str):
        self.source_video = cv.VideoCapture(source_link)

        if not self.source_video.isOpened():
            print("[Error] Video is Unavailable")
            return
        # 너비
        self.source_video_data["width"] = self.target_video_data["width"] = int(
            self.source_video.get(cv.CAP_PROP_FRAME_WIDTH)
        )
        # 높이
        self.source_video_data["height"] = self.target_video_data["height"] = int(
            self.source_video.get(cv.CAP_PROP_FRAME_HEIGHT)
        )
        # 주사율
        self.source_video_data["fps"] = self.source_video.get(cv.CAP_PROP_FPS)
        self.target_video_data["fps"] = FPS_LIST[self.target_video_data["fps_index"]]
        # 프레임 간 대기시간
        self.target_video_data["wait_msec"] = int(
            1000.0 / self.target_video_data["fps"]
        )
        # color 채널 수
        valid, self.frame = self.source_video.read()
        if valid:
            self.source_video_data["channel"] = self.target_video_data["channel"] = (
                0 if self.frame.ndim == 2 else self.frame.shape[2]
            )

    # 비디오 재생
    def playVideo(self):
        # 비디오 재생 시작
        while not self.fsm.isExit():
            """
            원본 프레임 읽기 (Pause가 아닐 때)
            -> 저장 (녹화 중일 때)
            -> 프레임 편집 (오버레이 적용)
            -> 대기 (wait_msec)
            -> 화면에 출력 (cv.imshow())
            """
            if not self.fsm.isPause():  # Pause가 아닌 경우에만 프레임 새로고침
                valid, self.frame = self.source_video.read()
                if not valid:
                    print("[Error] Frame is not Valid")
                    break

            # 상태에 따라 작업 수행
            self.fsm.execute()

            # 키 입력
            self.keyEventHandler(cv.waitKey(self.target_video_data["wait_msec"]))

            # 프레임 출력
            cv.imshow(self.window_title, self.frame)

        # 비디오 재생 종료
        self.source_video.release()
        cv.destroyAllWindows()

    # 프로그램 종료
    def exitProgram(self):
        print("[Log] Exit Program")
        self.fsm.switchToExit()

    # === 이벤트 ===

    # 키 입력 이벤트 핸들러
    def keyEventHandler(self, keycode: int):
        # 프로그램 종료
        if keycode == KEYCODE_DICT["esc"]:
            self.exitProgram()
        # 녹화
        elif keycode == KEYCODE_DICT["space"]:
            if self.fsm.isRecording():
                self.fsm.switchToIdle()
            else:
                self.fsm.switchToRecording()
        # 코덱 변경
        elif keycode == KEYCODE_DICT["c"] or keycode == KEYCODE_DICT["C"]:
            if self.fsm.isChangingCodec():
                self.fsm.switchToIdle()
            else:
                self.fsm.switchToChangingCodec()
        # 주사율 변경
        elif keycode == KEYCODE_DICT["f"] or keycode == KEYCODE_DICT["F"]:
            if self.fsm.isChangingFps():
                self.fsm.switchToIdle()
            else:
                self.fsm.switchToChangingFps()
        # 이전 값
        elif keycode == KEYCODE_DICT["-"] or keycode == KEYCODE_DICT["_"]:
            if self.fsm.current_state == self.fsm.changing_codec_state:
                self.shiftCodecIndex(-1)
            elif self.fsm.current_state == self.fsm.changing_fps_state:
                self.shiftFpsIndex(-1)
        # 다음 값
        elif keycode == KEYCODE_DICT["="] or keycode == KEYCODE_DICT["+"]:
            if self.fsm.current_state == self.fsm.changing_codec_state:
                self.shiftCodecIndex(1)
            elif self.fsm.current_state == self.fsm.changing_fps_state:
                self.shiftFpsIndex(1)
        # 비디오 정지
        elif keycode == KEYCODE_DICT["p"] or keycode == KEYCODE_DICT["P"]:
            if self.fsm.isPause():
                self.fsm.switchToIdle()
            else:
                self.fsm.switchToPause()
        # 단축키 가이드
        elif keycode == KEYCODE_DICT["/"] or keycode == KEYCODE_DICT["?"]:
            pass

    # === 녹화 ===

    # 녹화 시작
    def startRecording(self):
        codec = CODEC_LIST[self.target_video_data["codec_index"]]
        file_path = f"{VIDEO_RECORD_DIRECTORY}/{datetime.now().strftime(VIDEO_RECORD_FILENAME_FORMAT)}.{codec}"

        self.record_video = cv.VideoWriter(
            file_path,
            cv.VideoWriter_fourcc(*CODEC_TO_FOURCC_DICT[codec]),
            self.target_video_data["fps"],
            (self.target_video_data["width"], self.target_video_data["height"]),
            isColor=self.target_video_data["channel"] > 1,
        )

        if not self.record_video.isOpened():
            print("[Error] Failed to start Recording")

    # 현재 프레임 추가
    def writeFrameToRecording(self):
        if self.record_video.isOpened():
            self.record_video.write(self.frame)

    # 녹화 종료
    def releaseRecording(self):
        self.record_video.release()
        self.record_video = None

    # === 화면 오버레이 ===

    # Record 오버레이
    def drawRecordOverlay(self):
        cv.putText(  # 좌상단에 빨강색으로 Record 텍스트 출력
            img=self.frame,
            text="Record",
            org=(10, 15),
            fontFace=cv.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 0, 255),
        )

    # Codec 오버레이
    def drawCodecOverlay(self):
        cv.putText(  # 좌상단에 노랑색으로 현재 코덱 출력
            img=self.frame,
            text=f"Codec: {CODEC_LIST[self.target_video_data['codec_index']]}",
            org=(10, 15),
            fontFace=cv.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(0, 255, 255),
        )

    # FPS 오버레이
    def drawFpsOverlay(self):
        cv.putText(  # 좌상단에 하늘색으로 현재 FPS 출력
            img=self.frame,
            text=f"FPS: {self.target_video_data['fps']}fps",
            org=(10, 15),
            fontFace=cv.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(255, 200, 0),
        )

    # Pause 오버레이
    def drawPauseOverlay(self):
        cv.putText(  # 좌상단에 흰색으로 Pause 텍스트 출력
            img=self.frame,
            text="Pause",
            org=(10, 15),
            fontFace=cv.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(255, 255, 255),
        )

    # 단축키 가이드 오버레이
    def drawKeyGuideOverlay(self):
        pass

    # === etc. ===

    # 윈도우 제목 설정
    def setWindowTitle(self, title: str):
        self.window_title = title

    # 코덱 인덱스 이동
    def shiftCodecIndex(self, delta: int):
        self.target_video_data["codec_index"] += delta
        self.target_video_data["codec_index"] %= len(CODEC_LIST)

    # 주사율 인덱스 이동
    def shiftFpsIndex(self, delta: int):
        index = self.target_video_data["fps_index"] + delta
        self.target_video_data["fps_index"] = max(0, min(index, len(FPS_LIST) - 1))
        self.target_video_data["fps"] = FPS_LIST[self.target_video_data["fps_index"]]
        self.target_video_data["wait_msec"] = int(
            1000.0 / self.target_video_data["fps"]
        )
