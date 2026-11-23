
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

        stage('Pytest and Coverage') {
            steps {
                sh '''
                    mkdir -p reports
                    . .venv-ci/bin/activate

                    pytest -v \
                        --junitxml=reports/pytest.xml \
                        --cov=app \
                        --cov-report=xml:coverage.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('ACEest-SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=ACEest-Fitness \
                                -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        set +x

                        docker build \
                            -t aceest-fitness:${BUILD_NUMBER} \
                            -t ${DOCKERHUB_USER}/aceest-fitness:${BUILD_NUMBER} \
                            -t ${DOCKERHUB_USER}/aceest-fitness:latest .

                        echo "$DOCKERHUB_TOKEN" | docker login \
                            -u "$DOCKERHUB_USER" --password-stdin

                        docker push ${DOCKERHUB_USER}/aceest-fitness:${BUILD_NUMBER}
                        docker push ${DOCKERHUB_USER}/aceest-fitness:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Pytest Inside Docker') {
            steps {
                sh '''
                    docker run --rm --entrypoint python \
                        aceest-fitness:${BUILD_NUMBER} \
                        -m pytest -v
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                testResults: 'reports/pytest.xml'

            archiveArtifacts(
                artifacts: 'coverage.xml,reports/pytest.xml',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'ACEest Fitness CI pipeline completed successfully!'
        }

        failure {
            echo 'ACEest Fitness CI pipeline failed. Check the stage logs.'
        }
    }
}
