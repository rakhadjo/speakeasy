from nltk.tokenize import RegexpTokenizer
from keras.models import load_model
import tensorflow as tf
import numpy as np
import heapq

class word_suggestion:
    def __init__(self, filename):
        self.session = tf.Session()
        self.graph = tf.get_default_graph()
        self.tokenizer = RegexpTokenizer(r'\w+')
        with open(filename, "r") as f:
            text = f.read().lower()
        words = self.tokenizer.tokenize(text)
        self.unique_words = np.unique(words)
        self.unique_word_index = dict((c, i) for i, c in enumerate(self.unique_words))
        with self.graph.as_default():
            with self.session.as_default():
                "For some reason this needs to be in init to work with threads"

    def load(self, model_name):
        with self.graph.as_default():
            with self.session.as_default():
                self.model = load_model(model_name)

    def prepare_input(self, text):
        unique_word_index = self.unique_word_index.copy()
        x = np.zeros((1, 5, len(self.unique_words)))
        for t, word in enumerate(text.split()):
            if word not in unique_word_index:
                unique_word_index[word] = 1
            x[0, t, unique_word_index[word]] = 1
        return x

    def sample(self, preds, n=3):
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds)
        exp_preds = np.exp(preds)
        preds = exp_preds/np.sum(exp_preds)
        return heapq.nlargest(n, range(len(preds)), preds.take)

    def predict_completions(self, text, n=3):
        if text == "":
            return ["Would", "Where", "Why"]
        x = self.prepare_input(text)
        with self.graph.as_default():
            with self.session.as_default():
                preds = self.model.predict(x, verbose=0)[0]
        next_indices = self.sample(preds, n)
        return [self.unique_words[idx] for idx in next_indices]

    def prediction(self, sentence, n=3):
        seq = " ".join(self.tokenizer.tokenize(sentence.lower())[-3:])
        return self.predict_completions(seq, n)
