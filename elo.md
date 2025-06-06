**Elo rating** is a method for calculating the *relative skill levels* of players in competitor-versus-competitor games like chess, and it has been adapted for many sports, including **tennis**.

---

### 🔢 What is Elo Rating?

The **Elo system** updates a player’s rating based on the expected outcome of a match and the actual outcome. The key ideas:

* Every player starts with a default rating (e.g., 1500).
* A win increases your rating, and a loss decreases it.
* Beating a highly rated player earns you more points than beating a lower-rated one.

---

### 🧮 Elo Formula

When Player A plays against Player B:

1. **Expected Score (EA)**:

$$
E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}
$$

2. **Updated Rating**:

$$
R_A' = R_A + K \cdot (S_A - E_A)
$$

* $R_A$: Player A's current rating
* $R_B$: Player B's current rating
* $S_A$: Actual score (1 if A wins, 0 if A loses)
* $K$: A factor controlling sensitivity (commonly 32 in tennis Elo systems)

---

### 🎾 How Elo Is Applied to Tennis

Unlike team sports, tennis is 1v1, and you can calculate Elo updates **after each match** using:

* `winner_name`
* `loser_name`
* `tourney_date` (for chronological order)

You maintain a **dictionary of player ratings**, initialized at a default (e.g., 1500), and process the matches one by one to update ratings.

---

### 📋 Example Dataset Columns

| date       | tourney\_name | tourney\_date | winner\_name   | loser\_name    |
| ---------- | ------------- | ------------- | -------------- | -------------- |
| 2024-05-27 | Roland Garros | 20240527      | Novak Djokovic | Carlos Alcaraz |
| 2024-05-28 | Roland Garros | 20240528      | Jannik Sinner  | Casper Ruud    |

You would:

1. Sort the dataset by `tourney_date`
2. Initialize ratings (e.g., all players start at 1500)
3. For each row:

   * Get ratings for `winner_name` and `loser_name`
   * Compute expected scores
   * Update both ratings based on the match outcome

---

### 🧠 Why Use Elo in Tennis?

* **More dynamic than ATP ranking**: updates after every match
* **Surface-specific Elo**: you can maintain a separate Elo for clay, grass, hard
* **Used for predictions**: models can use Elo (and surface Elo) as features
