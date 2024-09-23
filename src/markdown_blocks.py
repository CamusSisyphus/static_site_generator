block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

from htmlnode import *
from textnode import *
from inline_markdown import *

def extract_title(markdown):
    lines = markdown.split('\n')
    title = None
    for line in lines:
         if line.startswith('# '):
              title = line.lstrip('#').strip()
    if title:
         return title
    else:
        raise Exception('Markdown must contain h1 header!')


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    filtered_blocks = []
    for block in blocks:
        if block != "":
            filtered_blocks.append(block.strip())

    return filtered_blocks

def block_to_block_type(block):

    s = " "
    for i in range(6):
        s = "#" + s
        if block.startswith(s):
            return block_type_heading
    lines = block.split('\n')
    if len(lines) >= 2 and lines[0].startswith("```")  and lines[-1].startswith("```"):
        return block_type_code
    
    quote = True
    ul = True
    ol = True
    lines = block.split('\n')
    count = 1
    for line in lines:
        if len(line) < 0 or not line.startswith(">"):
            quote = False
        if len(line) < 1 or (not line.startswith("* ") and not line.startswith("- ")):
            ul = False
        if len(line) < len(str(count))+2 or not line.startswith(f"{count}. "):
            ol = False
        count += 1
    if quote:
        return block_type_quote
    if ul:
        return block_type_ulist
    if ol:
        return block_type_olist
    
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block_type(block)
        if type == block_type_paragraph:
             children.append(paragraph_to_html(block))
        elif type == block_type_heading:
             children.append(heading_to_html(block))
        elif type == block_type_code:
             children.append(code_to_html(block))
        elif type == block_type_quote:
             children.append(quote_to_html(block))
        elif type == block_type_olist:
             children.append(ol_to_html(block))
        elif type == block_type_ulist:
             children.append(ul_to_html(block))
    main_node = ParentNode('div',children)
    return main_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = list(map(lambda x : text_node_to_html_node(x),text_nodes))
    return children

def paragraph_to_html(block):


    children = text_to_children(block.replace("\n"," "))
    paragraph = ParentNode("p",children)
    return paragraph

def quote_to_html(block):
    new_lines = []

    for line in block.split('\n'):
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    quotes = ParentNode("blockquote",text_to_children(content))
    return quotes

def code_to_html(block):
    children = []

    for line in block.split('\n'):
            if line.startswith('```'):
                 continue
            children.extend(text_to_children(line))
    code = ParentNode("code",children)
    return code

def ul_to_html(block):
    list_nodes = []

    for line in block.split('\n'):
            children = []
            children.extend(text_to_children(line[2:]))
            list_nodes.append(ParentNode("li",children))
    ul = ParentNode("ul",list_nodes)
    return ul

def ol_to_html(block):
    list_nodes = []

    count = 1
    for line in block.split('\n'):
            children = []
            children.extend(text_to_children(line[len(str(count))+2:]))
            list_nodes.append(ParentNode("li",children))
            count += 1
    ol = ParentNode("ol",list_nodes)
    return ol

def heading_to_html(block):
    count = 0
    s = " "
    for i in range(6):
        count += 1
        s = "#" + s
        if block.startswith(s):
            break

    for line in block[count+1:].split('\n'):
            children = []
            if line.startswith(s):
                children.extend(text_to_children(line[len(s):]))
            children.extend(text_to_children(line[:]))
    heading = ParentNode(f"h{count}",children)
    return heading