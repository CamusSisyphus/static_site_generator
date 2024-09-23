

class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):

        s = ""
        if self.props:
            for k,v in self.props.items():
                s += f' {k}="{v}"'
        return s
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
    


class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):

        if self.value == None:
            raise ValueError('All leaf nodes must have a value!')
        
        if self.tag == None:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):

    def __init__(self, tag=None, Children=None, props=None) -> None:
        super().__init__(tag, None, Children, props)

    
    def to_html(self):

        if self.tag == None:
            raise ValueError('All parent nodes must have a tag!')
        
        if self.children == None:
            raise ValueError('All parent nodes must have a child!')
        start = f'<{self.tag}{self.props_to_html()}>'
        mid = ""
        for child in self.children:
            mid += child.to_html()
        end = f'</{self.tag}>'
        return start + mid + end