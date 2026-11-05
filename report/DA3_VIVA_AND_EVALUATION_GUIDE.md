# SkyConnect DA-3: Complete Viva Defense & Presentation Guide
**A University Student's Step-by-Step Guide for the 60-Mark Final Evaluation**

* **Project Title**: SkyConnect DA-3 — A Statistically-Grounded Machine Learning Pipeline for Global Aviation Infrastructure & Airline Networks
* **Course**: Data Analytics using R (60-Mark Capstone Evaluation)
* **Team Members**: Chirag Asija (`24BDS1073`) & Saanvi Gupta (`24BDS1023`)
* **Faculty Guide**: Mrs. Vijayalakshmi

---

## 🎯 1. How to Structure Your 10–12 Minute Presentation

### Minute 0 to 2: Problem Motivation & Dataset Learning
> *"Respected Ma'am, in SkyConnect DA-3, we developed a complete end-to-end data analytics solution using R.  
> Following your guidance, we did not jump straight into machine learning. Instead, we followed a strict scientific methodology:
> 1. We first learned the dataset thoroughly and conducted a rigorous data quality audit.
> 2. We performed exploratory data analysis without any machine learning using standard academic visualizations.
> 3. We conducted formal statistical hypothesis testing with t-tests, Chi-square tests, and ANOVA to mathematically prove our relationships.
> 4. We selected our features strictly based on these statistical findings, while preventing target leakage.
> 5. And only then did we train our machine learning models for classification, regression, and clustering."*

---

### Minute 2 to 4: Data Quality Audit & Non-ML EDA
* **Point to show**: `results/data_quality_audit.csv` and **Figures 1 to 5**.
* **What to say**:
  > *"We combined 4,569 commercial airports from OpenFlights and OurAirports stored in an SQLite database.  
  > In our Data Quality Audit:
  > - Only 1.0% of records had missing elevation, which we handled using median imputation (368 ft).
  > - We resolved an R parsing trap where the North America continent code 'NA' is normally read as a missing null value, successfully preserving all 1,349 North American airports.
  > - In Figure 1, we see that runway length follows a near-perfect Gaussian normal distribution with a mean of 7,670 ft, while flight route traffic and airport elevation exhibit severe positive skewness."*

---

### Minute 4 to 6: Statistical Analysis & Hypothesis Testing
* **Point to show**: `results/statistical_test_results.csv` and **Figures 6, 7, and 8**.
* **What to say**:
  > *"To ensure academic rigor, we performed 5 formal hypothesis tests:
  > 1. **Welch's Two-Sample t-test**: In Figure 6, we tested if major hubs have longer runways than regular airports. We found t = -36.31 with p < 2.2e-16 and a large Cohen's d effect size of 1.39. Hub runways average 10,749 ft compared to 7,391 ft for regular airports (+3,358 ft difference).
  > 2. **Mann-Whitney U Test**: Confirmed that hubs have significantly more runways (W = 691,602, p = 1.80e-45).
  > 3. **Pearson's Chi-Square Test**: Proved strong categorical dependency between airport classification and hub status (Chi2 = 1,501.7, p < 2.2e-16, Cramér's V = 0.58).
  > 4. **One-Way ANOVA**: In Figure 7, we proved that runway lengths vary significantly across global continents (F = 102.42, p = 1.27e-102, Eta-squared = 0.102).
  > 5. **Multicollinearity VIF Test**: In Figure 8, our Pearson correlation heatmap and auxiliary regressions confirmed that all Variance Inflation Factors are under 1.15, proving zero multicollinearity."*

---

### Minute 6 to 8: Statistically Grounded Feature Engineering
* **Point to show**: `results/feature_selection_justification_matrix.csv` and **Figure 9**.
* **What to say**:
  > *"When selecting features for our predictive models, we did not guess. As shown in Figure 9, every retained feature has a mathematical justification:
  > - `max_runway_length`, `airport_type`, and `num_runways` were retained due to large effect sizes (Cohen's d = 1.39, Cramér's V = 0.58).
  > - `continent` was retained due to ANOVA significance.
  > - `latitude_deg` and `longitude_deg` were retained as non-collinear spatial transit predictors.
  > - **Most Importantly (Data Leakage Prevention)**: We strictly dropped `total_routes` from our predictor matrix. Because Hub Status was defined by route traffic, keeping total_routes would allow the model to cheat and produce fake 100% accuracy. Our models predict hub status purely from physical and geographical infrastructure."*

---

### Minute 8 to 10: Machine Learning Suite & Results
* **Point to show**: **Figures 10, 11, 12, 13, and 14**.
* **What to say**:
  > *"Using an 80% training set and an unseen 20% holdout test set of 900 airports:
  > 1. **Classification**: Evaluated 5 algorithms with 5-fold cross-validation. Gradient Boosting and Random Forest achieved a Cross-Validation ROC-AUC of 0.956. On the unseen test set, our champion model achieved **92.00% Accuracy, 97.62% Specificity, and a Test ROC-AUC of 0.9437**.
  > 2. **Regression**: In Figure 13, we predicted continuous runway lengths with Random Forest, achieving an R^2 of 0.455 and RMSE of 1,995 ft.
  > 3. **Unsupervised Clustering**: In Figure 14, K-Means clustering naturally grouped global aviation into three distinct operational archetypes: Regional Feeders, Primary Gateways, and International Super-Hubs."*

---

### Minute 10 to 12: Conclusion & Q&A
> *"In summary, SkyConnect DA-3 fulfills all requirements of the 60-mark rubric: rigorous data quality audit, non-ML statistical analysis, normal academic visualizations, hypothesis-proven feature engineering, and a leak-free machine learning suite. Thank you Ma'am, and we welcome your questions!"*

---

## 💡 Top 5 Teacher Questions & Model Answers

### Question 1: "Why did you choose Welch's t-test instead of Student's t-test?"
* **Answer**: *"Student's t-test assumes equal variances between the two groups (homoscedasticity). In our dataset, the variance in runway lengths for regular airports is different from hubs because regular airports span everything from small regional strips to major regional facilities. Welch's t-test does not assume equal variance, making it mathematically valid."*

### Question 2: "How did you ensure that there is no data leakage in your classification model?"
* **Answer**: *"Data leakage occurs when a predictor variable contains information derived directly from the target. We created Hub_Status using route counts (>50 routes = Hub). After creating the label, we **completely dropped total_routes and airport codes from the feature matrix**. Our models predict hub status purely from physical infrastructure (runway lengths, runway counts, paving) and geographical coordinates."*

### Question 3: "Why did you use Cramér's V and Cohen's d?"
* **Answer**: *"p-values only tell us whether an effect is statistically distinguishable from zero; they do not measure the magnitude or practical importance of the relationship, especially with a large sample size of 4,500 records. Cohen's d measures the standardized effect size for continuous variables (d = 1.39 is very large), while Cramér's V measures the strength of association for categorical variables (V = 0.58 indicates a strong relationship)."*

### Question 4: "Why did you use K-Means with K = 3?"
* **Answer**: *"In global aviation, airports naturally divide into three functional tiers: Regional Feeder airports (short runways, low route volume), Primary Domestic Gateways (medium-to-long runways, moderate routes), and Global Super-Hubs (multiple long runways, heavy international route banks). K = 3 captured these operational clusters cleanly."*

### Question 5: "What was the North America 'NA' bug and how did you resolve it?"
* **Answer**: *"In OurAirports, the continent code for North America is the two-letter string 'NA'. In R, read_csv() automatically interprets 'NA' as missing null data, which silently deleted over 1,300 North American airports. In Step 1, we intercepted the SQLite extract and explicitly converted missing continent values back to the string 'NA', ensuring all North American airports were properly analyzed."*
