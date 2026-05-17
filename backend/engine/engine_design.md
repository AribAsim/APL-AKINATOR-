# AI IPL Akinator Engine Design

## 1. Mathematical Model (Probability Engine)

The system relies on Bayesian probabilistic updates rather than hardcoded decision trees. This ensures adaptability, robust handling of incorrect user inputs, and smooth "Maybe/Don't Know" handling.

### Initial State
For a dataset of $N$ players, the initial probability for each player $i$ is uniform:
$$ P(player_i) = \frac{1}{N} $$

### Probability Update Formula
When the system asks a question regarding attribute $A$, the user provides an answer $R \in \{\text{Yes}, \text{No}, \text{Maybe}, \text{Don't Know}\}$.
We apply Bayes' Theorem to update the probability of each player:
$$ P(player_i | R) = \frac{P(R | player_i) P(player_i)}{P(R)} $$
Where $P(R)$ is the normalization constant across all players:
$$ P(R) = \sum_{j=1}^{N} P(R | player_j) P(player_j) $$

### Handling Answers (Likelihoods)
The term $P(R | player_i)$ represents the likelihood of the user giving response $R$ if $player_i$ is the actual player they are thinking of. We define the following likelihood matrix (tunable):

| User Answer ($R$) | If Player has Attribute ($A=True$) | If Player does NOT have Attribute ($A=False$) |
|-------------------|--------------------------------------|-------------------------------------------------|
| **Yes**           | 0.85                                 | 0.15                                            |
| **No**            | 0.15                                 | 0.85                                            |
| **Maybe**         | 0.60                                 | 0.40                                            |
| **Don't Know**    | 1.00                                 | 1.00                                            |

- **Yes/No**: Strong shift, but not absolute (1.0 / 0.0) to prevent the engine from completely eliminating a correct player if the user makes a slight mistake.
- **Maybe**: A slight tilt towards the attribute being true.
- **Don't Know**: Weight is 1.0 for both. The probabilities remain completely unchanged after normalization.

### Normalization Method
After calculating the new unnormalized probability for every player, we sum them up to find the total mass. We then divide each player's probability by this sum so the entire distribution always sums exactly to 1.0.

---

## 2. Entropy / Information Gain Logic (Question Selection)

To minimize the number of questions, the engine must select the attribute that provides the highest Information Gain.

### Candidate Split Calculation
Instead of calculating full Shannon Entropy which is overkill for binary splits, we aim for a perfectly balanced split (50/50 probability mass). 
For any candidate attribute $A$, we calculate the total probability mass of all players who possess that attribute:
$$ P_{mass}(A) = \sum_{i : A_i = True} P(player_i) $$

### Selecting the Best Attribute
The optimal attribute to ask about is the one where $P_{mass}(A)$ is closest to $0.5$.
We calculate a penalty score for each unasked attribute:
$$ \text{Score}_A = | P_{mass}(A) - 0.5 | $$
The attribute with the **lowest** score is selected as the next question.

- If an attribute has $P_{mass} = 1.0$ or $0.0$, its score is $0.5$ (the worst). This happens if all remaining likely candidates share the trait, meaning asking it yields zero new information.
- This logic runs in $O(N \times M)$ time (Players $\times$ Attributes), which for 250 players and 33 attributes is near instantaneous.
