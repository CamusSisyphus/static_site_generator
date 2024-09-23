from textnode import *
from os import(
    path,
    listdir,
    mkdir,
    makedirs,
)

from shutil import(
    copy,
    rmtree
)
from markdown_blocks import(
    markdown_to_html_node,
    extract_title
)

def copy_static_to_public(src,dst):

    if path.exists(dst):
        rmtree(dst)
    cur_path = ""
    if path.isfile(src):
        copy(src,dst)
    else:
        mkdir(dst)
        ls  = listdir(src)
        for ele in ls:
            copy_static_to_public(path.join(src,ele),path.join(dst,ele))

def generate_page(from_path, template_path, dest_path):
    dest_path = dest_path.replace('.md','.html')
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        src = f.read()
    with open(template_path) as f:
        template = f.read()
    src_html = markdown_to_html_node(src).to_html()
    title = extract_title(src)


    new_html = template.replace('{{ Title }}',title).replace('{{ Content }}',src_html)
    if not path.exists(path.dirname(dest_path)):
        makedirs(path.dirname(dest_path))
    with open(dest_path, mode='w') as f:
        f.write(new_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
    else:
        ls  = listdir(dir_path_content)
        for ele in ls:
            generate_pages_recursive(path.join(dir_path_content,ele),template_path,path.join(dest_dir_path,ele))

def main():

    txt  = ".ha"
    copy_static_to_public('static','public')
    generate_pages_recursive('content', 'template.html', 'public')
main()


