## Week 3: 인스타그램 데이터 모델링
### 인스타그램 서비스 설명 ('사진, 영상 업로드' 기능만)
모든 서비스는 유저 로그인 기반으로 동작
- 게시글에 사진, 동영상 등록 (1개 이상)
- 게시글에 댓글 (0개 이상)
- 게시글에 좋아요 (0개 이상)
- 게시글 삭제
- 댓글 삭제
- 좋아요 취소

### 모델 설명
<img width=75% src="https://user-images.githubusercontent.com/63996052/160384055-0edaa6fa-ed15-4afc-98e9-82f3982fc34a.png">

**[User]**
- 장고에서 기본으로 제공하는 auth_user와 OneToOne Link with User Model (Profile) (OneToOneField)
- 이름, 사용자 이름(아이디), 비밀번호, 웹사이트, 소개 컬럼
- 생성 날짜, 업데이트 날짜, 삭제 여부
- 사진, 영상 업로드 기능에만 집중하기 위해 유저의 다른 정보들은 생략

**[Post]**
- User와 1:N 관계, user_id (Foreignkey)
- 내용 컬럼, 생성 날짜, 업데이트 날짜, 삭제 여부

**[File]**
- Post와 1:N 관계, post_id (Foreignkey)
- 타입(이미지/비디오), 해당 파일의 url 주소 컬럼
- 생성 날짜, 업데이트 날짜, 삭제 여부

**[Like]**
- User와 N:M, Post와 N:M 관계 (ManyToManyField)
- 삭제 여부

**[Comment]**
- User와 N:M, Post와 N:M 관계 (ManyToManyField)
- 생성 날짜, 업데이트 날짜, 삭제 여부 

### ORM 적용해보기
1. 데이터베이스에 해당 모델 객체 3개 넣기
2. 삽입한 객체들을 쿼리셋으로 조회해보기 (단, 객체들이 객체의 특성을 나타내는 구분가능한 이름으로 보여야 함)
3. filter 함수 사용해보기


### 회고
