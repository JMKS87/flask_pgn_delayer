docker rm $(docker stop $(docker ps -a -q --filter ancestor=flask_pgn_delayer --format="{{.ID}}"))
docker build -t flask_pgn_delayer .
docker run -d -p 80:5000\
  --name flask_pgn_delayer --restart unless-stopped flask_pgn_delayer
