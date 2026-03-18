# Temporal Server (Local K8s)

Helm values for deploying Temporal to a local Kind cluster.

```bash
mise run k8s-up    # Creates Kind cluster + installs Temporal
mise run k8s-down  # Tears down the cluster
```

For local development without K8s, use:

```bash
temporal server start-dev
```
