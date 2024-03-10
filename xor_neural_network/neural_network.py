import numpy as np

from xor_neural_network.function import sigmoid, sigmoid_derivative


class Layer:
    """
    Neural network layer class. Contains weights and biases for the layer.
    """
    def __init__(self, input_size: int, output_size: int):
        """
        Initialize the layer with random weights and biases.
        :param input_size: Number of input weights.
        :param output_size: Number of output weights.
        """
        self.input_size = input_size
        self.output_size = output_size
        self.weights = np.random.uniform(size=(self.input_size, self.output_size))
        self.bias = np.random.uniform(size=(1, self.output_size))

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward pass through the layer.
        :param inputs: Input data to the layer.
        :return: Output data from the layer.
        """
        value = np.dot(inputs, self.weights)
        value += self.bias
        return value


class NeuralNetwork:
    """
    Two layer neural network class. Contains layers and methods for training and testing the network.
    """
    def __init__(self, weights_count: tuple[int, int, int]):
        """
        Initialize the neural network with two layers according to the provided weights count.
        :param weights_count: Tuple of input, hidden, and output layer sizes.
        """
        input_size, hidden_size, output_size = weights_count

        self.hidden_layer = Layer(input_size, hidden_size)
        self.output_layer = Layer(hidden_size, output_size)

    def train(self, data: np.ndarray, labels: np.ndarray, epochs: int = 100, learning_rate: float = 0.1) -> None:
        """
        Train the neural network on the provided data and labels.
        :param data: Numpy array with input data.
        :param labels: Numpy array with labels for the input data.
        :param epochs:
        :param learning_rate:
        :return:
        """
        for _ in range(epochs):
            # forward pass
            out_hidden = sigmoid(self.hidden_layer.forward(data))
            out_output = sigmoid(self.output_layer.forward(out_hidden))

            # backward pass
            error = labels - out_output
            delta_output = error * sigmoid_derivative(out_output)
            error_hidden = delta_output.dot(self.output_layer.weights.T)
            delta_hidden = error_hidden * sigmoid_derivative(out_hidden)

            # update weights and biases
            self.output_layer.weights += out_hidden.T.dot(delta_output) * learning_rate
            self.output_layer.bias += np.sum(delta_output, axis=0, keepdims=True) * learning_rate
            self.hidden_layer.weights += data.T.dot(delta_hidden) * learning_rate
            self.hidden_layer.bias += np.sum(delta_hidden, axis=0, keepdims=True) * learning_rate

    def test(self, data: np.ndarray) -> np.ndarray:
        """
        Test the trained neural network on the provided data.
        :param data: Numpy array with input data.
        :return: Numpy array with predicted labels.
        """
        out_hidden = sigmoid(self.hidden_layer.forward(data))
        return sigmoid(self.output_layer.forward(out_hidden))
