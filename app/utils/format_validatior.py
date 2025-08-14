# import re


def correct_format(content: str, file_type: str) -> bool:
    match file_type:
        case "markdown":
            return format_markdown(content)
        case "csv":
            return format_csv(content)
        case "tsv":
            return format_tsv(content)
        case "txt":
            return format_txt(content)
        case "html":
            return format_html(content)
        case _:
            raise ValueError


def format_markdown(content: str) -> bool:
    return True


def format_csv(content: str) -> bool:
    return True


def format_tsv(content: str) -> bool:
    return True


def format_txt(content: str) -> bool:
    return True


def format_html(content: str) -> bool:
    return True
