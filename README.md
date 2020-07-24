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

## Function Documentation
PrometheusOperator object includes all the funtions for calculation resource usages.
It gets prometheus root url from environment variable 'prom_addr'


####get_cpu_total(label_name, label_value, offset_value)
- **label_name**: Label for querying prometheus, for example "container_label_com_docker_swarm_service_name"
- **label_value**: Desired value for your desired label, for example "my_docker_service"
- **offset**: Resource usage will be calculated for the time between now and this offset,
format is the prometheus's time format. 1m (1 minute), 1h (1 hour), 2d (2 days)

####get_ram_total(label_name, label_value, offset_value, resolution)
- **label_name**: Label for querying prometheus, for example "container_label_com_docker_swarm_service_name"
- **label_value**: Desired value for your desired label, for example "my_docker_service"
- **offset**: Resource usage will be calculated for the time between now and this offset
- **resolution**: As container ram usage is not a cumulative function (it returns current usage),
 we calculate total ram usage by taking samples in desired resolution. 

