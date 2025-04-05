# Brainrot App Deployment Guide

This document provides instructions for deploying the Brainrot App using Docker and Kubernetes.

## Prerequisites

- Docker installed on your development machine
- Access to a Kubernetes cluster
- kubectl configured to communicate with your cluster

## Building the Docker Image

1. Navigate to the application directory:
   ```
   cd brainrot_app
   ```

2. Build the Docker image:
   ```
   docker build -t brainrot-app:latest .
   ```

3. (Optional) Push the image to a container registry if deploying to a remote cluster:
   ```
   docker tag brainrot-app:latest your-registry/brainrot-app:latest
   docker push your-registry/brainrot-app:latest
   ```
   Note: Update the deployment.yaml file to use your registry path if you push to a registry.

## Deploying to Kubernetes

1. Create the persistent volume claims:
   ```
   kubectl apply -f kubernetes/persistent-volume-claims.yaml
   ```

2. Create the ConfigMap:
   ```
   kubectl apply -f kubernetes/configmap.yaml
   ```

3. Deploy the application:
   ```
   kubectl apply -f kubernetes/deployment.yaml
   ```

4. Create the service to expose the application:
   ```
   kubectl apply -f kubernetes/service.yaml
   ```

5. Check the deployment status:
   ```
   kubectl get pods -l app=brainrot-app
   kubectl get svc brainrot-app-service
   ```

6. Access the application:
   - If using LoadBalancer service type, access via the external IP
   - If using NodePort, access via node IP and assigned port
   - If using Ingress (not included in basic setup), access via the configured host

## Scaling the Application

To scale the application horizontally:
```
kubectl scale deployment brainrot-app --replicas=3
```

## Monitoring and Logs

View logs for the application:
```
kubectl logs -l app=brainrot-app
```

## Updating the Application

1. Build a new Docker image with a new tag:
   ```
   docker build -t brainrot-app:v2 .
   ```

2. Update the deployment to use the new image:
   ```
   kubectl set image deployment/brainrot-app brainrot-app=brainrot-app:v2
   ```

## Cleanup

To remove the deployment:
```
kubectl delete -f kubernetes/service.yaml
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/configmap.yaml
kubectl delete -f kubernetes/persistent-volume-claims.yaml
```
