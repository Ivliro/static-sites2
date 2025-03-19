import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a test", {"class": "test"})
        self.assertEqual(node.to_html(),
                         '<p class="test">This is a test</p>')
        
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is a test", {"class": "test", "href": "https://boot.dev"})
        self.assertEqual(node.to_html(),
                         '<a class="test" href="https://boot.dev">This is a test</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None,'Hello world')
        self.assertEqual(node.to_html(),
                         'Hello world')


    def test_to_html_with_children(self):
        child = LeafNode('span','child')
        parent = ParentNode('div', [child])
        self.assertEqual(parent.to_html(),
                         '<div><span>child</span></div>')

    def test_to_html_with_children_and_props(self):
        child = LeafNode('span','child')
        parent = ParentNode('div', [child], {'class': 'test'})
        self.assertEqual(parent.to_html(),
                         '<div class="test"><span>child</span></div>')
        
    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode('b', 'grandchild')
        child = ParentNode('span', [grandchild])
        parent = ParentNode('div', [child])
        self.assertEqual(parent.to_html(),
                         '<div><span><b>grandchild</b></span></div>')

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),
                         '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()