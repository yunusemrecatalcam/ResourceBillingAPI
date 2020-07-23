import time
import requests
import os

class PrometheusOperator:

    def __init__(self):
        self.prometheus_address = os.environ['prom_addr']

    def get_cpu_total(self):
        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={
                                    'query': 'sum by (name) (container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=~".*yves_sc_tlsnr.*"})-(sum by (name) (container_cpu_usage_seconds_total{container_label_com_docker_swarm_service_name=~".*yves_sc_tlsnr.*"} offset 5d))'})

        query_response = response.json()
        if query_response['status'] == "success":

            for container_metric_dict in query_response['data']['result']:
                print(container_metric_dict['metric']['name'], container_metric_dict['value'])

        return 0


if __name__ == "__main__":
    print("leley")
    prop = PrometheusOperator()
    for i in range(10):
        prop.get_cpu_total()
        time.sleep(1)