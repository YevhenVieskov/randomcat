# prefix commands with sudo if user is not in docker group
# build docker image
docker build -t randomcat .

# check docker image
docker images | grep randomcat

# run docker container
docker run -p 8888:5000 --name randomcat 
