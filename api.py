from flask import Flask, request
from prometheus_ops import PrometheusOperator

app = Flask(__name__)

prom_op = PrometheusOperator()

@app.route("/", methods=['GET'])
def calculate():
    label = request.args.get('label_name')
    value = request.args.get('label_value')
    timestamp1 = int(request.args.get('t1'))
    timestamp2 = int(request.args.get('t2'))
    resolution = request.args.get('resolution')

    if all(v is not None for v in[label, value, timestamp1, timestamp2, resolution]):
        all_dict = prom_op.get_all_total(label_name=label,
                           label_value=value,
                           t1=timestamp1,
                           t2=timestamp2,
                           resolution=resolution)
        return all_dict
    else:
        return "Be sure the you set all the required fields; \n" \
               "label_name, label_value, offset_value, resolution"