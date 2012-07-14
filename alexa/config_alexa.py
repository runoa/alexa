#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
from tornado.options import define, options, parse_config_file, parse_command_line
import traceback
import logging

def setup_options(config_file_name='config.ini'):
    define('tornado_port', default=8888, help='tornado port')
    define('alexa_download_url', default='http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', help='alexa data download url')
    define('csv_cache_directory', default='./data/', help='csv file cache directory')
    define('zip_filename', default='top-1m.csv.zip', help='zipped ranking file name')
    define('mongodb_host', default='localhost', help='mongodb host')
    define('mongodb_port', default=27017, help='mongodb port')
    # config file
    try:
        parse_config_file(config_file_name)
    except Exception, e:
        logging.debug(traceback.print_exc())
        logging.error(e)
    # command line
    try:
        parse_command_line()
    except Exception, e:
        logging.debug(traceback.print_exc())
        logging.error(e)
    logging.info('tornado_port=%d' % options.tornado_port)
    logging.info('mongodb_host=%s' % options.mongodb_host)
    logging.info('mongodb_port=%d' % options.mongodb_port)
