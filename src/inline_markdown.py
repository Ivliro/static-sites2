import re
#from htmlnode import LeafNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # new_nodes = []
    # for node in old_nodes:
    #     if node.value == delimiter:
    #         new_nodes.append(LeafNode(text_type, node.value))
    #     else:
    #         new_nodes.append(node)
    # return new_nodes
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Initialize variables for parsing
        text = old_node.text
        current_index = 0
        segments = []
        
        while True:
            # Find the next delimiter
            delimiter_index = text.find(delimiter, current_index)
            
            # If no more delimiters, add the remaining text and break
            if delimiter_index == -1:
                if current_index < len(text):
                    segments.append((text[current_index:], TextType.TEXT))
                break
            
            # Add text before the delimiter if there is any
            if delimiter_index > current_index:
                segments.append((text[current_index:delimiter_index], TextType.TEXT))
            
            # Move past this delimiter
            current_index = delimiter_index + len(delimiter)
            
            # Find the closing delimiter
            closing_index = text.find(delimiter, current_index)
            
            # If no closing delimiter, treat the rest as regular text and break
            if closing_index == -1:
                segments.append((text[delimiter_index:], TextType.TEXT))
                break
            
            # Add the content between delimiters with the specified type
            segments.append((text[current_index:closing_index], text_type))
            
            # Move past the closing delimiter
            current_index = closing_index + len(delimiter)
        
        # Create TextNode objects from the parsed segments
        for content, node_type in segments:
            new_nodes.append(TextNode(content, node_type))
    
    return new_nodes

def extract_images(text):
    # Pattern to match markdown links: [anchor text](url)
    pattern = r"!\[(.*?)\]\((.*?)\)"
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    return matches

def extract_links(text):
    # Pattern to match markdown links: [anchor text](url)
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    return matches

def split_nodes_image(old_nodes):
    """
    Split TextNodes that have TextType.TEXT based on markdown image syntax.
    
    Args:
        old_nodes (list): List of TextNode objects
        
    Returns:
        list: New list of TextNode objects with images extracted as IMAGE type nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        
        # Extract all image matches
        image_matches = extract_images(text)
        
        # If no images found, keep the node as is
        if not image_matches:
            new_nodes.append(old_node)
            continue
        
        # Process the text by replacing image markers with placeholders
        # and then splitting on those placeholders
        current_text = text
        segments = []
        
        for i, (alt_text, image_url) in enumerate(image_matches):
            # Create a unique placeholder for this image
            placeholder = f"__IMAGE_PLACEHOLDER_{i}__"
            
            # Find the image markdown
            image_markdown = f"![{alt_text}]({image_url})"
            
            # Split at the current image
            parts = current_text.split(image_markdown, 1)
            
            if len(parts) < 2:  # This shouldn't happen if extract_markdown_images worked correctly
                continue
                
            # Save the text before the image
            if parts[0]:
                segments.append((parts[0], None, None))
                
            # Save the image data
            segments.append((alt_text, TextType.IMAGE, image_url))
            
            # Continue with the remaining text
            current_text = parts[1]
        
        # Add any remaining text
        if current_text:
            segments.append((current_text, None, None))
        
        # Create TextNodes from segments
        for text, text_type, url in segments:
            if text_type is None:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type, url))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes that have TextType.TEXT based on markdown link syntax.
    
    Args:
        old_nodes (list): List of TextNode objects
        
    Returns:
        list: New list of TextNode objects with links extracted as LINK type nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        
        # Extract all link matches
        link_matches = extract_links(text)
        
        # If no links found, keep the node as is
        if not link_matches:
            new_nodes.append(old_node)
            continue
        
        # Process the text by replacing link markers with placeholders
        # and then splitting on those placeholders
        current_text = text
        segments = []
        
        for i, (anchor_text, url) in enumerate(link_matches):
            # Find the link markdown
            link_markdown = f"[{anchor_text}]({url})"
            
            # Split at the current link
            parts = current_text.split(link_markdown, 1)
            
            if len(parts) < 2:  # This shouldn't happen if extract_markdown_links worked correctly
                continue
                
            # Save the text before the link
            if parts[0]:
                segments.append((parts[0], None, None))
                
            # Save the link data
            segments.append((anchor_text, TextType.LINK, url))
            
            # Continue with the remaining text
            current_text = parts[1]
        
        # Add any remaining text
        if current_text:
            segments.append((current_text, None, None))
        
        # Create TextNodes from segments
        for text, text_type, url in segments:
            if text_type is None:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type, url))
    
    return new_nodes

def text_to_textnodes(text):
    """
    Convert a raw string of markdown-flavored text into a list of TextNode objects.
    
    Args:
        text (str): The markdown-flavored text to convert
        
    Returns:
        list: A list of TextNode objects representing the parsed text
    """
    # Start with a single TextNode containing the entire text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply the splitting functions in sequence
    
    # First, handle images as they have the most complex syntax
    nodes = split_nodes_image(nodes)
    
    # Then handle links
    nodes = split_nodes_link(nodes)
    
    # Then handle bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Then handle italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Finally handle code blocks
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes