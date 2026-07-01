# AXIOM: A Chatbot That Explains Machine Learning Using Only Classical Machine Learning

AXIOM (Accessible eXplanation of Intelligence using Only Mathematics) is a hyper-specialist, self-referential chatbot built from first principles. It explains how ML works, using the exact classical ML algorithms it's explaining. 

## The Math Stack (Zero-Training Pipeline)
* **Domain Router**: Multinomial Naive Bayes (Laplace smoothing)
* **Intent Retriever**: Jaccard-like Cosine Similarity with Binary Bag-of-Words
* **Generator**: Template Generation & Markov Chains

Built strictly with `numpy`—no black boxes, no neural networks, no `scikit-learn`.

## Compute Specs
Runs on essentially anything:
- **CPU:** Any x86_64 from 2015+
- **RAM:** 512 MB
- **GPU:** None
