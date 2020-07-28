from flask import Flask, request
from prometheus_ops import PrometheusOperator

app = Flask(__name__)

prom_op = PrometheusOperator()

@app.route("/", methods=['GET'])
def calculate():
    label = request.args.get('label_name')
    value = request.args.get('label_value')
    label2 = request.args.get('label_name2')
    value2 = request.args.get('label_value2')
    timestamp1 = int(request.args.get('t1'))
    timestamp2 = int(request.args.get('t2'))
    resolution = request.args.get('resolution')

    if timestamp2 <= timestamp1:
        return "t2 should be bigger than t1"

    if all(v is not None for v in[label, value,
                                  label2, value2,
                                  timestamp1, timestamp2, resolution]):
        all_dict = prom_op.get_all_total(label_name=label,
                                         label_value=value,
                                         label_name2=label2,
                                         label_value2=value2,
                                         t1=timestamp1,
                                         t2=timestamp2,
                                         resolution=resolution)
        return all_dict
    else:
        return "Be sure the you set all the required fields; \n" \
               "label_name, label_value, offset_value, resolution"