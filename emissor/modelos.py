from dataclasses import dataclass, field


@dataclass
class Endereco:
    logradouro: str
    numero: str
    municipio: str
    uf: str
    cep: str


@dataclass
class Destinatario:
    cnpj: str
    razao_social: str
    email: str
    endereco: Endereco


@dataclass
class Produto:
    descricao: str
    ncm: str
    cfop: str
    quantidade: float
    valor_unitario: float
    aliquota_iss: float = 0.0

    @property
    def valor_total(self) -> float:
        return round(self.quantidade * self.valor_unitario, 2)


@dataclass
class NotaFiscal:
    destinatario: Destinatario
    produtos: list[Produto] = field(default_factory=list)
    forma_pagamento: str = ""
    observacoes: str = ""

    @property
    def valor_total(self) -> float:
        return round(sum(p.valor_total for p in self.produtos), 2)
