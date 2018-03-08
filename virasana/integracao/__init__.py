"""
Funções padrão para exploração do GridFS.

Como repositório de informações do Banco de Dados, facilitando a documentação
e o desenvolvimento.

Assim, neste arquivo e nos demais deste módulo pode-se conferir como está
sendo estruturado o Banco de Dados final, que nada mais é do que a integração
de diversas fontes de dados, cada uma com seu módulo neste pacote. Pode-se
também conferir os campos chave para os quais estão sendo criados índices,
conferir as "chaves primária e estrangeira", as datas, categorias, etc.

Além disso, podem ser criadas e mantidas aqui funções que dêem estatíticas
sobre a base para informar os usuários.

"""
from virasana.integracao import carga
from virasana.integracao import xml

IMAGENS = {'metadata.contentType': 'image/jpeg'}


def gridfs_count(db, filtro):
    """Aplica filtro, retorna contagem."""
    return db['fs.files'].find(filtro).count()


def stats_resumo(db):
    """Números gerais do Banco de Dados e suas integrações.""" 
    filtro = IMAGENS
    stats = {}
    total = gridfs_count(db, filtro)
    stats['total'] = total
    filtro = carga.FALTANTES
    stats['carga'] = total - gridfs_count(db, filtro)
    filtro = xml.FALTANTES
    stats['xml'] = total - gridfs_count(db, filtro)
    return stats


def plot_bars(lista):
    """Gera gráfico de barras da lista de valores."""
    pass


def stats_por_XXX(db):
    """XXX."""
    pass


def datas_bases(db):
    """Retorna nomes dos campos que possuem as datas de referência em cada
    integração"""
    pass