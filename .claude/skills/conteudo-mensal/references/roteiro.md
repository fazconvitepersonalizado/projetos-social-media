# Roteiro do carrossel (aprovado antes de qualquer HTML)

Padrão geral desde 2026-10-20. O roteiro é a história do carrossel, slide por slide,
com a função de cada slide e a ideia visual. Ele é aprovado pelo Thiago antes de a arte
existir: mexer na história no roteiro custa uma linha; mexer depois do HTML custa a arte.

## Onde fica
`<cliente>/conteudos/roteiros/<AAAA-MM>.md`, um bloco por carrossel do mês. Depois do OK,
o texto vira o "Texto da arte" do post no plano do mês (`planos/<AAAA-MM>.md`), que continua
sendo a fonte da verdade. No roteiro, anotar "Aprovado em AAAA-MM-DD" no topo.

## Formato
```
## POST NN · tema
Arco: de onde a história parte e aonde chega, numa frase.

| # | Função | Título | Apoio | Dado e fonte | Visual |
|---|---|---|---|---|---|
| 1 | gancho | ... | ... | | capa foto full + véu |
| 2 | por que importa | ... | | 600 quase acidentes para cada acidente grave · Fonte: Frank Bird, 1969 | creme + número gigante |
| ... |
| 8 | chamada | ... | ... | | degradê da marca + botão |
```
- **Função** (uma por slide): gancho · por que importa · o que muda · como fazer · chamada.
  Extras quando a história pede: contexto, consequência, virada, exemplo, pergunta, dado.
- **Título** até ~10 palavras; **Apoio** até ~15. Item de lista vai no apoio, separado por `;`.
  Nunca usar `|` dentro da célula (comparação: "No papel x Funcionando").
- **Dado e fonte**: só onde o número reforça o ponto (cerca de 1 por carrossel), sempre
  "número · frase · Fonte: X". Vazio quando não há dado.
- **Visual**: fundo + recurso (traço temático, forma de cor, recorte, foto). Nunca vazio.
  Escrever "creme", "claro" ou "branco" quando o fundo for claro (máximo 2; capa nunca).
- A composição do sorteio entra só aqui, na coluna Visual, depois da história escrita.

## Conferir antes de mostrar
```bash
python conferir_carrossel.py --roteiro "<cliente>/conteudos/roteiros/<AAAA-MM>.md"
```
Confere: gancho primeiro, chamada no fim, presença de "por que importa", "o que muda" e
"como fazer" (e "por que importa" antes de "como fazer"), linha "Arco:", tamanho de título e
apoio, travessão, dado sem fonte, dado demais, slide sem visual, fundo claro demais e títulos
com a mesma ideia. Achado: reescrever antes de mostrar, ou mostrar com a justificativa.

## Como mostrar ao Thiago
Os roteiros do mês de uma vez, cada um com o arco, a tabela, a nota anti-IA (mínimo 35/50) e
o resultado do conferidor. Pausa para o OK. Só então a skill `instagram-carousel` monta a arte.
