# Barz Media API — portfólio técnico

API demonstrativa em FastAPI para distribuir playlists a telas e receber estado de reprodução. Esta edição foi escrita do zero para portfólio e usa somente dados sintéticos em memória.

## Problema

Uma plataforma de mídia precisa entregar uma playlist consistente a cada tela, validar telemetria recebida e oferecer uma visão operacional simples. A API deve manter contratos claros e falhar sem revelar detalhes de infraestrutura.

## Solução

O serviço expõe endpoints de saúde, playlist, estado da tela, eventos de reprodução e resumo administrativo. Modelos Pydantic limitam tamanho, domínio e faixa dos dados. Um repositório em memória torna o exemplo executável sem banco, credenciais ou serviços externos.

## Arquitetura

- `app/models.py`: contratos e validação;
- `app/store.py`: estado sintético isolado por instância;
- `app/main.py`: rotas HTTP e tratamento genérico de erros;
- `tests/`: testes de contrato, mutação de estado e limites.

## Endpoints

- `GET /health`
- `GET /api/screens/{screen_id}/playlist`
- `POST /api/screens/{screen_id}/status`
- `POST /api/screens/{screen_id}/playback`
- `GET /api/admin/overview`
- `GET /docs`

Use `screen-demo` como identificador da demonstração.

## Como executar

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn app.main:app --reload
```

A documentação interativa estará em `http://127.0.0.1:8000/docs`.

## Segurança

O projeto não contém banco, token, endereço interno, dado de cliente, arquivo de mídia real ou histórico privado. Respostas de erro não expõem caminhos ou infraestrutura. Entradas têm limites explícitos e o pipeline aplica allowlist, scanner independente e aprovação por snapshot.

## Limitações

- armazenamento exclusivamente em memória;
- sem autenticação, autorização, rate limit ou auditoria persistente;
- uma única tela e duas mídias sintéticas;
- não indicado para publicação na internet sem as camadas de produção acima;
- não representa a topologia nem o código do backend privado.

## Minha participação

Projeto de autoria própria: desenho de contratos, validação, endpoints, modelo de estado, testes e pipeline seguro de portfólio.

## Uso e contribuições

Disponível apenas para leitura e avaliação profissional. Não aceita contribuições. Consulte [PORTFOLIO_NOTICE.md](PORTFOLIO_NOTICE.md).
