import json

def load_dataset():
    with open('dataset/dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

        texts, labels = [], []
        for intent, examples in data.items():
            for example in examples:
                texts.append(example)
                labels.append(intent)

        return texts, labels
