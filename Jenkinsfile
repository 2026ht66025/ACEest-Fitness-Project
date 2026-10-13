pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv-ci
                    . .venv-ci/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . .venv-ci/bin/activate
                    flake8 app.py tests --select=E9,F63,F7,F82
                    flake8 app.py tests
                '''
            }
        }

        stage('Pytest') {
            steps {
                sh '''
                    mkdir -p reports
                    . .venv-ci/bin/activate
                    pytest -v --junitxml=reports/pytest.xml
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-fitness:${BUILD_NUMBER} .'
            }
        }

        stage('Pytest Inside Docker') {
            steps {
                sh '''
                    docker run --rm --entrypoint python \
                    aceest-fitness:${BUILD_NUMBER} -m pytest -v
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'reports/pytest.xml'
        }
    }
}
