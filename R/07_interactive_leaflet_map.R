# ==============================================================================
# SkyConnect DA-3: Step 7 - Global Flight Routes & International Hub Map
# Dual Output:
#   1. RStudio Plots Pane: Publication-grade static ggplot2 map with flight arcs
#   2. RStudio Viewer Pane & HTML: Interactive Leaflet map (100% API-key free)
# Course: Data Analytics using R | Authors: Chirag Asija & Saanvi Gupta
# Faculty Guide: Mrs. Vijayalakshmi
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Load Required Libraries & Set Pandoc
# ------------------------------------------------------------------------------
if (file.exists("/Applications/RStudio.app/Contents/Resources/app/quarto/bin/tools/aarch64/pandoc")) {
  Sys.setenv(RSTUDIO_PANDOC = "/Applications/RStudio.app/Contents/Resources/app/quarto/bin/tools/aarch64")
  Sys.setenv(PATH = paste("/Applications/RStudio.app/Contents/Resources/app/quarto/bin/tools/aarch64", Sys.getenv("PATH"), sep = ":"))
}

suppressPackageStartupMessages({
  library(DBI)
  library(RSQLite)
  library(dplyr)
  library(readr)
  library(ggplot2)
  library(maps)
  library(leaflet)
  library(htmlwidgets)
  library(geosphere)
  library(scales)
})

cat("===============================================================================\n")
cat("      SkyConnect DA-3: Step 7 - Global Flight Routes & International Map       \n")
cat("===============================================================================\n\n")

# ------------------------------------------------------------------------------
# 2. Paths Setup (Dynamic Directory Detection)
# ------------------------------------------------------------------------------
if (dir.exists("database")) {
  project_dir <- "."
} else if (dir.exists("../database")) {
  project_dir <- ".."
} else if (dir.exists("/Users/chiragasija/Downloads/SkyConnect_DA3 2/database")) {
  project_dir <- "/Users/chiragasija/Downloads/SkyConnect_DA3 2"
} else {
  project_dir <- "/Users/chiragasija/Downloads/SkyConnect_DA3"
}

db_path <- file.path(project_dir, "database", "skyconnect.db")
viz_dir <- file.path(project_dir, "visualizations")

dir.create(viz_dir, recursive = TRUE, showWarnings = FALSE)

# ------------------------------------------------------------------------------
# 3. Ingest Airport Data & Comprehensive Worldwide Route Network from SQLite
# ------------------------------------------------------------------------------
cat("Step 7.1: Extracting airport coordinates and comprehensive route network from SQLite...\n")

con <- dbConnect(RSQLite::SQLite(), db_path)

# 3.1 Extract Airports with Full Physical Infrastructure & Route Counts
airports_sql <- "
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
  a.iata_code,
  a.name AS airport_name,
  a.municipality AS city,
  COALESCE(a.iso_country, '') AS country,
  CASE WHEN a.continent IS NULL OR a.continent = '' THEN 'NA' ELSE a.continent END AS continent,
  a.type AS airport_type,
  a.latitude_deg AS latitude,
  a.longitude_deg AS longitude,
  a.elevation_ft,
  COALESCE(rs.num_runways, 1) AS num_runways,
  COALESCE(rs.max_runway_length, 0) AS max_runway_length,
  COALESCE(rs.has_paved_runway, 1) AS has_paved_runway,
  COALESCE(rc.total_routes, 0) AS total_routes
FROM oa_airports a
LEFT JOIN runway_stats rs ON a.ident = rs.airport_ident
LEFT JOIN route_counts rc ON a.iata_code = rc.airport_iata
WHERE a.type IN ('large_airport', 'medium_airport')
  AND a.iata_code IS NOT NULL AND a.iata_code != ''
  AND a.latitude_deg IS NOT NULL AND a.longitude_deg IS NOT NULL;
"
airports_map <- dbGetQuery(con, airports_sql)

# 3.2 Extract Indian Routes (Complete Domestic Trunk Network + International Connections)
in_routes_sql <- "
SELECT DISTINCT 
  r.Source_airport AS source,
  r.Destination_airport AS target,
  'India' AS network_type
FROM of_routes r
JOIN oa_airports s ON r.Source_airport = s.iata_code
JOIN oa_airports d ON r.Destination_airport = d.iata_code
WHERE (s.iso_country = 'IN' OR d.iso_country = 'IN')
  AND s.latitude_deg IS NOT NULL AND d.latitude_deg IS NOT NULL
  AND r.Source_airport != r.Destination_airport;
"
in_routes_raw <- dbGetQuery(con, in_routes_sql)

# 3.3 Extract Global Balanced Corridors (Stratified across All Continent Pairs)
# This guarantees every continent (NA, SA, EU, AF, AS, OC) has realistic intercontinental & trunk routes
global_routes_sql <- "
WITH airport_vol AS (
  SELECT airport_iata, COUNT(*) AS vol FROM (
    SELECT Source_airport AS airport_iata FROM of_routes
    UNION ALL
    SELECT Destination_airport AS airport_iata FROM of_routes
  ) GROUP BY airport_iata
),
continent_clean AS (
  SELECT 
    r.Source_airport AS source,
    r.Destination_airport AS target,
    CASE WHEN s.continent IS NULL OR s.continent = '' THEN 'NA' ELSE s.continent END AS s_cont,
    CASE WHEN d.continent IS NULL OR d.continent = '' THEN 'NA' ELSE d.continent END AS d_cont,
    s.iso_country AS s_country,
    d.iso_country AS d_country,
    (COALESCE(vs.vol, 0) + COALESCE(vd.vol, 0)) AS importance
  FROM (
    SELECT DISTINCT Source_airport, Destination_airport FROM of_routes
    WHERE Source_airport IS NOT NULL AND Destination_airport IS NOT NULL
      AND Source_airport != Destination_airport
  ) r
  JOIN oa_airports s ON r.Source_airport = s.iata_code
  JOIN oa_airports d ON r.Destination_airport = d.iata_code
  LEFT JOIN airport_vol vs ON s.iata_code = vs.airport_iata
  LEFT JOIN airport_vol vd ON d.iata_code = vd.airport_iata
  WHERE s.type IN ('large_airport', 'medium_airport')
    AND d.type IN ('large_airport', 'medium_airport')
    AND s.latitude_deg IS NOT NULL AND d.latitude_deg IS NOT NULL
),
ranked AS (
  SELECT 
    source, target, importance, s_country, d_country,
    ROW_NUMBER() OVER (
      PARTITION BY 
        CASE WHEN s_cont < d_cont THEN s_cont || '-' || d_cont ELSE d_cont || '-' || s_cont END
      ORDER BY importance DESC
    ) AS rank_in_pair
  FROM continent_clean
  WHERE s_country != 'IN' AND d_country != 'IN'
)
SELECT source, target, 'Global' AS network_type
FROM ranked
WHERE rank_in_pair <= 45
ORDER BY importance DESC;
"
global_routes_raw <- dbGetQuery(con, global_routes_sql)
dbDisconnect(con)

# Fix continent coding and compute proportional display radii
airports_map <- airports_map %>%
  filter(!is.na(latitude) & !is.na(longitude)) %>%
  mutate(
    Hub_Status = ifelse(total_routes > 50, "Major International Hub", "Regional / Domestic Airport"),
    Is_India = (country == "IN"),
    # Clean proportional radius (subtle, non-overlapping)
    radius_leaflet = case_when(
      country == "IN" & total_routes > 50 ~ pmin(12, 4.5 + sqrt(total_routes) * 0.25),
      country == "IN" ~ 3.5,
      total_routes > 50 ~ pmin(11, 3.5 + sqrt(total_routes) * 0.22),
      TRUE ~ 2.0
    )
  )

cat(sprintf("Prepared %s airports worldwide (including %d commercial airports in India).\n", 
            comma(nrow(airports_map)), sum(airports_map$country == "IN", na.rm = TRUE)))

# Coordinate lookup
coords_lookup <- airports_map %>%
  dplyr::select(iata_code, latitude, longitude) %>%
  distinct(iata_code, .keep_all = TRUE)

# 3.4 Match Geographic Coordinates for Indian Routes
routes_in_geo <- in_routes_raw %>%
  inner_join(coords_lookup, by = c("source" = "iata_code")) %>%
  rename(lat_src = latitude, lon_src = longitude) %>%
  inner_join(coords_lookup, by = c("target" = "iata_code")) %>%
  rename(lat_tgt = latitude, lon_tgt = longitude)

# 3.5 Match Geographic Coordinates for Global Corridors
routes_gl_geo <- global_routes_raw %>%
  inner_join(coords_lookup, by = c("source" = "iata_code")) %>%
  rename(lat_src = latitude, lon_src = longitude) %>%
  inner_join(coords_lookup, by = c("target" = "iata_code")) %>%
  rename(lat_tgt = latitude, lon_tgt = longitude)

cat(sprintf("Matched %d Indian routes (Domestic & International gateways).\n", nrow(routes_in_geo)))
cat(sprintf("Matched %d Global intercontinental corridors across all continents.\n", nrow(routes_gl_geo)))
cat(sprintf("Total route arcs to display: %d.\n\n", nrow(routes_in_geo) + nrow(routes_gl_geo)))

# ==============================================================================
# PART A: RSTUDIO PLOTS PANE GRAPHIC (Standard ggplot2 Academic World Map)
# This renders directly in the RStudio 'Plots' Pane!
# ==============================================================================
cat("Step 7.2: Rendering publication world map for RStudio Plots Pane...\n")

world_map <- map_data("world")

p_rstudio <- ggplot() +
  # World Landmasses
  geom_polygon(data = world_map, aes(x = long, y = lat, group = group),
               fill = "#F8FAFC", color = "#CBD5E1", linewidth = 0.35) +
  
  # Global Intercontinental Corridors (Crimson Red)
  geom_curve(data = routes_gl_geo, 
             aes(x = lon_src, y = lat_src, xend = lon_tgt, yend = lat_tgt),
             curvature = 0.12, color = "#DC2626", alpha = 0.20, linewidth = 0.28) +
  
  # Indian Domestic & Gateway Routes (Vibrant Amber/Gold)
  geom_curve(data = routes_in_geo, 
             aes(x = lon_src, y = lat_src, xend = lon_tgt, yend = lat_tgt),
             curvature = 0.15, color = "#D97706", alpha = 0.40, linewidth = 0.38) +
  
  # Regular Global Airports (Soft Blue Points)
  geom_point(data = airports_map %>% filter(total_routes <= 50 & country != "IN"),
             aes(x = longitude, y = latitude), color = "#93C5FD", alpha = 0.25, size = 0.45) +
  
  # Major Global Hubs (Deep Blue Points, Size Proportional to Routes)
  geom_point(data = airports_map %>% filter(total_routes > 50 & country != "IN"),
             aes(x = longitude, y = latitude, size = total_routes),
             color = "#1D4ED8", alpha = 0.55) +
  
  # Indian Airports & Gateways (Distinct Warm Amber Points, Prominently Visible)
  geom_point(data = airports_map %>% filter(country == "IN"),
             aes(x = longitude, y = latitude, size = total_routes),
             color = "#EA580C", alpha = 0.85) +
  
  # Clean Scales & Controls
  scale_size_continuous(range = c(0.8, 4.5), breaks = c(50, 200, 500, 1000, 1800), name = "Route Capacity:") +
  coord_fixed(1.3, xlim = c(-170, 180), ylim = c(-60, 80)) +
  labs(
    title = "Figure 19: Comprehensive Global Flight Network & International Hub Connectivity Map",
    subtitle = "Red: Global Intercontinental Corridors | Orange: Indian Domestic & Gateway Routes | Blue/Orange Hubs",
    x = "Longitude", y = "Latitude",
    caption = "Source: OpenFlights Global Network Graph (67,663 routes) | Rendered for RStudio Plots Pane"
  ) +
  theme_bw(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = rel(1.1), hjust = 0, color = "#111827", margin = ggplot2::margin(b = 6)),
    plot.subtitle = element_text(size = rel(0.92), color = "#4B5563", margin = ggplot2::margin(b = 10)),
    axis.title = element_text(face = "bold", color = "#1F2937"),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(color = "#F1F5F9", linewidth = 0.4),
    panel.border = element_rect(color = "#9CA3AF", fill = NA, linewidth = 0.8),
    legend.position = "bottom"
  )

# Save high-res PNG for reports/slides
output_png <- file.path(viz_dir, "19_global_flight_routes_map.png")
ggsave(output_png, plot = p_rstudio, width = 11, height = 6.2, dpi = 300)

# Display in RStudio Plots Pane if running interactively
if (interactive() || Sys.getenv("RSTUDIO") == "1") {
  print(p_rstudio)
}
cat("  -> Static map drawn and saved to visualizations/19_global_flight_routes_map.png\n\n")

# ==============================================================================
# PART B: INTERACTIVE LEAFLET MAP (100% Free OpenStreetMap Tiles, NO API Key)
# This renders directly in the RStudio 'Viewer' Pane and as a standalone HTML!
# ==============================================================================
cat("Step 7.3: Building 100% API-key-free Interactive Leaflet Map...\n")

# Build rich HTML popups for each airport
airports_map <- airports_map %>%
  mutate(
    popup_content = sprintf("
      <div style='font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; min-width: 230px; padding: 4px;'>
        <div style='border-bottom: 2px solid %s; padding-bottom: 4px; margin-bottom: 6px;'>
          <h4 style='margin: 0; color: #1E3A8A; font-size: 14px;'>%s (%s) %s</h4>
          <span style='font-size: 11px; color: #6B7280;'>%s, %s | Continent: %s</span>
        </div>
        <table style='width: 100%%; font-size: 11px; border-collapse: collapse;'>
          <tr style='border-bottom: 1px solid #F3F4F6;'>
            <td style='padding: 3px 0; color: #6B7280;'>Total Route Connections:</td>
            <td style='padding: 3px 0; font-weight: bold; text-align: right; color: %s;'>%s routes</td>
          </tr>
          <tr style='border-bottom: 1px solid #F3F4F6;'>
            <td style='padding: 3px 0; color: #6B7280;'>Max Runway Length:</td>
            <td style='padding: 3px 0; font-weight: bold; text-align: right;'>%s ft</td>
          </tr>
          <tr style='border-bottom: 1px solid #F3F4F6;'>
            <td style='padding: 3px 0; color: #6B7280;'>Airport Elevation:</td>
            <td style='padding: 3px 0; text-align: right;'>%s ft</td>
          </tr>
          <tr style='border-bottom: 1px solid #F3F4F6;'>
            <td style='padding: 3px 0; color: #6B7280;'>Number of Runways:</td>
            <td style='padding: 3px 0; text-align: right;'>%d</td>
          </tr>
          <tr>
            <td style='padding: 4px 0; color: #6B7280;'>Hub Status:</td>
            <td style='padding: 4px 0; font-weight: bold; text-align: right; color: %s;'>%s</td>
          </tr>
        </table>
      </div>
    ",
    ifelse(country == "IN", "#EA580C", "#1D4ED8"),
    airport_name, iata_code, ifelse(country == "IN", "🇮🇳", ""),
    city, country, continent,
    ifelse(country == "IN", "#EA580C", "#1D4ED8"),
    comma(total_routes),
    comma(max_runway_length),
    comma(elevation_ft),
    num_runways,
    ifelse(total_routes > 50, "#DC2626", "#2563EB"),
    Hub_Status
    )
  )

# Precalculate Great Circle arc points with vectorized NA delimiters
# This renders hundreds of routes in milliseconds without UI lag!
cat("  Calculating Great Circle geodesic route segments...\n")

build_arc_segments <- function(df, n_points = 10) {
  all_lng <- c()
  all_lat <- c()
  for (i in seq_len(nrow(df))) {
    p1 <- c(df$lon_src[i], df$lat_src[i])
    p2 <- c(df$lon_tgt[i], df$lat_tgt[i])
    arc <- gcIntermediate(p1, p2, n = n_points, addStartEnd = TRUE, breakAtDateLine = TRUE)
    if (is.list(arc)) {
      for (sub in arc) {
        all_lng <- c(all_lng, sub[, 1], NA)
        all_lat <- c(all_lat, sub[, 2], NA)
      }
    } else if (!is.null(arc)) {
      all_lng <- c(all_lng, arc[, 1], NA)
      all_lat <- c(all_lat, arc[, 2], NA)
    }
  }
  list(lng = all_lng, lat = all_lat)
}

arcs_indian <- build_arc_segments(routes_in_geo, n_points = 12)
arcs_global <- build_arc_segments(routes_gl_geo, n_points = 10)

# Assemble Leaflet Map using OpenStreetMap & Esri (Zero Watermarks, No API Key Required)
m_leaflet <- leaflet() %>%
  # 1. Standard OpenStreetMap (Default - completely open, no API key, matches class example)
  addTiles(group = "OpenStreetMap (Default)") %>%
  
  # 2. Esri Clean Topographic Map (Alternative free tile, crisp cartography)
  addProviderTiles(providers$Esri.WorldTopoMap, group = "Esri Topographic (Clean)") %>%
  
  # Set global center showing Europe, Middle East, and Asia (centered on India)
  setView(lng = 50, lat = 25, zoom = 3) %>%
  
  # Layer 1: Global Intercontinental Corridors (Crimson Red Arcs)
  addPolylines(
    lng = arcs_global$lng, lat = arcs_global$lat,
    weight = 1.1, color = "#DC2626", opacity = 0.40,
    group = "Global Flight Corridors"
  ) %>%
  
  # Layer 2: Indian Routes - Domestic & International Gateways (Vibrant Amber Arcs)
  addPolylines(
    lng = arcs_indian$lng, lat = arcs_indian$lat,
    weight = 1.6, color = "#F59E0B", opacity = 0.80,
    group = "Indian Routes (Domestic & Gateway)"
  ) %>%
  
  # Layer 3: Regular Global Airports (Subtle, clean blue dots)
  addCircleMarkers(
    data = airports_map %>% filter(total_routes <= 50 & country != "IN"),
    lng = ~longitude, lat = ~latitude,
    radius = ~radius_leaflet,
    color = "#3B82F6", weight = 0.8, opacity = 0.5,
    fillColor = "#60A5FA", fillOpacity = 0.40,
    popup = ~popup_content,
    label = ~sprintf("%s (%s): %s routes", airport_name, iata_code, comma(total_routes)),
    group = "Regional Facilities (<= 50 routes)"
  ) %>%
  
  # Layer 4: Major Global Hubs (Proportional circles, deep blue, prominent)
  addCircleMarkers(
    data = airports_map %>% filter(total_routes > 50 & country != "IN"),
    lng = ~longitude, lat = ~latitude,
    radius = ~radius_leaflet,
    color = "#1E3A8A", weight = 1.4, opacity = 0.85,
    fillColor = "#1D4ED8", fillOpacity = 0.65,
    popup = ~popup_content,
    label = ~sprintf("★ GLOBAL HUB: %s (%s) — %s routes", airport_name, iata_code, comma(total_routes)),
    group = "Major Global Hubs (> 50 routes)"
  ) %>%
  
  # Layer 5: Indian Airports & International Hubs (Distinct Warm Amber/Orange Markers)
  addCircleMarkers(
    data = airports_map %>% filter(country == "IN"),
    lng = ~longitude, lat = ~latitude,
    radius = ~radius_leaflet,
    color = "#9A3412", weight = 1.8, opacity = 0.95,
    fillColor = "#EA580C", fillOpacity = 0.85,
    popup = ~popup_content,
    label = ~sprintf("🇮🇳 %s (%s) — %s routes", airport_name, iata_code, comma(total_routes)),
    group = "Indian Airports & Gateways"
  ) %>%
  
  # Layer Control (Toggle any layer on/off with one click)
  addLayersControl(
    baseGroups = c("OpenStreetMap (Default)", "Esri Topographic (Clean)"),
    overlayGroups = c(
      "Indian Routes (Domestic & Gateway)",
      "Global Flight Corridors",
      "Indian Airports & Gateways",
      "Major Global Hubs (> 50 routes)",
      "Regional Facilities (<= 50 routes)"
    ),
    options = layersControlOptions(collapsed = FALSE)
  ) %>%
  
  # Hide regional facilities by default to keep map uncluttered
  hideGroup("Regional Facilities (<= 50 routes)") %>%
  
  # Academic Legend Matching Project Theme
  addLegend(
    position = "bottomright",
    colors = c("#EA580C", "#1D4ED8", "#60A5FA", "#F59E0B", "#DC2626"),
    labels = c(
      "Indian Airports & Gateways (DEL, BOM, BLR, etc.)",
      "Major Global Hubs (> 50 Routes, Proportional)",
      "Regional Facilities (<= 50 Routes)",
      "Indian Routes (Domestic & International)",
      "Global Intercontinental Corridors"
    ),
    title = "SkyConnect Global Network",
    opacity = 0.9
  )

# Save Interactive HTML Widget
output_html <- file.path(viz_dir, "19_interactive_global_aviation_map.html")
cat("  Saving standalone HTML map widget...\n")
saveWidget(m_leaflet, file = output_html, selfcontained = TRUE)

# Display in RStudio Viewer Pane if running interactively
if (interactive() || Sys.getenv("RSTUDIO") == "1") {
  print(m_leaflet)
}

cat("===============================================================================\n")
cat("SUCCESS: Both outputs generated successfully!\n")
cat(sprintf("  1. RStudio Plots Pane / PNG: %s\n", output_png))
cat(sprintf("  2. RStudio Viewer Pane / HTML: %s\n", output_html))
cat("===============================================================================\n")
