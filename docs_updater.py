#!/usr/bin/env python3
import json
import os
import shutil
from git import Repo
import requests
import logging
from datetime import datetime

# Set up logging
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, f"docs_updater_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config file: {e}")
        raise

def save_config(config, config_file):
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logging.info(f"Config file updated: {config_file}")
    except Exception as e:
        logging.error(f"Failed to save config file: {e}")
        raise

def get_latest_release(repo_url):
    owner, repo = repo_url.split('/')[-2:]
    repo = repo.replace('.git', '')
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        version = response.json()['tag_name'].lstrip('v')
        logging.info(f"Latest release for {repo_url}: {version}")
        return version
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch latest release for {repo_url}: {e}")
        return None

def clone_or_pull_repo(url, branch, local_path):
    try:
        if os.path.exists(local_path):
            logging.info(f"Pulling latest changes for {url}")
            repo = Repo(local_path)
            origin = repo.remotes.origin
            origin.pull()
        else:
            logging.info(f"Cloning repository {url}")
            Repo.clone_from(url, local_path, branch=branch)
        return local_path
    except Exception as e:
        logging.error(f"Failed to clone or pull repository {url}: {e}")
        raise

def copy_docs(src, dest, docs_folder):
    try:
        if docs_folder:
            src = os.path.join(src, docs_folder)
        
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        logging.info(f"Docs copied from {src} to {dest}")
    except Exception as e:
        logging.error(f"Failed to copy docs from {src} to {dest}: {e}")
        raise

def update_docs(config, config_file):
    temp_storage_path = config['temp_storage_path']
    docs_storage_path = config['docs_storage_path']

    if not os.path.exists(temp_storage_path):
        os.makedirs(temp_storage_path)
    if not os.path.exists(docs_storage_path):
        os.makedirs(docs_storage_path)

    config_updated = False

    for repo in config['repositories']:
        logging.info(f"Processing repository: {repo['url']}")
        
        latest_version = get_latest_release(repo['url'])
        if latest_version and latest_version != repo['version']:
            logging.info(f"New version found for {repo['url']}: {latest_version}")
            repo['version'] = latest_version
            config_updated = True
        else:
            logging.info(f"No new version found for {repo['url']}")
        
        repo_name = repo['url'].split('/')[-1].replace('.git', '')
        temp_repo_path = os.path.join(temp_storage_path, repo_name)
        
        clone_or_pull_repo(repo['url'], repo['branch'], temp_repo_path)
        
        dest_dir = os.path.join(docs_storage_path, repo_name, repo['version'])
        
        copy_docs(temp_repo_path, dest_dir, repo['docs_folder'])
        
        logging.info(f"Docs updated for {repo_name} version {repo['version']}")

    if config_updated:
        save_config(config, config_file)
        logging.info("Config file updated with new versions")

    logging.info(f"All docs have been updated and stored in {docs_storage_path}")

if __name__ == '__main__':
    try:
        logging.info("Script execution started")
        config_file = 'repo_config.json'
        config = load_config(config_file)
        update_docs(config, config_file)
        logging.info("Script execution completed successfully")
    except Exception as e:
        logging.error(f"Script execution failed: {e}")