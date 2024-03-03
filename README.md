## buildコマンド
$ docker build -t hackit_terayuki .

## RUNコマンド
docker run -p 8501:8501 -v $(pwd)/app:/app hackit_terayuki