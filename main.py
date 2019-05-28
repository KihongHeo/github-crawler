#!/usr/bin/env

import base64
import getpass
import json
import sys
import time

from github import Github

data = {}
count = 0


def get_build_script(repo):
    files = [
        'Makefile', 'configure', 'CMakeLists.txt', 'autogen.sh', 'bootstrap',
        'buildconf', 'configure.ac'
    ]
    for f in files:
        try:
            repo.get_contents(f)
            return f
        except:
            pass
    return None


def find_repo_by_build_script(repo):
    build_script = get_build_script(repo)
    if build_script is not None:
        data[repo.full_name] = {
            'stars': repo.stargazers_count,
            'build_script': build_script
        }
        print('{}. {} : {}'.format(count, repo.full_name,
                                   repo.stargazers_count))
        count = count + 1


def get_ci_script(repo):
    files = [
        '.travis.yml', '.cirrus.yml', '.circleci/config.yml', 'Makefile',
        'Makefile.in', 'Makefile.am'
    ]
    for f in files:
        try:
            contents = repo.get_contents(f)
            if 'scan-build' in str(base64.b64decode(contents.content)):
                return contents
        except:
            pass
    return None


def find_repo_by_ci_script(repo):
    global count
    ci_script = get_ci_script(repo)
    if ci_script is not None:
        data[repo.full_name] = {
            'stars': repo.stargazers_count,
            'build_script': ci_script.html_url
        }
        print('{}. {} : {}\n{}'.format(
            count, repo.full_name, repo.stargazers_count, ci_script.html_url))
        count = count + 1


def main():
    username = input("Username: ")
    password = getpass.getpass()
    g = Github(username, password)
    repositories = g.search_repositories(query='language:C++')

    for repo in repositories:
        #        find_repo_by_build_script(repo)
        find_repo_by_ci_script(repo)
        time.sleep(1)

    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
