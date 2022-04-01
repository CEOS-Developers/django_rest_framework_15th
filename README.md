# Week2 : Docker와 Github Action을 이용한 자동 배포하기

## Docker
![Microsoft-Docker-logo](https://user-images.githubusercontent.com/68195241/160120711-231bf27e-8333-403a-aa99-a9d3ad5172c6.png)
- 리눅스 컨테이너 기반의 오픈소스 가상화 플랫폼
- 컨테이너에 '이미지(Image)'를 담아서 구동시키는 방식
  - 이미지(Image) : 도커 컨테이너 실행(생성)에 필요한 파일과 설정값(환경)등을 포함하고 있는 것 (컨테이너 생성 템플릿st)
    * 레이어(Layer) : 기존 이미지에 추가적인 파일이 필요할 때 해당 파일만 추가하는 방식 (추가하면 새로운 Layer 생성)
  - 컨테이너(Container) : 도커 이미지를 기반으로 생성; 파일 시스템과 어플리케이션이 구체화되어 실행되는 상태; 응용 프로그램의 종속성과 함께 프로그램 자체를 캡슐화하여 프로세스를 동작

### VM vs. Container
- VM : OS를 가상화 (Gust OS 생성)
  - 장점 - 사용법이 간단, 의존성 DOWN
  - 단점 - 속도 느림, 용량이 큼
- 컨테이너 : VM이 아닌 Docker Engine 위에서 동작; 프로세스를 격리
  - 장점 : 속도 빠름, 용량이 적음
  - 단점 : 의존성 UP

### docker-compose
![MainImage-2](https://user-images.githubusercontent.com/68195241/160120608-0232c880-a56e-46dd-b912-8e64e35a5280.jpg)
- 여러개의 컨테이너를 하나로 묶어주는 역할을 하는 툴 (for 다중 컨테이너 도커 애플리케이션)
- YAML(.yml) 파일로 작성됨 -> YAML 파일을 읽어 하나의 명령어로 모든 서비스 실행


## Github Actions
![Continuous-Deployment-con-GitHub-Actions](https://user-images.githubusercontent.com/68195241/160120267-8a25411d-0ad2-414f-84c2-48f955bf2746.png)
- Github에서 공식적으로 제공하는 CI/CD 툴
- Workflow 자동화툴

### CI/CD
> '빌드 -> 저장소에 전달 -> 배포' 까지의 과정
- CI (Continuous Integration)
  * 테스트, 빌드, Dockerizing, 저장소에 전달
  * 프로덕션 환경으로 서비스를 배포할 수 있도록 준비하는 프로세스
- CD (Continuous Delivery)
  * 배포
  * 저장소로 전달된 프로덕션 서비스를 실제 사용자들에게 배포하는 프로세스

### Workflow
- 하나 이상의 Job으로 구성되고, Event에 의해 예약되거나 트리거될 수 있는 자동화된 절차
- YAML 파일로 작성 + ```.git/workflows```에 저장


***

# Week3 : 모델링과 Django ORM

## 모델링

### Instagram 서비스 설명
- 사용자마다 한 개의 프로필을 가질 수 있음
- 사용자는 게시글을 올릴 수 있음 (수정 가능)
- 게시글에는 반드시 사진이나 영상 하나가 포함되어야 함
- 사용자는 게시글에 좋아요를 남길 수 있음
- 사용자는 게시글에 댓글을 달 수 있음 (수정 불가능)
- 사용자는 댓글에 대댓글을 달 수 있음 (수정 불가능)