import re

def correct_format(content: str, file_type: str) -> bool:
    match file_type:
        case "markdown":
            return is_markdown(content)
        case "csv":
            return is_csv(content)
        case "tsv":
            return is_tsv(content)
        case "txt":
            return is_txt(content)
        case "html":
            return is_html(content)
        case _:
            raise ValueError
        
def is_markdown(content: str) -> bool:
    pass

def is_csv(content: str) -> bool:
    pass

def is_tsv(content: str) -> bool:
    pass

def is_txt(content: str) -> bool:
    pass

def is_html(content: str) -> bool:
    pass 