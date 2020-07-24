#ResourceBilling API
This api queries prometheus and calculates resource usages for the desired container.

## Prometheus Queries
####CPU usage between now and given offset 
```
sum by (name) (container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=~".*yves_sc_tlsnr.*"})-(sum by (name) (container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=~".*yves_sc_tlsnr.*"} offset 5m))
```
####RAM usage summary between now and give offset in desired resolution
```
sum_over_time(container_memory_usage_bytes{container_label_com_docker_swarm_service_name="yves_sc_tlsnr"}[10m:1m]) 
```
