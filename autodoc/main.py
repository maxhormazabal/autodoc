import os
from generate_docs import create_documentation

DEFAULT_DESC = "No description available."


def render_markdown(src_folder, doc_folder):
    """Create documentation for all modules and components."""
    initial_content = ["# Modules\n"]
    
    markdown_content = create_documentation(initial_content, src_folder, doc_folder)
    
    with open(os.path.join(doc_folder, 'modules.md'), 'w', encoding='utf-8') as md_file:
        md_file.write('\n'.join(markdown_content))
        print(f"Generated documentation in {os.path.join(doc_folder, 'modules.md')}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate markdown documentation for Python scripts.")
    parser.add_argument("src_folder", type=str, help="Source folder containing Python modules")
    parser.add_argument("doc_folder", type=str, help="Documentation folder to save the markdown file")
    
    args = parser.parse_args()
    
    render_markdown(args.src_folder, args.doc_folder)
