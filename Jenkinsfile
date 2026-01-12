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

        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest
                '''
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

    post {
        success {
            withCredentials([string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')]) {
                sh '''
                    curl -X POST -H "Content-type: application/json" \
                    --data '{
                      "text": "✅ Pipeline SUCCESS\\n📦 Deploy OK"
                    }' $SLACK_URL
                '''
            }
        }

        failure {
            withCredentials([string(credentialsId: 'slack-webhook', variable: 'SLACK_URL')]) {
                sh '''
                    curl -X POST -H "Content-type: application/json" \
                    --data '{
                      "text": "❌ Pipeline FAILED"
                    }' $SLACK_URL
                '''
            }
        }
    }
}
