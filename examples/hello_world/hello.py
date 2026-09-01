"""Script de exemplo: Hello World.

Executa uma saudacao simples no terminal.
"""


def saudacao(nome: str = "mundo") -> str:
    """Retorna uma mensagem de saudacao."""
    return f"Ola, {nome}! Bem-vindo ao file-organizer."


def main() -> None:
    """Ponto de entrada do script."""
    print(saudacao())


if __name__ == "__main__":
    main()
