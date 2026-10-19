# Anexos no Trello

Cobre só o que esta skill precisa: achar o cartão de cada `POST NN` e anexar
os arquivos. Estrutura do quadro, etiquetas e `trello.json`:
`../../conteudo-mensal/references/trello.md`.

## Casar arte → cartão
- O número está no nome do cartão: `POST 01 · ...`, `POST 02 · ...`. O
  número que o script devolve casa com esse `NN`.
- Filtrar pela **etiqueta do mês**, não pela lista: um post do mês pode estar
  em qualquer etapa.
- Ignorar cartões da lista `Gaveta`.
- Os números podem não ser contínuos; casar pelo número, não pela ordem.
- Guardar o `id` de cada cartão: é o alvo do anexo.

## Anexar o arquivo
- Ferramenta: a de anexo do conector do Trello (localizar com `ToolSearch`,
  busca "trello attachment"/"trello"). Os parâmetros variam por conector;
  ler o schema antes da primeira chamada. Em geral: id do cartão + arquivo
  (caminho, conteúdo em base64 ou URL) + nome do arquivo com extensão (ex.:
  `post-05-slide_1.png`).
- Se precisar de base64 sem quebra de linha:
  `python -c "import base64,sys;print(base64.b64encode(open(sys.argv[1],'rb').read()).decode())" "<arquivo>"`.
- **Ordem dos slides:** enviar na ordem que o script devolveu (slide 1
  primeiro). O Trello mostra os anexos por ordem de envio.
- O Trello gratuito aceita anexos de até 10 MB por arquivo. PNG de
  1080×1350 costuma ficar bem abaixo disso; se algum passar, avisar antes.
- A primeira imagem anexada vira a capa do cartão (útil: a capa do carrossel
  aparece no quadro).

## Plano B (conector sem anexo de arquivo local)
Se o conector não tiver ferramenta de anexo, ou só aceitar URL:
1. Dizer isso claramente, sem fingir que anexou.
2. Oferecer: (a) o Thiago arrasta a pasta `slides/` para o cartão (o Trello
   mantém a ordem dos nomes); ou (b) anexar como link um arquivo já
   hospedado (ex.: pasta do Google Drive com as artes), se ele preferir.
3. Mesmo assim, entregar a tabela arte → cartão para ele conferir.

## Opcional: mover o cartão
Só se o Thiago pedir. Mover para a lista indicada usando o ID de
`trello.json`; confirmar o nome exato da lista antes. Por padrão, só anexar.
