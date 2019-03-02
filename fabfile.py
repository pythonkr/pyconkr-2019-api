# -*- coding: utf-8 -*-
import os

from fabric import task

@task
def deploy(c, branch='develop', sha1='', port='8000'):
    target_dir = f'~/pyconkr.kr'
    if branch == 'develop':
        target_dir = f'~/dev.pyconkr.kr'
    elif branch == 'master':
        target_dir = f'~/www.pyconkr.kr'

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
        if sha1:
            c.run(f'git reset --hard {sha1}')
        else:
            c.run(f'git reset --hard origin/{branch}')
        envs = [
            f'PSQL_VOLUME={target_dir}/postgresql/data',
            f'STATIC_VOLUME={target_dir}/static',
            f'MEDIA_VOLUME={target_dir}/media',
            f'PYCONKR_ADMIN_PASSWORD={os.environ.get("PYCONKR_ADMIN_PASSWORD", "pyconkr")}',
            f'PORT={port}',
        ]
        c.run(f'docker-compose down | true')
        env_command = ' '.join(envs)
        compose_command = f'docker-compose up -d --build --force-recreate'
        c.run(f'{env_command} {compose_command}')
        print('finish')
