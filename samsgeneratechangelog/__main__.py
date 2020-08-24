import logging
from .generatechangelog import GenerateChangelog

def main():
    logging.basicConfig(level='DEBUG')
    gc = GenerateChangelog()
    gc.config.register_arguments()
    if gc.config.verb[0].lower() == 'print':
        print(gc.render_markdown())