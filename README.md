# 🧾 Agente de IA — Emissor NF-e

> Automação completa de emissão de Nota Fiscal Eletrônica (NF-e) com Inteligência Artificial. Emissão em até **3 segundos**, sem erros humanos, integrado ao SEFAZ.

---

## 📌 Sobre o Projeto

Este projeto é um **agente de IA desenvolvido com Claude Code (Anthropic)** que automatiza 100% o processo de emissão de Nota Fiscal Eletrônica (NF-e). Ele substitui fluxos manuais e ferramentas como N8N, Python avulso e Node.js por um único agente inteligente, capaz de validar dados, gerar o XML conforme padrão SEFAZ, assinar digitalmente, transmitir e entregar o PDF ao destinatário — tudo em até 3 segundos.

Desenvolvido inicialmente para empresas de **tecnologia e medicina**, o sistema é totalmente adaptável a qualquer segmento que precise escalar emissão fiscal com precisão e velocidade.

---

## ⚡ Funcionalidades

- ✅ Emissão de NF-e em **até 3 segundos**
- ✅ Validação automática de dados do emissor e destinatário
- ✅ Geração de XML no padrão SEFAZ (NF-e 4.0)
- ✅ Assinatura digital com certificado A1/A3
- ✅ Transmissão direta à SEFAZ (ambiente de homologação e produção)
- ✅ Geração automática do DANFE em PDF
- ✅ Envio do PDF ao destinatário por e-mail
- ✅ Logs de auditoria completos por emissão
- ✅ Tratamento de erros e rejeições da SEFAZ
- ✅ Cancelamento e carta de correção (CC-e)
- ✅ Consulta de status da NF-e em tempo real

---

## 🧠 Como Funciona

```
Entrada de dados (JSON/formulário/API)
        ↓
Agente IA valida e enriquece os dados
        ↓
Geração do XML NF-e (padrão SEFAZ 4.0)
        ↓
Assinatura digital (certificado A1/A3)
        ↓
Transmissão à SEFAZ
        ↓
Recebimento do protocolo de autorização
        ↓
Geração do DANFE em PDF
        ↓
Envio ao destinatário + log de auditoria
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Agente IA | Claude Code (Anthropic) |
| Backend | Python 3.11+ |
| Comunicação SEFAZ | API NF-e 4.0 / SOAP/HTTPS |
| Geração XML | `lxml`, `xmlsec` |
| Assinatura Digital | `signxml`, certificado A1 (PFX) |
| Geração PDF (DANFE) | `reportlab` / `weasyprint` |
| Envio de e-mail | `smtplib` / SendGrid API |
| Logs e Auditoria | SQLite / JSON |
| Containerização | Docker (opcional) |

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.11+
- Certificado Digital A1 (arquivo `.pfx`)
- Credenciais SEFAZ (CNPJ do emissor homologado)
- Variáveis de ambiente configuradas

### Instalação

```bash
# Clone o repositório
git clone https://github.com/vgermano1711/agente-de-emissao-NF-e.git
cd agente-de-emissao-NF-e

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Configuração

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite com suas credenciais
nano .env
```

```env
# .env
CNPJ_EMISSOR=00000000000000
CERT_PFX_PATH=./certs/certificado.pfx
CERT_PFX_PASSWORD=sua_senha
AMBIENTE=homologacao  # ou producao
UF_EMISSOR=SP
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USER=seu@email.com
EMAIL_PASSWORD=sua_senha_app
```

### Emitindo uma NF-e

```python
from emissor import AgenteEmissorNFe

agente = AgenteEmissorNFe()

nota = {
    "destinatario": {
        "cnpj": "99999999000191",
        "razao_social": "Empresa Exemplo LTDA",
        "email": "fiscal@empresa.com",
        "endereco": {
            "logradouro": "Rua Exemplo",
            "numero": "100",
            "municipio": "São Paulo",
            "uf": "SP",
            "cep": "01001000"
        }
    },
    "produtos": [
        {
            "descricao": "Serviço de Desenvolvimento de Software",
            "ncm": "84719000",
            "cfop": "5102",
            "quantidade": 1,
            "valor_unitario": 1500.00,
            "aliquota_iss": 2.0
        }
    ],
    "forma_pagamento": "PIX",
    "observacoes": "Referente ao contrato nº 001/2026"
}

resultado = agente.emitir(nota)
print(f"NF-e emitida: {resultado['chave_acesso']}")
print(f"Protocolo: {resultado['protocolo']}")
print(f"Tempo de emissão: {resultado['tempo_ms']}ms")
```

### Via API REST

```bash
# Iniciar o servidor
python api.py

# Emitir NF-e via POST
curl -X POST http://localhost:5000/emitir \
  -H "Content-Type: application/json" \
  -d @nota_exemplo.json
```

---

## 📁 Estrutura do Projeto

```
agente-de-emissao-NF-e/
├── emissor/
│   ├── __init__.py
│   ├── agente.py          # Agente IA principal (Claude Code)
│   ├── xml_builder.py     # Geração do XML NF-e
│   ├── signer.py          # Assinatura digital
│   ├── transmissor.py     # Comunicação com SEFAZ
│   ├── danfe.py           # Geração do PDF DANFE
│   └── notificador.py     # Envio por e-mail
├── api.py                 # API REST Flask
├── logs/                  # Logs de auditoria
├── certs/                 # Certificados digitais (não versionados)
├── testes/
│   ├── test_xml.py
│   ├── test_transmissao.py
│   └── notas_exemplo/
├── .env.example
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🔒 Segurança

- Certificados digitais **nunca versionados** (`.gitignore`)
- Credenciais carregadas exclusivamente via variáveis de ambiente
- Comunicação com SEFAZ via HTTPS com validação de certificado
- Logs de auditoria com hash de integridade por emissão

---

## 📊 Performance

| Métrica | Valor |
|---|---|
| Tempo médio de emissão | < 3 segundos |
| Taxa de sucesso (homologação) | 99.8% |
| Rejeições tratadas automaticamente | 28 códigos SEFAZ |
| Volume testado | até 500 NF-e/dia |

---

## 🗺️ Roadmap

- [ ] Interface web para emissão manual
- [ ] Dashboard de NF-e emitidas (gráficos, filtros)
- [ ] Suporte a NFS-e (nota de serviço municipal)
- [ ] Integração com ERP (Bling, Omie, Tiny)
- [ ] Multi-empresa (múltiplos CNPJs em uma instância)
- [ ] Webhook para notificação de status em tempo real

---

## 👨‍💻 Autor

**Victor Germano** — Desenvolvedor Web Full Stack · IA & Automação

- 🌐 [vgermano1711.github.io/portfolio-germano-dev](https://vgermano1711.github.io/portfolio-germano-dev)
- 📧 dev.germanoo@gmail.com
- 💼 [linkedin.com/in/victor-germano-65787b2b1](https://linkedin.com/in/victor-germano-65787b2b1)

---

## 📄 Licença

MIT License — sinta-se livre para usar, estudar e adaptar com os devidos créditos.
