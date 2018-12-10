class Graph():

    def __init__(self):
        self.operations = []
        self.placeholders = []
        self.variables = []

    def set_as_default(self):
        global default_graph
        default_graph = self


class Placeholder():
    def __init__(self):
        self.output_nodes = []
        _default_graph.placeholders.append(self)


class Variable():
    def __init__(self, initial_value=None):
        self.value = initial_value
        self.output_nodes = []
        _default_graph.variables.append(self)


class Operation():

    def __init__(self, input_nodes=[]):

        self.input_nodes = input_nodes  # The list of input nodes
        self.output_nodes = []  # List of nodes consuming this node's output

        for node in input_nodes:
            print('node in operation', node)
            node.output_nodes.append(self)

        _default_graph.operations.append(self)

    def compute(self):
        pass


class add(Operation):

    def __init__(self, x, y):

        super().__init__([x, y])

    def compute(self, x_var, y_var):

        self.inputs = [x_var, y_var]
        return x_var + y_var


class multiply(Operation):

    def __init__(self, a, b):

        super().__init__([a, b])

    def compute(self, a_var, b_var):

        self.inputs = [a_var, b_var]
        return a_var * b_var


def traverse_postorder(operation):
    """ 
    PostOrder Traversal of Nodes. Basically makes sure computations are done in 
    the correct order (Ax first , then Ax + b). Feel free to copy and paste this code.
    It is not super important for understanding the basic fundamentals of deep learning.
    """

    nodes_postorder = []

    def recurse(node):
        if isinstance(node, Operation):
            for input_node in node.input_nodes:
                print('Input node in ', input_node)
                recurse(input_node)
        nodes_postorder.append(node)

    recurse(operation)
    return nodes_postorder


class Session:

    def run(self, operation, feed_dict={}):
        """ 
          operation: The operation to compute
          feed_dict: Dictionary mapping placeholders to input values (the data)  
        """

        # Puts nodes in correct order
        nodes_postorder = traverse_postorder(operation)
        print('TOP', feed_dict)

        for node in nodes_postorder:
            print('here node is', node)
            print('feed dict is', feed_dict)

            if type(node) == Placeholder:
                print(feed_dict[node], node, 'thisi s slsdlfsjdlfjl')

                node.output = feed_dict[node]

            elif type(node) == Variable:

                node.output = node.value

            else:  # Operation
                print('operation nodes', node)

                node.inputs = [
                    input_node.output for input_node in node.input_nodes]
                print(node.inputs)

                node.output = node.compute(*node.inputs)
            print('here node output is', node.output)

            # Convert lists to numpy arrays
            if type(node.output) == list:
                node.output = np.array(node.output)

        # Return the requested node value
        return operation.output
