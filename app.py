
import boto3
from filelock import FileLock
import logging, os
from config import *

config = Config()
logging.getLogger('').handlers = []
logging.basicConfig(filename=config['logging']['log_path'], level=config['logging']['log_level'], format=config['logging']['log_format'])
lock_file = 'yandex_object_storage.lock'
lock = FileLock(lock_file)

def process_lock():
    if lock.is_locked:
        logging.critical('Process already running, can not lock file %s' % lock_file)
        exit(1)
    lock.acquire()

def process_unlock():
    if lock.is_locked is not True:
        logging.critical('Can not unlock file %s' % lock_file)
        exit(1)
    lock.release()

def connectionYOS(aws_access_key_id, aws_secret_access_key ):

    logging.debug('Creating connection to storage.yandexcloud')
    # session = boto3.session.Session()
    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        s3 = session.client(service_name='s3',
                            endpoint_url='https://storage.yandexcloud.net')
        return s3
    except Exception as e:
        logging.error('Error occurred because the app couldn\'t build connection with the Object Storage: ' + str(e))


def create_bucket(s3, buscketname):
    try:
        s3.create_bucket(Bucket=buscketname)
    except Exception as e:
        logging.error('Error occured while trying to built bucket ' + buscketname + ' ' + str(e))


def getListofFiles (s3, buscketname):
    listOfFiles = []
    for files in s3.list_objects(Bucket=buscketname)['Contents']:
        try:
            fileInfo = {'File': files['Key'], 'Owner': files['Owner']['DisplayName'], 'ETag': files['ETag'],
                        'Type Of Storage': files['StorageClass'], 'Last Modified': str(files['LastModified']),
                        'Size': files['Size'], 'Link': downloadUrlGenerator(files['Key'])}
            listOfFiles.append(fileInfo)
        except Exception as e:
            logging.error('Error occured while trying to get names of files from ' + buscketname + ' ' +str(e))
    return listOfFiles


def uploadFiles(s3, bucketname, uploading_folder):
    for filename in os.listdir(uploading_folder):
        try:
            logging.debug('Uploading ' + bucketname + '...')
            s3.upload_file(uploading_folder + filename, bucketname, filename)
        except Exception as e:
            logging.error('Error while uploading ' + uploading_folder + str(e))


def deleteAllCalls(s3, bucketname):
    forDeletion = []
    allFiles = getListofFiles(s3, bucketname)

    for file in allFiles:
        newMap = {'Key': file['File']}
        forDeletion.append(newMap)

    try:
        s3.delete_objects(Bucket=bucketname, Delete={'Objects': forDeletion})
    except Exception as e:
        logging.error('Could\'t run deletion Function' + str(e))

def deleteCall(s3, bucketname, filename):
    forDeletion = [{'Key': filename + '.wav'}]
    try:
        response = s3.delete_objects(Bucket=bucketname, Delete={'Objects': forDeletion})
        logging.info('the file {} have been removed'.format(response))
    except Exception as e:
        logging.error('Could\'t delete file' + str(e))


def downloadUrlGenerator(filename):
    return 'https://storage.yandexcloud.net/neuro-call-records/' + filename



bucketname = config['general']['bucketname']
uploading_folder = config['general']['uploading_folder']
aws_access_key_id = config['general']['aws_access_key_id']
aws_secret_access_key = config['general']['aws_secret_access_key']
s3 = connectionYOS(aws_access_key_id, aws_secret_access_key)
process_lock()

try:
    uploadFiles(s3, bucketname, uploading_folder)

except Exception as e:
    logging.critical(e, exc_info=True)

process_unlock()
logging.info('done')



# if __name__ == '__main__':
#
#     s3 = connectionYOS()
#     bucketname = 'neuro-call-records'
#     # listOfFiles = getListofFiles(s3, bucketname)
#     # print(listOfFiles)
#     # uploadind_folder ='/home/ekoblov/Загрузки/sync/'
#     # uploadFiles(s3, bucketname, uploadind_folder)
#     filename = '32fc23ee-ef2f-11e9-90d1-ff8b43c97eb3'
#     deleteCall(s3, bucketname, filename)



