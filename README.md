# 🎭 Scamouflage  
### An Adversarial Guardrail Game for Understanding Spam Detection

---

## Overview

Scamouflage is an interactive adversarial learning experiment built around a spam detection model. The project explores how lexical machine learning classifiers behave under intentional manipulation.

A TF-IDF + Logistic Regression classifier is trained on the **SMSSpamCollection** dataset to predict whether a message is spam or legitimate. A game layer allows the user to iteratively modify a suspicious message and observe how the model’s predicted probability changes, attempting to bypass detection within limited attempts.

The objective is not just classification accuracy, but understanding guardrail vulnerability.

---

## Model Architecture

- **Text Representation:** TF-IDF (unigrams + bigrams)  
- **Classifier:** Logistic Regression  
- **Class Balancing:** Enabled  
- **Train/Test Split:** 80/20 (Stratified)

The classifier computes:

P(spam | x) = sigmoid(wᵀφ(x) + b)

Where:
- φ(x) = TF-IDF feature vector  
- w = learned weights  
- sigmoid = logistic function  

---

## Evaluation Metrics

The model is evaluated using:

- Accuracy  
- Precision  
- Recall  
- F1 Score  
- ROC-AUC  
- Confusion Matrix  

Despite strong aggregate performance, adversarial experiments reveal structural weaknesses.

---

## Adversarial Experiments

The notebook includes explicit adversarial manipulation techniques:

- Removal of high-weight spam tokens  
- Injection of benign tokens  
- Keyword obfuscation (e.g., "fr33", "cl@im")  
- Probability shift analysis  

These manipulations frequently reduce spam probability below the classification threshold, demonstrating that linear lexical models rely heavily on surface-level token presence.

---

## Key Insight

High accuracy does not imply robustness.

Traditional spam datasets contain strong lexical signals, making them easy to classify but also easy to exploit. Small token-level changes can significantly alter predictions, revealing limitations of surface-feature-based guardrails.

---

## Limitations

- Dataset is spam/ham, not intent-based scam detection  
- Linear model lacks semantic understanding  
- No adversarial training applied  

---

## Future Improvements

- Construct a more realistic intent-based scam dataset  
- Compare linear models with more expressive architectures  
- Add dual game modes (attacker vs legitimate sender)  
- Improve UI/UX with scoring and randomized feedback  

---

## Purpose

Scamouflage reframes spam detection as an adversarial interaction problem. Instead of treating classifiers as black boxes, it exposes how decisions are made and how they can fail.

The project demonstrates model interpretability, adversarial reasoning, and guardrail analysis through an interactive experiment.
Add dual game modes (attacker vs legitimate sender)
Improve UI/UX with scoring and randomized feedback
Purpose
Scamouflage reframes spam detection as an adversarial interaction problem. Instead of treating classifiers as black boxes, it exposes how decisions are made and how they can fail.
The project demonstrates model interpretability, adversarial reasoning, and guardrail analysis through an interactive experiment.
