# --- coding: utf-8 ---
import os
from fabric.api import local, hosts, env, run
from fabric.operations import prompt
from fabric.context_managers import lcd

env.use_ssh_config = True
env.project_path = '/home/vagrant/cinemaset/'


# def staging():
#     env.hosts = ['staging']
#
# def production():
#     env.hosts = ['production']
#
# def development():
#     env.hosts = ['development']


def github():
    local('ssh-add ~/.ssh/github')


def provision():
    """
    Setup all on provision/staging/deployment via Ansible. Development must run inside Vagrant box.

    Usage:
    fab [development|staging|production] provision
    """
    additional_params = '--skip-tags=vagrant_skip' if env.hosts[0] == 'development' else ''

    # Want more verbose output? Uncomment it.
    additional_params += ' -vvv'

    local('ansible-playbook -i inventories/all --limit {target} {additional_params} provision.yml'.
          format(target=env.hosts[0], additional_params=additional_params))


def drop_db():
    """
    Drop then create DB

    Usage:
    fab drop_db
    """
    with lcd(env.project_path + 'provision'):
        local('ansible-playbook -i inventories/all --limit development drop_db.yml')

    with lcd(env.project_path):
        local('find . -path *migrations* -name "*.py" -not -path "*__init__*" -exec rm {} \;')


def create_django_superuser():
    """
    Create django superuser

    Usage:
    fab create_django_superuser
    """
    verbose = ''
    #verbose += '-vvv'
    with lcd(env.project_path + 'provision'):
        local('ansible-playbook -i inventories/all --limit development {verbose} create_superuser.yml'
              .format(verbose=verbose))


def restore_db():
    with lcd(os.path.join(env.project_path, 'provision')):
        local('ansible-playbook -i inventories/all -vvv --limit development restore_db.yml')


def run_pgadmin():
    local('python /home/vagrant/pgadminvirt/lib/python3.4/site-packages/pgadmin4/pgAdmin4.py')


def get_heroku_dump():
    with lcd(env.project_path):
        local('heroku pg:backups capture')  # may be add --app `heroku app name`
        # local('curl -o latest.dump `heroku pg:backups public-url`')
        local('heroku pg:backups:download')


def heroku_migrate():
    local('heroku run python manage.py migrate')