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
                touch hello.txt
                python3 src/helloworld.py > report.txt 2>&1
                python3 src/helloworld.py --name Parthiv >> report.txt 2>&1
                python3 src/helloworld.py --name Adarsha >> report.txt 2>&1
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