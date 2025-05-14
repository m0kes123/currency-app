node {

    def tag = env.BUILD_NUMBER
    def helmReleaseName = "currency-app"
    def chartPath = "/currency-app/currency-app"
    def helmRepoUrl = "https://raw.githubusercontent.com/m0kes123/currency-app-helm/main/"

    try{
        stage('Checkout') {
            checkout scm
        }

        stage('Build Docker Image') {
            script {
                sh "docker build -t m0kes/yadro:${tag} ."
            }
        }

        stage('Hadolint') {
            sh """
                docker run --rm -i hadolint/hadolint < Dockerfile
            """
        }

        stage('Set Build Description') {
            script {
                currentBuild.description = "To pull the Docker image, run: docker pull m0kes/yadro:${tag}"
            }
        }
        

        stage('Push Docker Image') {
            script {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_TOKEN')]) {
                    sh '''
                        echo ${DOCKER_TOKEN} | docker login -u ${DOCKER_USERNAME} --password-stdin
                    '''
                    sh """
                        docker push m0kes/yadro:${tag}
                    """
                }
            }
        }

    // stage('Deploy') {
    //     script {
    //         sh 'docker compose up -d'
    //     }
    // }
        
        stage('Helm Deploy') {
            script {
                withCredentials([file(credentialsId: 'k3s-kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        export KUBECONFIG=${KUBECONFIG}
                    """
                    sh """
                        helm repo list | grep myrepo || helm repo add myrepo ${helmRepoUrl}
                        helm repo update
                    """
                    sh """
                        helm upgrade --install ${helmReleaseName} myrepo/currency-app \
                        --set app.image.tag=${tag} \
                        --atomic \
                        --cleanup-on-fail
                    """
                }
            }
        }
    } finally{
        stage('Cleanup') {
            cleanWs()
            sh 'docker logout || true'
            sh 'docker stop cur_app_cont'
            sh 'docker system prune -af'
        }
    }
}