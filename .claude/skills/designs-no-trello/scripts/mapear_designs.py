#!/usr/bin/env python3
"""
Mapeia as artes prontas para o numero do POST, com os slides ja na ordem
certa. Dois modos:

1) Pastas por post (artes vindas de designer/Canva):
    python mapear_designs.py <pasta_das_artes> [--out mapa.json]
   Uma pasta por post (post-05/, POST 05/, post 5/, 05/). Tambem aceita .zip
   com essas pastas dentro (descompacta numa pasta temporaria).

2) Plano do mes (artes exportadas pela skill instagram-carousel):
    python mapear_designs.py --plano <cliente>/conteudos/planos/AAAA-MM.md [--out mapa.json]
   Le cada "### POST NN" do plano e a linha "Pasta da arte: <pasta>" e pega
   os PNG/JPG de <pasta>/slides/ (ou da propria pasta, se nao houver slides/).
   Caminhos relativos sao resolvidos a partir da pasta do cliente.

Saida (JSON):
{
  "posts": [
    {"post": 5, "pasta": "post-05", "slides": 3,
     "arquivos": [".../post-05/01.png", ".../post-05/02.png", ".../post-05/03.png"]}
  ],
  "soltos": [".../algum_arquivo_sem_pasta.png"],   # arte fora de pasta de post
  "avisos": ["..."]
}

O numero do POST sai do NOME DA PASTA (modo 1) ou do cabecalho do plano
(modo 2). A ORDEM DOS SLIDES sai do nome dos arquivos, em ordem natural
(slide_2 < slide_10; 01 < 02 < 10).
"""
import sys
import os
import re
import json
import zipfile
import tempfile

# Extensoes de arte/midia que interessam anexar.
EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".heic",
        ".mp4", ".mov", ".pdf"}

# Lixo de zips de macOS/Windows a ignorar.
IGNORAR_NOMES = {".ds_store", "thumbs.db", "desktop.ini"}
IGNORAR_DIRS = {"__macosx"}


def numero_do_post(nome):
    """Tira o numero do POST do nome de uma pasta. Devolve int ou None."""
    n = nome.strip().lower()
    # post-05 / post 5 / post_5 / post05  ->  pega o numero depois de "post"
    m = re.search(r"post[\s_\-]*0*(\d{1,2})\b", n)
    if m:
        return int(m.group(1))
    # so digitos: "05", "5"
    m = re.fullmatch(r"0*(\d{1,2})", n)
    if m:
        return int(m.group(1))
    return None


def chave_natural(caminho):
    """Ordena nomes com numeros de forma humana: slide2 antes de slide10."""
    base = os.path.basename(caminho).lower()
    partes = re.split(r"(\d+)", base)
    return [int(p) if p.isdigit() else p for p in partes]


def e_arte(nome):
    n = nome.lower()
    if n in IGNORAR_NOMES or n.startswith("._"):
        return False
    return os.path.splitext(n)[1] in EXTS


def descompactar_zips(raiz, destino):
    """Descompacta qualquer .zip da raiz para `destino`. Devolve lista de avisos."""
    avisos = []
    for nome in os.listdir(raiz):
        if nome.lower().endswith(".zip"):
            cam = os.path.join(raiz, nome)
            try:
                with zipfile.ZipFile(cam) as z:
                    z.extractall(destino)
                avisos.append(f"Descompactado: {nome}")
            except zipfile.BadZipFile:
                avisos.append(f"ZIP invalido, ignorado: {nome}")
    return avisos


def coletar(raiz):
    """
    Percorre `raiz` e agrupa arquivos por pasta de post.
    Retorna (dict_post -> [arquivos], soltos, avisos).
    """
    posts = {}      # numero_post -> {"pasta": str, "arquivos": [..]}
    soltos = []
    avisos = []

    for dirpath, dirnames, filenames in os.walk(raiz):
        # nao descer em pastas de lixo
        dirnames[:] = [d for d in dirnames if d.lower() not in IGNORAR_DIRS]

        artes = [os.path.join(dirpath, f) for f in filenames if e_arte(f)]
        if not artes:
            continue

        nome_pasta = os.path.basename(os.path.normpath(dirpath))
        num = numero_do_post(nome_pasta)

        if num is None:
            # arquivos fora de uma pasta de post reconhecivel
            soltos.extend(sorted(artes, key=chave_natural))
            continue

        artes.sort(key=chave_natural)
        if num in posts:
            avisos.append(
                f"POST {num:02d}: mais de uma pasta aponta para o mesmo post "
                f"('{posts[num]['pasta']}' e '{nome_pasta}'); juntei os arquivos."
            )
            posts[num]["arquivos"].extend(artes)
        else:
            posts[num] = {"pasta": nome_pasta, "arquivos": artes}

    return posts, soltos, avisos


def coletar_do_plano(plano):
    """
    Le o plano do mes e devolve (dict_post -> {pasta, arquivos}, avisos).
    A pasta do cliente e a avo de conteudos/planos/AAAA-MM.md.
    """
    posts, avisos = {}, []
    cliente_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(plano))))
    atual = None
    with open(plano, encoding="utf-8") as f:
        for linha in f:
            m = re.match(r"^###\s+POST\s+0*(\d{1,2})\b", linha.strip(), re.I)
            if m:
                atual = int(m.group(1))
                continue
            m = re.match(r"^Pasta da arte:\s*(.+?)\s*$", linha.strip(), re.I)
            if m and atual is not None:
                alvo = m.group(1).strip().strip("`")
                if alvo.lower().startswith("ainda") or not alvo:
                    continue
                pasta = os.path.normpath(alvo if os.path.isabs(alvo) else os.path.join(cliente_dir, alvo))
                if not os.path.isdir(pasta):
                    avisos.append(f"POST {atual:02d}: pasta da arte nao encontrada: {alvo}")
                    continue
                slides = os.path.join(pasta, "slides")
                base = slides if os.path.isdir(slides) else pasta
                artes = sorted((os.path.join(base, n) for n in os.listdir(base) if e_arte(n)),
                               key=chave_natural)
                if not artes:
                    avisos.append(f"POST {atual:02d}: nenhuma arte exportada em {base}")
                    continue
                posts[atual] = {"pasta": alvo, "arquivos": artes}
    return posts, avisos


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = [a for a in sys.argv[1:]]
    out = None
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    plano = None
    if "--plano" in args:
        i = args.index("--plano")
        plano = args[i + 1]
        del args[i:i + 2]

    avisos = []
    posts = {}
    soltos = []

    if plano:
        if not os.path.isfile(plano):
            print(json.dumps({"erro": f"plano nao encontrado: {plano}"}, ensure_ascii=False))
            sys.exit(1)
        posts, avisos = coletar_do_plano(plano)
    else:
        if not args:
            print(__doc__)
            sys.exit(1)
        raiz = args[0]
        if not os.path.isdir(raiz):
            print(json.dumps({"erro": f"pasta nao encontrada: {raiz}"}, ensure_ascii=False))
            sys.exit(1)

        # Se houver zips, descompacta para uma pasta temporaria e olha as duas.
        raizes = [raiz]
        if any(n.lower().endswith(".zip") for n in os.listdir(raiz)):
            tmp = tempfile.mkdtemp(prefix="designs_")
            avisos += descompactar_zips(raiz, tmp)
            raizes.append(tmp)

        for r in raizes:
            p, s, a = coletar(r)
            for num, info in p.items():
                if num in posts:
                    posts[num]["arquivos"].extend(info["arquivos"])
                else:
                    posts[num] = info
            soltos.extend(s)
            avisos.extend(a)

    resultado = {
        "posts": [
            {
                "post": num,
                "pasta": posts[num]["pasta"],
                "slides": len(posts[num]["arquivos"]),
                "arquivos": posts[num]["arquivos"],
            }
            for num in sorted(posts)
        ],
        "soltos": sorted(set(soltos), key=chave_natural),
        "avisos": avisos,
    }

    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"mapa escrito em {out}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
