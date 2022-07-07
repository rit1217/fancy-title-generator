import argparse
import logging
from .scripts import train


log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='title_gen_model CLI.')
parser.add_argument('-t', '--train', action='store_true', help='Train model.')
args = parser.parse_args()


if args.train:
    log.info('Start training...')
    train()


log.info('All done.')