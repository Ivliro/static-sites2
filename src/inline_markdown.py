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