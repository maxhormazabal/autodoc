import os
import shutil
import re

DEFAULT_DESC = "No description available."

def centered_image_block(alt_text, path, md_only = False):
    if md_only:
        img_text_block = f"![{alt_text}]({path})\n"
    else:
        img_text_block = f"""
        <p align="center">
            <img src="{path}" alt="{alt_text}" />
        </p>
        """
        img_text_block = f'<div align="center"><img src="{path}" alt="{alt_text}"></div>'
    return img_text_block

def read_file_content(file_path):
    """Read the content of a file, return None if file does not exist."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    return None

def copy_image(src_image_path, dest_image_path):
    """Copy an image file to the destination path."""
    if os.path.exists(src_image_path):
        shutil.copy(src_image_path, dest_image_path)

def extract_docstring_from_file(file_path):
    """Extract docstrings from a Python file."""
    docstrings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        functions = re.findall(r'def (\w+)\(.*?\):\n\s+"""(.*?)"""', content, re.DOTALL)
        for func_name, docstring in functions:
            docstrings.append((func_name, docstring.strip()))
    return docstrings

def find_diagram_file(docs_path):
    """Find the diagram file in the docs path."""
    for ext in ['.jpg', '.jpeg', '.png', '.svg']:
        diagram_path = os.path.join(docs_path, f'diagram{ext}')
        if os.path.exists(diagram_path):
            return diagram_path, f'diagram{ext}'
    return None, None

def include_image(markdown_content, doc_folder, docs_path, name):
    # Include image if available
    diagram_path, diagram_file = find_diagram_file(docs_path)
    if diagram_file:
        dest_diagram_path = os.path.join(doc_folder, f'images/{name}_{diagram_file}')
        copy_image(diagram_path, dest_diagram_path)
        markdown_content.append(centered_image_block(alt_text="Module Diagram", path=f"images/{name}_{diagram_file}", md_only=True))
    else:
        markdown_content.append(centered_image_block(alt_text="Diagram", path=f"images/default_diagram.png", md_only=True))
    return markdown_content        

def generate_markdown_for_component(component_path, component_name, doc_folder):
    """Generate markdown content for a component."""
    markdown_content = [f"### {component_name.capitalize()}\n"]
    
    # Read component description
    component_docs_path = os.path.join(component_path, 'docs')
    component_desc = read_file_content(os.path.join(component_docs_path, 'desc.txt')) or DEFAULT_DESC

    # Add description to markdown
    markdown_content.append(f"{component_desc}\n")

    markdown_content = include_image(markdown_content, doc_folder, component_docs_path, component_name)
    
    use_cases_content = []
    services_content = []
    
    for root, _, files in os.walk(component_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, component_path)
                section_title = os.path.splitext(relative_path)[0].replace(os.sep, ' > ')
                docstrings = extract_docstring_from_file(file_path)
                if docstrings:
                    if 'useCases' in root:
                        use_cases_content.append(f"#### {section_title.capitalize()}\n")
                        for func_name, docstring in docstrings:
                            use_cases_content.append(f"##### {func_name.capitalize()}\n```\n{docstring}\n```\n")
                    elif 'services' in root:
                        services_content.append(f"#### {section_title.capitalize()}\n")
                        for func_name, docstring in docstrings:
                            services_content.append(f"##### {func_name.capitalize()}\n```\n{docstring}\n```\n")
    
    if use_cases_content:
        markdown_content.append("#### Use Cases\n")
        markdown_content.extend(use_cases_content)
    
    if services_content:
        markdown_content.append("#### Services\n")
        markdown_content.extend(services_content)
    
    return '\n'.join(markdown_content)

def generate_markdown_for_modules(module_path, markdown_content, module_name, doc_folder):
    module_docs_path = os.path.join(module_path, 'docs')
    module_desc = read_file_content(os.path.join(module_docs_path, 'desc.txt')) or DEFAULT_DESC
    
    markdown_content.append(f"## {module_name.capitalize()}\n")
    markdown_content.append(f"{module_desc}\n")

    markdown_content = include_image(markdown_content, doc_folder, module_docs_path, module_name)

    return markdown_content


def create_documentation(markdown_content, src_folder, doc_folder):
    for module_name in os.listdir(src_folder):
        module_path = os.path.join(src_folder, module_name)
        if os.path.isdir(module_path):
            markdown_content = generate_markdown_for_modules(module_path, markdown_content, module_name, doc_folder)
            module_path = module_path + "/components"
            for component_name in os.listdir(module_path):
                component_path = os.path.join(module_path, component_name)
                if os.path.isdir(component_path) and component_name != 'docs':
                    component_markdown = generate_markdown_for_component(component_path, component_name, doc_folder)
                    if component_markdown:
                        markdown_content.append(component_markdown)
    return markdown_content