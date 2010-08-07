"""
Convert XML to Python dict.

http://code.activestate.com/recipes/573463/
"""
from xml.dom.minidom import Document

def _xml_to_dict_helper(node):
    node_dict = {}
    
    if node.attributes:
        # if we have attributes, set them
        node_dict.update(dict(node.attributes))
    
    for child in node.childNodes:
        # recursively add the element's children
        newitem = _xml_to_dict_helper(child)
        if node_dict.has_key(child.nodeName):
            # found duplicate nodeName, force a list
            if type(node_dict[child.nodeName]) is type([]):
                # append to existing list
                node_dict[child.nodeName].append(newitem)
            else:
                # convert to list
                node_dict[child.nodeName] = [node_dict[child.nodeName], newitem]
        else:
            # only one, directly set the dictionary
            node_dict[child.nodeName] = newitem

        if node.nodeType == node.TEXT_NODE:
            text = node.nodeValue.strip()
            if len(node.childNodes) > 1:
                node_dict['_text'] = text
            else:
                node_dict = text
    return node_dict
        
def xml_to_dict(root):
    """
    Converts an XML file or ElementTree Element to a dictionary
    """
    if not isinstance(root, Document):
        raise TypeError, 'Expected ElementTree.Element or file path string'

    return {root.nodeName: _xml_to_dict_helper(root)}