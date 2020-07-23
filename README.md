#ResourceBilling API
This api queries prometheus and calculates resource usages for the desired container.

## Prometheus Queries
CPU usage between now and given offset 
```
sum by (name) (container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=~".*yves_sc_tlsnr.*"})-(sum by (name) (container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=~".*yves_sc_tlsnr.*"} offset 5m))
```

 