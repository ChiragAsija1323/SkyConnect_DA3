# SkyConnect DA-3: 12–15 Minute Video Presentation Script & Slide Guide
**Course:** Data Analytics using R (60-Mark Capstone Evaluation)  
**Academic Year:** 2026–2027 | **Faculty Guide:** Mrs. Vijayalakshmi  
**Presenters:** Chirag Asija (`24BDS1073`) & Saanvi Gupta (`24BDS1023`)  
**Total Target Duration:** 14 Minutes (Chirag: 7:00 min | Saanvi: 7:00 min — Exactly 50/50 Split)

---

## ⏱️ Video Presentation Timing & Structure Overview

| Timestamp | Section | Speaker | Duration | Visual / Screen to Display |
|---|---|---|:---:|---|
| **0:00 – 1:00** | Problem Motivation & Real-World Context | **Chirag** | 1:00 | Title Slide + Aviation Congestion Infographic |
| **1:00 – 2:00** | Data Architecture & Quality Audit | **Saanvi** | 1:00 | Teacher's Mandate Slide + `data_quality_audit.csv` |
| **2:00 – 3:05** | Exploratory Data Analysis: Physical Infrastructure | **Chirag** | 1:05 | Figures 1, 2, 3 (Runway normality, Elevation, Boxplots) |
| **3:05 – 4:10** | Exploratory Data Analysis: Continental Trends | **Saanvi** | 1:05 | Figures 4, 5 (Continental bars, GAM smoothed route curve) |
| **4:10 – 5:35** | Statistical Hypothesis Testing: Parametric Tests | **Chirag** | 1:25 | Figures 6, 8 (Welch's t-test, Mann-Whitney U, Heatmap) |
| **5:35 – 7:00** | Statistical Hypothesis Testing: ANOVA & Independence | **Saanvi** | 1:25 | Figure 7 (ANOVA boxplot, Chi-Square, VIF Table) |
| **7:00 – 8:00** | Feature Engineering & Leakage Prevention | **Chirag** | 1:00 | Figure 9 (Feature Ranking Justification Matrix) |
| **8:00 – 9:00** | Machine Learning Methodology & Architecture | **Saanvi** | 1:00 | ML Architecture Diagram (5 Classifiers, Regression, K-Means) |
| **9:00 – 10:15** | Supervised ML Results (Classification & Regression) | **Chirag** | 1:15 | Figures 10, 11, 12, 13 (ROC, Confusion Matrix, Diagnostics) |
| **10:15 – 11:30** | Unsupervised Clustering & igraph Network Analysis | **Saanvi** | 1:15 | Figures 14, 15, 16, 17 (K-Means, Betweenness, PageRank) |
| **11:30 – 12:30** | LIVE DEMO Part 1: Automated Pipeline in RStudio | **Chirag** | 1:00 | RStudio Console running `00_run_complete_pipeline.R` |
| **12:30 – 13:30** | LIVE DEMO Part 2: Interactive Leaflet Map | **Saanvi** | 1:00 | RStudio Viewer Pane showing `19_interactive_global_aviation_map.html` |
| **13:30 – 14:00** | GitHub Repository Walkthrough | **Chirag** | 0:30 | Browser / VS Code showing GitHub Repo & folder structure |
| **14:00 – 14:30** | Academic Conclusions & Defense Summary | **Saanvi** | 0:30 | Summary Slide & Acknowledgements to Mrs. Vijayalakshmi |

---

## 🎙️ Verbatim Speaker Dialogue & Screen Prompts

---

### [0:00 – 1:00] 1. Problem Motivation & Real-World Context
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Title Slide with Project Name, Team Details, and Faculty Guide Mrs. Vijayalakshmi*

> "Good day everyone, and respected faculty guide Mrs. Vijayalakshmi. My name is Chirag Asija, registration number 24BDS1073, and alongside my co-researcher Saanvi Gupta, 24BDS1023, we present **SkyConnect DA-3: A Statistically-Grounded Machine Learning Pipeline for Global Aviation Infrastructure and Airline Connectivity**.
> 
> The motivation behind our project stems from the severe post-pandemic capacity crisis in global air transportation. Every year, airlines open new routes and airports expand terminals. However, our fundamental research question asks: **Can the physical infrastructure of an airport—such as runway dimensions, surface composition, altitude, and geographic coordinates—statistically determine whether an airport can function as an international transit hub, completely independent of flight traffic numbers?**
>
> In real-world data science, machine learning models should never be deployed blindly. Before training a single algorithm, we must mathematically understand our data and prove underlying relationships. Now, Saanvi will introduce our data architecture and data quality audit."

---

### [1:00 – 2:00] 2. Data Architecture & Data Quality Audit
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: Relational SQLite schema + `data_quality_audit.csv` table*

> "Thank you, Chirag. To answer this research question, we adhered strictly to our faculty guide's instructions by following an end-to-end analytical workflow: mastering the dataset first, performing non-ML exploratory analysis, conducting rigorous hypothesis testing, justifying feature engineering, and only then training machine learning models.
>
> We connected to an authentic SQLite database containing over 67,000 flight routes and 4,569 commercial airports worldwide. 
> 
> In Step 1, we executed a rigorous Data Quality Audit. We classified every variable by its mathematical scale of measurement. We resolved the critical North America continent code trap, where the two-letter ISO code 'NA' was improperly read as missing. We imputed 47 missing elevation records using continent-specific medians, and audited distribution skewness and extreme outliers using Tukey's 1.5 times Interquartile Range rule. With our data validated and cleaned, Chirag will now walk through our exploratory findings."

---

### [2:00 – 3:05] 3. Exploratory Data Analysis: Physical Infrastructure
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Figure 1 (Runway Length Normality), Figure 2 (Elevation Skewness), Figure 3 (Runway Boxplot)*

> "In Step 2, we performed pure Exploratory Data Analysis without any machine learning, producing standard academic visualizations.
>
> Looking at **Figure 1**, we plotted the distribution of maximum runway lengths overlaid with a parametric Gaussian curve and kernel density estimation. Notice that runway lengths follow a bimodal distribution with peaks at 6,000 feet for regional aviation and 11,000 feet for wide-body international operations, showing a slight positive skewness of 0.07.
>
> Moving to **Figure 2**, airport elevation exhibits massive right-skewness of 2.94 and excess kurtosis of 11.41. Over 75% of global airports sit below 1,276 feet, but extreme outliers reach 14,472 feet in high-altitude terrain like Tibet and Bolivia.
>
> In **Figure 3**, our notched boxplots show a massive physical divide: large international airports maintain median runway lengths exceeding 10,000 feet, whereas medium airports plateau around 6,000 feet. The non-overlapping notches indicate that this physical difference is highly significant."

---

### [3:05 – 4:10] 4. Exploratory Data Analysis: Continental Trends
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: Figure 4 (Continental Infrastructure Breakdown) and Figure 5 (Route vs Runway Trend)*

> "Continuing our exploratory analysis, **Figure 4** examines continental infrastructure disparities with 95% confidence intervals. Asia and Europe lead the world with the longest average commercial runways, while Oceania and South America operate shorter runways suited for regional hops. 
>
> In **Figure 5**, we analyzed the relationship between runway capacity and route network traffic using a generalized additive model (GAM) smoother. We discovered a steep non-linear inflection point: airports with runways under 7,500 feet rarely support more than 20 routes. However, once runway length exceeds 10,000 feet—capable of handling long-haul Boeing 777s and Airbus A350s—route connectivity explodes exponentially.
>
> This purely exploratory visual discovery laid the mathematical foundation for our formal hypothesis testing, which Chirag will now present."

---

### [4:10 – 5:35] 5. Statistical Hypothesis Testing: Parametric Tests
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Figure 6 (Welch's t-test Plot) and Figure 8 (Correlation Matrix Heatmap)*

> "In Step 3, we subjected our observations to rigorous inferential statistics to test five formal hypotheses.
>
> **Hypothesis 1:** We hypothesized that international hubs require significantly longer runways than non-hubs. Because variances between groups were unequal, we conducted **Welch's Two-Sample t-test**. As shown in **Figure 6**, the results were astronomical: with a t-statistic of negative 36.31 and a p-value of 6.44 times 10 to the power of negative 168, we decisively rejected the null hypothesis. Major hubs average 10,749 feet compared to 7,391 feet for regular airports, with a Cohen's d of 1.39, representing a massive effect size.
>
> **Hypothesis 2:** Because runway counts and elevations are non-normal, we executed **Mann-Whitney U tests**. Runway counts yielded a W of 691,602 with a p-value of 1.8 times 10 to the power of negative 45, proving hubs require multi-runway systems. Elevation was also statistically detectable at p equals 4.3 times 10 to the negative 11.
>
> Saanvi will now explain our categorical and regional variance tests."

---

### [5:35 – 7:00] 6. Statistical Hypothesis Testing: ANOVA & Independence
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: Figure 7 (Continental ANOVA Boxplot with Tukey HSD) + Chi-Square & VIF Table*

> "Thank you, Chirag. **Hypothesis 3** evaluated categorical independence using **Pearson's Chi-Square Test**. The association between physical airport classification and hub status yielded a chi-square of 1,501.7 with a Cramér's V of 0.58, confirming an exceptionally strong relationship. Furthermore, paved runway status yielded a chi-square of 16.07; 99.7% of international hubs feature paved asphalt or concrete surfaces.
>
> **Hypothesis 4:** In **Figure 7**, we conducted a **One-Way ANOVA** across all six continents. The test returned an F-statistic of 102.42 with a p-value of 1.27 times 10 to the negative 102 and an eta-squared of 0.102. This proves that 10.2% of global runway variance is dictated purely by continental geography. Post-hoc Tukey HSD tests confirmed significant differences between Asia, North America, and Oceania.
>
> Finally, in **Hypothesis 5**, we computed Variance Inflation Factors (VIF) across all candidate numerical predictors. All VIF scores remained strictly below 1.15, well under the multicollinearity threshold of 5.0, proving zero redundancy among our features."

---

### [7:00 – 8:00] 7. Feature Engineering & Target Leakage Prevention
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Figure 9 (Statistically-Grounded Feature Selection Ranking Matrix)*

> "Step 4 represents a crucial requirement mandated by our faculty guide: **On what scientific basis were features selected?**
>
> Instead of picking predictors randomly, we constructed a formal Feature Justification Matrix, visualized in **Figure 9**. Predictors were mathematically ranked using their statistical p-values, Cohen's d, and Cramér's V effect sizes.
>
> Most importantly, we enforced strict **Target Leakage Prevention**. In our dataset, `total_routes` is an operational outcome of being a hub. If we included route counts to predict hub status, the model would suffer from trivial target leakage and fail in real-world infrastructure planning. We strictly excluded route counts, forcing our models to learn solely from physical and geographic predictors: runway length, runway count, paved surface, airport type, elevation, and latitude-longitude coordinates."

---

### [8:00 – 9:00] 8. Machine Learning Methodology & Architecture
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: ML Architecture Workflow (Train/Test Partition, 5-Fold CV, Multi-Model Suite)*

> "With our features mathematically vetted, Step 5 deployed an end-to-end Machine Learning suite.
>
> We partitioned our 4,508 operational commercial airports into an 80% stratified training set of 3,608 airports and a 20% unseen holdout test set of 900 airports.
>
> We framed a multi-task learning architecture:
> 1. **Supervised Classification**: Predicting Hub Status using 5 distinct algorithms: Logistic Regression, Decision Trees (CART), Linear Discriminant Analysis (LDA), Random Forest with 500 trees, and Gradient Boosting Machines (GBM). All models underwent 5-fold cross-validation.
> 2. **Supervised Regression**: Multiple Linear Regression predicting physical runway length requirements.
> 3. **Unsupervised Learning**: K-Means clustering to discover natural airport archetypes.
>
> Chirag will now reveal our classification and regression benchmarks."

---

### [9:00 – 10:15] 9. Supervised ML Results (Classification & Regression)
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Figures 10, 11, 12 (Model Leaderboard, Confusion Matrix, ROC curves) and Figure 13 (Regression Diagnostics)*

> "Evaluating on our 900 unseen holdout airports yielded outstanding results, shown in **Figures 10, 11, and 12**.
>
> Our champion model was the **Gradient Boosting Machine (GBM)**, achieving an overall accuracy of **92.0%**, a specificity of **97.6%**, and an Area Under the ROC Curve (AUC) of **0.9437**. Random Forest followed closely with an AUC of 0.9322. Feature importance diagnostics in Figure 12 confirmed that physical airport classification, maximum runway length, and runway count contributed over 85% of predictive power.
>
> In our regression analysis, shown in **Figure 13**, our multiple linear regression model predicted runway length with an R-squared of 0.455. The diagnostic residual panels confirmed that the normality and homoscedasticity assumptions held true across operational ranges.
>
> Saanvi will now present our unsupervised clustering and technical innovation in network graph analysis."

---

### [10:15 – 11:30] 10. Unsupervised Clustering & igraph Network Analysis
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: Figure 14 (K-Means Clusters) and Figures 15–18 (igraph Network Graph & Centrality)*

> "In **Figure 14**, K-Means clustering with k equals 3 naturally grouped airports into three distinct archetypes: Global Intercontinental Megahubs, Regional Gateways, and Domestic Feeder Airfields.
>
> For our project's technical innovation—earning top marks for analytical complexity—we modeled global aviation as an authentic Mathematical Network Graph using the `igraph` package in R, covering 66,288 directed routes.
>
> As shown in **Figures 15 through 18**, we computed graph topology metrics:
> * **Degree Centrality**: Frankfurt, Paris CDG, and Atlanta lead with the highest direct connectivity.
> * **Betweenness Centrality**: Identified Anchorage, Alaska (0.0702) and Dubai (0.0388) as the critical bridges connecting East-West global transit.
> * **Google PageRank**: Atlanta and Chicago emerged as the most authoritative global transit hubs.
> * **Louvain Community Detection**: Discovered continental airline alliance sub-networks with a high modularity Q of 0.66.
>
> Now, we transition to our live demonstration in RStudio."

---

### [11:30 – 12:30] 11. LIVE DEMO Part 1: Automated Pipeline in RStudio
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Live screen share of RStudio Desktop IDE running `00_run_complete_pipeline.R`*

> *(Demonstrating live on screen)*:
> "Here in RStudio, our entire academic pipeline is 100% reproducible with a single command. I will run `source('R/00_run_complete_pipeline.R')`.
>
> Notice the console output executing sequentially:
> * Step 1 ingests the SQLite database and executes the data quality audit.
> * Step 2 renders our 5 academic EDA figures.
> * Step 3 runs the Welch's t-test, ANOVA, and VIF calculations in real-time.
> * Step 4 computes the feature selection justification matrix and splits the dataset without target leakage.
> * Step 5 trains all 5 cross-validated machine learning models and regression diagnostics.
> * Step 6 builds the directed network graph in igraph.
> * And Step 7 generates our dual spatial visualizations.
>
> The entire pipeline completes in under 70 seconds! Saanvi will now demonstrate our interactive spatial visualization."

---

### [12:30 – 13:30] 12. LIVE DEMO Part 2: Interactive Leaflet Map
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: Live screen share of RStudio Viewer Pane and Web Browser displaying `19_interactive_global_aviation_map.html`*

> *(Demonstrating live on screen)*:
> "In the RStudio Viewer pane, we have rendered our interactive global aviation map using Leaflet and free OpenStreetMap tiles—completely free of API key watermarks.
>
> Notice the top-right layer control:
> * We can toggle **1,599 flight corridors**, including red global intercontinental corridors and golden amber Indian routes.
> * Zooming into India, we see full domestic trunk routes connecting Delhi, Mumbai, Bengaluru, Chennai, and Kolkata, alongside international long-haul routes to London, New York, Frankfurt, and Dubai.
> * Clicking on any airport—such as Indira Gandhi International in New Delhi—opens a rich popup displaying its 527 route connections, 14,500-foot runway, elevation, and hub status.
> * We can toggle between OpenStreetMap and Esri Topographic base tiles seamlessly.
>
> Chirag will now walk through our GitHub repository."

---

### [13:30 – 14:00] 13. GitHub Repository Walkthrough
**Speaker: Chirag Asija (`24BDS1073`)**  
*Screen: Web Browser showing the GitHub Repository structure and `README.md`*

> "Our project is hosted on GitHub under a clean, industry-standard modular repository structure:
> * The `R/` directory contains all 7 modular analytical scripts numbered 00 through 07.
> * The `database/` folder houses our 17MB relational SQLite database.
> * The `visualizations/` folder contains all 19 high-resolution 300-DPI publication figures plus the standalone interactive HTML map.
> * The `results/` folder stores all exported CSV tables for statistical tests, VIF, and ML metrics.
> * And our comprehensive `README.md` details reproducible execution instructions, mathematical formulas, and literature citations.
>
> Saanvi will now deliver our concluding remarks."

---

### [14:00 – 14:30] 14. Academic Conclusions & Defense Summary
**Speaker: Saanvi Gupta (`24BDS1023`)**  
*Screen: Summary Slide with Key Takeaways and Faculty Acknowledgements*

> "To conclude, our study conclusively demonstrates that physical airport infrastructure and geographic positioning are definitive determinants of global aviation hub viability. 
> 
> Our normal EDA and statistical tests proved that runway lengths (p < 10^-167) and continental location (p < 10^-101) establish physical operational thresholds, while our machine learning models proved that physical predictors alone predict hub status with 92% accuracy with zero target leakage.
>
> We express our sincere gratitude to our faculty guide, Mrs. Vijayalakshmi, for her invaluable guidance and rigorous academic standards throughout this capstone project. 
> 
> Thank you."

---

## 📋 Recording Checklist for the Team

* [ ] **Microphone & Audio**: Clear voice capture, no background noise.
* [ ] **RStudio Setup**: Resolution set to 1920x1080; zoom font in RStudio (`Cmd + +`) so code and console are easy to read.
* [ ] **Tabs Pre-opened**:
  1. Presentation Slides (Keynote / PowerPoint / Google Slides)
  2. RStudio open at `/Users/chiragasija/Downloads/SkyConnect_DA3 2`
  3. Interactive Leaflet Map open in RStudio Viewer Pane (or Chrome tab)
  4. GitHub Repository open in Web Browser
* [ ] **Timing Check**: Keep a stopwatch visible to ensure each speaker stays within their 7-minute budget.
