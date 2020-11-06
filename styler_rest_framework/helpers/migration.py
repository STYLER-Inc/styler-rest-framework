import logging
import time
from random import randint

from alembic.config import Config
from alembic import command


class MigrationError(Exception):
    """MigrationError class for exceptions in this module."""
    pass


def get_current_version(alembic_cfg):
    captured_text = None

    def print_stdout(text, *arg):
        nonlocal captured_text
        captured_text = text

    alembic_cfg.print_stdout = print_stdout
    command.current(alembic_cfg)
    return captured_text


def get_heads_version(alembic_cfg):
    captured_text = []

    def print_stdout(text, *arg):
        nonlocal captured_text
        captured_text.append(text)
    alembic_cfg.print_stdout = print_stdout
    command.heads(alembic_cfg)
    return captured_text


def retry_migration(alembic_cfg, count, max_count, max_backoff=32):
    try:
        logging.warning(f'retry migration now... (retry count:{count+1})')
        command.upgrade(alembic_cfg, 'head')
        logging.warning('retry migration succeed!')
        return
    except Exception:
        backoff = min(2**(count)+randint(1, 1000)/1000, max_backoff)
        count += 1
        if count >= max_count:
            raise MigrationError('Could not execute alembic migrations.')
        logging.warning(f'retry migration failed, \
            will retry again after {backoff} seconds...')
        time.sleep(backoff)
        retry_migration(alembic_cfg, count, max_count, max_backoff)


def check_and_retry_migration(cfg_path, max_retry_count=3):
    if not cfg_path:
        raise MigrationError('parameter required: cfg_path')
    alembic_cfg = Config(cfg_path)
    heads = get_heads_version(alembic_cfg)
    if len(heads) > 1:
        raise MigrationError(f'multiple heads detected! {heads}')
    current = get_current_version(alembic_cfg)
    if current == heads[0]:
        return
    logging.warning('alembic version is not up-to-date, \
        will retry migration...')
    retry_migration(alembic_cfg, 0, max_retry_count)
