# Развёртка приложения в Kubernetes

Этот документ описывает процесс разворачивания приложения в кластере.

## Ход выполнения задачи

### 1. Написание манифеста для подов с приложением

```yml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: currency-app
  labels:
    app.kubernetes.io/name: test-release
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: test-release
  template:
    metadata:
      labels:
        app.kubernetes.io/name: test-release
    spec:
      containers:
        - name: currency-app
          image: m0kes/yadro:latest
          imagePullPolicy: Always
          resources:
            limits:
              cpu: 500m
              memory: 384Mi
            requests:
              cpu: 250m
              memory: 192Mi
          ports:
            - containerPort: 8000
          env:
            - name: HOST
              value: 0.0.0.0
```

Мною был выбран DaemonSet вместо Deployment с указанием replicas с целью обеспечения отказоустойчивости. Демонсет гарантирует наличие пода с приложением на каждой ноде-воркере, в моем случае мастер-нода так же является воркером. Таким образом, при отключении одной из нод (если это не мастер-нода), приложение останется доступным за счет подов на двух других нодах.

### 2. Написание манифеста для сервиса

```yml
apiVersion: v1
kind: Service
metadata:
  name: currency-service
  labels:
    app.kubernetes.io/name: test-release
spec:
  ports:
    - name: http
      port: 8000
      protocol: TCP
      targetPort: 8000
  selector:
    app.kubernetes.io/name: test-release
  type: ClusterIP
status:
  loadBalancer: {}
```

### 3. Написание манифеста для ингресса

```yml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: currency-ingress
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: currency-service
            port:
              number: 8000
```

### 4. Создание домена

Аренда домена app-currency.online на рег.ру, чтобы доступ к приложению был возможен "снаружи", из интернета.

### 5. Аренда виртуальной машины для внешнего балансировщика

На Yandex Cloud была арендована ВМ на который был установлен и сконфигурирован NGINX.
Также были получены сертификаты для возможности соединения по https.

Финальная конфигурация NGINX:

```
server {
  listen 443 ssl;
  server_name app-currency.online;
  ssl_certificate /etc/nginx/ssl/fullchain.cer;
  ssl_certificate_key /etc/nginx/ssl/app-currency.online.key;
  location / {
    proxy_set_header X-Real-IP $remote_addr;
    proxy_pass http://37.230.195.207:8001;
  }
}
server {
  server_name app-currency.online;
  listen 80;
  if ($host = app-currency.online) {
    return 301 https://$host$request_uri;
  }
  return 404;
}
```

### 6. Создание Helm Chart

Для манифеста написан Helm Chart.
Воспользоваться можно выполнив следующие команды:

```bash
helm repo add currency-app https://m0kes123.github.io/currency-app-helm/
helm repo update
helm install currency-app currency-app/currency-app
```

## Результат

Приложение развернуто в кластере и дает ответ на запросы по домену:
[https://app-currency.online/info](https://app-currency.online/info)

**Автор** MaximAntropov
