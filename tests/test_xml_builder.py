import pytest

from emissor.modelos import Destinatario, Endereco, NotaFiscal, Produto
from emissor.xml_builder import NotaInvalidaError, construir_xml


def _nota_valida() -> NotaFiscal:
    return NotaFiscal(
        destinatario=Destinatario(
            cnpj="11.222.333/0001-81",
            razao_social="Empresa Exemplo LTDA",
            email="fiscal@empresa.com",
            endereco=Endereco(
                logradouro="Rua Exemplo",
                numero="100",
                municipio="São Paulo",
                uf="SP",
                cep="01001-000",
            ),
        ),
        produtos=[
            Produto(
                descricao="Serviço de Desenvolvimento de Software",
                ncm="84719000",
                cfop="5102",
                quantidade=1,
                valor_unitario=1500.00,
                aliquota_iss=2.0,
            )
        ],
        forma_pagamento="PIX",
        observacoes="Referente ao contrato nº 001/2026",
    )


def test_construir_xml_gera_elementos_esperados():
    xml = construir_xml(_nota_valida())

    assert "<notaFiscal>" in xml
    assert "<cnpj>11.222.333/0001-81</cnpj>" in xml
    assert "<descricao>Serviço de Desenvolvimento de Software</descricao>" in xml
    assert "<valorTotal>1500.00</valorTotal>" in xml


def test_construir_xml_rejeita_nota_invalida():
    nota = _nota_valida()
    nota.destinatario.cnpj = "00000000000000"

    with pytest.raises(NotaInvalidaError) as exc_info:
        construir_xml(nota)

    assert "CNPJ" in str(exc_info.value)
