# Barz Media API

API demonstrativa em FastAPI para entregar playlists sintéticas, receber o estado de uma tela e registrar eventos de reprodução em memória.

> Projeto independente escrito para portfólio, usando somente dados sintéticos. Não contém banco, credencial, mídia real, endereço interno, dado de cliente ou código do backend privado.

## Problema

Uma API de mídia precisa definir contratos claros, validar entradas e responder sem revelar detalhes de infraestrutura. Para uma demonstração pública, ela também precisa ser executável sem serviços externos ou dados reais.

## Solução implementada

O serviço reúne endpoints de saúde, playlist, estado da tela, eventos de reprodução e resumo administrativo. Modelos Pydantic limitam tipos, tamanhos e faixas. Um repositório em memória mantém o exemplo pequeno e reproduzível.

## Tecnologias

- Python 3.11;
- FastAPI e Uvicorn;
- Pydantic para validação de contratos;
- Pytest e cliente de testes HTTP;
- exportador fail-closed com allowlist e aprovação por snapshot.

## Funcionalidades demonstradas

- health check;
- playlist sintética por tela;
- validação e atualização do estado da tela;
- recepção e agregação de eventos de reprodução;
- visão administrativa resumida em memória;
- respostas de erro genéricas para entradas inválidas ou telas inexistentes.

## Arquitetura

- `app/models.py`: modelos e limites dos contratos;
- `app/store.py`: estado sintético isolado por instância;
- `app/main.py`: rotas HTTP e tratamento de erros;
- `tests/`: contratos, mutação de estado e limites.

## Endpoints

- `GET /health`
- `GET /api/screens/{screen_id}/playlist`
- `POST /api/screens/{screen_id}/status`
- `POST /api/screens/{screen_id}/playback`
- `GET /api/admin/overview`
- `GET /docs`

Use `screen-demo` na demonstração. Todos os IDs, URLs e conteúdos retornados são sintéticos.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

A documentação interativa ficará em `http://127.0.0.1:8000/docs`.

## Testes e validação

Os testes exercitam os endpoints, a validação de domínio, o isolamento do estado e os limites dos eventos. O pipeline do portfólio rejeita arquivos fora do manifesto, verifica hashes, procura segredos e exige aprovação vinculada ao snapshot.

## Segurança

Execute somente em `127.0.0.1`. O projeto não possui autenticação, autorização, rate limit, TLS, banco, auditoria persistente ou controles de implantação pública. Ele não deve ser exposto à internet.

## Limitações

- armazenamento exclusivamente em memória, perdido ao reiniciar;
- uma tela e duas mídias sintéticas;
- sem autenticação, autorização ou persistência;
- contrato criado apenas para esta demonstração de API;
- não representa topologia, endpoints nem código do backend privado;
- não é apresentado como o servidor compatível com o **Barz Player** nesta fase.

## Minha participação e direitos

Desenho dos contratos, validação, endpoints, modelo de estado, testes, pipeline seguro e documentação: Junior Barz.

Disponível apenas para leitura e avaliação profissional. Não aceita contribuições. Consulte [PORTFOLIO_NOTICE.md](PORTFOLIO_NOTICE.md).
