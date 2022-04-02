#### CEOS 15기 백엔드 스터디 (2) 모델링 및 drf 연습을 위한 레포


---
# 2. Docker

<details>
<summary> </summary>
<div markdown="1">       

## Docker

## 'Docker file', 'Docker-image', 'Docker-container' 
  ![92180EDC-95C4-4CAF-B9E1-13307D9AE09A](https://user-images.githubusercontent.com/77188666/160082911-846ce296-23c1-4351-a0e7-de671be024ae.jpeg)

### (1) Dockerfile 이란?
- 필요한 최소한의 패키지를 설치하고 동작하기 위한 자신만의 설정을 담은 파일.
- 이 파일로 이미지를 생성(빌드)함

**존재이유**
- 매번 애플리케이션을 동작하는 환경을 구성하기 위해 -> `패키지 설치`,  `환경설정 과정`을 반복하는 것이 불편
- `컨테이너`에 설치하는 `패키지`,`소스코드`,`명령어`,`환경변수설정` 등을 기록한 하나의 파일 `Dockerfile`을 통해 `환경변수 및 셋팅 값 명시화`
- `Dockerfile` 빌드-> 자동`Dockerimage` 생성 -> 애플리케이션 빌드/배포 자동화

.

### (2) Docker Image 란?
- 도커 컨테이너를 구성하는 파일 시스템과 실행한 애플리케이션 설정을 하나로 합친 것  
(Docker container를 생성하는 템플릿)
- 도커 이미지는 도커 컨테이너를 생성하기 위해 반드시 필요한 파일!
- 파일명을 `Dockerfile`로 저장하면, - docker가 호출한 디렉토리 내 `Dockerfile`로 저장되어 있는 파일로 컨테이너를 생성함
- 도커 이미지는 `레이어 저장방식`으로 컨테이너를 실행하기 위한 모든 정보를 가지고 있어 용량이 큼

.

## Docker의 장점
- **쉬운 컨트롤**
- **경량화**
- **CI/CD**

#### 경량화
- VM처럼 하드웨어 emulation 기반 virtualization 과 달리 `커널을 직접 컨트롤`하는 `container`기반 `Docker`는 리소스와 기능이 제한되어 있는 환경에서도 배포 가능하도록 경량화된 application 제공

#### CI/CD
- 지속적인 통합과 자동 배포를 진행하기 위해서 서비스 운영 환경을 패키징 하는 것

### Docker Compose ?
- `다중 컨테이너` 도커 애플리케이션을 정의하고 동작하게 해주는 툴.
- 'YAML`파일로 작성( 작성된 yaml 파일로 모든 서비스들을 생성하고 시작을 하나의 명령어로 실행 )

#### docker-compose.yml
![A2C3D26E-1D1A-4068-9462-C8719AA225A4](https://user-images.githubusercontent.com/77188666/160082978-dfc08651-c3e5-471d-b4e0-8ba07daf7b45.jpeg)
  
---

</div>
</details>

---
# 3. Instagram Data Modeling

<details>
<summary> </summary>
<div markdown="1">     
  
### Django-MySQL 
- img1
- img2
- img3
- img4

### ERD (using ERDCloud)
![CEOS15](https://user-images.githubusercontent.com/77188666/160993717-d5db4812-5d7c-400d-9075-8b9d77481bb1.png)


### Django Model Data Type

####
|Data type|Django model type|Database MySQL DDL|Description - Validation - Notes|
|---|---|---|---|
|Boolean|models.BooleanField()|bool NOT NULL|Creates a boolean field to store True/False (or 0/1) values|
|Date/time|models.DateField()|date NOT NULL|Creates a date field to store dates|
|Date/time|models.DateTimeField()|datetime NOT NULL|Creates a datetime field to store dates with times|
|Number|models.AutoField()|integer AUTO_INCREMENT NOT NULL|Creates an integer that autoincrements, primarly used for custom primary keys|
|Number|models.IntegerField()|integer NOT NULL|Creates a column to store integer numbers.|
|Number|models.DecimalField(decimal_places=X,max_digits=Y)|numeric(X, Y) NOT NULL|Enforces a number have a maximum X digits and Y decimal points Creates a decimal field to store decimal numbers.|
|Text|models.CharField(max_length=N)|varchar(50) NOT NULL|Creates a text column, where the max_length argument is required to specify the maximum length in characters.|
|Text (Specialized)|models.FileField()|varchar(100) NOT NULL|Enforces and provides various utilities to handle files.|


### How to Upload Files With Django  
https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html  

```
id = models.BigIntegerField()
id = models.AutoField(primary_key=True)     # Automatic primary key
```

</div>
</details>
