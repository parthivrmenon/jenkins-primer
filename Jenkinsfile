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
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                python3 src/helloworld.py
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."
                '''
            }
        }
    }
}