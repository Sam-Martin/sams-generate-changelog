import logging
from .generatechangelog import GenerateChangelog
from .config import ARG_PARSER

def main():
    args = ARG_PARSER.parse_args()
    logging.basicConfig(level=args.log_level.upper())
    gc = GenerateChangelog(
        old_version=args.old_version,
        new_version=args.new_version,
        git_path=args.git_path
    )
    
    if args.verb.lower() == 'print':
        print(gc.render_markdown())