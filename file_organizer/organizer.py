"""Lógica central de organização de arquivos."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .categories import category_for_extension


@dataclass
class Move:
    """Representa a movimentação planejada de um arquivo."""

    source: Path
    destination: Path


@dataclass
class OrganizeResult:
    """Resultado de uma operação de organização."""

    moves: list[Move] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)

    @property
    def moved_count(self) -> int:
        return len(self.moves)


def _unique_destination(destination: Path) -> Path:
    """Gera um caminho de destino único, evitando sobrescrever arquivos.

    Se ``arquivo.txt`` já existir, retorna ``arquivo (1).txt``, ``arquivo (2).txt``, etc.
    """
    if not destination.exists():
        return destination

    stem, suffix, parent = destination.stem, destination.suffix, destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _date_subfolder(path: Path) -> str:
    """Retorna a subpasta de data (AAAA/MM) com base na data de modificação."""
    modified = datetime.fromtimestamp(path.stat().st_mtime)
    return f"{modified.year:04d}/{modified.month:02d}"


def plan_moves(directory: Path, *, by_date: bool = False) -> OrganizeResult:
    """Planeja as movimentações de arquivos sem executá-las.

    Args:
        directory: diretório a ser organizado (não recursivo).
        by_date: se True, adiciona subpastas por ano/mês de modificação.

    Returns:
        Um :class:`OrganizeResult` com os movimentos planejados.
    """
    directory = Path(directory)
    if not directory.is_dir():
        raise NotADirectoryError(f"'{directory}' não é um diretório válido.")

    result = OrganizeResult()

    for entry in sorted(directory.iterdir()):
        if entry.is_dir() or entry.name.startswith("."):
            result.skipped.append(entry)
            continue

        category = category_for_extension(entry.suffix)
        target_dir = directory / category
        if by_date:
            target_dir = target_dir / _date_subfolder(entry)

        destination = _unique_destination(target_dir / entry.name)
        result.moves.append(Move(source=entry, destination=destination))

    return result


def organize(directory: Path, *, by_date: bool = False, dry_run: bool = False) -> OrganizeResult:
    """Organiza os arquivos de um diretório por categoria (e opcionalmente por data).

    Args:
        directory: diretório a ser organizado.
        by_date: se True, cria subpastas por ano/mês.
        dry_run: se True, apenas planeja sem mover nenhum arquivo.

    Returns:
        O :class:`OrganizeResult` com o que foi (ou seria) movido.
    """
    result = plan_moves(directory, by_date=by_date)

    if dry_run:
        return result

    for move in result.moves:
        move.destination.parent.mkdir(parents=True, exist_ok=True)
        move.source.rename(move.destination)

    return result
