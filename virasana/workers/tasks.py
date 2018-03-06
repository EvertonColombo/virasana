"""
Definição dos códigos que serão rodados pelo Celery.

Background tasks do sistema AJNA-virasana
Gerenciados por celery.sh
Aqui ficam as rotinas que serão chamadas periodicamente e
aquelas que rodam tarefas custosas/demoradas em background.

"""
# Código dos celery tasks
import json
import requests
import time
from base64 import decodebytes

import gridfs
from celery import Celery, states
from pymongo import MongoClient

from ajna_commons.flask.conf import (BACKEND, BROKER, BSON_REDIS, DATABASE,
                                     MONGODB_URI, redisdb)
from ajna_commons.models.bsonimage import BsonImageList

celery = Celery(__name__, broker=BROKER,
                backend=BACKEND)


def trata_bson(bson_file: str, db: MongoClient) -> list:
    """Recebe o nome de um arquivo bson e o insere no MongoDB."""
    # .get_default_database()
    fs = gridfs.GridFS(db)
    bsonimagelist = BsonImageList.fromfile(abson=bson_file)
    files_ids = bsonimagelist.tomongo(fs)
    return files_ids


@celery.task(bind=True)
def raspa_dir(self):
    """De base em arquivos para mongoDB.

    Background task that go to redis DB of incoming files
    AND load then to mongodb
    """
    self.update_state(state=states.STARTED,
                      meta={'current': '',
                            'status': 'Iniciando'})
    q = redisdb.lpop(BSON_REDIS)
    q = json.loads(q.decode('utf-8'))
    self.update_state(meta={'current': q.get('filename'),
                            'status': 'Processando arquivo'})
    file = bytes(q['bson'], encoding='utf-8')
    file = decodebytes(file)
    with MongoClient(host=MONGODB_URI) as conn:
        db = conn[DATABASE]
        trata_bson(file, db)
    return {'current': '',
            'status': 'Todos os arquivos processados'}


