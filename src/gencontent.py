import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title from the markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the full HTML page to the destination path
    with open(dest_path, 'w') as f:
        f.write(full_html)
    
    print(f"Successfully generated page at {dest_path}")


def extract_title(markdown):    
    lines = markdown.split('\n')
    
    # Look for a line starting with a single # followed by a space
    for line in lines:
        # Check if the line starts with exactly one # followed by a space
        if line.startswith('# '):
            # Extract the title by removing the # and any leading/trailing whitespace
            title = line[1:].strip()
            return title
    
    # If no h1 header is found, raise an exception
    raise ValueError("No h1 header found in the markdown content")