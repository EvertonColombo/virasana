"""
For tests with PyMongo and MongoDB.

Tests for sintax and operations before putting into main code

"""
import pprint
import timeit
from datetime import datetime
from pymongo import MongoClient

from virasana.workers.carga_functions import busca_info_container, \
    dados_carga_grava_fsfiles

db = MongoClient()['test']

#############################################
# CARGA - testes para checar como pegar Info do Contêiner na Base CARGA
###
container = 'tclu2967718'
container_vazio = 'apru5774515'
data_escaneamento_false = datetime.utcnow()
data_escaneamento_true = datetime.strptime('17-08-02', '%y-%m-%d')
# Teste de desempenho
reps = 3
tempo = timeit.timeit(
    stmt='busca_info_container(db, container_vazio, data_escaneamento_false)',
    number=reps, globals=globals())
print('loops(TUDO - data falsa):', reps,
      'total time:', tempo, 'per loop:', tempo / reps)
tempo = timeit.timeit(
    stmt='busca_info_container(db, container, data_escaneamento_true)',
    number=reps, globals=globals())
print('loops(cheio):', reps, 'total time:', tempo, 'per loop:', tempo / reps)
tempo = timeit.timeit(
    stmt='busca_info_container(db, container_vazio, data_escaneamento_true)',
    number=reps, globals=globals())
print('loops(vazio):', reps, 'total time:', tempo, 'per loop:', tempo / reps)

# teste de função
assert busca_info_container(db, container, data_escaneamento_false) == {}
assert busca_info_container(db, container, data_escaneamento_true) != {}
assert busca_info_container(db, container_vazio, data_escaneamento_false) == {}
assert busca_info_container(db, container_vazio, data_escaneamento_true) != {}

# Ver dados retornados do CARGA
print('Cheio')
# pprint.pprint(busca_info_container(db, container, data_escaneamento_true))
print('Vazio')
# pprint.pprint(busca_info_container(db, container_vazio,
#  data_escaneamento_true))
pprint.pprint(container)


# Teste com dados reais
data_inicio = datetime(2017, 8, 5)
file_cursor = db['fs.files'].find(
    {'metadata.carga': None,
     'metadata.dataescaneamento': {'$gt': data_inicio}})
count = file_cursor.count()
print('Total de arquivos sem metadata.carga', count, 'desde', data_inicio)
# A linha abaixo é apenas para linter não reclamar do import
dados_carga_grava_fsfiles(db, 1, 0, False)
batch_size = 100
# dados_carga_grava_fsfiles(db, 100, data_inicio)
tempo = timeit.timeit(
    stmt='dados_carga_grava_fsfiles(db, batch_size, data_inicio, False)',
    number=1, globals=globals())
print('Dados Carga do fs.files percorridos em ', tempo, 'segundos.',
      tempo / batch_size, 'por registro')

linha = db['CARGA.AtracDesatracEscala'].find().sort('dataatracacao').limit(1)
linha = next(linha)
print('Menor data de atracação (CARGA)', linha.get('dataatracacao'))
linha = db['CARGA.AtracDesatracEscala'].find().sort(
    'dataatracacao', -1).limit(1)
linha = next(linha)
print('Maior data de atracação (CARGA)', linha.get('dataatracacao'))

linha = db['fs.files'].find().sort('metadata.dataescaneamento', 1).limit(1)
linha = next(linha)
print('Menor data de importação (IMAGENS)',
      linha.get('metadata').get('dataescaneamento'))
linha = db['fs.files'].find().sort('metadata.dataescaneamento', -1).limit(1)
linha = next(linha)
print('Maior data de importação (IMAGENS)',
      linha.get('metadata').get('dataescaneamento'))


# Exemplo de script para atualizar um campo com base em outro
#  caso dados mudem de configuração, campos mudem de nome, etc
cursor = db['fs.files'].find({'metadata.dataescaneamento': None})
print(cursor.count())
for linha in cursor:
    data = linha.get('metadata').get('dataimportacao')
    db['fs.files'].update(
        {'_id': linha['_id']},
        {'$set': {'metadata.dataescaneamento': data}}
    )
