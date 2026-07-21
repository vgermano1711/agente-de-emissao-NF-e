import pytest

from emissor.modelos import Destinatario, Endereco, NotaFiscal, Produto
from emissor.validadores import (
    valida_cep,
    valida_cfop,
    valida_cnpj,
    valida_cpf,
    valida_ncm,
    validar_nota,
)


def _endereco_valido() -> Endereco:
    return Endereco(
        logradouro="Rua Exemplo",
        numero="100",
        municipio="São Paulo",
        uf="SP",
        cep="01001-000",
    )


def _destinatario_valido() -> Destinatario:
    return Destinatario(
        cnpj="11.222.333/0001-81",
        razao_social="Empresa Exemplo LTDA",
        email="fiscal@empresa.com",
        endereco=_endereco_valido(),
    )


def _produto_valido() -> Produto:
    return Produto(
        descricao="Serviço de Desenvolvimento de Software",
        ncm="84719000",
        cfop="5102",
        quantidade=1,
        valor_unitario=1500.00,
        aliquota_iss=2.0,
    )


@pytest.mark.parametrize(
    "cnpj,esperado",
    [
        ("11.222.333/0001-81", True),
        ("11222333000181", True),
        ("11.222.333/0001-80", False),
        ("00000000000000", False),
        ("123", False),
    ],
)
def test_valida_cnpj(cnpj, esperado):
    assert valida_cnpj(cnpj) is esperado


@pytest.mark.parametrize(
    "cpf,esperado",
    [
        ("529.982.247-25", True),
        ("52998224725", True),
        ("529.982.247-26", False),
        ("11111111111", False),
    ],
)
def test_valida_cpf(cpf, esperado):
    assert valida_cpf(cpf) is esperado


def test_valida_ncm():
    assert valida_ncm("84719000") is True
    assert valida_ncm("847190") is False


def test_valida_cfop():
    assert valida_cfop("5102") is True
    assert valida_cfop("0102") is False
    assert valida_cfop("51") is False


def test_valida_cep():
    assert valida_cep("01001-000") is True
    assert valida_cep("0100100") is False


def test_validar_nota_sem_erros():
    nota = NotaFiscal(destinatario=_destinatario_valido(), produtos=[_produto_valido()])
    assert validar_nota(nota) == []


def test_validar_nota_reporta_todos_os_problemas():
    destinatario_invalido = _destinatario_valido()
    destinatario_invalido.cnpj = "00000000000000"
    destinatario_invalido.endereco.cep = "123"

    produto_invalido = _produto_valido()
    produto_invalido.ncm = "123"
    produto_invalido.quantidade = 0

    nota = NotaFiscal(destinatario=destinatario_invalido, produtos=[produto_invalido])
    erros = validar_nota(nota)

    assert len(erros) == 4
    assert any("CNPJ" in e for e in erros)
    assert any("CEP" in e for e in erros)
    assert any("NCM" in e for e in erros)
    assert any("quantidade" in e for e in erros)


def test_validar_nota_sem_produtos():
    nota = NotaFiscal(destinatario=_destinatario_valido(), produtos=[])
    erros = validar_nota(nota)
    assert any("nenhum produto" in e for e in erros)
