import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode("div", "This is a test", None, {"class": "test"})
        self.assertEqual(node.tag,
                         "div",)
        self.assertEqual(node.value,
                         "This is a test")
        self.assertEqual(node.children,
                         None)
        self.assertEqual(node.props,
                         {'class': 'test'})                
        #HTMLNode('h1', 'This is a test', None, {'class': 'test'}))

    def test_not_eq(self):
        node = HTMLNode("h1", "This is a test", None, {"class": "test"})
        node2 = HTMLNode("h1", "This is a test", None, {"class": "test2"})
        self.assertNotEqual(node, node2)

    def test_props_eq(self):
        node = HTMLNode("h1", "This is a test", None, {"class": "test"})
        node2 = HTMLNode("h1", "This is a test", None, {"class": "test"})
        self.assertEqual(node.props, node2.props)

    def test_props_to_html(self):
        node = HTMLNode("h1", "This is a test", None, {"class": "test"})
        self.assertEqual(node.props_to_html(),
                         ' class="test"')
        
        

if __name__ == "__main__":
    unittest.main()