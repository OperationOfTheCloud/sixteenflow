from datasets import load_dataset
import tensorflow as tf
ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")

# Get all unique characters in dataset
tokens = set()
for split in ds:
    for example in ds[split]:
        tokens.update(example['instruction'])
        tokens.update(example['response'])
tokens.add('<|endoftext|>')  # Add end of text token

# create a mapping from characters to integers
token_to_id = {token: idx for idx, token in enumerate(sorted(tokens))}

InputTrain = []
OutputTrain = []
#get max length sentence in dataset
max_length = max(len(example['instruction']) + len('<|endoftext|>') for example in ds["train"]) + max(len(example['response']) + len('<|endoftext|>') for example in ds["train"])
print(f"Max length of sentence in dataset: {max_length}")
print(token_to_id["<|endoftext|>"])
# Create a tokenizer
for example in ds["train"]:
    SentenceToken = []
    for char in example['instruction']:
        SentenceToken.append(token_to_id[char])
    InputTrain.append(SentenceToken + [token_to_id['<|endoftext|>']])
    SentenceToken = []
    for char in example['response']:
        SentenceToken.append(token_to_id[char])
    OutputTrain.append(SentenceToken + [token_to_id['<|endoftext|>']])

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(max_length,)),
    tf.keras.layers.Embedding(input_dim=len(token_to_id), output_dim=64, mask_zero=True),
    tf.keras.layers.LSTM(128, return_sequences=True),
    tf.keras.layers.LSTM(128, return_sequences=True),  # <-- change here
    tf.keras.layers.Dense(len(token_to_id), activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
import numpy as np
InputTrain = tf.keras.preprocessing.sequence.pad_sequences(InputTrain, maxlen=max_length, padding='post', truncating='post')
OutputTrain = tf.keras.preprocessing.sequence.pad_sequences(OutputTrain, maxlen=max_length, padding='post', truncating='post')
OutputTrain = np.expand_dims(OutputTrain, -1)  # Add an extra dimension for sparse categorical crossentropy
# Train the model
model.fit(InputTrain, OutputTrain, epochs=1000, batch_size=32, validation_split=0.2)
# Save the model
model.save('customer_support_chatbot_model.h5')