# -*- coding: utf-8 -*-
import os

from fabric import task

@task
def deploy(c, project_name, sha1='', django_setting='pyconkr.staging_settings', port='8000'):
    target_dir = f'~/{project_name}'
    api_dir = f'{target_dir}/pyconkr-api'
    git_url = 'https://github.com/pythonkr/pyconkr-api.git'

    c.run(f'mkdir -p {target_dir}')

    # 이전에 deploy dir을 clone한 적이 없다면 clone
    result = c.run(f'test -e {api_dir}', warn=True)
    if result.exited:
        print(f'{api_dir} is not exists')
        c.run(f'git clone {git_url} {api_dir}')

    with c.cd(api_dir):
        c.run('git fetch --all -p')
        c.run(f'git reset --hard {sha1}')
        envs = [
            f'PSQL_VOLUME={target_dir}/postgresql/data',
            f'STATIC_VOLUME={target_dir}/static',
            f'MEDIA_VOLUME={target_dir}/media',
            f'PYCONKR_ADMIN_PASSWORD={os.environ.get("PYCONKR_ADMIN_PASSWORD", "pyconkr")}',
            f'PORT={port}',
            f'DJANGO_SETTINGS_MODULE={django_setting}'
        ]
        c.run(f'docker-compose -p {project_name} down | true')
        env_command = ' '.join(envs)
        compose_command = f'docker-compose -p {project_name} up -d --build --force-recreate'
        c.config.run.env = {
            'PSQL_VOLUME':f'{target_dir}/postgresql/data',
            'STATIC_VOLUME':f'{target_dir}/static',
            'MEDIA_VOLUME':f'{target_dir}/media',
            'PYCONKR_ADMIN_PASSWORD': f'{os.environ.get("PYCONKR_ADMIN_PASSWORD", "pyconkr")}',
            'PORT':f'{port}',
            'DJANGO_SETTINGS_MODULE':f'{django_setting}'
        }
        c.run(f'{compose_command}')

        print('finish')
@task
def deploy_dev(c, sha1=''):
    deploy(c, project_name='dev.pycon.kr', sha1=sha1, django_setting='pyconkr.staging_settings', port='8001')

@task
def deploy_master(c, sha1=''):
    deploy(c, project_name='www.pycon.kr', sha1=sha1, django_setting='pyconkr.production_settings', port='8000')
