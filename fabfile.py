# -*- coding: utf-8 -*-
import os

from fabric import task

@task
def deploy(c, sha1='', django_setting='pyconkr.staging_settings', port='8000'):
    target_dir = f'~/'
    api_dir = f'{target_dir}/pyconkr-api'
    git_url = 'https://github.com/pythonkr/pyconkr-api.git'

    # 이전에 deploy dir을 clone한 적이 없다면 clone
    result = c.run(f'test -e {api_dir}', warn=True)
    if result.exited:
        print(f'{api_dir} is not exists')
        c.run(f'git clone {git_url} {api_dir}')

    with c.cd(api_dir):
        c.run('git fetch --all -p')
        c.run(f'git reset --hard {sha1}')
        envs = [
            f'PORT={port}',
            f'DJANGO_SETTINGS_MODULE={django_setting}'
        ]
        c.run(f'bash -l -c "docker-compose down | true"')
        env_command = ' '.join(envs)
        compose_command = f'docker-compose up -d --build --force-recreate'
        c.run(f'bash -l -c "{env_command} {compose_command}"')
        print('finish')
@task
def deploy_dev(c, sha1=''):
    deploy(c, sha1=sha1, django_setting='pyconkr.staging_settings', port='8000')

@task
def deploy_master(c, sha1=''):
    deploy(c, sha1=sha1, django_setting='pyconkr.production_settings', port='8000')
