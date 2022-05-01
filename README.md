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

### 모델 설명
![instaCloneERD](https://user-images.githubusercontent.com/68195241/161428714-e9491632-a792-4a3f-8dcf-135b947cfebf.png)

#### Profile
- user : 사용자 id
- profile_pic : 프로필 사진
- profile_name : 프로필 이름
- profile_website : 프로필 웹사이트
- profile_bio : 프로필 소개

#### Post
- user : 사용자 id (게시글 작성자)
- content : 게시글 내용
- created_at : 게시글 최초 작성 날짜
- modified_at : 게시글 최근 수정 날짜

#### Media
- content : 미디어 내용
- content_type : 사진/영상 (미디어 종류)

#### Comment
- post : 게시글 id (어느 게시글에 단 댓글인지)
- user : 사용자 id (댓글 작성자)
- content : 댓글 내용
- created_at : 댓글 최초 작성 날짜

#### Reply
- post : 게시글 id (어느 게시글에 있는 댓글의 대댓글인지)
- comment : 댓글 id (어느 댓글의 대댓글인지)
- user : 사용자 id (대댓글 작성자)
- content : 대댓글 내용
- created_at : 대댓글 최초 작성 날짜

#### Like
- post : 게시글 id (어느 게시글의 좋아요인지)
- user : 사용자 id (좋아요 등록자)
- created_at : 좋아요 등록일


## ORM 적용해보기

### 1. 데이터베이스에 해당 모델 객체 3개 넣기
#### 코드
```
firstPost = Post.objects.create(content="1st Post", user=u1)
secondPost = Post.objects.create(content="2nd Post", user=u1)
thirdPost = Post.objects.create(content="3rd Post", , user=u1)
```
#### 결과화면
![객체3개넣기](https://user-images.githubusercontent.com/68195241/161427793-8c5d4147-b33f-4a5d-bc6d-db256939b181.JPG)

### 2. 삽입한 객체들을 쿼리셋으로 조회해보기
#### 코드
```
Post.objects.all()
```
#### 결과화면
![객체조회](https://user-images.githubusercontent.com/68195241/161427787-470003fc-a9c7-4cab-854a-f929f3af4dd6.JPG)

### 3. filter 함수 사용해보기
#### 코드
```
Post.objects.filter(content="1st Post")
```
#### 결과화면
![filter함수](https://user-images.githubusercontent.com/68195241/161427794-00448d86-b4be-4f3d-a116-16646b76f0f8.JPG)

***

> ### 회고
> 처음이 많았던 과제여서 수행 과정이 그리 효율적이지는 못했던 것 같습니다. 그리고 제출한 결과가 과연 최선의 결과였을지 아직도 확신이 서지 않아서 복습 후 제대로 손을 볼 수 있으면 좋곘다는 생각이 듭니다.
> <br/>
> <br/>
> #### 어려웠던 점
> - mysqlclient : ~~wsl 수동설치 & 환경변수 설정으로 문제 해결~~ venv과 requirements.txt. 설치된 pip가 그렇게 많은 것이 애초에 이상함의 지표였음 (pip list로 확인)
> - ERD : 생활코딩, 구글링 등등
> - ORM : 참고자료, 구글링 등등


***

# Week4 : DRF1-Serializer

## [1] 데이터 삽입
### - 모델 선택 및 데이터 삽입

```Post 모델```
```python
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.content)
```
![PostModel](https://user-images.githubusercontent.com/68195241/162532963-e3271d0e-0a82-4a24-a540-a1d5e52172f1.JPG)

## [2] 모든 데이터를 가져오는 API
- URL : ```api/post/```
- Method : ```GET```

#### 결과 코드
```json

```

## [3] 새로운 데이터를 create하도록 요청하는 API
- URL : ```api/post/```
- Method : ```POST```
- Body : ```{}```

#### 결과 코드
```json

```

***

> ### 회고
> 시험 기간으로 꽤 많은 시간을 날리고 나니 그 시간 동안 배웠던 지식들도 휘발되는 바람에 고생을 많이 했습니다... 그리고 지금도 어째선지 api를 요청했을 때 TypeError 창이 뜨고 있어서 끝이 좋지 못합니다. 부디 이번 주말 안에 해결할 수 있기를 바랍니다...
> <br/>
> <br/>
> #### 어려웠던 점
> - api 요청 결과 띄우기