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

    c.run(f'mkdir -p {target_dir}')
    c.run(f'mkdir -p {database_dir}')

    with c.cd(api_dir):
        c.run('git fetch --all -p')
        c.run('git reset --hard ' + sha1)
        envs = [
            f'PSQL_VOLUME={database_dir}',
            f'PORT={port}',
            f'PYCONKR_ADMIN_PASSWORD={os.environ.get("PYCONKR_ADMIN_PASSWORD", "pyconkr")}'
            f'GITHUB_CLIENT_ID={os.environ.get("GITHUB_CLIENT_ID", "")}',
            f'GITHUB_CLIENT_SECRET={os.environ.get("GITHUB_CLIENT_SECRET", "")}',
            f'GOOGLE_CLIENT_ID={os.environ.get("GOOGLE_CLIENT_ID", "")}',
            f'GOOGLE_CLIENT_SECRET={os.environ.get("GOOGLE_CLIENT_SECRET", "")}',
            f'FACEBOOK_CLIENT_ID={os.environ.get("FACEBOOK_CLIENT_ID", "")}',
            f'FACEBOOK_CLIENT_SECRET={os.environ.get("FACEBOOK_CLIENT_SECRET", "")}',
            f'NAVER_CLIENT_ID={os.environ.get("NAVER_CLIENT_ID", "")}',
            f'NAVER_CLIENT_SECRET={os.environ.get("NAVER_CLIENT_SECRET", "")}',
        ]

        env_command = ' '.join(envs)
        compose_command = f'docker-compose -p "{project_name}" up -d --build --force-recreate'
        c.run(f'{env_command} {compose_command}')
        print('finish')
