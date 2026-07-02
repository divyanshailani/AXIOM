# AXIOM V1 Test Results

This file contains the output of 50 test prompts (general & technical) run against the V1 Zero-Training math engines.

### Test 1: `hey`
- **Domain Route**: `chit_chat` (Confidence: 41.94%)
- **Intent Match**: `gen_greeting` (Sim Score: 0.45)
- **AXIOM Response**: Greetings! I am ready to process your questions using classical algorithms.

### Test 2: `hello`
- **Domain Route**: `chit_chat` (Confidence: 41.94%)
- **Intent Match**: `gen_greeting` (Sim Score: 0.45)
- **AXIOM Response**: Hello! I am AXIOM, a mathematical first-principles AI. How can I help you today?

### Test 3: `good morning`
- **Domain Route**: `chit_chat` (Confidence: 67.02%)
- **Intent Match**: `gen_greeting` (Sim Score: 0.63)
- **AXIOM Response**: Greetings! I am ready to process your questions using classical algorithms.

### Test 4: `how are you`
- **Domain Route**: `chit_chat` (Confidence: 46.87%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'chit_chat'.

### Test 5: `who are you`
- **Domain Route**: `chit_chat` (Confidence: 81.31%)
- **Intent Match**: `gen_identity` (Sim Score: 0.88)
- **AXIOM Response**: My name is AXIOM. I was built to be a transparent, mathematically rigorous AI assistant built entirely without black-box deep learning.

### Test 6: `what is your name`
- **Domain Route**: `chit_chat` (Confidence: 41.94%)
- **Intent Match**: `gen_identity` (Sim Score: 0.22)
- **AXIOM Response**: My name is AXIOM. I was built to be a transparent, mathematically rigorous AI assistant built entirely without black-box deep learning.

### Test 7: `are you a robot`
- **Domain Route**: `chit_chat` (Confidence: 71.24%)
- **Intent Match**: `gen_identity` (Sim Score: 0.22)
- **AXIOM Response**: I am AXIOM (Zero-Training Math Engine). I was created as a deterministic system built on Naive Bayes and Markov Chains.

### Test 8: `what can you do`
- **Domain Route**: `chit_chat` (Confidence: 41.48%)
- **Intent Match**: `gen_capability` (Sim Score: 0.67)
- **AXIOM Response**: I specialize in explaining classical Machine Learning algorithms. You can ask me how Decision Trees, Clustering, or my own Naive Bayes systems work.

### Test 9: `tell me a joke`
- **Domain Route**: `chit_chat` (Confidence: 61.23%)
- **Intent Match**: `gen_joke` (Sim Score: 0.71)
- **AXIOM Response**: I would tell you a joke about a Markov Chain, but it depends entirely on what I just said.

### Test 10: `bye`
- **Domain Route**: `chit_chat` (Confidence: 41.94%)
- **Intent Match**: `gen_farewell` (Sim Score: 0.42)
- **AXIOM Response**: Farewell! May your vectors always be orthogonal.

### Test 11: `what is machine learning`
- **Domain Route**: `classical_ml` (Confidence: 75.05%)
- **Intent Match**: `ml_overview` (Sim Score: 0.38)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 12: `explain classical ml`
- **Domain Route**: `classical_ml` (Confidence: 93.83%)
- **Intent Match**: `ml_overview` (Sim Score: 0.60)
- **AXIOM Response**: Classical ML involves algorithms like Regression, SVMs, and Decision Trees to classify data or predict continuous outcomes using pure mathematics and statistics.

### Test 13: `what is artificial intelligence`
- **Domain Route**: `classical_ml` (Confidence: 48.67%)
- **Intent Match**: `ml_overview` (Sim Score: 0.46)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 14: `maths`
- **Domain Route**: `classical_ml` (Confidence: 54.96%)
- **Intent Match**: `ml_overview` (Sim Score: 0.33)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 15: `algorithms`
- **Domain Route**: `classical_ml` (Confidence: 38.36%)
- **Intent Match**: `ml_overview` (Sim Score: 0.33)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 16: `data science`
- **Domain Route**: `classical_ml` (Confidence: 73.30%)
- **Intent Match**: `ml_overview` (Sim Score: 0.46)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 17: `what is linear regression`
- **Domain Route**: `classical_ml` (Confidence: 78.54%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.69)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 18: `how does regression work`
- **Domain Route**: `classical_ml` (Confidence: 50.73%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.63)
- **AXIOM Response**: It models continuous outcomes by fitting a linear equation. The algorithm adjusts coefficients to minimize the residual sum of squares between predicted and actual values.

### Test 19: `explain ordinary least squares`
- **Domain Route**: `classical_ml` (Confidence: 86.86%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.66)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 20: `what is logistic regression`
- **Domain Route**: `classical_ml` (Confidence: 98.19%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 0.46)
- **AXIOM Response**: Logistic regression predicts probabilities using the sigmoid function, which squeezes any real number into a range between zero and one. It is used for binary classification.

### Test 21: `explain logistic regression`
- **Domain Route**: `classical_ml` (Confidence: 99.50%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 0.46)
- **AXIOM Response**: Despite its name, it is a classification algorithm. It applies a logistic function to a linear combination of input features to estimate the probability of a class label.

### Test 22: `how does the sigmoid function work`
- **Domain Route**: `classical_ml` (Confidence: 33.87%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 0.25)
- **AXIOM Response**: Logistic regression predicts probabilities using the sigmoid function, which squeezes any real number into a range between zero and one. It is used for binary classification.

### Test 23: `what are decision trees`
- **Domain Route**: `classical_ml` (Confidence: 58.12%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.81)
- **AXIOM Response**: It creates a flowchart of decisions. Advanced versions like Random Forests use many trees, and algorithms like XGBoost use gradient boosting to sequentially correct errors of previous trees.

### Test 24: `how do decision trees work`
- **Domain Route**: `classical_ml` (Confidence: 60.58%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.81)
- **AXIOM Response**: It creates a flowchart of decisions. Advanced versions like Random Forests use many trees, and algorithms like XGBoost use gradient boosting to sequentially correct errors of previous trees.

### Test 25: `explain random forests`
- **Domain Route**: `classical_ml` (Confidence: 81.64%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.33)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 26: `what is entropy in a decision tree`
- **Domain Route**: `classical_ml` (Confidence: 94.48%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.66)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 27: `whats xgboost`
- **Domain Route**: `classical_ml` (Confidence: 44.86%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 28: `what is a support vector machine`
- **Domain Route**: `classical_ml` (Confidence: 91.19%)
- **Intent Match**: `ml_svm` (Sim Score: 0.55)
- **AXIOM Response**: Support vector machines map data into a higher dimensional space where a linear separation becomes possible. The kernel trick computes this mapping without explicitly calculating the coordinates.

### Test 29: `explain svm`
- **Domain Route**: `classical_ml` (Confidence: 97.10%)
- **Intent Match**: `ml_svm` (Sim Score: 0.82)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 30: `what is a kernel trick`
- **Domain Route**: `classical_ml` (Confidence: 54.96%)
- **Intent Match**: `ml_svm` (Sim Score: 0.47)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 31: `how does svm classify`
- **Domain Route**: `classical_ml` (Confidence: 91.97%)
- **Intent Match**: `ml_svm` (Sim Score: 0.82)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 32: `what is clustering`
- **Domain Route**: `classical_ml` (Confidence: 54.96%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.56)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 33: `explain k means clustering`
- **Domain Route**: `classical_ml` (Confidence: 90.91%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.92)
- **AXIOM Response**: K-means begins with random centroids. Each point joins the cluster of its nearest center. The centroids then shift to the mean of their assigned points, repeating until convergence.

### Test 34: `what is unsupervised learning`
- **Domain Route**: `classical_ml` (Confidence: 73.27%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.37)
- **AXIOM Response**: K-means begins with random centroids. Each point joins the cluster of its nearest center. The centroids then shift to the mean of their assigned points, repeating until convergence.

### Test 35: `how does k means work`
- **Domain Route**: `classical_ml` (Confidence: 33.99%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.73)
- **AXIOM Response**: K-means begins with random centroids. Each point joins the cluster of its nearest center. The centroids then shift to the mean of their assigned points, repeating until convergence.

### Test 36: `what is k nearest neighbors`
- **Domain Route**: `classical_ml` (Confidence: 64.67%)
- **Intent Match**: `ml_knn` (Sim Score: 0.80)
- **AXIOM Response**: K-nearest neighbors stores all training data and classifies a new point by majority vote of its K closest neighbors in feature space. It is a lazy learner.

### Test 37: `explain knn`
- **Domain Route**: `classical_ml` (Confidence: 90.84%)
- **Intent Match**: `ml_knn` (Sim Score: 0.87)
- **AXIOM Response**: K-nearest neighbors stores all training data and classifies a new point by majority vote of its K closest neighbors in feature space. It is a lazy learner.

### Test 38: `how does nearest neighbor work`
- **Domain Route**: `classical_ml` (Confidence: 71.71%)
- **Intent Match**: `ml_knn` (Sim Score: 0.92)
- **AXIOM Response**: It makes no assumptions about the underlying data distribution. It simply measures distance, usually Euclidean, between the query point and the stored examples.

### Test 39: `how do you understand my questions`
- **Domain Route**: `self` (Confidence: 76.00%)
- **Intent Match**: `self_cosine_similarity` (Sim Score: 0.55)
- **AXIOM Response**: I convert your question into a vector using word frequencies. Then I calculate the cosine angle between your vector and every question in my memory. The smallest angle wins.

### Test 40: `what is cosine similarity`
- **Domain Route**: `self` (Confidence: 54.94%)
- **Intent Match**: `self_cosine_similarity` (Sim Score: 0.45)
- **AXIOM Response**: I convert your question into a vector using word frequencies. Then I calculate the cosine angle between your vector and every question in my memory. The smallest angle wins.

### Test 41: `how do you generate sentences`
- **Domain Route**: `self` (Confidence: 54.94%)
- **Intent Match**: `self_markov_chain` (Sim Score: 0.46)
- **AXIOM Response**: My generator uses a Markov chain. I look at the previous one or two words, check my probability matrix, and select the next word based on historical frequency.

### Test 42: `what is a markov chain`
- **Domain Route**: `self` (Confidence: 54.94%)
- **Intent Match**: `self_markov_chain` (Sim Score: 0.46)
- **AXIOM Response**: I build a probability matrix from my training text. For any given word, I roll a dice weighted by which words usually follow it. I chain these dice rolls until I reach a stopping state.

### Test 43: `how do you pick a domain`
- **Domain Route**: `self` (Confidence: 64.65%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 0.56)
- **AXIOM Response**: I classify your intent into a domain using Bayes theorem. I assume each word contributes independently to the probability of a topic.

### Test 44: `what is naive bayes`
- **Domain Route**: `self` (Confidence: 54.94%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 0.62)
- **AXIOM Response**: My domain router uses a Naive Bayes classifier. It calculates the probability that your question belongs to each domain based on word frequencies, then sends you to the most likely specialist.

### Test 45: `how do you work`
- **Domain Route**: `self` (Confidence: 42.25%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 0.34)
- **AXIOM Response**: My domain router uses a Naive Bayes classifier. It calculates the probability that your question belongs to each domain based on word frequencies, then sends you to the most likely specialist.

### Test 46: `who invented the perceptron`
- **Domain Route**: `history` (Confidence: 87.50%)
- **Intent Match**: `hist_perceptron` (Sim Score: 0.77)
- **AXIOM Response**: The perceptron was the first machine learning algorithm that could iteratively adjust its weights based on classification errors. It sparked the first wave of AI optimism.

### Test 47: `who is alan turing`
- **Domain Route**: `history` (Confidence: 82.35%)
- **Intent Match**: `hist_turing` (Sim Score: 0.72)
- **AXIOM Response**: Alan Turing proposed the imitation game in 1950. A machine passes if a human cannot distinguish it from another human through text conversation alone.

### Test 48: `what is the turing test`
- **Domain Route**: `history` (Confidence: 69.28%)
- **Intent Match**: `hist_turing` (Sim Score: 0.69)
- **AXIOM Response**: Turing asked whether machines can think. He suggested that if a machine behaves indistinguishably from a human, we should grant it intelligence by operational definition.

### Test 49: `what are transformers`
- **Domain Route**: `chit_chat` (Confidence: 40.92%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'chit_chat'.

### Test 50: `how does chatgpt work`
- **Domain Route**: `modern_context` (Confidence: 43.44%)
- **Intent Match**: `mod_transformers` (Sim Score: 0.36)
- **AXIOM Response**: Transformers use a mechanism called self-attention to weigh the importance of every word in a sentence against every other word simultaneously. They process sequences in parallel.

### Test 51: `why are you not a neural network`
- **Domain Route**: `modern_context` (Confidence: 63.66%)
- **Intent Match**: `mod_vs_classical` (Sim Score: 0.59)
- **AXIOM Response**: Neural networks are black boxes. My cosine similarity scores and Markov probability tables are human-readable. You can see exactly why I chose every word.

