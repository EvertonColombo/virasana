import time
import sys
from datetime import datetime

# from gridfs import GridFS
from pymongo import MongoClient

from virasana.integracao import create_indexes, carga


db = MongoClient()['test']

create_indexes(db)
carga.create_indexes(db)


if len(sys.argv) > 1 and sys.argv[1] == 'update':
    print('Começando a procurar por dados do CARGA a inserir')
    batch_size = 8000
    today = datetime.today()
    if len(sys.argv) > 2:
        year = int(sys.argv[2])
    else:
        year = today.year
    if len(sys.argv) > 3:
        month = int(sys.argv[3])
    else:
        month = today.month

    print(year, month)
    for day in range(1, 30, 10):
        data_inicio = datetime(year, month, day)
        print('Data início', data_inicio)
        tempo = time.time()
        carga.dados_carga_grava_fsfiles(db, batch_size, data_inicio, days=4)
        tempo = time.time() - tempo
        print(batch_size, 'dados Carga do fs.files percorridos em ',
              tempo, 'segundos.',
              tempo / batch_size, 'por registro')
