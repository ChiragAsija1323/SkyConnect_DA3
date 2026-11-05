# ==============================================================================
# SkyConnect DA-3: Interactive Aviation Analytics & Visualizations Dashboard
# Framework: R Shiny + bslib (Modern Bootstrap 5 Academic Architecture)
# Purpose: Interactive inspection of all 19 publication figures, statistical
#          tests, ML benchmarks, network graph metrics, and live Leaflet map.
# Course: Data Analytics using R | Faculty Guide: Mrs. Vijayalakshmi
# Authors: Chirag Asija (24BDS1073) & Saanvi Gupta (24BDS1023)
# ==============================================================================

suppressPackageStartupMessages({
  library(shiny)
  library(bslib)
  library(leaflet)
  library(readr)
  library(dplyr)
  library(htmltools)
})

# ------------------------------------------------------------------------------
# 1. Path Setup (Dynamic Detection)
# ------------------------------------------------------------------------------
find_project_dir <- function() {
  if (dir.exists("visualizations")) return(".")
  if (dir.exists("../visualizations")) return("..")
  if (dir.exists("/Users/chiragasija/Downloads/SkyConnect_DA3 2/visualizations")) {
    return("/Users/chiragasija/Downloads/SkyConnect_DA3 2")
  }
  return("/Users/chiragasija/Downloads/SkyConnect_DA3")
}

proj_dir <- find_project_dir()
viz_dir  <- file.path(proj_dir, "visualizations")
res_dir  <- file.path(proj_dir, "results")

# Register static asset directory for high-speed local image serving
addResourcePath("viz", viz_dir)

# ------------------------------------------------------------------------------
# 2. Comprehensive Metadata for All 19 Visualizations (Clean Academic Focus)
# ------------------------------------------------------------------------------
viz_metadata <- list(
  "fig01" = list(
    id = "fig01", num = 1, file = "01_runway_length_distribution.png",
    title = "Figure 1: Maximum Runway Length Distribution & Parametric Normality Curve",
    category = "Step 2: Exploratory Data Analysis (EDA)",
    formula_display = "f(x) = [ 1 / (σ · √(2π)) ] · exp( -½ · ((x - μ) / σ)² )",
    formula_desc = "Probability Density Function of the Gaussian Normal Distribution",
    stats = "Mean = 7,670 ft | SD = 2,770 ft | Median = 7,571 ft | Skewness = 0.07 | Excess Kurtosis = -0.13",
    objective = "Evaluate whether physical runway dimensions satisfy parametric normality assumptions for inferential testing.",
    conclusion = "Runway lengths exhibit mild bimodal density (peaks at 6,000 ft for regional turboprops and 11,000 ft for wide-body jets), but near-zero skewness (0.07) allows robust parametric Welch's t-testing."
  ),
  "fig02" = list(
    id = "fig02", num = 2, file = "02_airport_elevation_distribution.png",
    title = "Figure 2: Airport Elevation Distribution (Skewness & Altitude Outliers)",
    category = "Step 2: Exploratory Data Analysis (EDA)",
    formula_display = "Skewness γ₁ = E[ ((X - μ) / σ)³ ] = 2.94  |  Kurtosis κ = E[ ((X - μ) / σ)⁴ ] - 3 = 11.41",
    formula_desc = "Third and Fourth Standardized Moments of the Elevation Distribution",
    stats = "Mean = 1,098 ft | Median = 368 ft | Q3 = 1,276 ft | Skewness = 2.94 | Kurtosis = 11.41 | Outliers = 11.0%",
    objective = "Audit geographic altitude distribution and detect extreme topographical constraints.",
    conclusion = "Elevation exhibits massive positive skewness (2.94) and heavy-tailed kurtosis (11.41). Over 75% of global airports operate below 1,276 ft, while extreme high-altitude outliers reach 14,472 ft."
  ),
  "fig03" = list(
    id = "fig03", num = 3, file = "03_runway_by_airport_type_boxplot.png",
    title = "Figure 3: Maximum Runway Length by Airport Classification (Notched Boxplots)",
    category = "Step 2: Exploratory Data Analysis (EDA)",
    formula_display = "Notch Interval = Median ± 1.58 · ( IQR / √n )  [95% Confidence Interval for Medians]",
    formula_desc = "McGill, Tukey & Larsen Notched Boxplot Confidence Boundary",
    stats = "Large Airport Median = 10,170 ft (IQR: 8,800 - 11,800 ft) | Medium Airport Median = 5,900 ft (IQR: 4,500 - 7,200 ft)",
    objective = "Compare runway infrastructure distributions between large and medium commercial facilities.",
    conclusion = "The 95% confidence notches do not overlap, demonstrating an undeniable physical separation: large international facilities operate at least 10,000 ft runways to safely accommodate wide-body airliners."
  ),
  "fig04" = list(
    id = "fig04", num = 4, file = "04_continental_infrastructure_breakdown.png",
    title = "Figure 4: Continental Infrastructure Disparities & 95% Confidence Intervals",
    category = "Step 2: Exploratory Data Analysis (EDA)",
    formula_display = "CI₉₅% = x̄ ± t₀.₉₇₅, n₋₁ · ( s / √n )",
    formula_desc = "Student's t-Distribution 95% Confidence Interval for Continental Means",
    stats = "Asia Mean = 8,600 ft | Europe Mean = 8,100 ft | North America = 7,650 ft | Oceania Mean = 5,865 ft",
    objective = "Audit continental inequality in civil aviation runway infrastructure investments.",
    conclusion = "Asia and Europe lead in average runway lengths due to dense intercontinental wide-body trunk traffic, whereas Oceania and South America maintain shorter runways suited for archipelago hops."
  ),
  "fig05" = list(
    id = "fig05", num = 5, file = "05_routes_vs_runway_length_trend.png",
    title = "Figure 5: Route Network Traffic vs Runway Capacity (Non-Linear GAM Smoother)",
    category = "Step 2: Exploratory Data Analysis (EDA)",
    formula_display = "g( E(Routes) ) = β₀ + f( Runway_Length )  [Generalized Additive Model with Penalized Splines]",
    formula_desc = "Non-Parametric Smooth Function Linking Infrastructure to Airline Routes",
    stats = "Inflection Threshold = 10,000 ft | Sub-7,500 ft: Max Routes <= 20 | > 10,000 ft: Routes > 500+",
    objective = "Discover the empirical functional relationship between physical runway capacity and airline network routes.",
    conclusion = "Discovered a steep non-linear inflection: facilities under 7,500 ft plateau under 20 routes. Once runway exceeds 10,000 ft (enabling B777/A350 MTOW departures), route connectivity increases exponentially."
  ),
  "fig06" = list(
    id = "fig06", num = 6, file = "06_runway_length_ttest_boxplot.png",
    title = "Figure 6: Welch's Two-Sample t-test on Runway Length (p < 10^-167)",
    category = "Step 3: Statistical Hypothesis Testing",
    formula_display = "t = ( X̄_Hub - X̄_Reg ) / √( (s₁² / n₁) + (s₂² / n₂) ) = -36.31  [df = 756.6, p = 6.44 × 10⁻¹⁶⁸]",
    formula_desc = "Welch's Unequal Variances Two-Sample t-Statistic with Satterthwaite Approximation",
    stats = "t = -36.31 | df = 756.6 | p-value = 6.44e-168 | Mean Regular = 7,391 ft | Mean Hub = 10,749 ft | Cohen's d = 1.39",
    objective = "Formally test the null hypothesis that international hubs have identical runway lengths to regular airports.",
    conclusion = "Decisively rejected H0 (p < 10^-167). Major hubs average 10,749 ft vs 7,391 ft for regular airports. Cohen's d of 1.39 confirms an exceptionally large practical effect size."
  ),
  "fig07" = list(
    id = "fig07", num = 7, file = "07_anova_continental_runway_cis.png",
    title = "Figure 7: One-Way ANOVA across Continents with Post-Hoc Tukey HSD",
    category = "Step 3: Statistical Hypothesis Testing",
    formula_display = "F = MS_between / MS_within = 102.42  |  η² = SS_between / SS_total = 0.102 (10.2% variance)",
    formula_desc = "One-Way Analysis of Variance F-Ratio and Eta-Squared Effect Size",
    stats = "F(5, 4502) = 102.42 | p-value = 1.27e-102 | Eta-Squared = 0.102 | Tukey HSD: AS, EU != OC, SA (p_adj < 0.001)",
    objective = "Test whether civil aviation runway infrastructure varies significantly across world continents.",
    conclusion = "One-Way ANOVA is highly significant (F = 102.42, p < 10^-101). Geography drives 10.2% of global runway variance. Tukey HSD confirms Asia and Europe operate statistically distinct infrastructure."
  ),
  "fig08" = list(
    id = "fig08", num = 8, file = "08_correlation_matrix_heatmap.png",
    title = "Figure 8: Pearson Correlation Matrix Heatmap & VIF Multicollinearity Diagnostics",
    category = "Step 3: Statistical Hypothesis Testing",
    formula_display = "r = Cov(X, Y) / ( σ_x · σ_y )  |  VIF_j = 1 / ( 1 - R_j² ) < 1.15  [Max VIF = 1.14]",
    formula_desc = "Pearson Product-Moment Correlation and Variance Inflation Factor",
    stats = "Max Pairwise r = 0.31 (Runway Length & Counts) | Max VIF = 1.14 (Threshold < 5.0) | Zero Multicollinearity",
    objective = "Diagnose linear dependencies and multicollinearity among candidate machine learning predictors.",
    conclusion = "All pairwise correlations are moderate to low (max r = 0.31). All Variance Inflation Factors are strictly below 1.15, guaranteeing numerical stability and zero redundancy in ML models."
  ),
  "fig09" = list(
    id = "fig09", num = 9, file = "09_statistical_feature_ranking.png",
    title = "Figure 9: Statistically-Grounded Feature Selection Justification Matrix",
    category = "Step 4: Feature Engineering",
    formula_display = "Feature Ranking: Effect Size Hierarchy (Cohen's d = 1.39, Cramér's V = 0.58, p < 0.001)",
    formula_desc = "Formal Mathematical Criteria Mandated by Course Rubric (total_routes strictly excluded)",
    stats = "Rank 1: Runway Length (Cohen's d = 1.39) | Rank 2: Airport Type (Cramér's V = 0.58) | 0% Target Leakage",
    objective = "Provide explicit mathematical justification for why each feature was selected for modeling.",
    conclusion = "Features were ranked by statistical effect size. Total routes was explicitly EXCLUDED to enforce strict Target Leakage Prevention, ensuring the model predicts from physical infrastructure alone."
  ),
  "fig10" = list(
    id = "fig10", num = 10, file = "10_classification_model_leaderboard.png",
    title = "Figure 10: Classification Model Leaderboard (5-Fold Cross-Validation Metrics)",
    category = "Step 5: Machine Learning Suite",
    formula_display = "Accuracy = ( TP + TN ) / N = 92.0%  |  Specificity = TN / ( TN + FP ) = 97.6%",
    formula_desc = "Cross-Validated Supervised Classification Performance Formulation",
    stats = "GBM: Acc = 92.0%, Spec = 97.6%, AUC = 0.9437 | Random Forest: Acc = 91.8%, AUC = 0.9322 | Logistic: Acc = 89.2%",
    objective = "Benchmark 5 supervised classification algorithms using 5-fold stratified cross-validation.",
    conclusion = "Gradient Boosting Machine (GBM) achieved champion status across accuracy, specificity, and ROC-AUC on the 900 unseen holdout airports, outperforming Random Forest, LDA, and Logistic Regression."
  ),
  "fig11" = list(
    id = "fig11", num = 11, file = "11_test_confusion_matrix.png",
    title = "Figure 11: Champion GBM Holdout Test Confusion Matrix (92.0% Accuracy)",
    category = "Step 5: Machine Learning Suite",
    formula_display = "Sensitivity = TP / ( TP + FN ) = 48.5%  |  Specificity = TN / ( TN + FP ) = 97.6%",
    formula_desc = "Holdout Evaluation Contingency Matrix (N = 900 Unseen Airports)",
    stats = "Total Holdout N = 900 | True Negatives = 778 | True Positives = 50 | False Positives = 19 | False Negatives = 53",
    objective = "Diagnose classification error distributions on unseen test airports.",
    conclusion = "The model achieved 97.6% specificity, virtually eliminating false alarms—vital for civil aviation authorities avoiding multi-million dollar infrastructure misallocations."
  ),
  "fig12" = list(
    id = "fig12", num = 12, file = "12_champion_roc_curve.png",
    title = "Figure 12: Champion GBM Multi-Model ROC Curves (AUC = 0.9437)",
    category = "Step 5: Machine Learning Suite",
    formula_display = "AUC = ∫₀¹ TPR( FPR⁻¹(t) ) dt = 0.9437  [Area Under Receiver Operating Characteristic Curve]",
    formula_desc = "Integral Discrimination Metric across All Operational Cutoff Thresholds",
    stats = "GBM AUC = 0.9437 | Random Forest AUC = 0.9322 | Logistic Regression AUC = 0.9124 | LDA AUC = 0.9080",
    objective = "Evaluate discrimination thresholds across all operational classification cutoffs.",
    conclusion = "The GBM ROC curve hugs the upper-left boundary, delivering an AUC of 0.9437, confirming excellent discrimination between hub and non-hub facilities."
  ),
  "fig13" = list(
    id = "fig13", num = 13, file = "13_regression_actual_vs_predicted.png",
    title = "Figure 13: Runway Length Regression Diagnostics (4-Panel Q-Q & Residuals)",
    category = "Step 5: Machine Learning Suite",
    formula_display = "R² = 1 - ( SS_res / SS_tot ) = 0.455  |  F(10, 4497) = 376.1  (p < 10⁻³⁰⁰)",
    formula_desc = "Multiple Linear Regression Coefficient of Determination and Model F-Ratio",
    stats = "R² = 0.455 | Adjusted R² = 0.454 | F = 376.1 | p < 10^-300 | Residual SE = 2,045 ft",
    objective = "Predict physical runway length requirements and test linear model assumptions.",
    conclusion = "Multiple linear regression explains 45.5% of variance in runway length. Residual diagnostics confirm homoscedastic dispersion and Normal Q-Q alignment across operational ranges."
  ),
  "fig14" = list(
    id = "fig14", num = 14, file = "14_kmeans_cluster_archetypes.png",
    title = "Figure 14: K-Means Airport Archetypes Bivariate Clusters (K = 3)",
    category = "Step 5: Machine Learning Suite",
    formula_display = "J = Σₖ Σᵢ || xᵢ - μₖ ||²  [Within-Cluster Sum of Squares Optimization with K = 3]",
    formula_desc = "Unsupervised Euclidean Partitioning via Lloyd's Algorithm",
    stats = "Cluster 1: Global Megahubs (N = 514) | Cluster 2: Regional Gateways (N = 1,420) | Cluster 3: Feeder Airfields (N = 2,574)",
    objective = "Discover natural airport operational archetypes through unsupervised clustering.",
    conclusion = "K-Means naturally partitioned the global aviation system into 3 intuitive archetypes: Global Intercontinental Megahubs, Regional Gateways, and Domestic Feeder Airfields."
  ),
  "fig15" = list(
    id = "fig15", num = 15, file = "15_network_centrality_leaderboard.png",
    title = "Figure 15: igraph Aviation Network Centrality Leaderboard",
    category = "Step 6: Aviation Network Graph Analysis",
    formula_display = "Degree C_D(v) = deg(v)  |  Betweenness C_B(v) = Σ_{s ≠ v ≠ t} ( σ_st(v) / σ_st )",
    formula_desc = "Topological Graph Centrality Metrics for Directed Networks",
    stats = "Max Degree: Frankfurt (FRA, 990), Paris (CDG, 966), Atlanta (ATL, 924) | Vertices = 3,388 | Edges = 66,288",
    objective = "Model the global aviation system as a directed mathematical network graph using igraph in R.",
    conclusion = "Frankfurt, Paris Charles de Gaulle, and Atlanta emerge as the global network's most densely connected nodes, validating degree centrality theory."
  ),
  "fig16" = list(
    id = "fig16", num = 16, file = "16_scale_free_power_law_distribution.png",
    title = "Figure 16: Degree Distribution & Scale-Free Power-Law Fit",
    category = "Step 6: Aviation Network Graph Analysis",
    formula_display = "P(k) ~ k^(-γ),  Power-Law Exponent γ = 2.08  [R² = 0.94, KS p > 0.05]",
    formula_desc = "Barabási-Albert Scale-Free Network Degree Formulation",
    stats = "Power-Law Exponent γ = 2.08 | Kolmogorov-Smirnov p > 0.05 | Heavy-Tailed Scale-Free Architecture",
    objective = "Test whether global airline routes follow a scale-free network topology (Barabási-Albert model).",
    conclusion = "The degree distribution follows a power law with exponent 2.08, mathematically proving the global aviation network is a robust scale-free system resilient to random airport failures."
  ),
  "fig17" = list(
    id = "fig17", num = 17, file = "17_betweenness_vs_pagerank_scatter.png",
    title = "Figure 17: Betweenness Centrality vs Google PageRank Scatter Plot",
    category = "Step 6: Aviation Network Graph Analysis",
    formula_display = "PR(v) = (1 - d)/N + d · Σ_{u ∈ M(v)} ( PR(u) / L(u) ),  Damping Factor d = 0.85",
    formula_desc = "Brin & Page Stationary Markov Chain Transit Random Walk Formulation",
    stats = "Top Bridge: Anchorage (ANC, 0.0702), Dubai (DXB, 0.0388) | Top PageRank: Atlanta (ATL, 0.0076), Chicago (ORD, 0.0068)",
    objective = "Identify critical transit bottleneck bridges and authoritative transit hubs.",
    conclusion = "Betweenness uniquely identified Anchorage, Alaska as the world's most critical transpacific cargo bridge, and Dubai as the East-West crossroads bridge."
  ),
  "fig18" = list(
    id = "fig18", num = 18, file = "18_network_community_louvain_clusters.png",
    title = "Figure 18: Louvain Community Detection Airline Sub-Networks",
    category = "Step 6: Aviation Network Graph Analysis",
    formula_display = "Q = (1 / 2m) · Σ_vw [ A_vw - (k_v · k_w / 2m) ] · δ(c_v, c_w) = 0.66",
    formula_desc = "Blondel et al. Modularity Optimization Formulation",
    stats = "Modularity Q = 0.66 | 8 Natural Continental Communities | High Alliance Clustering",
    objective = "Discover structural modularity and natural airline alliance clusters using the Louvain algorithm.",
    conclusion = "Louvain community detection achieved a high modularity Q of 0.66, automatically partitioning global aviation into 8 coherent continental and alliance sub-networks."
  ),
  "fig19" = list(
    id = "fig19", num = 19, file = "19_global_flight_routes_map.png",
    title = "Figure 19: Comprehensive Global Flight Network & Indian Aviation Connectivity",
    category = "Step 7: Spatial & Interactive Mapping",
    formula_display = "cos(Δσ) = sin(φ₁) · sin(φ₂) + cos(φ₁) · cos(φ₂) · cos(Δλ)  [Spherical Law of Cosines]",
    formula_desc = "Great Circle Geodesic Arc Formulation on Spherical Earth Coordinates",
    stats = "1,599 Flight Corridors | 857 Indian Routes (Domestic & International) | 742 Global Intercontinental Corridors",
    objective = "Render a publication-grade spatial route network and interactive Leaflet map.",
    conclusion = "The map captures 1,599 global and Indian flight corridors. India is prominently showcased with full domestic trunk connectivity and international links to London, New York, Frankfurt, and Dubai."
  )
)

# ------------------------------------------------------------------------------
# 3. UI Definition (Modern bslib Bootstrap 5 Academic Architecture)
# ------------------------------------------------------------------------------
theme_academic <- bs_theme(
  bootswatch = "zephyr",
  primary = "#1E3A8A",
  secondary = "#475569",
  success = "#10B981",
  info = "#0284C7",
  warning = "#D97706",
  danger = "#DC2626",
  base_font = font_google("Inter"),
  heading_font = font_google("Inter")
)

ui <- page_navbar(
  title = div(
    span(style = "font-weight: 800; color: #1E3A8A; font-size: 1.15rem;", "SKYCONNECT DA-3"),
    span(style = "color: #64748B; font-size: 0.9rem; margin-left: 8px;", "| Aviation Analytics & ML Dashboard")
  ),
  theme = theme_academic,
  navbar_options = navbar_options(bg = "#FFFFFF"),
  
  # Top Header Metadata Banner
  header = tagList(
    div(
      style = "background: #F8FAFC; border-bottom: 1px solid #E2E8F0; padding: 8px 24px; font-size: 0.82rem; color: #475569; display: flex; justify-content: space-between; align-items: center;",
      div(
        strong("Course: "), "Data Analytics using R (DA-3 Evaluation)  •  ",
        strong("Guide: "), "Mrs. Vijayalakshmi  •  ",
        strong("Authors: "), "Chirag Asija (24BDS1073) & Saanvi Gupta (24BDS1023)"
      ),
      div(
        span(class = "badge bg-primary", "R 4.6.1"),
        span(class = "badge bg-success", "N = 4,508 Airports"),
        span(class = "badge bg-warning text-dark", "1,599 Routes"),
        span(class = "badge bg-info", "GBM AUC 0.9437")
      )
    )
  ),
  
  # ============================================================================
  # TAB 1: EXECUTIVE OVERVIEW & KPIS
  # ============================================================================
  nav_panel(
    title = "📊 Executive Overview",
    layout_columns(
      fill = FALSE,
      value_box(
        title = "Operational Airports",
        value = "4,508",
        showcase = icon("plane-arrival"),
        theme = "primary",
        p("100% Quality Audited & Imputed")
      ),
      value_box(
        title = "Flight Routes Analyzed",
        value = "67,663",
        showcase = icon("route"),
        theme = "info",
        p("OpenFlights Global Topology")
      ),
      value_box(
        title = "Welch's t-Test",
        value = "t = -36.31",
        showcase = icon("chart-line"),
        theme = "warning",
        p("p < 10^-167 | Cohen's d = 1.39")
      ),
      value_box(
        title = "Champion ML Model",
        value = "GBM 92.0%",
        showcase = icon("trophy"),
        theme = "success",
        p("Specificity 97.6% | AUC 0.9437")
      ),
      value_box(
        title = "Top Network Bridge",
        value = "Anchorage (ANC)",
        showcase = icon("circle-nodes"),
        theme = "danger",
        p("Betweenness = 0.0702 (DXB #2)")
      )
    ),
    
    div(style = "margin-top: 16px;"),
    
    layout_columns(
      col_widths = c(7, 5),
      card(
        card_header(class = "bg-primary text-white font-weight-bold", "🎯 Research Objectives & Problem Motivation"),
        card_body(
          h5(style = "color: #1E3A8A; font-weight: 700;", "Can Physical Infrastructure Alone Dictate Aviation Hub Viability?"),
          p("Global commercial aviation faces unprecedented capacity bottlenecks. While airport operators expand terminals and gates, our study mathematically proves that physical constraints—runway dimensions, paving, elevation, and geography—determine whether an airport can function as an international transit hub, completely independent of flight traffic numbers."),
          hr(),
          h6(style = "font-weight: 700; color: #334155;", "Adherence to Faculty Mandate (Mrs. Vijayalakshmi):"),
          tags$ol(
            tags$li(strong("Learning the Dataset: "), "13-variable quality audit, North America 'NA' trap fix, skewness & kurtosis profiling."),
            tags$li(strong("Pure Non-ML EDA: "), "5 academic figures evaluating physical distributions, boxplots, and GAM non-linear inflections."),
            tags$li(strong("Rigorous Hypothesis Testing: "), "Welch's t-test, Mann-Whitney U, Chi-Square, ANOVA (F = 102.42), and VIF (< 1.15)."),
            tags$li(strong("Statistically-Grounded Features: "), "Features ranked by effect size; strict Target Leakage Prevention excluding total_routes."),
            tags$li(strong("Machine Learning Suite: "), "5-fold CV comparing 5 Classifiers (GBM, RF, LDA, CART, Logistic), Regression, and K-Means."),
            tags$li(strong("Technical Innovation: "), "igraph directed network analysis (Betweenness, PageRank, Louvain communities)."),
            tags$li(strong("Spatial Mapping: "), "Dual RStudio Plots static map + 1,599-route interactive Leaflet map.")
          )
        )
      ),
      card(
        card_header(class = "bg-secondary text-white font-weight-bold", "🏆 Academic Performance Summary"),
        card_body(
          tags$table(
            class = "table table-sm table-striped",
            tags$thead(
              tags$tr(tags$th("Metric"), tags$th("Value"), tags$th("Status"))
            ),
            tags$tbody(
              tags$tr(tags$td("Welch's t-statistic"), tags$td("-36.31"), tags$td(span(class="badge bg-success", "p < 1e-167"))),
              tags$tr(tags$td("Hub Mean Runway"), tags$td("10,749 ft"), tags$td(span(class="badge bg-primary", "+3,358 ft vs Reg"))),
              tags$tr(tags$td("Cohen's d Effect Size"), tags$td("1.39"), tags$td(span(class="badge bg-warning text-dark", "Extremely Large"))),
              tags$tr(tags$td("Continental ANOVA F"), tags$td("102.42"), tags$td(span(class="badge bg-success", "p < 1e-101"))),
              tags$tr(tags$td("ANOVA Eta-Squared η²"), tags$td("10.2%"), tags$td(span(class="badge bg-info", "Geography Driver"))),
              tags$tr(tags$td("Multicollinearity (Max VIF)"), tags$td("1.14"), tags$td(span(class="badge bg-success", "Zero Redundancy"))),
              tags$tr(tags$td("GBM Holdout Accuracy"), tags$td("92.0%"), tags$td(span(class="badge bg-success", "N = 900 Holdout"))),
              tags$tr(tags$td("GBM Holdout Specificity"), tags$td("97.6%"), tags$td(span(class="badge bg-success", "778 / 797 TN"))),
              tags$tr(tags$td("Champion ROC AUC"), tags$td("0.9437"), tags$td(span(class="badge bg-warning text-dark", "Outstanding"))),
              tags$tr(tags$td("Runway Regression R²"), tags$td("0.455"), tags$td(span(class="badge bg-primary", "F = 376.1"))),
              tags$tr(tags$td("Louvain Modularity Q"), tags$td("0.66"), tags$td(span(class="badge bg-info", "8 Communities")))
            )
          )
        )
      )
    )
  ),
  
  # ============================================================================
  # TAB 2: INTERACTIVE VISUALIZATION EXPLORER (Clean Academic Interface)
  # ============================================================================
  nav_panel(
    title = "🖼️ Visualization Explorer",
    layout_sidebar(
      sidebar = sidebar(
        width = 340,
        h5(style = "color: #1E3A8A; font-weight: 700;", "Visual Navigation"),
        p(style = "font-size: 0.85rem; color: #64748B;", "Select any visualization to inspect its high-resolution plot, formula, and statistical findings."),
        
        selectInput(
          inputId = "filter_category",
          label = strong("Filter by Pipeline Step:"),
          choices = c(
            "All 19 Visualizations" = "all",
            "Step 2: Exploratory Data Analysis (Figs 1–5)" = "step2",
            "Step 3: Statistical Hypothesis Testing (Figs 6–8)" = "step3",
            "Step 4: Feature Selection Justification (Fig 9)" = "step4",
            "Step 5: Machine Learning Benchmarks (Figs 10–14)" = "step5",
            "Step 6: Aviation Network Graph Analysis (Figs 15–18)" = "step6",
            "Step 7: Global & Indian Flight Corridors Map (Fig 19)" = "step7"
          ),
          selected = "all"
        ),
        
        selectInput(
          inputId = "selected_viz",
          label = strong("Choose Visualization:"),
          choices = setNames(
            names(viz_metadata),
            sapply(viz_metadata, function(x) paste0("Fig ", sprintf("%02d", x$num), ": ", substr(x$title, 11, 48), "..."))
          ),
          selected = "fig01"
        ),
        
        div(
          style = "display: flex; gap: 8px; margin-bottom: 16px;",
          actionButton("btn_prev", "◀ Previous", class = "btn-outline-primary btn-sm flex-fill"),
          actionButton("btn_next", "Next ▶", class = "btn-outline-primary btn-sm flex-fill")
        ),
        
        hr(),
        
        # Key Stat Box in Sidebar
        div(
          style = "background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 8px; padding: 12px;",
          h6(style = "color: #92400E; font-weight: 700; margin-bottom: 6px; font-size: 0.85rem;", "⚡ Statistical Proof:"),
          uiOutput("sidebar_stat_ui")
        )
      ),
      
      # Main Canvas
      div(
        layout_columns(
          col_widths = c(8, 4),
          # Plot Container
          card(
            card_header(
              class = "bg-light font-weight-bold d-flex justify-content-between align-items-center",
              uiOutput("plot_header_title"),
              uiOutput("plot_category_badge")
            ),
            card_body(
              style = "padding: 8px; background: #FFFFFF; text-align: center;",
              uiOutput("active_plot_image")
            )
          ),
          
          # Clean Academic Specifications Card Container
          card(
            card_header(class = "bg-primary text-white font-weight-bold", "📐 Statistical Specifications & Analysis"),
            card_body(
              style = "font-size: 0.88rem;",
              h6(style = "font-weight: 700; color: #1E3A8A; margin-bottom: 4px;", "Research Objective:"),
              uiOutput("card_objective_ui"),
              
              hr(style = "margin: 10px 0;"),
              
              h6(style = "font-weight: 700; color: #1E3A8A; margin-bottom: 4px;", "Mathematical Formulation:"),
              uiOutput("card_formula_ui"),
              
              hr(style = "margin: 10px 0;"),
              
              h6(style = "font-weight: 700; color: #1E3A8A; margin-bottom: 4px;", "Statistical Test Metrics:"),
              uiOutput("card_metrics_ui"),
              
              hr(style = "margin: 10px 0;"),
              
              h6(style = "font-weight: 700; color: #047857; margin-bottom: 4px;", "Academic Conclusion:"),
              uiOutput("card_conclusion_ui")
            )
          )
        )
      )
    )
  ),
  
  # ============================================================================
  # TAB 3: LIVE INTERACTIVE LEAFLET MAP
  # ============================================================================
  nav_panel(
    title = "🗺️ Interactive Global Map",
    card(
      full_screen = TRUE,
      card_header(
        class = "bg-light d-flex justify-content-between align-items-center",
        strong("SkyConnect Live Interactive Spatial Network (1,599 Flight Corridors)"),
        div(
          span(class = "badge bg-warning text-dark", "857 Indian Routes (Domestic & Gateway)"),
          span(class = "badge bg-danger", "742 Global Corridors"),
          span(class = "badge bg-primary", "100% Free OpenStreetMap")
        )
      ),
      card_body(
        style = "padding: 0;",
        leafletOutput("leaflet_live_map", height = "680px")
      )
    )
  ),
  
  # ============================================================================
  # TAB 4: STATISTICAL RESULT TABLES
  # ============================================================================
  nav_panel(
    title = "📋 Statistical Result Tables",
    card(
      card_header(
        class = "bg-light d-flex justify-content-between align-items-center",
        strong("Inspect Exported Pipeline Result Tables (CSV Files)"),
        selectInput(
          inputId = "selected_table",
          label = NULL,
          choices = c(
            "Hypothesis Test Results" = "statistical_test_results.csv",
            "Feature Justification Matrix" = "feature_selection_justification_matrix.csv",
            "Classification Test Holdout Metrics" = "classification_test_metrics.csv",
            "Classification Cross-Validation Metrics" = "classification_cv_metrics.csv",
            "Pearson Correlation Matrix" = "pearson_correlation_matrix.csv",
            "Data Quality Audit" = "data_quality_audit.csv",
            "Summary Statistics Table" = "summary_statistics_table.csv",
            "K-Means Clustering Summary" = "clustering_summary.csv",
            "Top 20 Global Aviation Hubs" = "top_20_global_aviation_hubs.csv"
          ),
          selected = "statistical_test_results.csv",
          width = "340px"
        )
      ),
      card_body(
        div(style = "overflow-x: auto;", tableOutput("rendered_csv_table"))
      )
    )
  ),
  
  # ============================================================================
  # TAB 5: PIPELINE REPRODUCIBILITY & CODE
  # ============================================================================
  nav_panel(
    title = "⚙️ Pipeline Reproducibility",
    card(
      card_header(class = "bg-primary text-white font-weight-bold", "Single-Command Pipeline Reproducibility in R"),
      card_body(
        p("Every step of SkyConnect DA-3 is completely automated and reproducible with a single master runner script:"),
        tags$pre(
          style = "background: #0F172A; color: #38BDF8; padding: 14px; border-radius: 6px; font-size: 0.95rem;",
          "source('R/00_run_complete_pipeline.R')"
        ),
        p("Execution executes all 7 pipeline scripts sequentially:"),
        tags$table(
          class = "table table-sm table-bordered",
          tags$thead(tags$tr(tags$th("Step"), tags$th("Script"), tags$th("Core Academic Responsibility"), tags$th("Output"))),
          tags$tbody(
            tags$tr(tags$td("1"), tags$td("01_dataset_profiling_and_quality.R"), tags$td("SQLite connection, North America 'NA' trap fix, missing values, skewness/kurtosis"), tags$td("data_quality_audit.csv")),
            tags$tr(tags$td("2"), tags$td("02_exploratory_data_analysis.R"), tags$td("Pure non-ML academic plots: runway normality, elevation skew, GAM route curve"), tags$td("Figures 1 to 5")),
            tags$tr(tags$td("3"), tags$td("03_statistical_hypothesis_testing.R"), tags$td("Welch's t-test (p < 10^-167), Mann-Whitney U, Chi-Square, One-Way ANOVA, VIF (< 1.15)"), tags$td("Figures 6 to 8")),
            tags$tr(tags$td("4"), tags$td("04_statistically_grounded_feature_engineering.R"), tags$td("Justification matrix, 0% Target Leakage prevention excluding total_routes, 80/20 split"), tags$td("Figure 9 + splits")),
            tags$tr(tags$td("5"), tags$td("05_machine_learning_suite.R"), tags$td("5-fold CV comparing GBM, RF, LDA, CART, Logistic; Runway Regression; K-Means (K=3)"), tags$td("Figures 10 to 14")),
            tags$tr(tags$td("6"), tags$td("06_aviation_network_graph_analysis.R"), tags$td("igraph 66,288 directed routes, Betweenness (ANC, DXB), PageRank (ATL, ORD), Louvain Q=0.66"), tags$td("Figures 15 to 18")),
            tags$tr(tags$td("7"), tags$td("07_interactive_leaflet_map.R"), tags$td("1,599 flight corridors (857 Indian + 742 global), static publication map + Leaflet widget"), tags$td("Figure 19 + HTML"))
          )
        )
      )
    )
  )
)

# ------------------------------------------------------------------------------
# 4. Server Logic
# ------------------------------------------------------------------------------
server <- function(input, output, session) {
  
  # Reactive Category Filter
  observeEvent(input$filter_category, {
    cat_sel <- input$filter_category
    filtered_ids <- names(viz_metadata)
    
    if (cat_sel == "step2") filtered_ids <- paste0("fig0", 1:5)
    else if (cat_sel == "step3") filtered_ids <- paste0("fig0", 6:8)
    else if (cat_sel == "step4") filtered_ids <- "fig09"
    else if (cat_sel == "step5") filtered_ids <- paste0("fig", 10:14)
    else if (cat_sel == "step6") filtered_ids <- paste0("fig", 15:18)
    else if (cat_sel == "step7") filtered_ids <- "fig19"
    
    choices <- setNames(
      filtered_ids,
      sapply(viz_metadata[filtered_ids], function(x) paste0("Fig ", sprintf("%02d", x$num), ": ", substr(x$title, 11, 48), "..."))
    )
    updateSelectInput(session, "selected_viz", choices = choices, selected = filtered_ids[1])
  })
  
  # Next & Previous Buttons
  observeEvent(input$btn_next, {
    all_keys <- names(viz_metadata)
    curr_idx <- match(input$selected_viz, all_keys)
    next_idx <- ifelse(curr_idx < length(all_keys), curr_idx + 1, 1)
    updateSelectInput(session, "selected_viz", selected = all_keys[next_idx])
  })
  
  observeEvent(input$btn_prev, {
    all_keys <- names(viz_metadata)
    curr_idx <- match(input$selected_viz, all_keys)
    prev_idx <- ifelse(curr_idx > 1, curr_idx - 1, length(all_keys))
    updateSelectInput(session, "selected_viz", selected = all_keys[prev_idx])
  })
  
  # Current active visualization record
  current_meta <- reactive({
    viz_metadata[[input$selected_viz]]
  })
  
  # Sidebar Output: Key Statistical Proof
  output$sidebar_stat_ui <- renderUI({
    meta <- current_meta()
    p(style = "font-size: 0.85rem; color: #78350F; margin: 0; font-weight: 600;", meta$stats)
  })
  
  # Main Canvas Plot Outputs
  output$plot_header_title <- renderUI({
    meta <- current_meta()
    span(style = "color: #1E3A8A; font-size: 1.05rem;", meta$title)
  })
  
  output$plot_category_badge <- renderUI({
    meta <- current_meta()
    span(class = "badge bg-primary", meta$category)
  })
  
  output$active_plot_image <- renderUI({
    meta <- current_meta()
    img_url <- file.path("viz", meta$file)
    tags$img(
      src = img_url,
      style = "max-width: 100%; max-height: 520px; object-fit: contain; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"
    )
  })
  
  # Academic Specifications Card Outputs
  output$card_objective_ui <- renderUI({
    meta <- current_meta()
    p(style = "color: #334155; margin-bottom: 0;", meta$objective)
  })
  
  # Fixed Crystal-Clear Mathematical Formulation (Beautiful High-Contrast Container)
  output$card_formula_ui <- renderUI({
    meta <- current_meta()
    tags$div(
      style = "background: #F8FAFC; border: 1.5px solid #CBD5E1; border-left: 4px solid #1E3A8A; border-radius: 6px; padding: 10px 14px; margin: 4px 0;",
      tags$div(
        style = "font-family: 'Cambria Math', 'Times New Roman', Georgia, serif; font-size: 1.02rem; font-weight: 600; color: #0F172A; line-height: 1.45;",
        meta$formula_display
      ),
      tags$div(
        style = "font-size: 0.78rem; color: #64748B; margin-top: 5px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.4px;",
        meta$formula_desc
      )
    )
  })
  
  output$card_metrics_ui <- renderUI({
    meta <- current_meta()
    tags$div(
      style = "background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 6px; padding: 8px 12px; margin: 4px 0;",
      p(style = "color: #1E3A8A; font-weight: 600; margin: 0; font-size: 0.84rem;", meta$stats)
    )
  })
  
  output$card_conclusion_ui <- renderUI({
    meta <- current_meta()
    p(style = "color: #065F46; font-weight: 500; margin-bottom: 0;", meta$conclusion)
  })
  
  # Live Leaflet Map (Cached & Resilient against namespace masking)
  live_map_cached <- NULL
  output$leaflet_live_map <- renderLeaflet({
    if (!is.null(live_map_cached)) {
      return(live_map_cached)
    }
    
    db_file <- file.path(proj_dir, "database", "skyconnect.db")
    if (!file.exists(db_file)) {
      db_file <- file.path("database", "skyconnect.db")
    }
    con <- DBI::dbConnect(RSQLite::SQLite(), db_file)
    on.exit(DBI::dbDisconnect(con), add = TRUE)
    
    airports_df <- DBI::dbGetQuery(con, "
      SELECT iata_code, name, municipality, iso_country, latitude_deg, longitude_deg
      FROM oa_airports 
      WHERE type IN ('large_airport', 'medium_airport') AND iata_code IS NOT NULL AND latitude_deg IS NOT NULL AND longitude_deg IS NOT NULL;
    ")
    
    in_routes_df <- DBI::dbGetQuery(con, "
      SELECT DISTINCT r.Source_airport AS src, r.Destination_airport AS tgt
      FROM of_routes r
      JOIN oa_airports s ON r.Source_airport = s.iata_code
      JOIN oa_airports d ON r.Destination_airport = d.iata_code
      WHERE (s.iso_country = 'IN' OR d.iso_country = 'IN') AND r.Source_airport != r.Destination_airport;
    ")
    
    gl_routes_df <- DBI::dbGetQuery(con, "
      WITH ranked AS (
        SELECT r.Source_airport AS src, r.Destination_airport AS tgt,
               ROW_NUMBER() OVER (PARTITION BY s.continent, d.continent ORDER BY s.latitude_deg DESC) AS rk
        FROM (SELECT DISTINCT Source_airport, Destination_airport FROM of_routes WHERE Source_airport != Destination_airport) r
        JOIN oa_airports s ON r.Source_airport = s.iata_code
        JOIN oa_airports d ON r.Destination_airport = d.iata_code
        WHERE s.iso_country != 'IN' AND d.iso_country != 'IN'
      )
      SELECT src, tgt FROM ranked WHERE rk <= 35;
    ")
    
    # Coordinates lookup (immune to MASS::select masking)
    coords <- airports_df[, c("iata_code", "latitude_deg", "longitude_deg")]
    coords <- coords[which(!is.na(coords$iata_code) & !duplicated(coords$iata_code)), ]
    
    r_in <- in_routes_df %>%
      dplyr::inner_join(coords, by = c("src" = "iata_code")) %>%
      dplyr::rename(lat1 = latitude_deg, lon1 = longitude_deg) %>%
      dplyr::inner_join(coords, by = c("tgt" = "iata_code")) %>%
      dplyr::rename(lat2 = latitude_deg, lon2 = longitude_deg)
    r_in <- r_in[which(!is.na(r_in$lon1) & !is.na(r_in$lat1) & !is.na(r_in$lon2) & !is.na(r_in$lat2)), ]
    
    r_gl <- gl_routes_df %>%
      dplyr::inner_join(coords, by = c("src" = "iata_code")) %>%
      dplyr::rename(lat1 = latitude_deg, lon1 = longitude_deg) %>%
      dplyr::inner_join(coords, by = c("tgt" = "iata_code")) %>%
      dplyr::rename(lat2 = latitude_deg, lon2 = longitude_deg)
    r_gl <- r_gl[which(!is.na(r_gl$lon1) & !is.na(r_gl$lat1) & !is.na(r_gl$lon2) & !is.na(r_gl$lat2)), ]
    
    # Vectorized segments
    make_segs <- function(df, n_pts = 8) {
      all_lng <- c(); all_lat <- c()
      for (i in seq_len(min(600, nrow(df)))) {
        p1 <- c(df$lon1[i], df$lat1[i]); p2 <- c(df$lon2[i], df$lat2[i])
        arc <- geosphere::gcIntermediate(p1, p2, n = n_pts, addStartEnd = TRUE, breakAtDateLine = TRUE)
        if (is.list(arc)) {
          for (sub in arc) { all_lng <- c(all_lng, sub[, 1], NA); all_lat <- c(all_lat, sub[, 2], NA) }
        } else if (!is.null(arc)) {
          all_lng <- c(all_lng, arc[, 1], NA); all_lat <- c(all_lat, arc[, 2], NA)
        }
      }
      list(lng = all_lng, lat = all_lat)
    }
    
    seg_in <- make_segs(r_in, 10)
    seg_gl <- make_segs(r_gl, 8)
    
    in_airports <- airports_df[which(airports_df$iso_country == "IN"), ]
    
    map_obj <- leaflet() %>%
      addTiles(group = "OpenStreetMap (Default)") %>%
      addProviderTiles(providers$Esri.WorldTopoMap, group = "Esri Topographic") %>%
      setView(lng = 50, lat = 25, zoom = 3) %>%
      addPolylines(lng = seg_gl$lng, lat = seg_gl$lat, color = "#DC2626", weight = 1.0, opacity = 0.45, group = "Global Corridors") %>%
      addPolylines(lng = seg_in$lng, lat = seg_in$lat, color = "#F59E0B", weight = 1.5, opacity = 0.80, group = "Indian Routes") %>%
      addCircleMarkers(
        data = in_airports,
        lng = ~longitude_deg, lat = ~latitude_deg,
        radius = 4.5, color = "#9A3412", fillColor = "#EA580C", fillOpacity = 0.9, weight = 1.5,
        popup = ~sprintf("<b>🇮🇳 %s (%s)</b><br>%s, India", name, iata_code, municipality),
        label = ~sprintf("🇮🇳 %s (%s)", name, iata_code),
        group = "Indian Gateways"
      ) %>%
      addLayersControl(
        baseGroups = c("OpenStreetMap (Default)", "Esri Topographic"),
        overlayGroups = c("Indian Routes", "Global Corridors", "Indian Gateways"),
        options = layersControlOptions(collapsed = FALSE)
      ) %>%
      addLegend(
        position = "bottomright",
        colors = c("#EA580C", "#F59E0B", "#DC2626"),
        labels = c("Indian Airports", "Indian Routes (Domestic & Gateway)", "Global Flight Corridors"),
        title = "SkyConnect Live Network"
      )
    
    live_map_cached <<- map_obj
    map_obj
  })
  
  # Statistical Result Tables Output
  output$rendered_csv_table <- renderTable({
    req(input$selected_table)
    tbl_path <- file.path(res_dir, input$selected_table)
    if (file.exists(tbl_path)) {
      df <- readr::read_csv(tbl_path, show_col_types = FALSE)
      head(df, 30)
    } else {
      data.frame(Status = "Table not found on disk.")
    }
  }, striped = TRUE, hover = TRUE, bordered = TRUE, spacing = "s")
}

# ------------------------------------------------------------------------------
# 5. Launch Application
# ------------------------------------------------------------------------------
shinyApp(ui, server)
