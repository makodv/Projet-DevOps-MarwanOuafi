pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python & venv') {
            steps {
                dir('.') {
                    sh '''
                        set -e
                        apt-get update
                        apt-get install -y python3 python3-venv python3-pip

                        python3 -m venv venv
                        . venv/bin/activate

                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run tests') {
            steps {
                dir('.') {
                    sh '''
                        . venv/bin/activate
                        pytest
                    '''
                }
            }
        }

    }

 stage('Archive') {
            steps {
                archiveArtifacts artifacts: '**/*', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f devops-app || true
                    docker build -t devops-app .
                    docker run -d --name devops-app devops-app
                '''
            }
        }
    }
  
 
       

