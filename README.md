# SkyConnect DA-3: Comprehensive End-to-End Analytics in R
**A Statistically-Grounded Machine Learning Pipeline for Global Aviation Infrastructure & Airline Connectivity**

---

### Academic & Project Metadata
* **Academic Year**: 2026–2027
* **Faculty Guide**: Mrs. Vijayalakshmi
* **Student Authors**:
  * **Chirag Asija** (`24BDS1073`)
  * **Saanvi Gupta** (`24BDS1023`)
* **Project Directory**: `/Users/chiragasija/Downloads/SkyConnect_DA3`

---

## 🎯 Project Motivation & Research Objectives
In real-world data science, machine learning algorithms should never be applied arbitrarily without first mastering the dataset and proving underlying relationships mathematically. 

In **SkyConnect DA-3**, we structure our study into an end-to-end analytical workflow directly adhering to our teacher's mandate:
1. **Learning the Dataset & Data Quality Audit**: Understanding data types, scales of measurement, missing data imputation, skewness, and outlier detection.
2. **Exploratory Data Analysis WITHOUT Machine Learning**: Pure univariate and bivariate physical infrastructure exploration using normal academic visualizations.
3. **Statistical Hypothesis Testing**: Rigorously testing assumptions with Welch's $t$-tests, Mann-Whitney U, Chi-Square tests of independence, One-Way ANOVA, and Pearson/Spearman correlation matrices with Variance Inflation Factors (VIF).
4. **Statistically-Grounded Feature Engineering**: Explicitly answering *"On what scientific basis were features selected?"* by ranking predictors by $p$-value ($p < 0.001$) and effect size, while strictly enforcing **Target Leakage Prevention** by excluding flight volume.
5. **Multi-Task Machine Learning Suite**: Deploying Classification (Hub vs Regular), Regression (Runway Length Estimation), and Unsupervised Clustering (Airport Archetypes) with 5-fold cross-validation and holdout testing.

---

## 📁 Repository Directory Structure
```
SkyConnect_DA3/
├── README.md                                  # Complete project documentation & guide
├── database/
│   └── skyconnect.db                          # Relational SQLite database (5 aviation tables, 17MB)
├── data/
│   ├── raw/                                   # Original OpenFlights & OurAirports datasets
│   └── processed/
│       ├── raw_commercial_airports.csv        # Extracted cohort (4,569 commercial facilities)
│       ├── model_features_complete.csv        # Statistically vetted modeling matrix (4,508 airports)
│       ├── train_features.csv                 # 80% Stratified Training Partition (3,608 airports)
│       └── test_features.csv                  # 20% Holdout Testing Partition (900 airports)
├── R/                                         # Clean, Modular R Pipeline Scripts
│   ├── 00_run_complete_pipeline.R             # Master execution script (reproduces all steps)
│   ├── 01_dataset_profiling_and_quality.R     # Step 1: Learning data, quality audit, skewness
│   ├── 02_exploratory_data_analysis.R         # Step 2: Non-ML EDA & standard academic plots
│   ├── 03_statistical_hypothesis_testing.R    # Step 3: Parametric & non-parametric tests + VIF
│   ├── 04_statistically_grounded_feature_engineering.R # Step 4: Statistical feature justification & split
│   └── 05_machine_learning_suite.R            # Step 5: Classification, Regression, Clustering
├── results/                                   # Exported Statistical CSV Tables
│   ├── data_quality_audit.csv
│   ├── summary_statistics_table.csv
│   ├── statistical_test_results.csv
│   ├── pearson_correlation_matrix.csv
│   ├── feature_selection_justification_matrix.csv
│   ├── classification_cv_metrics.csv
│   ├── classification_test_metrics.csv
│   ├── regression_performance_metrics.csv
│   └── clustering_summary.csv
├── models/                                    # Serialized Model Artifacts (.rds files)
│   ├── model_logistic.rds
│   ├── model_decision_tree.rds
│   ├── model_lda.rds
│   ├── model_random_forest.rds
│   └── model_gbm.rds
├── visualizations/                            # 14 Publication-Grade Academic Figures (.png)
│   ├── 01_runway_length_distribution.png
│   ├── 02_airport_elevation_distribution.png
│   ├── 03_runway_by_airport_type_boxplot.png
│   ├── 04_continental_infrastructure_breakdown.png
│   ├── 05_routes_vs_runway_length_trend.png
│   ├── 06_runway_length_ttest_boxplot.png
│   ├── 07_anova_continental_runway_cis.png
│   ├── 08_correlation_matrix_heatmap.png
│   ├── 09_statistical_feature_ranking.png
│   ├── 10_classification_model_leaderboard.png
│   ├── 11_test_confusion_matrix.png
│   ├── 12_champion_roc_curve.png
│   ├── 13_regression_actual_vs_predicted.png
│   └── 14_kmeans_cluster_archetypes.png
└── report/                                    # Viva & Presentation Guides
    └── DA3_VIVA_AND_EVALUATION_GUIDE.md
```

---

## 📊 Summary of Statistical Hypothesis Findings

| Test Name | Variables Tested | Test Statistic | $p$-value | Effect Size | Academic Conclusion |
|---|---|:---:|:---:|:---:|---|
| **Welch's Two-Sample $t$-test** | `max_runway_length` across Hub Status | $t = -36.31$ | $6.44 \times 10^{-168}$ | Cohen's $d = 1.39$ | **Extremely significant**. Hubs average 10,749 ft vs 7,391 ft for regular airports. |
| **Mann-Whitney U Test** | `num_runways` across Hub Status | $W = 691,602$ | $1.80 \times 10^{-45}$ | Rank-Biserial $= 0.48$ | **Significant**. Major hubs have multi-runway configurations. |
| **Mann-Whitney U Test** | `elevation_ft` across Hub Status | $W = 1,209,563$ | $4.32 \times 10^{-11}$ | Rank-Biserial $= 0.08$ | Statistically detectable, but negligible effect size. |
| **Pearson's $\chi^2$ Test** | `airport_type` vs Hub Status | $\chi^2 = 1,501.7$ | $< 2.2 \times 10^{-16}$ | Cramér's $V = 0.58$ | **Very strong categorical association**. Large facility designation is a primary driver. |
| **Pearson's $\chi^2$ Test** | `has_paved_runway` vs Hub Status | $\chi^2 = 16.07$ | $6.11 \times 10^{-5}$ | Cramér's $V = 0.06$ | **Significant condition**. 99.7% of hubs are paved vs 87% regular. |
| **One-Way ANOVA** | `max_runway_length` across Continents | $F = 102.42$ | $1.27 \times 10^{-102}$ | $\eta^2 = 0.102$ | **Significant regional variance**. Asia & Africa feature longest average runways. |
| **Multicollinearity (VIF)** | All 5 numerical predictors | $\text{Max VIF} = 1.14$ | N/A | VIF $< 5.0$ | **Zero multicollinearity**. Predictors are completely non-redundant. |

---

## 🏆 Machine Learning Benchmarks (Unseen Holdout Test N = 900)
* **Champion Classifier**: Gradient Boosting / Random Forest
* **Test Accuracy**: **92.00%**
* **Test Specificity**: **97.62%**
* **Test Precision (PPV)**: **72.06%**
* **Test ROC-AUC**: **0.9437**
* **Runway Length Regression**: $R^2 = 0.4551$, $\text{RMSE} = 1,995\text{ ft}$
* **Target Leakage Safeguard**: **0% Data Leakage**. The target (`Hub_Status`) was generated from route counts, but `total_routes` was strictly dropped from all predictor matrices.

---

## 🚀 How to Run the Entire Project

Open R or RStudio in the project directory and execute:
```R
setwd("/Users/chiragasija/Downloads/SkyConnect_DA3/R")
source("00_run_complete_pipeline.R")
```
Or execute from terminal:
```bash
Rscript /Users/chiragasija/Downloads/SkyConnect_DA3/R/00_run_complete_pipeline.R
```
All 14 figures, 9 CSV summary tables, and 5 trained `.rds` models will be generated and saved automatically.
