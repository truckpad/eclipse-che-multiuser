import docker
import os
import psutil
import random
import requests
from base64 import b64decode 
from bottle import redirect, request, route, run, template

che_data_base_path = '/var/lib/eclipse-che'
docker_client = docker.from_env()

def find_unused_port(start=8000, end=9000):
    busy_ports = []
    for port in psutil.net_connections():
        busy_ports.append(port.laddr[1])
    while True:
        new_port = random.randint(start, end)
        if new_port not in busy_ports:
            return new_port

def logged_user(cookie='_oauth2_proxy'):
    data = request.cookies.get(cookie)
    if data:
        decoded_data = b64decode(data.split('|')[0]).decode('UTF-8')
        return decoded_data.split('|')[0]

@route('/')
def initialize():
    email = logged_user()
    user_path = os.path.join(che_data_base_path, email)
    port_path = os.path.join(user_path, 'port')
    if not os.path.isdir(user_path):
        os.mkdir(user_path)
    if not os.path.exists(port_path):
        user_port = find_unused_port()
        with open(port_path, 'w') as port_file:
            port_file.write(str(user_port))
    else:
        with open(port_path, 'r') as port_file:
            user_port = int(port_file.readline())

    container_name = ''.join(char for char in email if char.isalnum())
    try:
        docker_client.containers.get(container_name)
        print('Container %s already exists' % container_name)
    except docker.errors.NotFound:        
        docker_client.containers.run(
            'eclipse/che:5.15.0', 
            'start', 
            detach=True, 
            name=container_name,
            volumes={
                '/var/lib/eclipse-che/data': {'bind':'/data'}, 
                '/var/run/docker.sock': {'bind': '/var/run/docker.sock'}
            }, 
            environment=[
                'CHE_CONTAINER_PREFIX=%s' % container_name,
                'CHE_HOST=che.it.truckpad.com.br',
                'CHE_PORT=%i' % user_port,
                # 'CHE_SINGLE_PORT=true'
            ]
        )

    tmpl = '''
    <html>
    <head>
        <meta http-equiv=refresh content=\"5;URL=/wait\">
    </head>
    <body>
        <b>Starting a fresh environment for {{email}}!</b>!
    </body>
    </html>
    '''
    return template(tmpl, email=email)

@route('/wait')
def wait_for_workspace():
    email = logged_user()
    user_path = os.path.join(che_data_base_path, email)
    port_path = os.path.join(user_path, 'port')
    with open(port_path, 'r') as port_file:
        user_port = int(port_file.readline())
    try:
        response = requests.get('http://127.0.0.1:%i/api/' % user_port, timeout=(0.2,1))
        if response.status_code == 200:
            redirect('/update-config')
    except requests.exceptions.RequestException as e:
        print(e)
        print(type(e).__name__)
    tmpl = '''
    <html>
    <head>
        <meta http-equiv=refresh content=\"5;URL=/wait\">
    </head>
    <body>
        <b>Waiting for {{email}} personal environment to boot...</b>!<br/>
    </body>
    </html>
    '''
    return template(tmpl, email=email)

@route('/update-config')
def update_nginx_routes():
    print('lalala')
    return 'lelele'

run(host='localhost', port=5678)