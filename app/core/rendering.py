import re
from re import Match


def to_html(content: str, file_type: str) -> str:
    match file_type:
        case "markdown":
            return markdown_to_html(content)
        case "csv":
            return table_to_html(content, "csv")
        case "tsv":
            return table_to_html(content, "tsv")
        case "txt":
            return "<pre>" + content + "</pre>"
        case "html":
            return content
        case _:
            raise ValueError


def markdown_to_html(markdown_text: str) -> str:
    html = []
    in_list = False
    in_code = False

    for line in markdown_text.splitlines():
        line = line.strip()

        # Code Blocks
        if line.startswith("```"):
            if not in_code:
                html.append("<pre><code>")
                in_code = True
            else:
                html.append("</code></pre>")
                in_code = False
            continue
        if in_code:
            html.append(line)
            continue

        # Header
        is_header = re.match(r"^(#{1,6})(.*)", line)
        if is_header:
            level = len(is_header.group(1))
            text = is_header.group(2).strip()
            html.append(f"<h{level}>{text}</h{level}>")
            continue

        # Quote
        if line.startswith(">"):
            html.append(f"<blockquote>{line[1:].strip()}</blockquote>")
            continue

        # Separators
        if re.match(r"^(\s*[-*_]\s*){3,}$", line):
            html.append("<hr />")
            continue

        # List
        if re.match(r"^[+*-]", line):
            if not in_list:
                html.append("<ul>")
                in_list = True

            item = line[2:].strip()
            html.append(f"<li>{item}</li>")
            continue

        elif in_list:
            html.append("</ul>")
            in_list = False

        # Bold, italic, crossed, and code
        line = re.sub(r"(_|\*){2}(.+?)(_|\*){2}", r"<strong>\2</strong>", line)
        line = re.sub(r"(_|\*)(.+?)(_|\*)", r"<em>\2</em>", line)
        line = re.sub(r"~~(.+?)~~", r"<del>\1</del>", line)
        line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)

        # Images and links
        line = re.sub(r"!\[(.*?)\]\((.*?)\)", r'<img src="\2" alt="\1" />', line)
        line = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', line)

        # Paragraphs
        if line.strip():
            html.append(f"<p>{line}</p>")

    if in_list:
        html.append("</ul>")

    return "\n".join(html)


def table_to_html(csv_text: str, mode: str) -> str:
    separator = "," if mode == "csv" else "\t"
    lines = csv_text.splitlines()
    headers = lines[0].split(separator)
    print(headers)

    html = ["<table>"]
    html.append("<tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>")

    for line in lines[1:]:
        columns = line.split(separator)
        html.append("<tr>" + "".join(f"<td>{col}</td>" for col in columns) + "</tr>")

    html.append("</table>")
    return "\n".join(html)


def to_markdown(content: str, file_type: str) -> str:
    match file_type:
        case "markdown":
            return content
        case "csv":
            return table_to_markdown(content, "csv")
        case "tsv":
            return table_to_markdown(content, "tsv")
        case "latex":
            return latex_to_markdown(content)
        case "txt":
            return content
        case "html":
            return html_to_markdown(content)
        case _:
            raise ValueError


def table_to_markdown(csv_text: str, mode: str) -> str:
    separator = "," if mode == "csv" else "\t"
    lines = csv_text.splitlines()
    headers = lines[0].split(separator)

    markdown = "| " + " | ".join(headers) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for line in lines[1:]:
        columns = line.split(separator)
        markdown += "| " + " | ".join(columns) + " |\n"

    return markdown


def html_to_markdown(html_text: str) -> str:
    markdown = html_text

    # Code blocks
    markdown = re.sub(
        r"<pre><code>(.*?)</code></pre>", r"```\n\1\n```", markdown, flags=re.DOTALL
    )

    # Headers
    for i in range(6, 0, -1):
        markdown = re.sub(
            rf"<h{i}>(.*?)</h{i}>",
            lambda m: "#" * i + " " + m.group(1).strip(),
            markdown,
        )

    # Quotes
    markdown = re.sub(
        r"<blockquote>(.*?)</blockquote>", lambda m: "> " + m.group(1).strip(), markdown
    )

    # Separators
    markdown = re.sub(r"<hr\s*/?>", "---", markdown)

    # Lists
    def replace_list(match: Match[str]) -> str:
        items = re.findall(r"<li>(.*?)</li>", match.group(1), flags=re.DOTALL)
        return "\n".join(f"- {item.strip()}" for item in items)

    markdown = re.sub(r"<ul>(.*?)</ul>", replace_list, markdown, flags=re.DOTALL)

    # Bold and italic
    markdown = re.sub(r"<strong>(.*?)</strong>", r"**\1**", markdown)
    markdown = re.sub(r"<em>(.*?)</em>", r"*\1*", markdown)
    markdown = re.sub(r"<del>(.*?)</del>", r"~~\1~~", markdown)

    # Inline code
    markdown = re.sub(r"<code>(.*?)</code>", r"`\1`", markdown)

    # Images
    markdown = re.sub(r'<img\s+src="(.*?)"\s+alt="(.*?)"\s*/?>', r"![\2](\1)", markdown)

    # Links
    markdown = re.sub(r'<a\s+href="(.*?)">(.*?)</a>', r"[\2](\1)", markdown)

    # Paragraphs to newlines
    markdown = re.sub(r"<p>(.*?)</p>", r"\1\n", markdown)

    markdown = re.sub(r"</?[^>]+>", "", markdown)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()


def latex_to_markdown(latex_text: str) -> str:
    text = latex_text

    # Remove preamble
    text = re.sub(r".*?\\begin\{document\}", "", text, flags=re.S)
    text = re.sub(r"\\end\{document\}.*", "", text, flags=re.S)

    # Sections
    text = re.sub(r"\\section\{(.+?)\}", r"# \1", text)
    text = re.sub(r"\\subsection\{(.+?)\}", r"## \1", text)
    text = re.sub(r"\\subsubsection\{(.+?)\}", r"### \1", text)

    # Text formatting
    text = re.sub(r"\\textbf\{(.+?)\}", r"**\1**", text)
    text = re.sub(r"\\textit\{(.+?)\}", r"*\1*", text)
    text = re.sub(r"\\emph\{(.+?)\}", r"*\1*", text)
    text = re.sub(r"\\sout\{(.+?)\}", r"~~\1~~", text)  # strikethrough
    text = re.sub(r"\\texttt\{(.+?)\}", r"`\1`", text)  # inline code

    # Itemize -> bullet list
    text = re.sub(r"\\begin\{itemize\}", "", text)
    text = re.sub(r"\\end\{itemize\}", "", text)
    text = re.sub(r"\\item\s+", r"- ", text)

    # Enumerate -> numbered list
    text = re.sub(r"\\begin\{enumerate\}", "", text)
    text = re.sub(r"\\end\{enumerate\}", "", text)
    text = re.sub(r"\\item\s+", r"1. ", text)

    # Quote environment
    text = re.sub(r"\\begin\{quote\}", "\n> ", text)
    text = re.sub(r"\\end\{quote\}", "", text)

    # Horizontal rule
    text = text.replace(r"\hrule", "\n\n---\n\n")

    # Block math \[...\] -> $$...$$
    text = re.sub(r"\\\[(.+?)\\\]", r"$$\1$$", text, flags=re.S)

    # Clean up leftover commands (ignore \sout etc. already handled)
    text = re.sub(r"\\[a-zA-Z]+\s*", "", text)

    # Clean multiple newlines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()
