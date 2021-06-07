#!/usr/bin/groovy

//variables
def DOCKER_USER = "vieskov1980"
def DOCKER_PASSWORD = "xkdPzjUzzXZtgz9"
def WORKSPACE = "/usr/lib/python"                            //"/var/lib/jenkins/jobs/randomcat"

pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

	environment {
		PYTHONPATH = "${WORKSPACE}" // /var/lib/python "${WORKSPACE}" "${GIT_COMMIT}"
	}

    stages {

		//Download code from the repository
		stage("Checkout") {			 
            steps {
                git credentialsId: 'github-ssh-key-micro', url: 'https://github.com/YevhenVieskov/randomcat.git', branch: 'main' 
            }
	    } 
		
		stage("Test - Unit tests") {
			steps { runUnittests() }
		}

        //Building a Docker image with an application
        stage("Build") {
            steps { buildApp() }
		}
        
		//Uploading the  image to the remote Docker repository 
		stage("Push to Docker-repo") {
            steps { pushImage() }
                }

        //Deploying the application from the Docker image on the Dev server 
		stage("Deploy - Dev") {
            steps { deploy('dev') }
		}

		//a) checking if there is already a running container with the specified name and stopping such a container, if it exists
        //b) deleting the container stopped at the previous step
        //c) launching a container based on the image collected in step stage("Build")

        //The name of the container and the port number that is exposed outside (opens for listening on the docker host) depends on the environment
        //Environment: container name, port 

		//Dev: app_dev, 8085
        //Stage:  app_stage, 8086
        //Live: app_live, 8087

		
		//Running UAT Test on Dev Server 		
		stage("Test - UAT Dev") {
            steps { runUAT(8888) }
		}

		//The script sh «tests / runUAT.sh is launched with the positional parameter $ {port}, where instead of
        //the port number is substituted with the port number according to the environment

        
		//Deploying the application from the Docker image built in step stage("Build") on the Stage server
		//(similar to how it was done in step  	stage("Deploy - Dev")

	
        //Deploying the application from the Docker image built in step stage("Build") on the Stage
		// server (similar to how it was done in step stage("Deploy - Dev"))
		stage("Deploy - Stage") {
            steps { deploy('stage') }
		}


        //Running a UAT test on a Stage server (similar to how it was done in step stage("Test - UAT Dev")) 
		stage("Test - UAT Stage") {
            steps { runUAT(88) }
		}

        //Manual confirmation of application deployment on the Live server 
        stage("Approve") {
            steps { approve() }
		}

        //Deploying the application from the Docker image collected in step stage("Build") 
		//on the Live server (similar to how it was done in step stage("Deploy - Dev")) 
        stage("Deploy - Live") {
            steps { deploy('live') }
		}
        
		//Running a UAT test on a Live server (similar to how it was done in step stage("Test - UAT Dev")) 
		stage("Test - UAT Live") {
            steps { runUAT(80) }
		}

	}
}


// steps



def pushImage(){
    withCredentials([usernamePassword(credentialsId: 'docker-login-password-authentification', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) 
                {
				 //https://mydocker.repo.servername	
                 sh "docker login --username ${DOCKER_USER} --password ${DOCKER_PASSWORD}  https://hub.docker.com/repository/docker/vieskov1980/randomcat "
                 sh "docker push vieskov1980/randomcat:${BUILD_ID}"
				 
                }
}

def buildApp() {
	dir ('mnist-flask-app' ) {
		//def appImage = docker.build("mydocker.repo.servername/myapp:${BUILD_NUMBER}")
		def appImage = docker.build("randomcat:${BUILD_NUMBER}")
	}
}


def deploy(environment) {

	def containerName = ''
	def port = ''

	if ("${environment}" == 'dev') {
		containerName = "app_dev"
		port = "8888"
	} 
	else if ("${environment}" == 'stage') {
		containerName = "app_stage"
		port = "88"
	}
	else if ("${environment}" == 'live') {
		containerName = "app_live"
		port = "80"
	}
	else {
		println "Environment not valid"
		System.exit(0)
	}

	sh "docker ps -f name=${containerName} -q | xargs --no-run-if-empty docker stop"
	sh "docker ps -a -f name=${containerName} -q | xargs -r docker rm"
	sh "docker run -d -p ${port}:5000 --name ${containerName} randomcat:${BUILD_ID}"

}


def approve() {

	timeout(time:1, unit:'DAYS') {
		input('Do you want to deploy to live?')
	}

}


def runUnittests() {
	sh "pip3 install --no-cache-dir -r ./requirements.txt"
	sh "python3 ./tests/test_flask_app.py"
}


def runUAT(port) {
	sh "./tests/runUAT.sh ${port}"
}
