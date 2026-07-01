# AXIOM V1 Test Results

This file contains the output of 50 test prompts (general & technical) run against the V1 Zero-Training math engines.

### Test 1: `hey`
- **Domain Route**: `chit_chat` (Confidence: 44.28%)
- **Intent Match**: `gen_greeting` (Sim Score: 0.45)
- **AXIOM Response**: Greetings! I am ready to process your questions using classical algorithms.

### Test 2: `hello`
- **Domain Route**: `chit_chat` (Confidence: 44.28%)
- **Intent Match**: `gen_greeting` (Sim Score: 0.45)
- **AXIOM Response**: Hello! I am AXIOM, a mathematical first-principles AI. How can I help you today?

### Test 3: `good morning`
- **Domain Route**: `chit_chat` (Confidence: 71.25%)
- **Intent Match**: `gen_greeting` (Sim Score: 0.63)
- **AXIOM Response**: Greetings! I am ready to process your questions using classical algorithms.

### Test 4: `how are you`
- **Domain Route**: `chit_chat` (Confidence: 52.48%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'chit_chat'.

### Test 5: `who are you`
- **Domain Route**: `chit_chat` (Confidence: 71.39%)
- **Intent Match**: `gen_identity` (Sim Score: 0.58)
- **AXIOM Response**: My name is AXIOM. I am a transparent, mathematically rigorous AI assistant built entirely without black-box deep learning.

### Test 6: `what is your name`
- **Domain Route**: `chit_chat` (Confidence: 44.28%)
- **Intent Match**: `gen_identity` (Sim Score: 0.58)
- **AXIOM Response**: My name is AXIOM. I am a transparent, mathematically rigorous AI assistant built entirely without black-box deep learning.

### Test 7: `are you a robot`
- **Domain Route**: `chit_chat` (Confidence: 77.68%)
- **Intent Match**: `gen_identity` (Sim Score: 0.58)
- **AXIOM Response**: My name is AXIOM. I am a transparent, mathematically rigorous AI assistant built entirely without black-box deep learning.

### Test 8: `what can you do`
- **Domain Route**: `chit_chat` (Confidence: 51.45%)
- **Intent Match**: `gen_capability` (Sim Score: 0.71)
- **AXIOM Response**: I specialize in explaining classical Machine Learning algorithms. You can ask me how Decision Trees, Clustering, or my own Naive Bayes systems work.

### Test 9: `tell me a joke`
- **Domain Route**: `chit_chat` (Confidence: 71.25%)
- **Intent Match**: `gen_joke` (Sim Score: 0.71)
- **AXIOM Response**: I would tell you a joke about a Markov Chain, but it depends entirely on what I just said.

### Test 10: `bye`
- **Domain Route**: `chit_chat` (Confidence: 44.28%)
- **Intent Match**: `gen_farewell` (Sim Score: 0.41)
- **AXIOM Response**: Goodbye! Shutting down the mathematical matrices.

### Test 11: `what is machine learning`
- **Domain Route**: `classical_ml` (Confidence: 76.31%)
- **Intent Match**: `ml_overview` (Sim Score: 0.38)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 12: `explain classical ml`
- **Domain Route**: `classical_ml` (Confidence: 84.53%)
- **Intent Match**: `ml_overview` (Sim Score: 0.46)
- **AXIOM Response**: Classical ML involves algorithms like Regression, SVMs, and Decision Trees to classify data or predict continuous outcomes using pure mathematics and statistics.

### Test 13: `what is artificial intelligence`
- **Domain Route**: `classical_ml` (Confidence: 50.06%)
- **Intent Match**: `ml_overview` (Sim Score: 0.46)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 14: `maths`
- **Domain Route**: `classical_ml` (Confidence: 55.29%)
- **Intent Match**: `ml_overview` (Sim Score: 0.33)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 15: `algorithms`
- **Domain Route**: `classical_ml` (Confidence: 38.69%)
- **Intent Match**: `ml_overview` (Sim Score: 0.33)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 16: `data science`
- **Domain Route**: `classical_ml` (Confidence: 73.93%)
- **Intent Match**: `ml_overview` (Sim Score: 0.46)
- **AXIOM Response**: Machine Learning is a subset of Artificial Intelligence that uses statistical algorithms to learn patterns from data, rather than relying on explicitly programmed rules.

### Test 17: `what is linear regression`
- **Domain Route**: `classical_ml` (Confidence: 79.09%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.69)
- **AXIOM Response**: It models continuous outcomes by fitting a linear equation. The algorithm adjusts coefficients to minimize the residual sum of squares between predicted and actual values.

### Test 18: `how does regression work`
- **Domain Route**: `classical_ml` (Confidence: 86.55%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.64)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 19: `explain ordinary least squares`
- **Domain Route**: `classical_ml` (Confidence: 90.09%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.65)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 20: `what is logistic regression`
- **Domain Route**: `classical_ml` (Confidence: 85.01%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 0.86)
- **AXIOM Response**: Despite its name, it is a classification algorithm. It applies a logistic function to a linear combination of input features to estimate the probability of a class label.

### Test 21: `explain logistic regression`
- **Domain Route**: `classical_ml` (Confidence: 96.40%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 0.86)
- **AXIOM Response**: Logistic regression predicts probabilities using the sigmoid function, which squeezes any real number into a range between zero and one. It is used for binary classification.

### Test 22: `how does the sigmoid function work`
- **Domain Route**: `classical_ml` (Confidence: 76.67%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 0.50)
- **AXIOM Response**: Logistic regression predicts probabilities using the sigmoid function, which squeezes any real number into a range between zero and one. It is used for binary classification.

### Test 23: `what are decision trees`
- **Domain Route**: `classical_ml` (Confidence: 62.16%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.78)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 24: `how do decision trees work`
- **Domain Route**: `classical_ml` (Confidence: 90.79%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.78)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 25: `explain random forests`
- **Domain Route**: `classical_ml` (Confidence: 85.61%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.31)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 26: `what is entropy in a decision tree`
- **Domain Route**: `classical_ml` (Confidence: 88.42%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.64)
- **AXIOM Response**: It creates a flowchart of decisions. Advanced versions like Random Forests use many trees, and algorithms like XGBoost use gradient boosting to sequentially correct errors of previous trees.

### Test 27: `whats xgboost`
- **Domain Route**: `classical_ml` (Confidence: 65.41%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.22)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 28: `what is a support vector machine`
- **Domain Route**: `classical_ml` (Confidence: 75.17%)
- **Intent Match**: `ml_svm` (Sim Score: 0.53)
- **AXIOM Response**: Support vector machines map data into a higher dimensional space where a linear separation becomes possible. The kernel trick computes this mapping without explicitly calculating the coordinates.

### Test 29: `explain svm`
- **Domain Route**: `classical_ml` (Confidence: 88.61%)
- **Intent Match**: `ml_svm` (Sim Score: 0.64)
- **AXIOM Response**: Support vector machines map data into a higher dimensional space where a linear separation becomes possible. The kernel trick computes this mapping without explicitly calculating the coordinates.

### Test 30: `what is a kernel trick`
- **Domain Route**: `classical_ml` (Confidence: 55.77%)
- **Intent Match**: `ml_svm` (Sim Score: 0.45)
- **AXIOM Response**: Support vector machines map data into a higher dimensional space where a linear separation becomes possible. The kernel trick computes this mapping without explicitly calculating the coordinates.

### Test 31: `how does svm classify`
- **Domain Route**: `classical_ml` (Confidence: 79.09%)
- **Intent Match**: `ml_svm` (Sim Score: 0.68)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 32: `what is clustering`
- **Domain Route**: `classical_ml` (Confidence: 55.29%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.56)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 33: `explain k means clustering`
- **Domain Route**: `classical_ml` (Confidence: 93.05%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.92)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 34: `what is unsupervised learning`
- **Domain Route**: `classical_ml` (Confidence: 74.30%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.36)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 35: `how does k means work`
- **Domain Route**: `classical_ml` (Confidence: 76.29%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.73)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 36: `what is k nearest neighbors`
- **Domain Route**: `classical_ml` (Confidence: 65.41%)
- **Intent Match**: `ml_knn` (Sim Score: 0.80)
- **AXIOM Response**: It makes no assumptions about the underlying data distribution. It simply measures distance, usually Euclidean, between the query point and the stored examples.

### Test 37: `explain knn`
- **Domain Route**: `classical_ml` (Confidence: 79.55%)
- **Intent Match**: `ml_knn` (Sim Score: 0.35)
- **AXIOM Response**: K-nearest neighbors stores all training data and classifies a new point by majority vote of its K closest neighbors in feature space. It is a lazy learner.

### Test 38: `how does nearest neighbor work`
- **Domain Route**: `classical_ml` (Confidence: 83.13%)
- **Intent Match**: `ml_knn` (Sim Score: 0.77)
- **AXIOM Response**: It makes no assumptions about the underlying data distribution. It simply measures distance, usually Euclidean, between the query point and the stored examples.

### Test 39: `how do you understand my questions`
- **Domain Route**: `self` (Confidence: 79.44%)
- **Intent Match**: `self_cosine_similarity` (Sim Score: 0.55)
- **AXIOM Response**: I convert your question into a vector using word frequencies. Then I calculate the cosine angle between your vector and every question in my memory. The smallest angle wins.

### Test 40: `what is cosine similarity`
- **Domain Route**: `self` (Confidence: 54.64%)
- **Intent Match**: `self_cosine_similarity` (Sim Score: 0.45)
- **AXIOM Response**: I convert your question into a vector using word frequencies. Then I calculate the cosine angle between your vector and every question in my memory. The smallest angle wins.

### Test 41: `how do you generate sentences`
- **Domain Route**: `self` (Confidence: 54.64%)
- **Intent Match**: `self_markov_chain` (Sim Score: 0.46)
- **AXIOM Response**: My generator uses a Markov chain. I look at the previous one or two words, check my probability matrix, and select the next word based on historical frequency.

### Test 42: `what is a markov chain`
- **Domain Route**: `self` (Confidence: 54.64%)
- **Intent Match**: `self_markov_chain` (Sim Score: 0.46)
- **AXIOM Response**: I build a probability matrix from my training text. For any given word, I roll a dice weighted by which words usually follow it. I chain these dice rolls until I reach a stopping state.

### Test 43: `how do you pick a domain`
- **Domain Route**: `self` (Confidence: 64.37%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 0.56)
- **AXIOM Response**: I classify your intent into a domain using Bayes theorem. I assume each word contributes independently to the probability of a topic.

### Test 44: `what is naive bayes`
- **Domain Route**: `self` (Confidence: 54.64%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 0.62)
- **AXIOM Response**: My domain router uses a Naive Bayes classifier. It calculates the probability that your question belongs to each domain based on word frequencies, then sends you to the most likely specialist.

### Test 45: `how do you work`
- **Domain Route**: `classical_ml` (Confidence: 58.34%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.20)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 46: `who invented the perceptron`
- **Domain Route**: `history` (Confidence: 89.61%)
- **Intent Match**: `hist_perceptron` (Sim Score: 0.77)
- **AXIOM Response**: The perceptron was the first machine learning algorithm that could iteratively adjust its weights based on classification errors. It sparked the first wave of AI optimism.

### Test 47: `who is alan turing`
- **Domain Route**: `history` (Confidence: 85.18%)
- **Intent Match**: `hist_turing` (Sim Score: 0.72)
- **AXIOM Response**: Alan Turing proposed the imitation game in 1950. A machine passes if a human cannot distinguish it from another human through text conversation alone.

### Test 48: `what is the turing test`
- **Domain Route**: `history` (Confidence: 66.10%)
- **Intent Match**: `hist_turing` (Sim Score: 0.69)
- **AXIOM Response**: Alan Turing proposed the imitation game in 1950. A machine passes if a human cannot distinguish it from another human through text conversation alone.

### Test 49: `what are transformers`
- **Domain Route**: `chit_chat` (Confidence: 48.41%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'chit_chat'.

### Test 50: `how does chatgpt work`
- **Domain Route**: `classical_ml` (Confidence: 41.31%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 0.20)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 51: `why are you not a neural network`
- **Domain Route**: `modern_context` (Confidence: 69.26%)
- **Intent Match**: `mod_vs_classical` (Sim Score: 0.59)
- **AXIOM Response**: Deep learning uses layered neural networks with millions of learned weights. I use explicit probability matrices and vector geometry. Both are mathematical models, but mine is fully inspectable.

