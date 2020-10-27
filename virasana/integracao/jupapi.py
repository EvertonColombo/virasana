"""Funções para leitura e tratamento dos dados de pesagem e gate dos recintos.
"""
import os
from datetime import datetime, timedelta

import requests
from ajna_commons.flask.conf import SQL_URI
from ajna_commons.flask.log import logger
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from virasana.integracao.gmci_alchemy import GMCI

DTE_USERNAME = os.environ.get('DTE_USERNAME')
DTE_PASSWORD = os.environ.get('DTE_PASSWORD')

if DTE_PASSWORD is None:
    dte_file = os.path.join(os.path.dirname(__file__), 'jupapi.info')
    with open(dte_file) as dte_info:
        linha = dte_info.readline().rstrip('\n')
    DTE_USERNAME = linha.split(',')[0]
    DTE_PASSWORD = linha.split(',')[1]

API_TOKEN = 'https://jupapi.org.br/api/jupgmcialf/autenticar'
GMCI_URL = 'https://jupapi.org.br/api/jupgmcialf/gmci/PegaGmcisPorPeriodo'
FIELDS = ()

# Fields to be converted to ISODate
DATE_FIELDS = ('Date', 'UpdateDateTime', 'LastStateDateTime',
               'SCANTIME', 'ScanTime')


def get_token_api(username=DTE_USERNAME, password=DTE_PASSWORD):
    data = {'username': username, 'password': password, 'grant_type': 'password'}
    r = requests.post(API_TOKEN, data=data, verify=False)
    print(r.url)
    print(r.text)
    # print(data)
    print(r.status_code)
    token = r.json().get('access_token')
    return token


def get_gmci(datainicial, datafinal, token):
    payload = {'DataInicial': datetime.strftime(datainicial, '%d/%m/%Y %H:%M:%S'),
               'DataFinal': datetime.strftime(datafinal, '%d/%m/%Y %H:%M:%S')}
    headers = {'Authorization': 'Bearer ' + token}
    print(payload)
    r = requests.post(GMCI_URL, headers=headers, data=payload, verify=False)
    logger.debug('get_gmci ' + r.url)
    print('get_gmci', r.url)
    try:
        lista_gmci = r.json()
        return lista_gmci
    except:
        logger.error(r, r.text)


def novas_gmcis(engine, days=2):
    Session = sessionmaker(bind=engine)
    session = Session()
    start = session.query(func.max(GMCI.datahora)).scalar()
    end = start + timedelta(days=days)
    print(start, end)
    token = get_token_api()
    gmcis_dict = get_gmci(start, end, token)
    for gmci_dict in gmcis_dict['DadosGmcis']['gmci_ctr']:
        print(gmci_dict)
        gmci = GMCI()
        gmci.cod_recinto = gmci_dict['cod_recinto']
        gmci.num_gmci = gmci_dict['num_gmci']
        gmci.num_conteiner = gmci_dict['num_conteiner']
        datahora = gmci_dict['data_dt'] + ' ' + gmci_dict['hora_dt']
        gmci.datahora = datetime.strptime(datahora, '%Y-%m-%d %H:%M:%S')
        try:
            session.add(gmci)
            session.commit()
        except Exception as err:
            logger.error(err)
            session.rollback()


if __name__ == '__main__':  # pragma: no cover
    engine = create_engine(SQL_URI)
    novas_gmcis(engine, days=5)
    start = datetime.combine(datetime.today(), datetime.min.time()) - timedelta(days=2)
    end = datetime.now()
    token = get_token_api()
    print(token)
    gmcis_dict = get_gmci(start, end, token)
    print(gmcis_dict.keys())
    # print(gmcis_dict['DadosGmcis'])
    for gmci_dict in gmcis_dict['DadosGmcis']['gmci_ctr']:
        print(gmci_dict)
