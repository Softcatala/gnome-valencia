# -*- coding: utf-8 -*-
import os
import subprocess
import sys


def main():
    repos = get_repositories_folder()
    ca_to_val_script = get_valencianization_script()
    gnome_user = get_gnome_git_user()

    convert(repos, ca_to_val_script, gnome_user)


def get_repositories_folder():
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        print(f'Using {folder} as the repositories root')
    else:
        folder = input('Which folder contains the repositories? ')
    _create_if_needed(folder)
    return folder


def _create_if_needed(folder):
    if os.path.exists(folder):
        if os.path.isdir(folder):
            return True

        raise ValueError(f'{folder} is not a folder!')

    print(f'Creating {folder}')
    os.makedirs(folder)


def get_valencianization_script():
    script = input('Where is the script (default: ca_to_va.sh)? ')
    if os.path.exists(script):
        return script

    message = f'{script} does not exist, double check the script location'
    raise ValueError(message)


def get_gnome_git_user():
    user = input('Which username do you have on GNOME git? ')
    if user != '':
        return user

    raise ValueError('Please provide a user!')


def convert(repos_folder, script, username):
    repo = _get_next_repo()
    while repo != '':
        repo_folder = _create_or_update(repos_folder, repo, username)

        raw_branches = input('Which branches (default: master)? ')
        for branch in _process_branches_input(raw_branches):
            _checkout_branch(repo_folder, branch)
            _update_translation(repo_folder, script)

        repo = _get_next_repo()


def _get_next_repo():
    return input('Which repository needs to be updated (empty to quit)? ')


def _create_or_update(root_folder, repo_name, username):
    repo_folder = os.path.join(root_folder, repo_name)

    if not os.path.exists(repo_folder):
        _create_repo(repo_folder, repo_name, username)
        return repo_folder

    if os.path.isdir(repo_folder):
        _update_repo(repo_folder)
        _clean_repo(repo_folder)
        return repo_folder

    raise ValueError(f'Repo {repo_folder} is not a folder')


def _create_repo(repo_folder, repo_name, username):
    _run_command([
        'git'
        'clone'
        f'ssh://{username}@git.gnome.org/git/{repo_name}'
        f'{repo_folder}'
    ])


def _update_repo(repo_folder):
    with change_dir(repo_folder):
        _run_command(['git fetch', '-p'])
        _run_command(['git', 'checkout', 'master'])
        _run_command(['git', 'rebase', 'origin/master'])


def _clean_repo(repo_folder):
    with change_dir(repo_folder):
        _run_command(['git', 'clean', '-dfx'])


def _process_branches_input(raw_branches):
    if raw_branches == '':
        return 'master'
    return raw_branches.split(',')


def _checkout_branch(repo_folder, branch):
    with change_dir(repo_folder):
        _run_command(['git', 'checkout', branch])


def _update_translation(repo_folder, script):
    po_folder = os.path.join(repo_folder, 'po')
    with change_dir(po_folder):
        _convert_po_file(script)
        _check_in_LINGUAS()
        _commit_and_push()


def _convert_po_file(script):
    _run_command([script])


def _check_in_LINGUAS():
    if 'ca@valencia' not in open('LINGUAS').read():
        print('ca@valencia missing in LINGUAS')


def _commit_and_push():
    _run_command(['git', 'add', 'ca@valencia.po'])
    _run_command([
        'git',
        'commit',
        '-m"[l10n] Updated Catalan (Valencian) translation"',
        '--author',
        '"Xavi Ivars <xavi.ivars@gmail.com>"',
    ])
    _run_command(['git', 'push'])


def _run_command(cmd):
    print(cmd)
    return True
    return_code = subprocess.call(cmd)
    if return_code < 0:
        raise ValueError(f'{cmd} failed with return code {return_code}')

    return return_code


class change_dir(object):
    """Step into a directory temporarily

    Copied from https://pythonadventures.wordpress.com/2013/12/15/chdir-a-context-manager-for-switching-working-directories/  # noqa: E501
    """

    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)


if __name__ == '__main__':
    main()
