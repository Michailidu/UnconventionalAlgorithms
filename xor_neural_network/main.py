import numpy as np

from xor_neural_network.data import generate_xor_data
from xor_neural_network.neural_network import NeuralNetwork

if __name__ == "__main__":
    data, labels = generate_xor_data(1000)
    nn = NeuralNetwork((2, 2, 1))

    nn.train(data, labels, epochs=100, learning_rate=0.1)
    predicted = nn.test(data)
    predicted = np.round(predicted)
    accuracy = np.mean(predicted == labels)
    print(f"Accuracy: {accuracy * 100:.2f}%")
