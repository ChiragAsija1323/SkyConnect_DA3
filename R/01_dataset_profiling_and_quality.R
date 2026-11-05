# ==============================================================================
# SkyConnect DA-3: Step 1 - Dataset Profiling, Quality Audit & Data Learning
# Rubric Focus: Dataset Selection & Data Quality (10 Marks)
# Course: Data Analytics using R | Authors: Chirag Asija & Saanvi Gupta
# Faculty Guide: Mrs. Vijayalakshmi
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Load Required Libraries
# ------------------------------------------------------------------------------
suppressPackageStartupMessages({
  library(DBI)
  library(RSQLite)
  library(dplyr)
  library(readr)
  library(tidyr)
})

cat("===============================================================================\n")
cat("      SkyConnect DA-3: Step 1 - Learning the Dataset & Data Quality Audit      \n")
cat("===============================================================================\n\n")

# ------------------------------------------------------------------------------
# 2. Paths Setup
# ------------------------------------------------------------------------------
project_dir <- "/Users/chiragasija/Downloads/SkyConnect_DA3"
db_path     <- file.path(project_dir, "database", "skyconnect.db")
proc_dir    <- file.path(project_dir, "data", "processed")
res_dir     <- file.path(project_dir, "results")

dir.create(proc_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(res_dir, recursive = TRUE, showWarnings = FALSE)

if (!file.exists(db_path)) {
  stop("Database not found at: ", db_path)
}

# ------------------------------------------------------------------------------
# 3. Connect to SQLite & Extract Complete Aviation Data Cohort
# ------------------------------------------------------------------------------
cat("Step 1.1: Connecting to SQLite database (skyconnect.db)...\n")
con <- dbConnect(RSQLite::SQLite(), db_path)

# Query aggregates route connectivity (both inbound and outbound) and joins
# airport physical infrastructure (runway lengths and paving) from OurAirports.
sql_query <- "
WITH route_counts AS (
  SELECT airport_iata, SUM(routes) AS total_routes
  FROM (
    SELECT Source_airport AS airport_iata, COUNT(*) AS routes 
    FROM of_routes 
    GROUP BY Source_airport
    UNION ALL
    SELECT Destination_airport AS airport_iata, COUNT(*) AS routes 
    FROM of_routes 
    GROUP BY Destination_airport
  )
  GROUP BY airport_iata
),
runway_stats AS (
  SELECT 
    airport_ident,
    COUNT(*) AS num_runways,
    MAX(length_ft) AS max_runway_length,
    MAX(CASE WHEN surface IN ('ASP', 'CON', 'ASPH', 'CONC', 'BIT', 'PVD', 'ASPHALT', 'CONCRETE') THEN 1 ELSE 0 END) AS has_paved_runway
  FROM oa_runways
  GROUP BY airport_ident
)
SELECT 
  a.ident AS airport_ident,
  a.iata_code,
  a.name AS airport_name,
  a.type AS airport_type,
  a.latitude_deg,
  a.longitude_deg,
  a.elevation_ft,
  a.continent,
  a.iso_country,
  COALESCE(rs.num_runways, 0) AS num_runways,
  COALESCE(rs.max_runway_length, 0) AS max_runway_length,
  COALESCE(rs.has_paved_runway, 0) AS has_paved_runway,
  COALESCE(rc.total_routes, 0) AS total_routes
FROM oa_airports a
LEFT JOIN runway_stats rs ON a.ident = rs.airport_ident
LEFT JOIN route_counts rc ON a.iata_code = rc.airport_iata
WHERE a.type IN ('large_airport', 'medium_airport')
  AND a.iata_code IS NOT NULL 
  AND a.iata_code != '';
"

raw_cohort <- dbGetQuery(con, sql_query)
dbDisconnect(con)

cat(sprintf("Extracted %d commercial airports from SQLite database.\n\n", nrow(raw_cohort)))

# ------------------------------------------------------------------------------
# 4. Resolve the North America 'NA' Parsing Trap
# ------------------------------------------------------------------------------
# Note: In R, the string 'NA' represents missing data. For North American
# airports, OurAirports codes the continent as 'NA'. We explicitly handle this
# so that North American airports are accurately preserved rather than dropped.
raw_cohort <- raw_cohort %>%
  mutate(
    continent = ifelse(is.na(continent) | continent == "", "NA", continent)
  )

cat("Step 1.2: North America continent code ('NA') verified and preserved.\n")
cat("Continent Breakdown:\n")
print(table(raw_cohort$continent, useNA = "always"))
cat("\n")

# Save the full extracted cohort
write_csv(raw_cohort, file.path(proc_dir, "raw_commercial_airports.csv"))

# ------------------------------------------------------------------------------
# 5. Data Quality Audit: Missing Values & Data Types
# ------------------------------------------------------------------------------
cat("Step 1.3: Conducting Comprehensive Data Quality Audit...\n")

col_names <- names(raw_cohort)
quality_audit <- data.frame(
  Variable = col_names,
  Data_Type = sapply(raw_cohort, class),
  Scale_of_Measurement = case_when(
    col_names %in% c("latitude_deg", "longitude_deg", "elevation_ft", "max_runway_length") ~ "Continuous Ratio",
    col_names %in% c("num_runways", "total_routes") ~ "Discrete Ratio",
    col_names %in% c("has_paved_runway") ~ "Binary Nominal",
    col_names %in% c("airport_type", "continent", "iso_country") ~ "Categorical Nominal",
    TRUE ~ "Identifier / Text"
  ),
  Total_Records = nrow(raw_cohort),
  Missing_Count = sapply(raw_cohort, function(x) sum(is.na(x))),
  Missing_Percentage = sapply(raw_cohort, function(x) round((sum(is.na(x)) / nrow(raw_cohort)) * 100, 2)),
  stringsAsFactors = FALSE
)

# Filter out NA elevations: Impute with global median elevation (262 ft)
elevation_median <- median(raw_cohort$elevation_ft, na.rm = TRUE)
raw_cohort$elevation_ft[is.na(raw_cohort$elevation_ft)] <- elevation_median

write_csv(quality_audit, file.path(res_dir, "data_quality_audit.csv"))
cat("Data Quality Audit Table:\n")
print(quality_audit[, c("Variable", "Data_Type", "Scale_of_Measurement", "Missing_Count", "Missing_Percentage")])
cat("\n")

# ------------------------------------------------------------------------------
# 6. Outlier Analysis & Descriptive Statistics
# ------------------------------------------------------------------------------
cat("Step 1.4: Computing Parametric & Non-Parametric Summary Statistics...\n")

# Helper function for skewness
calc_skewness <- function(x) {
  x <- x[!is.na(x)]
  n <- length(x)
  m3 <- sum((x - mean(x))^3) / n
  s3 <- (sum((x - mean(x))^2) / n)^(3/2)
  m3 / s3
}

# Helper function for kurtosis
calc_kurtosis <- function(x) {
  x <- x[!is.na(x)]
  n <- length(x)
  m4 <- sum((x - mean(x))^4) / n
  s4 <- (sum((x - mean(x))^2) / n)^2
  (m4 / s4) - 3 # Excess kurtosis
}

numeric_vars <- c("elevation_ft", "num_runways", "max_runway_length", "total_routes")

summary_stats <- lapply(numeric_vars, function(v) {
  vals <- raw_cohort[[v]]
  q1 <- quantile(vals, 0.25, na.rm = TRUE)
  q3 <- quantile(vals, 0.75, na.rm = TRUE)
  iqr_val <- q3 - q1
  lower_bound <- q1 - 1.5 * iqr_val
  upper_bound <- q3 + 1.5 * iqr_val
  outliers <- sum(vals < lower_bound | vals > upper_bound, na.rm = TRUE)
  
  data.frame(
    Variable = v,
    Mean = round(mean(vals, na.rm = TRUE), 2),
    Std_Dev = round(sd(vals, na.rm = TRUE), 2),
    Median = round(median(vals, na.rm = TRUE), 2),
    Q1 = round(q1, 2),
    Q3 = round(q3, 2),
    IQR = round(iqr_val, 2),
    Min = round(min(vals, na.rm = TRUE), 2),
    Max = round(max(vals, na.rm = TRUE), 2),
    Skewness = round(calc_skewness(vals), 2),
    Excess_Kurtosis = round(calc_kurtosis(vals), 2),
    Outlier_Count = outliers,
    Outlier_Pct = round((outliers / length(vals)) * 100, 2)
  )
}) %>% bind_rows()

write_csv(summary_stats, file.path(res_dir, "summary_statistics_table.csv"))

cat("Descriptive Statistics & Outlier Audit:\n")
print(summary_stats)
cat("\n")

cat("===============================================================================\n")
cat("SUCCESS: Step 1 Complete! Quality audit and summary statistics saved to results/ \n")
cat("===============================================================================\n")
