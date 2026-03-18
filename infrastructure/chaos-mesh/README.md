# Chaos Mesh

Used for failure simulation in chapter examples.

```bash
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh \
    -f infrastructure/chaos-mesh/values.yaml \
    --namespace chaos-mesh --create-namespace
```
