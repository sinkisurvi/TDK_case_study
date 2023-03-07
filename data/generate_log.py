import random
from datetime import datetime
import os

ips = ['127.0.0.1', '192.168.1.1', '10.0.0.2', '172.16.0.1', '172.16.0.2']
userids = ['1234', '1235', '9101', '1121', '3141','1286','1255']
methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']
resources = ['/apache_pb.gif', '/apache_sample.gif', '/test_pb.gif', '/example_pb.gif', '/apache_test.gif']
protocols = ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0']
status_codes = ['200', '404', '500', '301', '302']
sizes = ['100', '200', '300', '400', '500']

def generate_log():      
    logs = ''
    for i in range(1000):
        ip = random.choice(ips)
        userid = random.choice(userids)
        method = random.choice(methods)
        resource = random.choice(resources)
        protocol = random.choice(protocols)
        status_code = random.choice(status_codes)
        size = random.choice(sizes)
        log = f'{ip} - {userid} [{random.randint(10, 28)}/Oct/{random.randint(2000, 2022)}:{random.randint(10, 23)}:{random.randint(10, 59)}:{random.randint(10, 59)} +0{random.choice([100,200])}] "{method} {resource} {protocol}" {status_code} {size}\n'
        logs += log

    date_format = "%d-%m-%Y"
    file_dir = os.path.dirname(os.path.abspath(__file__))
    current_date = datetime.today().strftime(date_format)
    with open(f'{file_dir}/{current_date}.log', "w") as f:
            f.write(logs)

if __name__ == "__main__":
     generate_log()