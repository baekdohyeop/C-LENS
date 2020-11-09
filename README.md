# C-lens
19.09 ~ 20.01

### Description
C-LENS는 쇼핑을 할 때, 모르는 상품이라도 쉽게 정보를 찾게 도와주는 앱입니다.\
가격표를 찍어서 찍힌 사진 안의 모든 상품정보를 한번에 찾아 보여줍니다.

### Role
서버/안드로이드로 나눠서 2인 팀으로 진행했습니다. Django 기반의 서버를 담당했습니다.

### Tech Stack
java, android, python, django, yolo, tensorflow

### Resources
+ 입력 예시

<img src='http://drive.google.com/uc?export=view&id=13tcqn5EIo0e3MSPhsD2y2WYyors0_zdr' /><br>

+ 결과 예시

<img src='http://drive.google.com/uc?export=view&id=1ihytQ8gc6CbtkW7aFY3n-k7jJqxXg-wE' /><br>

### Description in Detail
- 컴퓨터비전프로그래밍 수업의 팀 프로젝트로 진행했습니다.
- 개인 컴퓨터로 서버를 돌렸고, 현재는 내려간 상태입니다.
- 팀 규모가 작고 주어진 시간이 많지 않았기에, 포괄적인 모든 가격표 그리고 모든 상점에 적용하기에는 어려운 점이 많아 전자가격표가 부착된 매장으로 경우를 제한하여 진행했습니다. 
- Darknet(YOLO) 기반으로 직접 데이터를 촬영, 레이블링, 어그멘테이션하여 모델을 학습시켜 사용했습니다.
- 서버는 앱으로부터 사진을 받아서 사진 내의 가격표들을 탐지하고, 구글 OCR을 이용해 가격표에 적힌 상품정보에서 검색어를 추출합니다. 
이 검색어를 구글 검색, 네이버 검색 등을 통해 보정하고, 네이버쇼핑 API를 사용하여 관련 상품을 조회하여 상품 정보를 전송합니다.
- 앱은 사진을 찍어 http 통신으로 서버로 보내고, 받아온 결과를 보여주는 역할을 합니다. 분석 결과는 네이버쇼핑의 상품링크, 상품명, 이미지 등 입니다. 사진을 누르면 해당 네이버 쇼핑 링크로 이동합니다.
