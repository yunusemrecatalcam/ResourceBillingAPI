import time
import requests
import os

class PrometheusOperator:

    def __init__(self):
        self.prometheus_address = os.environ['prom_addr']

    @staticmethod
    def checkoffset(offset_string: str):
        if offset_string[-1] in "smhd":
            return offset_string
        else:
            return "30d"

    @staticmethod
    def timestamp2offset(timestamp: int):
        diff = str(int(time.time()) - timestamp) + 's'
        return diff if diff != '0s' else "1s"

    def get_cpu_total(self, label_name: str, label_value: str, t1: int, t2: int):

        query_string = 'sum by (name) (container_cpu_usage_seconds_total{{ {label}=~".*{label_value}.*"}} offset {offset_2})-' \
                       '(sum by (name) (container_cpu_usage_seconds_total{{ {label}=~".*{label_value}.*"}} offset {offset_1}))'.format(label=label_name,
                                                                                                                                       label_value=label_value,
                                                                                                                                       offset_1=t1,
                                                                                                                                       offset_2=t2)
        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={'query': query_string})
        query_response = response.json()

        results_dict = {}
        if query_response['status'] == "success":
            for container_metric_dict in query_response['data']['result']:
                results_dict[container_metric_dict['metric']['name']] = container_metric_dict['value']

        return results_dict

    def get_network_receive_total(self, label_name: str, label_value: str, t1: int, t2: int):

        query_string = 'sum by (name) (container_network_receive_bytes_total{{ {label}=~".*{label_value}.*"}} offset {offset_2})-' \
                       '(sum by (name) (container_network_receive_bytes_total{{ {label}=~".*{label_value}.*"}} offset {offset_1}))'.format(label=label_name,
                                                                                                                               label_value=label_value,
                                                                                                                                           offset_1=t1,
                                                                                                                                           offset_2=t2)
        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={'query': query_string})
        query_response = response.json()

        results_dict = {}
        if query_response['status'] == "success":
            for container_metric_dict in query_response['data']['result']:
                results_dict[container_metric_dict['metric']['name']] = container_metric_dict['value']

        return results_dict

    def get_network_transmit_total(self, label_name: str, label_value: str, t1: int, t2: int):

        query_string = 'sum by (name) (container_network_transmit_bytes_total{{ {label}=~".*{label_value}.*"}} offset {offset_2})-' \
                       '(sum by (name) (container_network_transmit_bytes_total{{ {label}=~".*{label_value}.*"}} offset {offset_1}))'.format(label=label_name,
                                                                                                                               label_value=label_value,
                                                                                                                                            offset_1=t1,
                                                                                                                                            offset_2=t2)
        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={'query': query_string})
        query_response = response.json()

        results_dict = {}
        if query_response['status'] == "success":
            for container_metric_dict in query_response['data']['result']:
                results_dict[container_metric_dict['metric']['name']] = container_metric_dict['value']

        return results_dict

    def get_ram_total(self, label_name: str, label_value: str,
                      t1: int, t2: int, resolution:str):

        resolution = self.checkoffset(resolution)
        query_string = 'sum_over_time(container_memory_usage_bytes{{{label}=~".*{label_value}.*"}}[{offset_1}:{resolution}]) -' \
                       'sum_over_time(container_memory_usage_bytes{{{label}=~".*{label_value}.*"}}[{offset_2}:{resolution}])'.format(label=label_name,
                                                                                                                    label_value=label_value,
                                                                                                                    offset_1=t1,
                                                                                                                    offset_2=t2,
                                                                                                                    resolution=resolution)

        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={'query': query_string})
        query_response = response.json()

        results_dict = {}
        if query_response['status'] == "success":
            for container_metric_dict in query_response['data']['result']:
                results_dict[container_metric_dict['metric']['name']] = container_metric_dict['value']

        return results_dict

    def get_disk_total(self, label_name: str, label_value: str,
                      offset_value: str, resolution:str):

        offset_value = self.checkoffset(offset_value)
        resolution = self.checkoffset(resolution)
        query_string = 'sum_over_time(container_fs_usage_bytes{{{label}=~".*{label_value}.*"}}[{offset_value}:{resolution}])'.format(label=label_name,
                                                                                                                    label_value=label_value,
                                                                                                                    offset_value=offset_value,
                                                                                                                    resolution=resolution)
        response = requests.get(self.prometheus_address + '/api/v1/query',
                                params={'query': query_string})
        query_response = response.json()

        results_dict = {}
        if query_response['status'] == "success":
            for container_metric_dict in query_response['data']['result']:
                results_dict[container_metric_dict['metric']['name']] = container_metric_dict['value']

        return results_dict

    def get_all_total(self, label_name: str, label_value: str,
                      offset_value: str, resolution: str):
        cpu_dict = self.get_cpu_total(label_name=label_name, label_value=label_value,
                           offset_value=offset_value)
        ram_dict = self.get_ram_total(label_name=label_name, label_value=label_value,
                                      offset_value=offset_value, resolution=resolution)
        disk_dict = self.get_disk_total(label_name=label_name, label_value=label_value,
                                      offset_value=offset_value, resolution=resolution)
        network_receive = self.get_network_receive_total(label_name=label_name, label_value=label_value,
                           offset_value=offset_value)
        network_transmit = self.get_network_transmit_total(label_name=label_name, label_value=label_value,
                                                       offset_value=offset_value)
        all_dict = {key: {'cpu': cpu_dict.get(key),
                          'ram': ram_dict.get(key),
                          'disk': disk_dict.get(key),
                          'network_receive': network_receive.get(key),
                          'network_transmit': network_transmit.get(key)} for key in cpu_dict}

        return all_dict

if __name__ == "__main__":

    prop = PrometheusOperator()
    ts = int(time.time())-600#1595849010
    t2 = int(time.time())
    prop.get_cpu_total(label_name='container_label_com_docker_swarm_service_name',
                       label_value='sc_tlsnr',
                       t1=prop.timestamp2offset(ts),
                        t2=prop.timestamp2offset(t2),
                       )
    prop.get_all_total(label_name='container_label_com_docker_swarm_service_name',
                       label_value='sc_tlsnr',
                       offset_value="10m",
                       resolution="1m")
    print("Done!")