from state import *


class VideoFSM:
    current_state: State = None  # 현재 상태

    idle_state: IdleState
    recording_state: RecordingState
    changing_codec_state: ChangingCodecState
    changing_fps_state: ChangingFPSState
    pause_state: PauseState
    exit_state: ExitState

    def __init__(self, controller):
        self.idle_state = IdleState(controller)
        self.recording_state = RecordingState(controller)
        self.changing_codec_state = ChangingCodecState(controller)
        self.changing_fps_state = ChangingFPSState(controller)
        self.pause_state = PauseState(controller)
        self.exit_state = ExitState(controller)

        self.switchToIdle()

    def execute(self):
        if self.current_state:
            self.current_state.execute()

    # 상태 전환
    def switchState(self, new_state: State):
        if self.current_state:
            self.current_state.exit()
        self.current_state = new_state
        if self.current_state:
            self.current_state.enter()

    def switchToIdle(self):
        self.switchState(self.idle_state)

    def switchToRecording(self):
        self.switchState(self.recording_state)

    def switchToChangingCodec(self):
        self.switchState(self.changing_codec_state)

    def switchToChangingFps(self):
        self.switchState(self.changing_fps_state)

    def switchToPause(self):
        self.switchState(self.pause_state)

    def switchToExit(self):
        self.switchState(self.exit_state)

    # 현재 상태 확인
    def checkCurrentState(self, state: State) -> bool:
        return self.current_state is state

    def isIdle(self) -> bool:
        return self.checkCurrentState(self.idle_state)

    def isRecording(self) -> bool:
        return self.checkCurrentState(self.recording_state)

    def isChangingCodec(self) -> bool:
        return self.checkCurrentState(self.changing_codec_state)

    def isChangingFps(self) -> bool:
        return self.checkCurrentState(self.changing_fps_state)

    def isPause(self) -> bool:
        return self.checkCurrentState(self.pause_state)

    def isExit(self) -> bool:
        return self.checkCurrentState(self.exit_state)
