# Интеграция Jenkins в проект

Этот документ описывает Jenkins Pipeline, определённый в предоставленном Jenkinsfile. Пайплайн автоматизирует процесс сборки, публикации и развёртывания Docker-образа.

## Ход создания pipeline

### 1. Установка Java, Jenkins и Docker на виртуальную машину

### 2. Скачивание дополнительных плагинов для Jenkins

### 3. Создание mulibranch pipeline и настройка связи Jenkins с GitLab

### 4. Настройка связи Jenkins с DockerHub

## Подробное описание этапов

### 1. Этап получения кода

```
stage('Checkout') {
    checkout scm
}
```

Этот этап загружает исходный код из системы контроля версий, а точнее из удаленного репозитория проекта на GitLab.

### 2. Этап сборки Docker-образа

```
stage('Build Docker Image') {
    script {
        sh "docker build -t m0kes/yadro:${tag} ."
    }
}
```

### 3. Этап установки описания образа

```
stage('Hadolint') {
    sh """
        docker run --rm -i hadolint/hadolint < Dockerfile
    """
}
```

Этот этап выполняет статический анализ Dockerfile с использованием утилиты Hadolint. Hadolint проверяет Dockerfile на наличие ошибок, уязвимостей и нарушений лучших практик.

Команда ```docker run --rm -i hadolint/hadolint < Dockerfile``` запускает контейнер с утилитой Hadolint. Опция --rm автоматически удаляет контейнер после завершения его работы. Опция -i позволяет передать содержимое Dockerfile в контейнер через стандартный ввод (stdin).

### 4. Этап установки описания образа

```
stage('Set Build Description') {
    script {
        currentBuild.description = "To pull the Docker image, run: docker pull m0kes/yadro:${tag}"
    }
}
```

Этот этап добавляет описание к текущей сборке в Jenkins. Описание содержит команду для загрузки собранного Docker-образа.

Внутри блока script используется переменная ```currentBuild.description```, которая позволяет задать текстовое описание для текущей сборки. Это описание содержит команду для загрузки Docker-образа:
```docker pull m0kes/yadro:latest```.

### 5. Этап публикации образа

```
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
```

Этот этап публикует собранный Docker-образ в Docker Hub.
Пайплайн использует учётные данные Jenkins (dockerhub-creds) для безопасного хранения логина и токена Docker Hub.

Блок ```withCredentials``` связывает учётные данные с переменными окружения (DOCKER_USERNAME и DOCKER_TOKEN). Для его изспользования для Jenkins необходим плагин Credentials Binding Plugin.

Команды:

1. Команда ```echo $DOCKER_TOKEN | docker login -u $DOCKER_USERNAME --password-stdin``` выполняет вход в Docker Hub с использованием предоставленных учётных данных.

2. Команда ```docker push m0kes/yadro:latest``` публикует Docker-образ в Docker Hub.

### 6. Этап развёртывания

```
stage('Deploy') {
    script {
        sh 'docker compose up -d'
    }
}
```
Этот этап развёртывает приложение с помощью Docker Compose.

Команда ```docker compose up -d``` запускает Docker-контейнер, определённыq в файле docker-compose.yml

### 7. Этап очистки

```
    stage('Cleanup') {
        cleanWs()
        sh 'docker logout || true'
        sh 'docker stop cur_app_cont'
        sh 'docker system prune -af'
    }
```
Этот этап выполняет очистку рабочего пространства и завершает сессию Docker.

Команды:

1. Команда ```cleanWs()``` удаляет все файлы и директории, созданные в процессе выполнения сборки, в рабочей директории Jenkins.

2. Команда ```sh 'docker logout || true``` выполняет выход из Docker Hub. Это важно для безопасности, чтобы не оставлять активные сессии с учётными данными. Добавление ```|| true``` гарантирует, что этап не завершится с ошибкой, даже если команда docker logout не выполнится.

3. Команда ```sh 'docker stop cur_app_cont'``` выполняет остановку раннее созданного контейнера.

4. Команда ```sh 'docker system prune -af'``` удаляет все неиспользуемые контейнеры и образы.
---

**Автор** MaximAntropov