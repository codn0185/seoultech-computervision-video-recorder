from controller import VideoController

# https://www.data.go.kr/data/15063717/fileData.do#/tab-layer-file
# CCTV001	127.1504447	36.8625719	세집매 삼거리	충청남도 천안시 서북구 신당동 482-22
VIDEO_URL: str = "rtsp://210.99.70.120:1935/live/cctv001.stream"


def main():
    vc = VideoController()
    vc.setWindowTitle("Video Recorder")
    vc.initializeSourceVideo(VIDEO_URL)
    vc.playVideo()


if __name__ == "__main__":
    main()
