import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,

)
def split_nodes_delimiter(old_nodes, delimiter, text_type):


    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_node = []
    for old_node in old_nodes:
        matches =  extract_markdown_images(old_node.text)
        if not matches:
            new_node.append(old_node)
            continue
        split_nodes = []
        cur_text =old_node.text
        for i in range(len(matches)):
            alt_txt, url = matches[i]
            string = f'![{alt_txt}]({url})'
            text, cur_text = cur_text.split(string)
            if text != "":
                split_nodes.append(TextNode(text,text_type_text))
            split_nodes.append(TextNode(alt_txt,text_type_image,url))
            if i == len(matches) - 1 and cur_text:
                split_nodes.append(TextNode(cur_text,text_type_text))

        if split_nodes:
            new_node.extend(split_nodes)
    return new_node
        
def split_nodes_link(old_nodes):
    new_node = []
    for old_node in old_nodes:
        matches =  extract_markdown_links(old_node.text)
        if not matches:
            new_node.append(old_node)
            continue
        split_nodes = []
        cur_text =old_node.text
        for i in range(len(matches)):
        
            link_text, url = matches[i]
            string = f'[{link_text}]({url})'
            text, cur_text = cur_text.split(string)
            if text != "":
                split_nodes.append(TextNode(text,text_type_text))
            split_nodes.append(TextNode(link_text,text_type_link,url))
            if i == len(matches) - 1 and cur_text:
                split_nodes.append(TextNode(cur_text,text_type_text))

        if split_nodes:

            new_node.extend(split_nodes)
    return new_node

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    init = TextNode(text,text_type_text)
    image_and_text = split_nodes_link(split_nodes_image([init]))
    bold = split_nodes_delimiter(image_and_text,"**",text_type_bold)
    italic = split_nodes_delimiter(bold,"*",text_type_italic)
    code = split_nodes_delimiter(italic,'`',text_type_code)
    final = code
    return final