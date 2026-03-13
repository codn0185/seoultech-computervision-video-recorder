# 상태 추상 클래스
class State:
    controller = None

    def __init__(self, controller):
        self.controller = controller

    def enter(self):
        print(f"[Log] Enter: {type(self).__name__}")

    def execute(self):
        pass

    def exit(self):
        print(f"[Log] Exit: {type(self).__name__}")


# Preview
class IdleState(State):
    def enter(self):
        super().enter()

    def execute(self):
        pass

    def exit(self):
        super().exit()


# Recording
class RecordingState(State):
    def enter(self):
        super().enter()
        # 녹화 시작
        self.controller.startRecording()

    def execute(self):
        super().execute()
        # 녹화 저장
        self.controller.writeFrameToRecording()

        # 화면에 녹화 레이아웃 표시
        self.controller.drawRecordOverlay()

    def exit(self):
        super().exit()
        # 녹화 종료
        self.controller.releaseRecording()


# 코덱 변경
class ChangingCodecState(State):
    def enter(self):
        super().enter()

    def execute(self):
        # Codec 오버레이 표시
        self.controller.drawCodecOverlay()

    def exit(self):
        super().exit()


# 주사율 변경
class ChangingFPSState(State):
    def enter(self):
        super().enter()

    def execute(self):
        # FPS 오버레이 표시
        self.controller.drawFpsOverlay()

    def exit(self):
        super().exit()


# 비디오 정지
class PauseState(State):
    def enter(self):
        super().enter()

    def execute(self):
        # Pause 오버레이 표시
        self.controller.drawPauseOverlay()

    def exit(self):
        super().exit()


# 프로그램 종료
class ExitState(State):
    def enter(self):
        super().enter()

    def execute(self):
        pass

    def exit(self):
        super().exit()
