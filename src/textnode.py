from htmlnode import *

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self,text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (self.text == other.text) and (self.text_type == other.text_type)
    
    def __repr__(self) -> str:
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    


def text_node_to_html_node(text_node:TextNode):
     
    type_to_tag = {
        'text' : None,
        'bold' : 'b',
        'italic' : 'i',
        'code' : 'code',
        'link' : 'a',
        'image' : 'img'
        }
    type = text_node.text_type
    if type in type_to_tag:
        tag = type_to_tag[type]
        if type == 'link':
                return LeafNode(tag,text_node.text,{"href":text_node.url})
        if type == 'image':
                return LeafNode(tag,"",{"src":text_node.url,"alt":text_node.text})

        return LeafNode(tag,text_node.text)
    else:
        raise ValueError('Invalid Text_type')