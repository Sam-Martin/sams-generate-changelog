import logging
from .generatechangelog import GenerateChangelog

def main():
    logging.basicConfig(level='DEBUG')
    gc = GenerateChangelog()
    gc.render_markdown()