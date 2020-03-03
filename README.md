** fills files to storage.yandexcloud.net (Yandex Cloud Storage)**
** all necessary methods have been implemented**

**Setting**
- you need to install the venv virtual environment
- - then execute ./venv/bin/zip 3.7 install-r requirements.txt
- copy the default config * * config.ini.default** in * * config.ini** and edit your environment settings

[logging] - logging
- log_path: path to the log file, if empty, in stdout stderr
- - log_level: NOT SET, DEBUG, INFO, WARNING, ERROR, CRITICAL 
- log_format: log record format (asctime, levelname, message)

[general]
bucketname = bucket name
uploading_ifolder = folder from where we transfer calls
aws_access_key_id= key id 
aws_secret_access_key= secret static key