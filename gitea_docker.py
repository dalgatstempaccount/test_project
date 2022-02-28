# -*- coding: utf-8 -*- 

import subprocess
from configparser import ConfigParser

# Функция для запуска докер-контейнера, возвращает id контейнера. Нужен sudo пароль.
def start_gitea_docker(sudo_password):

    config = ConfigParser()
    config.read('config.ini')

    run_docker_command = 'docker run -d -p {}:3000 gitea/gitea:1.16.0'.format(
        config['gitea']['port'], config['gitea']['version'])

    cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S'] + run_docker_command.split(), stdin=cmd1.stdout, stdout=subprocess.PIPE)

    container_id = cmd2.stdout.read().decode().split('\n')[0]
    docker_run_exit_code = cmd2.poll()

    return container_id, docker_run_exit_code

# Функция для остановки докер-контейнера, возвращает статус завершение. Нужен sudo пароль и 
# id контейнера
def stop_gitea_docker(container_id='', sudo_password='your_sudo_password_goes_here'):
    config = ConfigParser()
    config.read('config.ini')
    
    stop_docker_command = 'docker stop {}'.format(container_id)
    remove_docker_command = 'docker rm -vf {}'.format(container_id)

    cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo','-S'] + stop_docker_command.split(), stdin=cmd1.stdout, stdout=subprocess.PIPE)

    docker_stop_exit_code =  cmd2.poll()

    cmd3 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    cmd4 = subprocess.Popen(['sudo','-S'] + stop_docker_command.split(), stdin=cmd1.stdout, stdout=subprocess.PIPE)

    return docker_stop_exit_code