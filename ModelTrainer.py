import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical


data = []
for _ in range(200): data.append([np.random.uniform(3, 4), np.random.uniform(3, 4), "SAFE"])
for _ in range(200): data.append([np.random.uniform(5, 6), np.random.uniform(5, 6), "MODERATE"])
for _ in range(200): data.append([np.random.uniform(7, 8), np.random.uniform(7, 8), "OVERLOADED"])
for _ in range(200): data.append([np.random.uniform(9, 10), np.random.uniform(9, 10), "DAMAGED"])
df = pd.DataFrame(data, columns=["load1", "load2", "label"])

X = df[["load1", "load2"]].values
y = df["label"].values
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)


X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2)


model = Sequential([
    Dense(16, input_dim=2, activation='relu'),
    Dense(12, activation='relu'),
    Dense(4, activation='softmax')  # 4 classes
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=1)


model.save("stress_model.h5")
print("Model saved as stress_model.h5")
