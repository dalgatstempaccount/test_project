import subprocess
from configparser import ConfigParser
from time import sleep

def set_global_user(username):
    cli_string = 'git config --global user.email "{}"'.format(username)
    cli = subprocess.Popen(cli_string.split(' '))
    exit_code =  cli.poll()
    print('set global user pass, code:' + str(exit_code) )

def git_init():
    cli_string = 'git init'
    cli = subprocess.Popen(cli_string.split(' '))

    reset_changes = 'git reset --hard HEAD'
    cli_reset = subprocess.Popen(reset_changes.split(' '))

    exit_code =  cli.poll()
    print('git init pass, code:' + str( exit_code ) )

def push_file_to_repo(filename, username, password, repository_url, branch='master'):

    subprocess.Popen('pwd')
    
    string_add_file = 'git add {}'.format('config.ini')
    subprocess.Popen(string_add_file.split(' '))

    commands_commit = 'git commit -m'.split(' ') + ['\"file {} was added\"'.format(filename)]
    subprocess.Popen(commands_commit)

    string_add_remote_origin = 'git remote add origin {}'.format(repository_url)
    subprocess.run(string_add_remote_origin.split(' '))

    string_push_changes = 'git push {}'.format(
        repository_url.replace('http://',
            'http://' + username + ':' + password + '@'))

    cli_commit = subprocess.Popen(string_push_changes.split(' '),
        stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')

    print( 'exit code:' + str(cli_commit.poll()) )
