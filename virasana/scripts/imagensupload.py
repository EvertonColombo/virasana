"""Script de linha de comando para processar diretório de arquivos BSON.

Script de linha de comando para fazer atualização 'manual'
processando diretório contendo arquivos BSON gerados pelo Avatar

Args:

    --dir: diretório a processar
    --dir: endereço do Servidor Virasana
    --sync: Fazer upload de forma síncrona (True ou False)

"""
import os
import click

from virasana.workers.dir_monitor import VIRASANA_URL, despacha_dir

BSON_DIR = os.path.join(os.path.dirname(__file__), 'BSON')


@click.command()
@click.option('--dir', default=BSON_DIR,
              help='diretório a processar - padrão %s ' % BSON_DIR)
@click.option('--url', default=VIRASANA_URL,
              help='URL do Servidor - padrão %s ' % VIRASANA_URL)
@click.option('--sync', is_flag=True,
              help='Fazer consulta de forma síncrona')
def carrega(dir, url, sync):
    """Script de linha de comando para integração do arquivo XML."""
    dir, erros, exceptions = despacha_dir(dir=dir, url=url, sync=sync)
    print('Diretorio processado: %s' %  dir +
          '\nErros: %s' % erros +
          '\nExceções: %s' % exceptions)


if __name__ == '__main__':
    carrega()
