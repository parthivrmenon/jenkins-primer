pipeline {
    agent { 
        node {
            label 'python-agent'
            }
      }
    // triggers {
    //     pollSCM('*/2 * * * *')
    // }
    stages {

        stage('Build') {
            steps {
                echo 'Building from requirements.txt'
                sh '''
                cd src
                pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                touch report.txt
                python3 src/helloworld.py > report.txt
                '''
            }
        }
    }
    post {
        always {
            echo 'Archiving report...'
            archiveArtifacts artifacts: 'report.txt'
        }
    }
}