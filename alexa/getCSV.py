import timecount
import config_alexa
from tornado.options import options

import urllib
import zipfile
import os

class GetCSV():
    def unzip(self):
        zip_file = zipfile.ZipFile(self.zip_path, "r")
        for filename in zip_file.namelist():
            unzip_file = file(options.csv_cache_directory + filename, "wb")
            unzip_file.write(zip_file.read(filename))
            unzip_file.close()
        zip_file.close()

    def get_csv(self):
        t = timecount.Timecount()
        csv_filename = str(t.start())[:-16] + ".csv"
        if os.path.isdir(options.csv_cache_directory) == False:
            os.mkdir(options.csv_cache_directory)
        self.zip_path = options.csv_cache_directory + options.zip_filename
        self.csv_path = options.csv_cache_directory + csv_filename

        urllib.urlretrieve(options.alexa_download_url, self.zip_path)
        self.unzip()
        os.rename(self.zip_path[:-4], self.csv_path)

        print " --end: get_csv : ", t.end()
        return options.csv_cache_directory + csv_filename

if __name__ == "__main__":
#    config_alexa.setup_options("../config.ini")
    config_alexa.setup_options("/Users/uranoshouhei/alexa/config.ini")
    
    g = GetCSV()
    g.get_csv()
