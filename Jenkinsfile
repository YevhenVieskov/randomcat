#!/usr/bin/groovy

//variables
def DOCKER_USER = "vieskov"
def DOCKER_PASSWORD = "xxxx"
def WORKSPACE = "/usr/lib/python"                            //"/var/lib/jenkins/jobs/randomcat"
def IP_DEPLOY = "52.14.158.47"
def IP_JMASTER = "18.117.238.202"
def IP_JSLAVE = "18.117.196.122"
def PATH_KEY ="/home/ubuntu/.ssh/vieskovtf.pem"
/*def remote = [name:"ubuntu", host: "52.14.77.84", user: "ubuntu", identityFile: "vieskovtf.pem", allowAnyHosts: "true" ]*/

properties([pipelineTriggers([githubPush()])])

pipeline {
    agent { label "Slave1" }   //any

    options {
        disableConcurrentBuilds()
    }

	environment {
		PYTHONPATH = "${WORKSPACE}" // /var/lib/python "${WORKSPACE}" "${GIT_COMMIT}"
		MY_PROD_CRED = credentials('ssh-prod')
		registry = "vieskov1980/randomcat" 
        registryCredential = 'ssh-dockerhub' 
        dockerImage = '' 

	}

    stages {

		//Download code from the repository
		stage("Checkout") {			 
            steps {
                git credentialsId: 'github-ssh-key', url: 'https://github.com/YevhenVieskov/randomcat.git', branch: 'main' 
            }
	    } 
		
		stage("Build Image - Unit tests") {
			agent { docker { image 'python:3.5-alpine' } }
			stages{
				stage("Build Python image"){
					steps{
						withEnv(["HOME=${env.WORKSPACE}"]) {
						    sh "python -m pip install --user --no-cache-dir -r requirements.txt "
						}
					}
					
				}

				stage("Perform Unit Tests") {
					steps{
						withEnv(["HOME=${env.WORKSPACE}"]) {
						    sh "python test_flask_app.py"
						}
					}

					post {
						always {
							
							junit(
                                allowEmptyResults: true,
                                testResults: '**/test-reports/*.xml'
                            )
							
						}
					}
				}

			}
			
		}

        //Building a Docker image with an application
        stage("Build") {
            steps { 
				//buildApp() 
				script {
					dockerImage=docker.build registry + ":$BUILD_NUMBER"
				}
			}
		}

		stage("Deploy image on dockerhub")
		{
			steps{
				script{
					docker.withRegistry('', registryCredential) {
						dockerImage.push()
					}
				}
			}
		}

		//Deploying the application from the Docker image on the Dev server 
		stage("Run - Dev") {
            steps { deploy('dev') }
		}

			
			
		stage("Test - UAT Dev") {
            steps { runUAT(80) }
		}

				

        //Manual confirmation of application deployment on the Prod server 
        stage("Approve") {
            steps { approve('Do you want to deploy to production?') }
		}

		stage("Clean up  Jenkins server")
		{
			steps{
				sh  '''#!/bin/bash
				       docker stop $(docker ps -a -q) 2> /dev/null || true
					   docker rm -f $(docker ps -a -q) 2> /dev/null || true
					   docker rmi -f $(docker images -a -q) 2> /dev/null || true
					   yes | docker system prune -f 2> /dev/null || true
					'''				

			}
			
		}

		stage("Clean up  Jenkins slave")
		{
			steps{
				//    /^randomcat:[0-9]{1,10000}$/
				sshagent(credentials : ['ssh-prod']) {
					sh  '''#!/bin/bash					       
						   ssh -o "StrictHostKeyChecking=no" ubuntu@18.117.196.122 'docker stop $(docker ps -a -q) 2> /dev/null || true'
                           ssh -o "StrictHostKeyChecking=no" ubuntu@18.117.196.122 'docker rm -f $(docker ps -a -q) 2> /dev/null || true'
	                       ssh -o "StrictHostKeyChecking=no" ubuntu@18.117.196.122 'docker rmi -f $(docker images -a -q) 2> /dev/null || true'				    
				           ssh -o "StrictHostKeyChecking=no" ubuntu@18.117.196.122 'yes | docker system prune -f 2> /dev/null || true'				                   
				           
				        '''	
				
			    }
			}
			
		}

       		
		//Clean old docker images on production server		
		stage("Clean up  production server")
		{
			steps{
				//    /^randomcat:[0-9]{1,10000}$/
				sshagent(credentials : ['ssh-prod']) {
					sh  '''#!/bin/bash					                   
				           ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'docker stop $(docker ps -a -q) 2> /dev/null || true'
                           ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'docker rm -f $(docker ps -a -q) 2> /dev/null || true'
	                       ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'docker rmi -f $(docker images -a -q) 2> /dev/null || true'				    
				           ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'yes | docker system prune -f 2> /dev/null || true'
				        '''	
				
			    }
			}
			
		}

        

       stage("Pull image from dockerhub on prod")
		{
			steps{
                sshagent(credentials : ['ssh-prod']) {                    
					
					//sh "ssh -i ${PATH_KEY} ubuntu@${IP_DEPLOY}  docker pull ${registry}:${BUILD_NUMBER}"
					sh "ssh -o StrictHostKeyChecking=no ubuntu@${IP_DEPLOY} uptime"
                    sh "ssh -v ubuntu@${IP_DEPLOY}"
					sh "ssh  ubuntu@${IP_DEPLOY}  docker pull ${registry}:${BUILD_NUMBER}"
                }
            }
		}

		stage ("Run - prod") {
            steps{
                sshagent(credentials : ['ssh-prod']) {                    
					
					sh "ssh -o StrictHostKeyChecking=no ubuntu@${IP_DEPLOY} uptime"
                    sh "ssh -v ubuntu@${IP_DEPLOY}"					
					sh "ssh  ubuntu@${IP_DEPLOY}  docker run -d -p 8080:5000 ${registry}:${BUILD_NUMBER}"
					
                }
            }
        }
    

	    stage("Approve stop application and cleanup prod") {
            steps { approve('Do you want to destroy application?') }
		}

		stage("Clean up prod after stop app ")
		{
			steps{
				//    /^randomcat:[0-9]{1,10000}$/
				sshagent(credentials : ['ssh-prod']) {
					sh  '''#!/bin/bash					                   
				           ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'docker stop $(docker ps -a -q) 2> /dev/null || true'
                           ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'docker rm -f $(docker ps -a -q) 2> /dev/null || true'
	                       ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'docker rmi -f $(docker images -a -q) 2> /dev/null || true'				    
				           ssh -o "StrictHostKeyChecking=no" ubuntu@52.14.158.47 'yes | docker system prune -f 2> /dev/null || true'
                           
				        '''	
				
			    }
			}
			
		}
 
	}
}


def buildApp() {
	
	sh"docker build -t randomcat:${BUILD_NUMBER} ."
}


def approve(msg) {

	timeout(time:1, unit:'DAYS') {
		input(msg)     //'Do you want to deploy to production?'
	}
}


def runUnittests() {	   
	sh "chmod +x -R ${env.WORKSPACE}"
	sh "./tests/runUT.sh"
}

//accessibility test
def runUAT(port) {
	sh "chmod +x -R ${env.WORKSPACE}"
	sh "./tests/runUAT.sh ${port}"
}

def deploy(environment) {
 
        def containerName = ''
        def port = ''
 
        if ("${environment}" == 'dev') {
                containerName = "app_dev"
                port = "80" //8085
        }         
        
        
        
        else {
                println "Environment not valid"
                System.exit(0)
        }
 
        sh "docker ps -f name=${containerName} -q | xargs --no-run-if-empty docker stop"
        sh "docker ps -a -f name=${containerName} -q | xargs --no-run-if-empty docker rm"
        sh "docker run -d -p ${port}:5000 --name ${containerName} ${registry}:${BUILD_NUMBER}"
}