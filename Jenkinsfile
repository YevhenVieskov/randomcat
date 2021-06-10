#!/usr/bin/groovy

//variables
def DOCKER_USER = "vieskov"
def DOCKER_PASSWORD = "xxxx"
def WORKSPACE = "/usr/lib/python"                            //"/var/lib/jenkins/jobs/randomcat"
def remote = [name:"ubuntu", host: "52.14.77.84", user: "ubuntu", identityFile: "vieskovtf.pem", allowAnyHosts: "true" ]

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
			agent { docker { image 'python:3.5-alpine' } }
			stages{
				stage("Build Python image"){
					steps{
						withEnv(["HOME=${env.WORKSPACE}"]) {
						    sh "python -m pip install --user --no-cache-dir -r requirements.txt "
						}
					}

					/*post {
                        cleanup {
                            cleanWs()
                        }
                    }*/
				}

				stage("Perform Unit Tests") {
					steps{
						withEnv(["HOME=${env.WORKSPACE}"]) {
						    sh "python test_flask_app.py"
						}
					}

					post {
						always {
							//sh 'ln -s tests/test-results-unit.xml $WORKSPACE'
							//junit "**/test-reports/*.xml"
							junit(
                                allowEmptyResults: true,
                                testResults: '**/test-reports/*.xml'
                            )
						}
					}
				}

			}
			//steps { runUnittests() }
		}

        //Building a Docker image with an application
        stage("Build") {
            steps { buildApp() }
		}
        
		//Uploading the  image to the remote Docker repository 
		/*stage("Push to Docker-repo") {
            steps { pushImage() }
                }*/

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
        //Prod: app_prod, 8087

		
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

        //Manual confirmation of application deployment on the Prod server 
        stage("Approve") {
            steps { approve() }
		}

        //Deploying the application from the Docker image collected in step stage("Build") 
		//on the Prod server (similar to how it was done in step stage("Deploy - Dev")) 
       
	    stage ("Save image") {
			steps {
			    sh "docker image save -o ~/app.tar randomcat:${BUILD_NUMBER}"
			}
		}

		/*stage ("Copy image to remote server") {
			steps {
			    //sh "scp -r ~/app.tar ubuntu@52.14.77.84: /home/ubuntu/"
				//sshPublisher(publishers: [sshPublisherDesc(configName: 'SERVER_NAME', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'apt-get update', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '*.war')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
				}
		}*/	
			
           
		withCredentials([sshUserPrivateKey(credentialsId: 'vieskovtf', keyFileVariable: '~/.ssh/vieskovtf.pem', passphraseVariable: '', usernameVariable: 'ubuntu')]) {
                
            stage("SSH copy image to prod") {
                steps{   
                
				    sshPut remote: remote, from: '~/app.tar', into: '~/'
					 //writeFile file: 'abc.sh', text: 'ls'
                    //sshCommand remote: remote, command: 'for i in {1..5}; do echo -n \"Loop \$i \"; date ; sleep 1; done'
                    //sshGet remote: remote, from: 'abc.sh', into: 'bac.sh', override: true
                    //sshScript remote: remote, script: 'abc.sh'
                    //sshRemove remote: remote, path: 'abc.sh'
				}
            }
        }
			

		withCredentials([sshUserPrivateKey(credentialsId: 'vieskovtf', keyFileVariable: '~/.ssh/vieskovtf.pem', passphraseVariable: '', usernameVariable: 'ubuntu')]) {

            stage("Deploy - prod") {
                steps { 
                    sshCommand remote: remote, command: 'docker load -i ~/app.tar'
                    sshCommand remote: remote, command: 'docker run -d -p 80:5000 randomcat:${BUILD_NUMBER}'               
                } 
            }

		}

        /*stage("Deploy - prod") {
           steps { 
				deploy('prod')  //randomcat:${BUILD_ID}
				}
		}*/
        
		//Running a UAT test on a Prod server (similar to how it was done in step stage("Test - UAT Dev")) 
		stage("Test - UAT prod") {
            steps { runUAT(80) }
		}

	}
}


// steps



def pushImage(){
    withCredentials([usernamePassword(credentialsId: 'docker-login-password-authentification', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASSWORD')]) 
                {
				 //https://mydocker.repo.servername	 https://hub.docker.com/repository/docker/vieskov1980/randomcat
                 sh "docker login --username ${DOCKER_USER} --password ${DOCKER_PASSWORD}"
                 sh "docker push vieskov1980/randomcat:${BUILD_ID}"
				 
                }
}

def buildApp() {
	//dir ('randomcat' ) {
		//def appImage = docker.build("mydocker.repo.servername/myapp:${BUILD_NUMBER}")
	//	def appImage = docker.build("randomcat:${BUILD_NUMBER}")
	//}
	sh"docker build -t randomcat:${BUILD_NUMBER} ."
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
	else if ("${environment}" == 'prod') {
		containerName = "app__prod"
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
		input('Do you want to deploy to production?')
	}

}


def runUnittests() {
	
    //sh"export WORKSPACE=`pwd`"
	//python3 -m pip install --user virtualenv
	//sh "pip3 install --user virtualenv"
    //sh"virtualenv testenv -p /usr/bin/python3"
    //sh"python3 -m venv testenv"  //!
    //sh"source testenv/bin/activate" //!
	//sh "pip3 install --no-cache-dir -r ./requirements.txt"	
	//sh "cd /var/lib/jenkins/workspace/randomcat/"
	//sh "python3  ./test_flask_app.py"
	//sh "deactivate"
	//sh "exit"
	sh "chmod +x -R ${env.WORKSPACE}"
	sh "./tests/runUT.sh"
	

	
	
}


def runUAT(port) {
	sh "chmod +x -R ${env.WORKSPACE}"
	sh "./tests/runUAT.sh ${port}"
}