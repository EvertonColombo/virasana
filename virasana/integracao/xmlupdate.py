"""Script de linha de comando para integração do arquivo XML.

Script de linha de comando para fazer atualização 'manual'
dos metadados do arquivo XML nas imagens.
Args:
    year: ano de início da pesquisa
    month: mês de início da pesquisa
    batch_size: tamanho do lote de atualização/limite de registros da consulta

"""
import time
from datetime import datetime

import click
from pymongo import MongoClient

from virasana.integracao import create_indexes, gridfs_count, xmli

batch_size = 50000
today = datetime.today()


@click.command()
@click.option('--year', default=today.year, help='Ano - padrão atual')
@click.option('--month', default=today.month, help='Mes - padrão atual')
@click.option('--batch_size', default=batch_size,
              help='Tamanho do lote - padrão' + str(batch_size))
def update(year, month, batch_size):
    """Script de linha de comando para integração do arquivo XML."""
    db = MongoClient()['test']
    create_indexes(db)
    xmli.create_indexes(db)
    print('Começando a procurar por dados de XML a inserir')
    number = gridfs_count(db, xmli.FALTANTES)
    print(number, 'registros sem metadata de xml')
    print(year, month, batch_size)
    data_inicio = datetime(year, month, 1)
    print('Data início', data_inicio)
    tempo = time.time()
    xmli.dados_xml_grava_fsfiles(db, batch_size, data_inicio)
    tempo = time.time() - tempo
    print(batch_size, 'dados XML do fs.files percorridos em ',
          tempo, 'segundos.',
          tempo / batch_size, 'por registro')


if __name__ == '__main__':
    update()
