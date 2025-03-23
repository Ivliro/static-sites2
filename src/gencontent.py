import os
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Crawling directory: {dir_path_content}")
    
    # Check if the content directory exists
    if not os.path.exists(dir_path_content):
        print(f"Error: Content directory '{dir_path_content}' does not exist.")
        return
    
    # Check if the template file exists
    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' does not exist.")
        return
    
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    # Get all items in the content directory
    items = os.listdir(dir_path_content)
    
    # Process each item in the content directory
    for item in items:
        source_path = os.path.join(dir_path_content, item)
        
        # If item is a directory, recursively process it
        if os.path.isdir(source_path):
            # Create the corresponding destination directory path
            nested_dest_dir = os.path.join(dest_dir_path, item)
            
            # Recursively process the subdirectory
            generate_pages_recursive(source_path, template_path, nested_dest_dir)
        
        # If item is a markdown file, generate an HTML page
        elif item.endswith('.md'):
            # Create the destination path with .html extension
            dest_file_name = os.path.splitext(item)[0] + '.html'
            dest_path = os.path.join(dest_dir_path, dest_file_name)
            
            # Generate the HTML page
            try:
                generate_page(source_path, template_path, dest_path)
            except Exception as e:
                print(f"Error generating page from {source_path}: {str(e)}")


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