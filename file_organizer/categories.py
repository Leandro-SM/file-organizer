"""Mapeamento de extensões de arquivo para categorias."""

CATEGORIES: dict[str, tuple[str, ...]] = {
    "Imagens": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"),
    "Documentos": (".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"),
    "Videos": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"),
    "Audio": (".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"),
    "Arquivos_Compactados": (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"),
    "Codigo": (".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".rb", ".php", ".html", ".css", ".json", ".xml", ".sh"),
    "Executaveis": (".exe", ".msi", ".deb", ".rpm", ".dmg", ".app", ".apk"),
}

OTHER_CATEGORY = "Outros"


def category_for_extension(extension: str) -> str:
    """Retorna a categoria correspondente a uma extensão de arquivo.

    A comparação é feita de forma case-insensitive. Extensões não mapeadas
    retornam a categoria padrão ``Outros``.
    """
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return OTHER_CATEGORY
