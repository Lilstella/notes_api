import re


def markdown_to_html(markdown_text: str):
    html = []
    in_list = False
    in_code = False

    for line in markdown_text.splitlines():
        line = line.strip()
        print(f"linea: {line}")

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
        line = re.sub(r"~~(.+?)~~", r"/<del>\1</del>", line)
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
