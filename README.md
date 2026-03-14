# seoultech-computervision-video-recorder

컴퓨터비전 2주차 과제용 비디오 재생/녹화 프로그램입니다.

## 기능

각 기능의 오버레이를 화면에 표시한다.

- **CCTV의 RTSP 스트림을 재생하여 화면에 출력** - `Preview`
![alt text](images/{58FA4406-9D66-4D99-9053-FF31914A5C8A}.png)

- **녹화 시작/종료 및 저장** - `Record`
![alt text](images/{B9553875-CF68-43C6-B305-C287BFDE2569}.png)

- **주사율 변경 가능** - `12fps`, `24fps`, `30fps`, `60fps`, `120fps`
![alt text](images/{E3F76919-A3BA-4F26-A75C-2AE13E23E8EC}.png)

- **저장 파일의 확장자/코덱 변경 가능** - `.avi`, `.mp4`, `.mov`
![alt text](images/{B8BCC2A6-8C94-46CC-A37E-0D6471903C4F}.png)

- **동영상 정지 기능** - `Pause`
![alt text](images/{8AD6FD35-434F-4D58-AF1C-CC8B1C1B0B03}.png)

## 실행 파일

- `app.py`
- (`main.py`는 더 이상 사용하지 않음)

## 키 조작

- `Esc`: 프로그램 종료
- `Space`: 녹화 시작/종료 및 저장
- `C`/`c`: 코덱 변경 모드 토글
- `F`/`f`: FPS 변경 모드 토글
- `P`/`p`: 일시정지 모드 토글
- `-`/`_`: 이전 값
- `=`/`+`: 다음 값

## 저장 파일

- 저장 폴더: `./records`
- 파일명 형식: `%Y-%m-%d %H-%M-%S.확장자`
- 확장자(코덱): `avi(XVID)`, `mp4(mp4v)`, `mov(MJPG)`
