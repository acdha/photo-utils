#!/usr/bin/env python
# encoding: utf-8
"""Move image files into date-based hierarchy using EXIF/IPTC dates"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import logging
import os

import pyexiv2


def rename_file(filename, target_directory):
    metadata = pyexiv2.ImageMetadata(filename)
    metadata.read()

    metadata_keys = metadata.exif_keys

    dt = None
    # n.b. pyexiv2 treats these at bytestrings, not Unicode:
    for k in (b'Exif.Photo.DateTimeOriginal', b'Exif.Image.DateTime'):
        if k in metadata_keys:
            dt = metadata[k].value
            break
    else:
        logging.error('%s does not contain EXIF dates!', filename)
        return

    logging.info('Using date %s for %s', dt, filename)

    target_dir = os.path.join(target_directory, '%02d' % dt.year, '%02d' % dt.month, '%02d' % dt.day)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logging.info('Created directory %s', target_dir)

    new_filename = os.path.join(target_dir, os.path.basename(filename))

    if os.path.exists(new_filename):
        # TODO: compare content hash for duplicates
        logging.warning('Not moving %s: %s already exists', filename, new_filename)
    else:
        logging.info('Moving %s to %s', filename, new_filename)
        os.rename(filename, new_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.strip(),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(dest='base_directory', metavar='BASE_DIR',
                        default=os.path.expanduser('~/Dropbox/Photos/'),
                        help='The base directory where photos will be moved under')
    parser.add_argument('filenames', nargs='+', metavar='FILE',
                        help='One or more image files to be reorganized')

    args = parser.parse_args()

    base_dir = os.path.expanduser(args.base_directory)

    if not os.path.isdir(base_dir):
        parser.error('Expected directory %s to exist!' % args.base_directory)

    try:
        import coloredlogs
        coloredlogs.install()
    except ImportError:
        pass

    for f in args.filenames:
        if not os.path.exists(f):
            logging.warning('Skipping non-existent file %s', f)
            continue

        try:
            rename_file(f, base_dir)
        except StandardError as exc:
            logging.error('Unable to process %s: %s', f, exc)
