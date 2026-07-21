import re

from .modelos import NotaFiscal

_CFOP_PRIMEIRO_DIGITO_VALIDO = {"1", "2", "3", "5", "6", "7"}


def _somente_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor)


def valida_cnpj(cnpj: str) -> bool:
    digitos = _somente_digitos(cnpj)
    if len(digitos) != 14 or digitos == digitos[0] * 14:
        return False

    def calcular_dv(base: str) -> str:
        pesos = list(range(len(base) - 7, 1, -1)) + list(range(9, 1, -1))
        pesos = pesos[: len(base)]
        soma = sum(int(d) * p for d, p in zip(base, pesos))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    dv1 = calcular_dv(digitos[:12])
    dv2 = calcular_dv(digitos[:12] + dv1)
    return digitos[-2:] == dv1 + dv2


def valida_cpf(cpf: str) -> bool:
    digitos = _somente_digitos(cpf)
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        return False

    def calcular_dv(base: str) -> str:
        peso_inicial = len(base) + 1
        pesos = range(peso_inicial, 1, -1)
        soma = sum(int(d) * p for d, p in zip(base, pesos))
        resto = (soma * 10) % 11
        return "0" if resto == 10 else str(resto)

    dv1 = calcular_dv(digitos[:9])
    dv2 = calcular_dv(digitos[:9] + dv1)
    return digitos[-2:] == dv1 + dv2


def valida_ncm(ncm: str) -> bool:
    digitos = _somente_digitos(ncm)
    return len(digitos) == 8


def valida_cfop(cfop: str) -> bool:
    digitos = _somente_digitos(cfop)
    return len(digitos) == 4 and digitos[0] in _CFOP_PRIMEIRO_DIGITO_VALIDO


def valida_cep(cep: str) -> bool:
    return len(_somente_digitos(cep)) == 8


def validar_nota(nota: NotaFiscal) -> list[str]:
    """Retorna a lista de problemas encontrados na nota. Lista vazia = nota válida."""
    erros: list[str] = []

    if not valida_cnpj(nota.destinatario.cnpj):
        erros.append(f"CNPJ do destinatário inválido: {nota.destinatario.cnpj}")

    if not nota.destinatario.razao_social.strip():
        erros.append("Razão social do destinatário não informada")

    if not valida_cep(nota.destinatario.endereco.cep):
        erros.append(f"CEP do destinatário inválido: {nota.destinatario.endereco.cep}")

    if not nota.produtos:
        erros.append("A nota não possui nenhum produto/serviço")

    for i, produto in enumerate(nota.produtos, start=1):
        if not valida_ncm(produto.ncm):
            erros.append(f"Produto {i}: NCM inválido ({produto.ncm})")
        if not valida_cfop(produto.cfop):
            erros.append(f"Produto {i}: CFOP inválido ({produto.cfop})")
        if produto.quantidade <= 0:
            erros.append(f"Produto {i}: quantidade deve ser maior que zero")
        if produto.valor_unitario <= 0:
            erros.append(f"Produto {i}: valor unitário deve ser maior que zero")

    return erros
