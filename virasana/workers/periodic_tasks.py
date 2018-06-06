"""
Definição dos códigos que serão rodados pelo Celery.

Background tasks do sistema AJNA-virasana
Gerenciados por celery.sh
Aqui ficam as rotinas que serão chamadas periodicamente.

"""
from datetime import datetime, timedelta

from celery import Celery
from pymongo import MongoClient

from ajna_commons.flask.conf import (BACKEND, BROKER, DATABASE,
                                     MONGODB_URI)
from virasana.integracao import carga, xmli

from .dir_monitor import despacha_dir


celery = Celery(__name__, broker=BROKER,
                backend=BACKEND)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Agenda tarefas que serão executadas com frequência fixa."""
    sender.add_periodic_task(15 * 61.0, processa_carga.s())
    sender.add_periodic_task(11 * 60.0, processa_xml.s())
    sender.add_periodic_task(4 * 57.0, processa_bson.s())


@celery.task
def processa_xml():
    """Verifica se há arquivos XML a carregar no GridFS.

    Verifica se há novas imagens no Banco de Dados que ainda estão
    sem a integração com XML. Havendo, grava dados XML disponíveis,
    se encontrados, no GridFS
    """
    with MongoClient(host=MONGODB_URI) as conn:
        db = conn[DATABASE]
        cincodias = datetime.now() - timedelta(days=5)
        xmli.dados_xml_grava_fsfiles(db, 10000, cincodias)
        # Olhar o passado tbm...
        doisanos = datetime.now() - timedelta(days=730)
        xmli.dados_xml_grava_fsfiles(db, 10000, doisanos)


@celery.task
def processa_carga():
    """Verifica se há dados do Sistema CARGA a carregar no GridFS.

    Verifica se há novas imagens no Banco de Dados que ainda estão
    sem a integração com o sistema CARGA. Havendo, grava dados disponíveis,
    se encontrados, no GridFS
    """
    with MongoClient(host=MONGODB_URI) as conn:
        db = conn[DATABASE]
        doisdias = datetime.now() - timedelta(days=2)
        carga.dados_carga_grava_fsfiles(db, 5000, doisdias)


@celery.task
def processa_bson():
    """Chama função do módulo dir_monitor.

    Para permitir o upload de BSON do AVATAR através da simples
    colocação do arquivo em um diretório.
    Neste módulo pode ser configurado o endereço de um diretório
    e o endereço do virasana. A função a seguir varre o diretório e,
    havendo arquivos, envia por request POST para o URL do virasana.
    Se obtiver sucesso, exclui o arquivo enviado do diretório.


    """
    despacha_dir()
