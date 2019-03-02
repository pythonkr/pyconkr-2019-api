# -*- coding: utf-8 -*-
import os

from fabric import task


#from fabric.api import local, run, cd, prefix, env, sudo, settings, shell_env

# env.use_ssh_config = True
# env.user = 'pyconkr'
# env.hosts = ['pythonkorea1']


@task
def deploy(c, target='dev', port='8000', sha1=''):
    project_name = f'{target}.pycon.kr'
    target_dir = f'~/{project_name}/pyconkr-2019'
    api_dir = f'{target_dir}/pyconkr-api'
    database_dir = f'{target_dir}/postgresql/data'
    git_url = 'https://github.com/pythonkr/pyconkr-api.git'

    c.run(f'mkdir -p {database_dir}')

    # 이전에 deploy dir을 clone한 적이 없다면 clone
    result = c.run(f'test -e {api_dir}', warn=True)
    if result.exited:
        print(f'{api_dir} is not exists')
        c.run(f'git clone {git_url} {api_dir}')

    with c.cd(api_dir):
        c.run('git fetch --all -p')
        c.run('git reset --hard ' + sha1)
        envs = [
            f'PSQL_VOLUME={database_dir}',
            f'PORT={port}',
            f'PYCONKR_ADMIN_PASSWORD={os.environ.get("PYCONKR_ADMIN_PASSWORD", "pyconkr")}',
        ]
        c.run(f'docker-compose -p "{project_name}" down')
        env_command = ' '.join(envs)
        compose_command = f'docker-compose -p "{project_name}" up -d --build --force-recreate'
        c.run(f'{env_command} {compose_command}')
        print('finish')
