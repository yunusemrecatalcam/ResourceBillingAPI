#ResourceBilling API
This api queries prometheus and calculates resource usages for the desired container.

## Prometheus Queries
####CPU usage between two timestamps
```
sum by (name) (container_cpu_usage_seconds_total{ container_label_com_docker_swarm_service_name=~".*devops_prometheus.*", container_label_com_docker_stack_namespace=~".*devops.*"} offset 16806s)-(sum by (name) (container_cpu_usage_seconds_total{ container_label_com_docker_swarm_service_name=~".*devops_prometheus.*", container_label_com_docker_stack_namespace=~".*devops.*"} offset 17406s))
```
####RAM usage summary between two timestamps in desired resolution
```
sum_over_time(container_memory_usage_bytes{container_label_com_docker_swarm_service_name=~".*devops_prometheus.*", container_label_com_docker_stack_namespace=~".*devops.*"}[17406s:1h]) -sum_over_time(container_memory_usage_bytes{container_label_com_docker_swarm_service_name=~".*devops_prometheus.*", container_label_com_docker_stack_namespace=~".*devops.*"}[16806s:1h])
```

## Function Documentation
PrometheusOperator object includes all the funtions for calculation resource usages.
It gets prometheus root url from environment variable 'prom_addr'


####get_cpu_total(label_name, label_value, t1, t2)
#####This function calculates the total cpu before t2 and t1 seperately and returns the difference.
- **label_name**: Label for querying prometheus, for example "container_label_com_docker_swarm_service_name"
- **label_value**: Desired value for your desired label, for example "my_docker_service"
- **t1 - t2**: Resource usage will be calculated for the time between two timestamps, 
t2 should be bigger than t1.

#####get_network_transmit_total and get_network_receive_total functions works same as get_cpu_total function.
####get_ram_total(label_name, label_value, t1, t2, resolution)
#####This function takes samples in desired resolution and returns the sum of them.
- **label_name**: Label for querying prometheus, for example "container_label_com_docker_swarm_service_name"
- **label_value**: Desired value for your desired label, for example "my_docker_service"
- **t1 - t2**: Resource usage will be calculated for the time between two timestamps, 
t2 should be bigger than t1.
- **resolution**: As container ram usage is not a cumulative function (it returns current usage),
 we calculate total ram usage by taking samples in desired resolution. It should be given as
 prometheus's time format (1s, 1m, 2h)

#####get_disk_total function works same as the get_ram_total function.
####WARNING! Resolution must be less than the difference between t2 and t1 in order to getting a meaningful result.

##Docker
Build
```
docker build -t resourcebilling:latest .
```
Run
```
docker run --network=host -e prom_addr=http://58.18.155.36:9090 -it resourcebilling:latest
```