# ==============================================================================
# SkyConnect DA-3: Master Pipeline Execution Script
# Purpose: Execute the entire DA-3 analytical, statistical, and ML pipeline
#          sequentially with a single command for complete academic reproducibility.
# ==============================================================================

cat("\n")
cat("===============================================================================\n")
cat("          SKYCONNECT DA-3: END-TO-END DATA ANALYTICS PIPELINE IN R             \n")
cat("   A Statistically-Grounded Machine Learning Pipeline for Global Aviation      \n")
cat("   Authors: Chirag Asija (24BDS1073) & Saanvi Gupta (24BDS1023)                \n")
cat("   Faculty Guide: Mrs. Vijayalakshmi | Academic Year: 2026-2027                \n")
cat("===============================================================================\n\n")

# Handle non-interactive graphics device to prevent default Rplots.pdf creation
if (!interactive()) {
  pdf(file = NULL)
}

start_time <- Sys.time()

scripts <- c(
  "01_dataset_profiling_and_quality.R",
  "02_exploratory_data_analysis.R",
  "03_statistical_hypothesis_testing.R",
  "04_statistically_grounded_feature_engineering.R",
  "05_machine_learning_suite.R",
  "06_aviation_network_graph_analysis.R",
  "07_interactive_leaflet_map.R"
)

# Dynamic script directory detection
if (dir.exists("R")) {
  script_dir <- "R"
} else if (file.exists("01_dataset_profiling_and_quality.R")) {
  script_dir <- "."
} else if (dir.exists("/Users/chiragasija/Downloads/SkyConnect_DA3 2/R")) {
  script_dir <- "/Users/chiragasija/Downloads/SkyConnect_DA3 2/R"
} else {
  script_dir <- "/Users/chiragasija/Downloads/SkyConnect_DA3/R"
}

for (i in seq_along(scripts)) {
  s <- scripts[i]
  cat(sprintf("\n>>> [%d/%d] EXECUTING: %s ...\n\n", i, length(scripts), s))
  source(file.path(script_dir, s))
}

end_time <- Sys.time()
elapsed <- round(difftime(end_time, start_time, units = "secs"), 1)

cat("\n===============================================================================\n")
cat(sprintf("ALL 7 DA-3 PIPELINE SCRIPTS COMPLETED SUCCESSFULLY IN %.1f SECONDS!\n", elapsed))
cat("All figures saved to: visualizations/ (19 Publication Figures + Interactive HTML Map)\n")
cat("All data tables saved to: results/ and data/processed/\n")
cat("All trained model files saved to: models/ (.rds objects)\n")
cat("===============================================================================\n\n")
