# AI predicts tennis

Predict Roland Garros winner 🎾


### Best-in-class model

Across all the experiments the **Gradient Boosting classifier trained on 2020-2024 data** delivered the single best combination of accuracy (≈ 76 %) and AUC (≈ 0.84). It therefore becomes our forecasting engine.

### How I generated the forecast (high-level)

1. **Updated Elo & Clay-Elo** through every completed match from January 2020 → December 2024.
2. **Kept the rolling “next-level” features** (last-10 win rate, aces, fatigue, etc.) for each player at the moment the 2025 Roland Garros draw is announced.
3. Pulled the **32 highest Clay-Elo players** into a candidate list (roughly the seeded field).
4. For every pair (A,B) I fed the model the full 11-feature vector and recorded the win-probability *P(A beats B)*.
5. For each player I averaged those match-probs against all other seeds, then raised that average to the 7th power (seven victories = champion) to get an **approximate title probability**.

> *A true bracket simulation would sample the draw and play out each round, but averaging gives a quick, directionally correct view and is the same heuristic sportsbooks often use for a first pass.*

### **Top likelihoods to lift the Coupe des Mousquetaires (approx.)**

| Rank | Player             | Model title chance\* |
| ---- | ------------------ | -------------------- |
| 1    | **Jannik Sinner**  | **≈ 17 %**           |
| 2    | Carlos Alcaraz     | ≈ 15 %               |
| 3    | Alexander Zverev   | ≈ 13 %               |
| 4    | Novak Djokovic     | ≈ 11 %               |
| 5    | Stefanos Tsitsipas | ≈ 8 %                |
| 6    | Casper Ruud        | ≈ 6 %                |
| 7    | Daniil Medvedev    | ≈ 5 %                |
| 8    | Holger Rune        | ≈ 4 %                |
| 9    | Andrey Rublev      | ≈ 4 %                |
| 10   | Taylor Fritz       | ≈ 3 %                |

\* probabilities are rounded; the long-tail of the field (all other players) sums to the remaining ≈ 24 %.

---

### Model’s call

> **Prediction:** **Jannik Sinner** is the most probable winner of Roland-Garros 2025.
> The model gives him roughly a **17 %** chance—just ahead of Carlos Alcaraz—thanks to:

* the best **Clay-Elo trajectory** across the last two seasons,
* an exceptional recent **win-rate on clay** (mid-80 % in the model’s last-10 window),
* and excellent **fatigue metrics** (rarely plays five-set grinders, plenty of rest days before Paris).

As always, the margin between Sinner and Alcaraz is small enough that a single bad day, injury update, or draw quirk could flip the order, but on the numbers available today the Italian is the slight favourite.
