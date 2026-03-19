# 🎭 Scamouflage  
A simple game to understand how scam detection models can be fooled

---

## What is this?

Scamouflage is a small ML project where I built a **scam vs safe message classifier** and then turned it into a **game**.

Instead of just predicting labels, the idea is:
> Can you rewrite a scam message so the model thinks it’s safe?

---

## How it works

- Text → TF-IDF features (unigrams + bigrams)  
- Model → Logistic Regression  
- Output → Probability of being a scam  

\[
P(\text{scam}) = \sigma(w^T \phi(x) + b)
\]

---

## The Game

- Enter a message  
- See scam probability  
- Modify it to bypass detection  
- You get only 1 attempts  

### Difficulty levels

- Easy → threshold = 0.7  
- Medium → 0.5  
- Hard → 0.3  

Lower threshold = stricter model

---

## What I found

Even with good accuracy, the model is easy to trick.

Some simple tricks that work:
- Adding “safe” words like *team, meeting, payroll*  
- Removing obvious scam keywords  
- Slight obfuscation (*ver1fy, acc0unt*)  
- Using completely new words (model gets confused)

In many cases, the model just outputs ~0.5 because it doesn't recognize the input.

---

## Limitations

- Dataset is synthetic  
- Model is purely word-based (no real understanding)  
- Easy to bypass with small changes  

---

## Future Improvements

- Better dataset (more realistic messages)  
- Add character-level features  
- Compare with stronger models  
- Add more game modes + scoring system  

---


## Why I built this

Most projects stop at accuracy.  
I wanted to understand **how models fail** — and make that visible in a fun way.
