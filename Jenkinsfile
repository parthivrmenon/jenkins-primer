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
                cleanWs()
                echo "Testing.."
                sh '''
                touch report.txt
                ls -l
                python3 src/helloworld.py > report.txt
                '''
            }
        }
    }
    // post {
    //     always {
    //         echo 'Archiving report...'
    //         archiveArtifacts artifacts: 'hello.txt'
    //     }
    // }
}