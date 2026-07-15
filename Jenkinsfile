pipeline {
    agent { 
        node {
            label 'python-agent'
            }
      }
    triggers {
        pollSCM('*/2 * * * *')
    }
    stages {
        stage('Build') {
            steps {
                echo 'Build....'
                sh '''
                cd src
                pip install -r requirements.txt
                pip freeze
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                python3 src/helloworld.py
                python3 src/helloworld.py --name Parthiv
                '''
            }
        }
    }
}