# Copy sem cara de IA

Revisão obrigatória da copy de todo carrossel, **antes** de gerar o HTML
(Fase 2, junto com o plano). Fontes: humanizer (blader, baseado no guia
"Signs of AI writing" da Wikipédia), stop-slop (Hardik Pandya) e a skill
no-ai-slop, adaptadas para português e para carrossel. Testado em
2026-10-19 no carrossel "Carboidrato à noite engorda?" (Marina Couto):
nota da copy foi de 25/50 para 38/50.

## A voz do cliente vem primeiro

Estas regras tiram vícios genéricos; elas **não** substituem a voz de cada
cliente. Antes de revisar, leia a skill de marca do cliente
(`skills/marca-<slug>/SKILL.md`), o brand-kit (`tone`) e as legendas/carrosséis
já aprovados. Expressões da marca (ex.: "Comida de verdade, sem neura." da
Marina) ficam, mesmo que pareçam bordão: bordão do cliente é assinatura,
bordão genérico é vício. Gírias, regionalismos, humor e o jeito de falar do
cliente também ficam.

## Padrões para cortar

| Padrão | Exemplo real (antes) | Como fica |
|---|---|---|
| "Não é X; é Y" (inclusive dividido em duas frases ou com "sim" no fim) | "Uma concha de arroz não é o problema; o prato que vira montanha, sim." | Diga o Y direto: "O resultado depende do tamanho do prato." |
| Revelação encenada ("Spoiler:", "A verdade é", "O ponto é", "Aqui vai o segredo") | "Spoiler: o relógio pesa bem menos do que você imagina." | Afirme: "Seu corpo usa o arroz das 20h do mesmo jeito que usa o do meio-dia." |
| Grupo de três forçado | "Sem balança, sem contar, sem neura." / "quanto você come, o que come e como se movimenta" | Dois itens, ou um só; três apenas quando o assunto tem três partes de verdade. |
| Frase de efeito no fim do slide, que repete o que já foi dito | "É essa mistura que segura a fome até de manhã." | Corte, ou troque por um fato novo. |
| Abstração no lugar da cena | "Fome à noite vira beliscada no armário." | Cena concreta: "Aí aparece a torrada, depois o biscoito." |
| Coisa fazendo ação de gente | "A fome vira beliscada", "o dado mostra" | Ponha a pessoa como sujeito: "Quem corta o arroz costuma ir dormir com fome." |
| Pergunta respondida na hora, só para criar suspense | "E sabe o que acontece? A fome volta." | Afirme direto. Pergunta só quando é para o público responder. |
| Etiqueta antes do título ("O que conta", "Dica prática", "O ponto") | Uma etiqueta igual em todo slide | Sem etiqueta; o título carrega o assunto. |
| Palavras de IA | "crucial", "fundamental", "potencializar", "jornada", "transformador", "no mundo de hoje", "vale ressaltar", "é importante destacar" | Palavra comum ou corte. |
| Travessão | qualquer "—" ou "–" | Ponto e vírgula, vírgula ou ponto (regra do CLAUDE.md da raiz). |
| Advérbio vazio | "realmente", "simplesmente", "literalmente", "basicamente" | Corte, salvo quando é jeito de falar do cliente. |
| Autoridade sem nome | "estudos mostram", "especialistas dizem" | Nomeie a fonte ou corte a afirmação. |

## Não inventar

Nunca acrescente fato, número, caso de paciente, fala ou depoimento que o
cliente não deu. Se um slide pede algo real que não existe (fala de
paciente, dado do consultório), escreva uma frase mais simples ou pergunte.
Detalhe ilustrativo (ex.: "23h10") pode, desde que não seja apresentado como
dado. Afirmações técnicas novas ou mais fortes que as do briefing vão para
validação do cliente.

## Nota antes de seguir (stop-slop)

Dê nota de 1 a 10 em cada eixo e mostre junto com o plano:

| Eixo | Pergunta |
|---|---|
| Direto | Afirma ou anuncia? |
| Ritmo | As frases variam de tamanho ou todas têm o mesmo molde? |
| Confiança | Respeita a inteligência de quem lê? |
| Autenticidade | Soa como o cliente falando? |
| Densidade | Tem algo para cortar? |

Abaixo de 35/50: reescreva antes de montar o HTML. Use a skill `no-ai-slop`
em modo detecção sobre a copy para conferir os padrões que sobraram.

## Checagem final rápida

- Nenhum "não é X; é Y", nenhum "Spoiler:", nenhum travessão.
- Nenhum grupo de três que não seja de três coisas reais.
- Nenhum slide terminando em frase de efeito repetida.
- Pelo menos uma cena concreta do dia a dia do público.
- As expressões e o tom do cliente continuam lá.
