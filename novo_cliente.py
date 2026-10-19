"""Cria a pasta de um cliente novo a partir de _modelo-cliente/.

Uso:
    python novo_cliente.py "Nome do Cliente"
    python novo_cliente.py "Nome do Cliente" --slug nome-curto

Copia a estrutura padrão (briefing/, manual/, apresentacoes/, logo/,
assets/raw/, conteudos/, skills de carrossel e publicação, exportador) e
preenche {{NOME}}, {{SLUG}} e {{DATA}} no README.md e no ONBOARDING.md.
Nunca sobrescreve uma pasta que já existe.
"""
import argparse
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "_modelo-cliente"
FILLED = ["README.md", "ONBOARDING.md"]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.replace("&", "e")
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("nome", help="Nome do cliente (vira o nome da pasta)")
    parser.add_argument("--slug", help="Slug da marca (padrão: derivado do nome)")
    args = parser.parse_args()

    nome = args.nome.strip()
    slug = args.slug or slugify(nome)
    dest = ROOT / nome

    if dest.exists():
        print(f"A pasta '{nome}' já existe; nada foi criado. Veja {dest / 'ONBOARDING.md'}.")
        return 1
    if not TEMPLATE.exists():
        print(f"Modelo não encontrado em {TEMPLATE}.")
        return 1

    shutil.copytree(TEMPLATE, dest)
    hoje = date.today().isoformat()
    for name in FILLED:
        f = dest / name
        text = f.read_text(encoding="utf-8")
        text = text.replace("{{NOME}}", nome).replace("{{SLUG}}", slug).replace("{{DATA}}", hoje)
        f.write_text(text, encoding="utf-8")

    print(f"Pasta criada: {dest}")
    print(f"Slug da marca: {slug}  (skill futura: skills/marca-{slug}/SKILL.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
