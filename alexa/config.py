#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.options import define, options, parse_config_file, parse_command_line
import traceback
import logging

def default_options():
    define('tornado_port', default=8888, help='tornado port')
    define('alexa_downurl', default='http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', help='alexa data download url')
    define('csv_cache_directory', default='./data/', help='csv file cache directory')
    define('zip_filename', default='top-1m.csv.zip', help='zipped ranking file name')
    define('mongodb_host', default='localhost', help='mongodb host')
    define('mongodb_port', default=27017, help='mongodb port')

def config_file(config_file_name):
    try:
        parse_config_file(config_file_name)
    except Exception, e:
        logging.debug(traceback.print_exc())
        logging.error(e)

def command_line():
    try:
        parse_command_line()
    except Exception, e:
        logging.debug(traceback.print_exc())
        logging.error(e)

def setup_options(config_file_name='config.ini'):
    default_options()
    config_file(config_file_name)
    command_line()

if __name__ == "__main__":
    import sys
    option_num = len(sys.argv)
    if option_num == 2:
        config_file_path = sys.argv[1]
    elif option_num == 1:
        config_file_path = ""
    else:
        logging.info("Usage: python %s config_file_path" % sys.argv[0])
        sys.exit(1)
    setup_options(config_file_path)
    logging.info("tornado_port: %s" % options.tornado_port)
    logging.info("alexa_download_url: %s" % options.alexa_downurl)
    logging.info("csv_cache_directory: %s" % options.csv_cache_directory)
    logging.info("zip_filename: %s" % options.zip_filename)
    logging.info("mongodb_host: %s" % options.mongodb_host)
    logging.info("mongodb_port: %s" % options.mongodb_port)
