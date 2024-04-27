import numpy as np
import matplotlib
from matplotlib.lines import Line2D
from sklearn.model_selection import train_test_split

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam


def get_logistic_map_values(a_values, iterations=1000, last_n=100):
    lm_values = np.empty((len(a_values), last_n))
    for i, a in enumerate(a_values):
        x = 0.5
        for j in range(iterations):
            x = a * x * (1 - x)
            if j >= iterations - last_n:
                lm_values[i, j - (iterations - last_n)] = x
    return lm_values


def plot_logistic_map(a_values, lm_values, predicted_lm_values):
    markersize = 0.05
    fig, ax = plt.subplots()
    for i, a in enumerate(a_values):
        ax.plot([a] * len(lm_values[i]), lm_values[i], 'k.', markersize=markersize)
        ax.plot([a] * len(predicted_lm_values[i]), predicted_lm_values[i], 'r.', markersize=markersize)

    legend_handles = [Line2D([0], [0], color='k', marker='.', linestyle='None', markersize=10, label='Original'),
                      Line2D([0], [0], color='r', marker='.', linestyle='None', markersize=10, label='Predicted')]

    ax.legend(handles=legend_handles)
    ax.set_xlabel('a')
    ax.set_ylabel('x')
    plt.show()


def build_model():
    model = Sequential([
        Dense(256, activation='relu', input_dim=1),
        Dropout(0.2),
        Dense(256, activation='relu'),
        Dropout(0.2),
        Dense(128, activation='relu'),
        Dense(100, activation='linear')
    ])
    model.compile(optimizer=Adam(0.001), loss='mse')
    return model


def main():
    a_values = np.linspace(0, 4, 1000)
    lm_values = get_logistic_map_values(a_values, iterations=1000, last_n=100)

    X = a_values.reshape(-1, 1)
    y = lm_values.reshape(-1, 100)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model()
    model.fit(X_train, y_train, epochs=300, verbose=1, batch_size=32, validation_data=(X_test, y_test))

    predicted_lm_values = model.predict(X)

    plot_logistic_map(a_values, lm_values, predicted_lm_values)


if __name__ == '__main__':
    main()
