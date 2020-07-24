import time
import requests
import os

class PrometheusOperator:

    def __init__(self):
        self.prometheus_address = os.environ['prom_addr']

    def get_cpu_total(self, label_name: str, label_value: str):
        query_string = 'sum by (name) (container_cpu_usage_seconds_total{{ {label}=~".*{label_value}.*"}})-' \
                       '(sum by (name) (container_cpu_usage_seconds_total{{ {label}=~".*{label_value}.*"}} offset 5d))'.format(label=label_name,
                                                                                                                               label_value=label_value)
        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={'query': query_string})
        query_response = response.json()

        results_dict = {}
        if query_response['status'] == "success":
            for container_metric_dict in query_response['data']['result']:
                results_dict[container_metric_dict['metric']['name']] = container_metric_dict['value']
                print(container_metric_dict['metric']['name'], container_metric_dict['value'])

        return results_dict


if __name__ == "__main__":
    print("leley")
    prop = PrometheusOperator()
    for i in range(10):
        prop.get_cpu_total(label_name='container_label_com_docker_swarm_service_name',
                           label_value='yves_sc_tlsnr')
        time.sleep(1)