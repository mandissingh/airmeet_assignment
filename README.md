# Containerized Rest API for metrics

Following application is running using **python flask** framework, it's using **redis** to store data in memory.

## Following repo contains following fles
- api.py (Contains all the code and logic)
- requirements.txt (Contains dependencies required by python code)
- Dockerfile (Dockerfile to build docker image to run python code)
- docker-compose.yml (docker-compose file to run containers)

## Please follow following steps run the application:

- Clone the repository to your system or server.
- `cd <repo_dir>`
- `docker-compose up`
- Application should now be runnning on port 8080 of you localhost.

## Use below curl command to inject metrics:

`curl -XPOST -H "Content-Type: application/json" --data '{"percentage_cpu_used": 55, "percentage_memory_used": 60}' http://localhost:8080/metrics`

## Use below curl command to get stored metrics:

`curl -XGET -H "Content-Type: application/json" http://localhost:8080/report`


