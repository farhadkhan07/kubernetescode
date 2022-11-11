# Openstack Deploy on kubernetes by ArgoCD
Documents Link:
https://github.com/helm/charts/tree/master/stable/nginx-ingress
https://argoproj.github.io/argo-cd/



### Pre-Requisites
1. Latest Kubernetes
2. Helm
3. Metrics-server
4. Nginx-Ingress
```
helm install --name nginx-ingress  --namespace kube-system stable/nginx-ingress --set controller.service.type=NodePort

kubectl -n kube-system edit deploy nginx-ingress-controller
...
spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --default-backend-service=kube-system/nginx-ingress-default-backend
        - --election-id=ingress-controller-leader
        - --ingress-class=nginx
        - --enable-ssl-passthrough # Add this flag
        - --configmap=kube-system/nginx-ingress-controller
...
```

**Note: Follow k8s documents for above requirements**

### Deploy ArgoCD
```
#   kubectl create namespace argocd

#   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

#   cat <<EOF >> argocd-ingress.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
spec:
  tls:
  - secretName: argocd-secret
    hosts:
    - deploy.brilliant.com.bd
  rules:
  - host: deploy.brilliant.com.bd
    http:
      paths:
      - backend:
          serviceName: argocd-server
          servicePort: https
        path: /
EOF

#   kubectl apply -f  argocd-ingress.yaml 
```


### ArgoCD web Login & default Password change
```
web login:
https://deploy.brilliant.com.bd:31191/applications
user: admin
pass: "password is the argocd pod name"

### Enable ArgoCD Cli

VERSION=$(curl --silent "https://api.github.com/repos/argoproj/argo-cd/releases/latest" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')

echo $VERSION
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/$VERSION/argocd-linux-amd64

argocd login deploy.brilliant.com.bd:31191
argocd account update-password
argocd logout deploy.brilliant.com.bd:31191
```

### Setup a helm repo for helm-toolkit
```
1. Create a new github repo & clone it locally

#    cd helm-charts    # git repo name

#    cp -r  /opt/openstack-helm-infra/helm-toolkit .

#     helm package helm-toolkit

#    helm repo index --url https://cloud-operations.github.io/helm-charts/ .

#    git add . 

#    git commit -m "Added helm repo"

#    git push 

Now it’s time to publish the contents of our git repository as Github pages. Go back to your browser, in the “settings” section of your git repository, scroll down to Github Pages and set source to master branch.

# To verify add repo locally

helm repo add repo-add-test https://cloud-operation.github.io/helm-charts/

helm update
helm search --repo  repo-add-test

```
```
