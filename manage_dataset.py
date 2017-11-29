#!/usr/bin/env python
import argparse
import glob
import os
import shutil
import json
import errno
import logging
import collections
import functools


IMG_FILE_EXT = 'jpg'
LOGGING_INTERVAL = 500


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def collect_labels(source_path):
    #: Mapping from label to filenames
    labels = collections.defaultdict(list)
    num_processed = 0
    logger.info("Collecting labels...")

    pattern = os.path.join(source_path, '*')
    for filename in glob.iglob(pattern):
        if not filename.endswith('json'):
            continue
        if num_processed % LOGGING_INTERVAL == 0:
            logger.info("Loading labels from %s files", num_processed)

        with open(filename, 'r') as fd:
            json_data = json.load(fd)
            label = json_data['label']

            img_filename = '.'.join(filename.split('.')[:-1] + [IMG_FILE_EXT])
            if os.path.exists(img_filename):
                labels[label].append(img_filename)

        num_processed += 1
    return labels


def group_files(source_path, target_path, labels):
    num_processed = 0
    logger.info("Grouping files into subfolders by label...")

    for label, filenames in labels.items():
        label_path = os.path.join(target_path, label)
        ensure_path_exists(label_path)

        for source in filenames:
            if num_processed % LOGGING_INTERVAL == 0:
                logger.info("Moving %s files", num_processed)

            img_filename = source.split(os.path.sep)[-1]
            dest = os.path.join(target_path, label, img_filename)
            shutil.move(source, dest)
            num_processed += 1


def compose(*funcs):
    def wrapped(*args, **kwargs):
        result = None
        is_init = False
        for func in funcs:
            if result is None:
                result = func() if is_init else func(*args, **kwargs)
                is_init = True
            else:
                result = func(result)
        return result
    return wrapped


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dataset utility')
    parser.add_argument('--images', type=str, required=True,
        help='Folder containing images and JSON annotations')
    parser.add_argument('--target', type=str,
        help='Target folder with subfolders for each label')
    args = parser.parse_args()

    source_path = args.images
    target_path = args.target or source_path

    pipeline = compose(
        collect_labels,
        functools.partial(group_files, source_path, target_path)
    )
    pipeline(source_path)
