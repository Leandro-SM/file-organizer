"""Interface de linha de comando do file-organizer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .organizer import organize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Organiza arquivos de um diretório por tipo e, opcionalmente, por data.",
    )
    parser.add_argument("directory", type=Path, help="Diretório a ser organizado.")
    parser.add_argument(
        "--by-date",
        action="store_true",
        help="Cria subpastas por ano/mês de modificação dentro de cada categoria.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a organização, mostrando o que seria feito sem mover arquivos.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = organize(args.directory, by_date=args.by_date, dry_run=args.dry_run)
    except (NotADirectoryError, FileNotFoundError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    prefix = "[simulação] " if args.dry_run else ""
    for move in result.moves:
        rel_dest = move.destination.relative_to(args.directory)
        print(f"{prefix}{move.source.name} -> {rel_dest}")

    action = "seriam movidos" if args.dry_run else "movidos"
    print(f"\n{result.moved_count} arquivo(s) {action}; {len(result.skipped)} ignorado(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
