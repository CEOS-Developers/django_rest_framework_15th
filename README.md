# 2주차 과제
## Docker란?
도커는 컨테이너를 기반으로 하여 독립적으로 애플리케이션을 실행할 수 있도록 컨테이너를 만들고 관리하는 것을 도와주는 도구입니다.

### VM 과의 차이점
![docker.com](https://images.velog.io/images/offsujin/post/5958876c-6eef-4aaf-9d62-c0cd227df6e1/VMdocker.png)

오른쪽에 보이는 VM은 호스트 OS 위에 게스트 OS를 가상화하여 사용하기 때문에 오버헤드가 많아지고 속도문제가 발생하게 됩니다.

하지만 왼쪽과 같은 Docker는 호스트 OS 위에 게스트 OS를 분리하는 것이 아니라, 프로세스를 분리하여 사용합니다.

따라서 VM 처럼 완전히 분리된 환경을 이루면서도 오버헤드를 줄일 수 있습니다.

## image와 container
![생활코딩](https://images.velog.io/images/offsujin/post/2676d4dd-074c-4884-afe2-8682c058247d/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.04.01.png)

**docker hub**는 우리가 사용하는 app store처럼 다양한 프로그램들을 다운로드, 업로드 할 수 있는 공간입니다.

**image**는 app store에서 다운받는 프로그램과 같은 의미입니다.

**container**는 프로그램에서 실행하는 프로세스라고 볼 수 있습니다.

하나의 이미지에서 여러 개의 컨테이너를 생성할 수 있고, 각각의 컨테이너는 독립된 환경을 가지고 있기 때문에 서로 영향을 받지 않습니다.

## image pull
docker hub에서 이미지를 다운받는 것을 pull이라고 합니다.

https://hub.docker.com/
위의 docker hub 사이트에 접속하면 다양한 이미지들을 확인할 수 있습니다.

![](https://images.velog.io/images/offsujin/post/46c17bd9-ed2c-4002-9a88-db856f92ab92/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.30.16.png)

`docker pull httpd` 명령어를 사용해서 아파치 웹 서버 이미지를 pull 해보겠습니다.

`docker images` 로 아래처럼 이미지가 잘 받아졌는지 확인할 수 있습니다.

![](https://images.velog.io/images/offsujin/post/62a117c6-a040-497e-85a3-0c73d082a82b/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.36.58.png)

## container
### 생성
![](https://images.velog.io/images/offsujin/post/dbd8b65d-b376-4629-a5d3-dbbd0c61159d/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.40.19.png)

`docker run httpd`

### 실행 중인 container
컨테이너가 제대로 만들어졌는지 확인하려면 ps 라는 명령어를 이용합니다.
![](https://images.velog.io/images/offsujin/post/31d0ab1c-d02f-417f-ba33-078d756dad5c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.41.19.png)
위의 결과처럼 httpd 이미지로 컨테이너가 하나 만들어진 것을 확인할 수 있습니다.

### 이름 지정
docs에서 option 카테고리에 가보면 다양한 옵션을 찾을 수 있습니다.
![](https://images.velog.io/images/offsujin/post/8972ed5e-7f17-40c0-a757-ac759d19f54c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.43.24.png)
그 중 --name 이라는 옵션을 주면 컨테이너의 이름을 지정할 수 있습니다.

만약 컨테이너 이름을 web-server라고 하고싶다면 명령어는 다음과 같습니다.

`docker run --name web-server httpd`

### 실행 중지
`docker stop web-server`를 이용해서 컨테이너를 끌 수 있습니다.

`ps` 명령어를 이용해서 컨테이너가 실행되고 있는지 확인합니다.

![](https://images.velog.io/images/offsujin/post/b91e4180-221a-401d-b92d-bf425ac77552/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.52.00.png)

컨테이너 리스트에서 ws1 컨테이너가 사라진 것을 확인했습니다.

### 재실행
이미 만들어놓은 컨테이너를 다시 시작하고 싶다면 `start` 를 사용합니다.

`docker start web-server`

`ps` 명령어에 `-a` 옵션을 지정하면 지금까지 만들어둔 사용가능한 컨테이너를 확인할 수 있습니다.
![](https://images.velog.io/images/offsujin/post/e28db155-4c18-409c-97b5-4d342dfd0951/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202022-02-01%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%209.55.22.png)

제가 stop시킨 ws1도 있습니다.

### 삭제
컨테이너를 지우고 싶다면 `rm`을 사용합니다.

`docker rm ws1`

간혹 에러가 뜨고 제대로 삭제되지 않는 경우가 있습니다.

이럴 때에는 `--force` 옵션을 주면 강제로 삭제할 수 있습니다.

### images 삭제

이미지는 `rmi` 라는 명령어로 삭제할 수 있습니다.

`docker rmi httpd`

## 명령어 정리

`docker pull IMAGE` : IMAGE pull

`docker rmi IMAGE` : IMAGE 삭제

`docker images` : IMAGE 리스트 보기

`docker run --name CNAME IMAGE` : IMAGE를 CNAME이라는 이름으로 컨테이너 생성

`docker ps -a` : 존재하는 컨테이너 리스트 보기

`docker ps` : 실행 중인 컨테이너 리스트 보기

`docker stop CONTAINER` : 컨테이너 실행 중지

`docker start CONTAINER` : 컨테이너 실행

