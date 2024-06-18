import os
import subprocess
from git import Repo
import scrapy
import git

class GitspiderSpider(scrapy.Spider):
    name = "gitspider"
    allowed_domains = ["github.com"]

    base_urls = [
        'https://github.com/andragri/Hacking_w_Python',
        'https://github.com/atzaka-git/HackPy',
        'https://codeberg.org/user_ljfg/HackPyth'
    ]

    start_urls = [url for url in base_urls]
    base_directory = './cloned_repos'

    def parse(self, response):
        repo_urls = [url + '.git' for url in self.base_urls]

        for repo_url in repo_urls:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            clone_directory = f'{self.base_directory}/{repo_name}'

            try:
                Repo.clone_from(repo_url, clone_directory)
                self.log(f'Repository {repo_name} cloned successfully into {clone_directory}')
                self.check_for_sensitive_data(clone_directory)
            except git.exc.GitError as e:
                self.log(f'Error cloning repository {repo_name}: {e}')

    def check_for_sensitive_data(self, repo_directory):
        findings_file = './findings.txt'

        for root, _, files in os.walk(repo_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Run bandit on the file and capture output
                bandit_cmd = f'bandit -f json {file_path}'
                try:
                    output = subprocess.check_output(bandit_cmd, shell=True, stderr=subprocess.STDOUT)
                    output = output.decode('utf-8').strip()

                    # Check if bandit found any issues
                    if output:
                        with open(findings_file, 'a') as findings:
                            findings.write(f'Bandit findings in {file_path}:\n{output}\n\n')

                except subprocess.CalledProcessError as e:
                    self.log(f'Bandit error in {file_path}: {e.output.decode("utf-8").strip()}')

