import os
import re
import sys
import json
import urllib3
import logging
import argparse

from pathlib import Path
from python_on_whales import docker
from python_on_whales.exceptions import NoSuchImage
from concurrent.futures import ThreadPoolExecutor

from .__version__ import __version__

###>> Configure logging
from .CustomLogger import colors as c
logger = logging.getLogger('budi')

def check_internet_connection():
    http = urllib3.PoolManager(timeout=3.0)
    r = http.request('GET', 'google.com', preload_content=False)
    r.release_conn()

    if r.status == 200:
        return True
    else:
        return False

def get_local_image(image:dict) -> str:
    return docker.image.inspect(
        "{image_repo}{image_name}{image_tag}".format(
            image_name=image['name'],
            image_tag=f':{image["tag"]}',
            image_repo=f'{image["repo"]}/'
        )
    )

def get_remote_image_hash(image:dict) -> str:
    ###>> Adapted from
    ##> https://stackoverflow.com/a/62627500

    http = urllib3.PoolManager(timeout=3.0)

    ##> Get an autorization token
    url = f'https://auth.docker.io/token?service=registry.docker.io&scope=repository:{image["repo"]}/{image["name"]}:pull'
    r = http.request('GET', url, preload_content=False)
    token = json.loads(r.data)
    token = token['token']

    ##> Configure custom headers
    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": f'Bearer {token}'
    }

    ##> Get the remote image digest
    url = f'https://registry-1.docker.io/v2/{image["repo"]}/{image["name"]}/manifests/{image["tag"]}'
    r = http.request('GET', url, headers=headers, preload_content=False)
    digest = json.loads(r.data)
    digest = digest['config']['digest']

    return digest

def run(i:str, delete_image:bool=False, force_delete:str=False):
    logger.info(f'Checking image {i}', extra={'msgC':''})

    image = regex.match(i).groupdict()
    image['repo'] = f'{image["repo"]}' if image['repo'] else f'library'
    image['tag'] = f'{image["tag"]}' if image['tag'] else f'latest'

    remote_image_hash = get_remote_image_hash(image)

    try:
        local_image = get_local_image(image)
        local_image_hash = local_image.id
    except NoSuchImage as e:
        logger.warning(f'Image {i} not found locally')
        local_image = None
        local_image_hash = 'NaH'

    if local_image_hash == remote_image_hash:
        logger.info(f'Image {i} is up to date', extra={'msgC':c["green"]})
    else:
        if local_image_hash == 'NaH':
            logger.info(f'{c["cyan"]}Installing{c["reset"]} {i}', extra={'msgC':''})
        else:
            logger.info(f'{c["cyan"]}Updating{c["reset"]} {i}', extra={'msgC':''})

        docker.pull(
            "{image_repo}{image_name}{image_tag}".format(
                image_name=image['name'],
                image_tag=f':{image["tag"]}',
                image_repo=f'{image["repo"]}/'
            ), quiet=True
        )

        if delete_image and bool(local_image):
            logger.info(f'{c["red"]}Deleting{c["reset"]} old {i}', extra={'msgC':''})
            docker.image.remove(local_image, force=force_delete)

    return

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--file", help="File containing docker image names",
        action="store", type=str, required=True
    )

    parser.add_argument(
        "-t", "--threads", help="Number of concurrent threads (default: 2)",
        action="store", type=int, required=False, default=2
    )

    parser.add_argument(
        "-d", "--delete", help="Delete existing image after update (default: false)",
        action="store_true"
    )

    parser.add_argument(
        "-F", "--force", help="Froce remove image after update (default: false)",
        action="store_true"
    )

    parser.add_argument(
        '-v', '--version', help='Display version information',
        action='version', version=f'BUDI v{__version__}'
    )

    args = parser.parse_args()


    ###>> Verify internet connection
    logger.info(f'Checking your internet connectivity.', extra={'msgC':''})
    if not check_internet_connection():
        logger.critical(f'You seem to be offline. Check your connection & try again.')
        sys.exit(1)

    ###>> Make sure the images file exists
    imagesFile = Path(args.file)
    if not imagesFile.exists():
        logger.critical(f'File not found {imagesFile}')
    else:
        images = imagesFile.open('r').read().splitlines()

    ###>> Run the update
    ##> Parse the input into dict with keys ['repo', 'name', 'tag']
    global regex
    regex = re.compile('^(?P<repo>[\w.\-_]+(?=/[a-z0-9._-]+)|)(?:/|)(?P<name>[a-z0-9.\-_]+)(:(?P<tag>[\w.\-_]{1,127})|)$')

    with ThreadPoolExecutor(max_workers=int(args.threads)) as executor:
        for i in images:
            executor.submit(run, i, args.delete, args.force)

    logger.info(f'All done!!!', extra={'msgC':''})
    quit()
