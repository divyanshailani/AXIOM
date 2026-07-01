# AXIOM V1 Test Results

This file contains the output of 50 test prompts (general & technical) run against the V1 Zero-Training math engines.

### Test 1: `hey`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 2: `hello`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 3: `good morning`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 4: `how are you`
- **Domain Route**: `modern_context` (Confidence: 31.57%)
- **Intent Match**: `mod_vs_classical` (Sim Score: 0.44)
- **AXIOM Response**: Neural networks are black boxes. My cosine similarity scores and Markov probability tables are human-readable. You can see exactly why I chose every word.

### Test 5: `who are you`
- **Domain Route**: `history` (Confidence: 36.47%)
- **Intent Match**: `hist_perceptron` (Sim Score: 0.29)
- **AXIOM Response**: Frank Rosenblatt built the perceptron in 1957 at the Cornell Aeronautical Laboratory. It was an electronic model of a biological neuron and could learn weights from data.

### Test 6: `what is your name`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.58)
- **AXIOM Response**: K-means begins with random centroids. Each point joins the cluster of its nearest center. The centroids then shift to the mean of their assigned points, repeating until convergence.

### Test 7: `are you a robot`
- **Domain Route**: `modern_context` (Confidence: 31.57%)
- **Intent Match**: `mod_vs_classical` (Sim Score: 0.57)
- **AXIOM Response**: Deep learning uses layered neural networks with millions of learned weights. I use explicit probability matrices and vector geometry. Both are mathematical models, but mine is fully inspectable.

### Test 8: `what can you do`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.29)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 9: `tell me a joke`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.22)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 10: `bye`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 11: `what is machine learning`
- **Domain Route**: `classical_ml` (Confidence: 42.95%)
- **Intent Match**: `ml_clustering` (Sim Score: 0.75)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 12: `explain classical ml`
- **Domain Route**: `modern_context` (Confidence: 42.24%)
- **Intent Match**: `mod_vs_classical` (Sim Score: 0.52)
- **AXIOM Response**: Deep learning uses layered neural networks with millions of learned weights. I use explicit probability matrices and vector geometry. Both are mathematical models, but mine is fully inspectable.

### Test 13: `what is artificial intelligence`
- **Domain Route**: `history` (Confidence: 36.51%)
- **Intent Match**: `hist_perceptron` (Sim Score: 0.50)
- **AXIOM Response**: The perceptron was the first machine learning algorithm that could iteratively adjust its weights based on classification errors. It sparked the first wave of AI optimism.

### Test 14: `maths`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 15: `algorithms`
- **Domain Route**: `self` (Confidence: 41.42%)
- **Intent Match**: `self_overview` (Sim Score: 0.50)
- **AXIOM Response**: I am not a neural network. I am a pipeline of classical algorithms. A Naive Bayes router picks a domain, cosine similarity matches your intent, and a Markov chain generates my response.

### Test 16: `data science`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 17: `what is linear regression`
- **Domain Route**: `classical_ml` (Confidence: 81.31%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 1.00)
- **AXIOM Response**: Linear regression finds a straight line that minimizes the total squared distance to all observed data points. It assumes a linear relationship between an input feature and a target value.

### Test 18: `how does regression work`
- **Domain Route**: `classical_ml` (Confidence: 86.53%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 1.00)
- **AXIOM Response**: It models continuous outcomes by fitting a linear equation. The algorithm adjusts coefficients to minimize the residual sum of squares between predicted and actual values.

### Test 19: `explain ordinary least squares`
- **Domain Route**: `classical_ml` (Confidence: 89.29%)
- **Intent Match**: `ml_linear_regression` (Sim Score: 1.00)
- **AXIOM Response**: It models continuous outcomes by fitting a linear equation. The algorithm adjusts coefficients to minimize the residual sum of squares between predicted and actual values.

### Test 20: `what is logistic regression`
- **Domain Route**: `classical_ml` (Confidence: 86.71%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 1.00)
- **AXIOM Response**: Logistic regression predicts probabilities using the sigmoid function, which squeezes any real number into a range between zero and one. It is used for binary classification.

### Test 21: `explain logistic regression`
- **Domain Route**: `classical_ml` (Confidence: 95.78%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 1.00)
- **AXIOM Response**: Despite its name, it is a classification algorithm. It applies a logistic function to a linear combination of input features to estimate the probability of a class label.

### Test 22: `how does the sigmoid function work`
- **Domain Route**: `classical_ml` (Confidence: 78.02%)
- **Intent Match**: `ml_logistic_regression` (Sim Score: 1.00)
- **AXIOM Response**: Logistic regression predicts probabilities using the sigmoid function, which squeezes any real number into a range between zero and one. It is used for binary classification.

### Test 23: `what are decision trees`
- **Domain Route**: `classical_ml` (Confidence: 78.64%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 1.00)
- **AXIOM Response**: It creates a flowchart of decisions. At each branch, the algorithm chooses the feature that best separates the data, often using entropy or Gini impurity as a metric.

### Test 24: `how do decision trees work`
- **Domain Route**: `classical_ml` (Confidence: 91.42%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 1.00)
- **AXIOM Response**: It creates a flowchart of decisions. At each branch, the algorithm chooses the feature that best separates the data, often using entropy or Gini impurity as a metric.

### Test 25: `explain random forests`
- **Domain Route**: `classical_ml` (Confidence: 83.46%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 1.00)
- **AXIOM Response**: A decision tree splits data at each node by asking a question about a feature. It recursively partitions the space until it reaches a leaf node containing a prediction.

### Test 26: `what is entropy in a decision tree`
- **Domain Route**: `classical_ml` (Confidence: 90.11%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 1.00)
- **AXIOM Response**: It creates a flowchart of decisions. At each branch, the algorithm chooses the feature that best separates the data, often using entropy or Gini impurity as a metric.

### Test 27: `whats xgboost`
- **Domain Route**: `classical_ml` (Confidence: 35.00%)
- **Intent Match**: `unknown` (Sim Score: 0.00)
- **AXIOM Response**: I don't have knowledge about that in my current memory. Try asking about topics in 'classical_ml'.

### Test 28: `what is a support vector machine`
- **Domain Route**: `classical_ml` (Confidence: 63.75%)
- **Intent Match**: `ml_svm` (Sim Score: 1.00)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 29: `explain svm`
- **Domain Route**: `classical_ml` (Confidence: 85.92%)
- **Intent Match**: `ml_svm` (Sim Score: 1.00)
- **AXIOM Response**: Support vector machines map data into a higher dimensional space where a linear separation becomes possible. The kernel trick computes this mapping without explicitly calculating the coordinates.

### Test 30: `what is a kernel trick`
- **Domain Route**: `classical_ml` (Confidence: 59.19%)
- **Intent Match**: `ml_svm` (Sim Score: 1.00)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 31: `how does svm classify`
- **Domain Route**: `classical_ml` (Confidence: 81.31%)
- **Intent Match**: `ml_svm` (Sim Score: 1.00)
- **AXIOM Response**: An SVM finds the optimal hyperplane that maximizes the margin between two classes. The data points closest to the boundary are called support vectors, and they define the decision surface.

### Test 32: `what is clustering`
- **Domain Route**: `classical_ml` (Confidence: 57.01%)
- **Intent Match**: `ml_clustering` (Sim Score: 1.00)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 33: `explain k means clustering`
- **Domain Route**: `classical_ml` (Confidence: 91.91%)
- **Intent Match**: `ml_clustering` (Sim Score: 1.00)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 34: `what is unsupervised learning`
- **Domain Route**: `classical_ml` (Confidence: 57.78%)
- **Intent Match**: `ml_clustering` (Sim Score: 1.00)
- **AXIOM Response**: K-means begins with random centroids. Each point joins the cluster of its nearest center. The centroids then shift to the mean of their assigned points, repeating until convergence.

### Test 35: `how does k means work`
- **Domain Route**: `classical_ml` (Confidence: 76.26%)
- **Intent Match**: `ml_clustering` (Sim Score: 1.00)
- **AXIOM Response**: Clustering is unsupervised learning. It groups data points by similarity without predefined labels. K-means iteratively assigns points to the nearest centroid and updates the center.

### Test 36: `what is k nearest neighbors`
- **Domain Route**: `classical_ml` (Confidence: 68.51%)
- **Intent Match**: `ml_knn` (Sim Score: 1.00)
- **AXIOM Response**: K-nearest neighbors stores all training data and classifies a new point by majority vote of its K closest neighbors in feature space. It is a lazy learner.

### Test 37: `explain knn`
- **Domain Route**: `classical_ml` (Confidence: 75.32%)
- **Intent Match**: `ml_knn` (Sim Score: 1.00)
- **AXIOM Response**: It makes no assumptions about the underlying data distribution. It simply measures distance, usually Euclidean, between the query point and the stored examples.

### Test 38: `how does nearest neighbor work`
- **Domain Route**: `classical_ml` (Confidence: 84.19%)
- **Intent Match**: `ml_knn` (Sim Score: 1.00)
- **AXIOM Response**: K-nearest neighbors stores all training data and classifies a new point by majority vote of its K closest neighbors in feature space. It is a lazy learner.

### Test 39: `how do you understand my questions`
- **Domain Route**: `self` (Confidence: 75.46%)
- **Intent Match**: `self_cosine_similarity` (Sim Score: 1.00)
- **AXIOM Response**: Using linear algebra, I measure the cosine similarity between your input vector and my stored knowledge vectors. A smaller angle means a closer match.

### Test 40: `what is cosine similarity`
- **Domain Route**: `self` (Confidence: 59.72%)
- **Intent Match**: `self_cosine_similarity` (Sim Score: 1.00)
- **AXIOM Response**: I convert your question into a vector using word frequencies. Then I calculate the cosine angle between your vector and every question in my memory. The smallest angle wins.

### Test 41: `how do you generate sentences`
- **Domain Route**: `self` (Confidence: 59.72%)
- **Intent Match**: `self_markov_chain` (Sim Score: 1.00)
- **AXIOM Response**: I build a probability matrix from my training text. For any given word, I roll a dice weighted by which words usually follow it. I chain these dice rolls until I reach a stopping state.

### Test 42: `what is a markov chain`
- **Domain Route**: `self` (Confidence: 59.72%)
- **Intent Match**: `self_markov_chain` (Sim Score: 1.00)
- **AXIOM Response**: I build a probability matrix from my training text. For any given word, I roll a dice weighted by which words usually follow it. I chain these dice rolls until I reach a stopping state.

### Test 43: `how do you pick a domain`
- **Domain Route**: `self` (Confidence: 68.98%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 1.00)
- **AXIOM Response**: I classify your intent into a domain using Bayes theorem. I assume each word contributes independently to the probability of a topic.

### Test 44: `what is naive bayes`
- **Domain Route**: `self` (Confidence: 59.72%)
- **Intent Match**: `self_naive_bayes` (Sim Score: 1.00)
- **AXIOM Response**: I classify your intent into a domain using Bayes theorem. I assume each word contributes independently to the probability of a topic.

### Test 45: `how do you work`
- **Domain Route**: `classical_ml` (Confidence: 56.35%)
- **Intent Match**: `ml_decision_trees` (Sim Score: 0.67)
- **AXIOM Response**: It creates a flowchart of decisions. At each branch, the algorithm chooses the feature that best separates the data, often using entropy or Gini impurity as a metric.

### Test 46: `who invented the perceptron`
- **Domain Route**: `history` (Confidence: 94.70%)
- **Intent Match**: `hist_perceptron` (Sim Score: 1.00)
- **AXIOM Response**: Frank Rosenblatt built the perceptron in 1957 at the Cornell Aeronautical Laboratory. It was an electronic model of a biological neuron and could learn weights from data.

### Test 47: `who is alan turing`
- **Domain Route**: `history` (Confidence: 92.25%)
- **Intent Match**: `hist_turing` (Sim Score: 1.00)
- **AXIOM Response**: Alan Turing proposed the imitation game in 1950. A machine passes if a human cannot distinguish it from another human through text conversation alone.

### Test 48: `what is the turing test`
- **Domain Route**: `history` (Confidence: 72.42%)
- **Intent Match**: `hist_turing` (Sim Score: 1.00)
- **AXIOM Response**: Alan Turing proposed the imitation game in 1950. A machine passes if a human cannot distinguish it from another human through text conversation alone.

### Test 49: `what are transformers`
- **Domain Route**: `modern_context` (Confidence: 49.58%)
- **Intent Match**: `mod_transformers` (Sim Score: 1.00)
- **AXIOM Response**: Transformers use a mechanism called self-attention to weigh the importance of every word in a sentence against every other word simultaneously. They process sequences in parallel.

### Test 50: `how does chatgpt work`
- **Domain Route**: `modern_context` (Confidence: 39.46%)
- **Intent Match**: `mod_transformers` (Sim Score: 1.00)
- **AXIOM Response**: Unlike my Markov chains, which only look back one or two words, transformers compute relationships across entire paragraphs using attention scores and billions of parameters.

### Test 51: `why are you not a neural network`
- **Domain Route**: `modern_context` (Confidence: 82.54%)
- **Intent Match**: `mod_vs_classical` (Sim Score: 1.00)
- **AXIOM Response**: Deep learning uses layered neural networks with millions of learned weights. I use explicit probability matrices and vector geometry. Both are mathematical models, but mine is fully inspectable.

