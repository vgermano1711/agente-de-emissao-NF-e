"""Geração do XML interno da nota fiscal.

Este módulo produz uma representação XML estruturada dos dados da nota,
já validados. Ele NÃO implementa o schema oficial da NF-e 4.0 exigido pela
SEFAZ (assinatura digital, protocolo de transmissão, etc. — ver Roadmap no
README) — é a base sobre a qual essas etapas serão construídas.
"""

import xml.etree.ElementTree as ET

from .modelos import NotaFiscal
from .validadores import validar_nota


class NotaInvalidaError(ValueError):
    def __init__(self, erros: list[str]):
        self.erros = erros
        super().__init__("Nota fiscal inválida: " + "; ".join(erros))


def construir_xml(nota: NotaFiscal) -> str:
    erros = validar_nota(nota)
    if erros:
        raise NotaInvalidaError(erros)

    raiz = ET.Element("notaFiscal")

    dest = ET.SubElement(raiz, "destinatario")
    ET.SubElement(dest, "cnpj").text = nota.destinatario.cnpj
    ET.SubElement(dest, "razaoSocial").text = nota.destinatario.razao_social
    ET.SubElement(dest, "email").text = nota.destinatario.email

    endereco = ET.SubElement(dest, "endereco")
    ET.SubElement(endereco, "logradouro").text = nota.destinatario.endereco.logradouro
    ET.SubElement(endereco, "numero").text = nota.destinatario.endereco.numero
    ET.SubElement(endereco, "municipio").text = nota.destinatario.endereco.municipio
    ET.SubElement(endereco, "uf").text = nota.destinatario.endereco.uf
    ET.SubElement(endereco, "cep").text = nota.destinatario.endereco.cep

    produtos = ET.SubElement(raiz, "produtos")
    for produto in nota.produtos:
        item = ET.SubElement(produtos, "produto")
        ET.SubElement(item, "descricao").text = produto.descricao
        ET.SubElement(item, "ncm").text = produto.ncm
        ET.SubElement(item, "cfop").text = produto.cfop
        ET.SubElement(item, "quantidade").text = str(produto.quantidade)
        ET.SubElement(item, "valorUnitario").text = f"{produto.valor_unitario:.2f}"
        ET.SubElement(item, "valorTotal").text = f"{produto.valor_total:.2f}"
        ET.SubElement(item, "aliquotaIss").text = f"{produto.aliquota_iss:.2f}"

    ET.SubElement(raiz, "formaPagamento").text = nota.forma_pagamento
    ET.SubElement(raiz, "observacoes").text = nota.observacoes
    ET.SubElement(raiz, "valorTotal").text = f"{nota.valor_total:.2f}"

    ET.indent(raiz, space="  ")
    return ET.tostring(raiz, encoding="unicode", xml_declaration=False)
