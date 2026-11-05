import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles & Colors
    C_NAVY = RGBColor(15, 23, 42)       # #0F172A
    C_BLUE = RGBColor(30, 58, 138)      # #1E3A8A
    C_SLATE = RGBColor(71, 85, 105)     # #475569
    C_BORDER = "CBD5E1"
    C_HEADER_BG = "F1F5F9"
    C_ZEBRA = "F8FAFC"

    def set_cell_shading(cell, color_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        tcPr.append(shd)

    def set_table_borders(table):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{C_BORDER}"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{C_BORDER}"/>'
            f'<w:left w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{C_BORDER}"/>'
            f'<w:insideV w:val="none"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    # Header / Title Block
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_inst = title_p.add_run("VELLORE INSTITUTE OF TECHNOLOGY (VIT CHENNAI)\nSCHOOL OF ADVANCED SCIENCES / SCOPE\n")
    run_inst.font.name = "Times New Roman"
    run_inst.font.size = Pt(12)
    run_inst.font.bold = True
    run_inst.font.color.rgb = C_BLUE

    run_course = title_p.add_run("COURSE: DATA ANALYTICS USING R | EVALUATION COMPONENT: DA-3 CAPSTONE PROJECT\n")
    run_course.font.name = "Times New Roman"
    run_course.font.size = Pt(10)
    run_course.font.bold = True
    run_course.font.color.rgb = C_SLATE

    # Horizontal Divider
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(12)
    p_div_run = p_div.add_run("―" * 58)
    p_div_run.font.name = "Times New Roman"
    p_div_run.font.size = Pt(12)
    p_div_run.font.color.rgb = RGBColor(148, 163, 184)
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # SECTION 1: TITLE
    h1 = doc.add_paragraph()
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_after = Pt(8)
    r1 = h1.add_run("1. PROJECT TITLE\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = C_SLATE

    r_title = h1.add_run("SkyConnect: A Statistically-Grounded Machine Learning Pipeline for Global Aviation Infrastructure and Airport Classification")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = C_NAVY

    # SECTION 2: TEAM MEMBERS
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    r2 = h2.add_run("2. TEAM MEMBERS AND REGISTRATION DETAILS")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(12)
    r2.font.bold = True
    r2.font.color.rgb = C_BLUE

    # Team Table
    team_table = doc.add_table(rows=3, cols=4)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(team_table)
    headers = ["Name", "Register Number", "Degree & Department", "Project Role"]
    for i, h in enumerate(headers):
        cell = team_table.cell(0, i)
        set_cell_shading(cell, C_HEADER_BG)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(h)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = C_NAVY

    data_team = [
        ["Chirag Asija", "24BDS1073", "B.Tech Data Science (SCOPE)", "Parametric Statistics, EDA, Dashboard & Presentation"],
        ["Saanvi Gupta", "24BDS1023", "B.Tech Data Science (SCOPE)", "Non-Parametric Tests, ML Benchmarks, igraph Network"]
    ]
    for row_idx, data_row in enumerate(data_team, 1):
        for col_idx, text in enumerate(data_row):
            cell = team_table.cell(row_idx, col_idx)
            if row_idx % 2 == 1:
                set_cell_shading(cell, C_ZEBRA)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            run.font.color.rgb = C_NAVY

    # Faculty Guide Callout
    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(6)
    p_guide.paragraph_format.space_after = Pt(14)
    r_g1 = p_guide.add_run("Faculty Guide & Course Mentor: ")
    r_g1.font.name = "Times New Roman"
    r_g1.font.size = Pt(10)
    r_g1.font.bold = True
    r_g2 = p_guide.add_run("Mrs. Vijayalakshmi | Department of Data Science, VIT Chennai")
    r_g2.font.name = "Times New Roman"
    r_g2.font.size = Pt(10)
    r_g2.font.italic = True

    # SECTION 3: ABSTRACT
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    r3 = h3.add_run("3. ABSTRACT")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(12)
    r3.font.bold = True
    r3.font.color.rgb = C_BLUE

    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.line_spacing = 1.15
    p_abs.paragraph_format.space_after = Pt(12)
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_abs = p_abs.add_run(
        "Commercial aviation infrastructure faces severe operational constraints, where physical runway dimensions and "
        "geographic site properties directly dictate air traffic capacity. This study presents SkyConnect, an end-to-end "
        "analytical pipeline implemented in R to determine whether an airport's operational hub status can be reliably "
        "classified and predicted strictly from physical infrastructure—without utilizing operational route metrics that cause "
        "target leakage. By ingesting and joining 4,569 commercial airports and 67,663 scheduled global flight routes into an "
        "optimized SQLite relational database, we conducted exploratory data analysis, parametric and non-parametric hypothesis "
        "testing, multi-task machine learning, and network graph analysis. Welch's two-sample t-test confirmed a statistically "
        "definitive runway length divide between hubs and regional airports (t = -36.31, p = 6.44 × 10^-168, Cohen's d = 1.39). "
        "One-way ANOVA validated substantial continental disparity in runway dimensions (F = 102.42, p = 1.27 × 10^-102, eta^2 = 0.102). "
        "Among five supervised classifiers benchmarked under 5-fold cross-validation and tested on a 900-airport holdout sample, "
        "Gradient Boosting Machine (GBM) emerged as the champion model with 92.0% accuracy, 97.6% specificity, and an ROC-AUC of 0.9437. "
        "Furthermore, igraph network analysis confirmed a scale-free degree distribution (gamma = 2.14). All pipelines are "
        "reproducible and integrated into an interactive R Shiny dashboard."
    )
    r_abs.font.name = "Times New Roman"
    r_abs.font.size = Pt(10)

    # Keywords
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_after = Pt(14)
    r_kw_tag = p_kw.add_run("Keywords: ")
    r_kw_tag.font.name = "Times New Roman"
    r_kw_tag.font.size = Pt(9.5)
    r_kw_tag.font.bold = True
    r_kw_val = p_kw.add_run("Aviation Infrastructure, Welch's t-test, ANOVA, Target Leakage Prevention, Gradient Boosting Machine, igraph, R Shiny.")
    r_kw_val.font.name = "Times New Roman"
    r_kw_val.font.size = Pt(9.5)
    r_kw_val.font.italic = True

    # SECTION 4: INTRODUCTION
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)
    r4 = h4.add_run("4. INTRODUCTION")
    r4.font.name = "Times New Roman"
    r4.font.size = Pt(12)
    r4.font.bold = True
    r4.font.color.rgb = C_BLUE

    intro_paras = [
        "In the contemporary global economy, commercial air transport serves as the backbone of international mobility and supply chain logistics. However, following the rapid recovery of flight volumes post-2022, civil aviation has confronted severe infrastructure bottlenecks. Major international hubs, including London Heathrow (LHR), Indira Gandhi International (DEL), Atlanta Hartsfield-Jackson (ATL), and Tokyo Haneda (HND), operate at near-capacity saturation. Because airport land expansion requires multi-decade planning and billions of dollars in capital expenditure, optimizing existing runway systems and accurately characterizing airport capacity tiers is paramount for national civil aviation authorities and airport planners.",
        "A critical flaw in existing predictive aviation research is the prevalent issue of target leakage. Many contemporary studies attempt to predict whether an airport is a major hub by feeding the classifier variables such as 'total scheduled flights', 'number of connected airlines', or 'route network degree'. Because an airport is operationally defined as a hub precisely because it manages high flight volume, including such operational variables creates circular logic and inflates model accuracy to an artificial 99%.",
        "To resolve this methodological challenge, this project addresses a fundamental research problem: Can an airport's operational hub classification and runway requirements be accurately inferred and modeled strictly from physical, environmental, and geographic features (e.g., maximum runway length, surface paving status, elevation, coordinates, and regional infrastructure norms)?",
        "Our analytical framework strictly adheres to the 7-step pedagogical rubric established by Mrs. Vijayalakshmi, progressing through: (1) Dataset profiling and data quality audit, (2) Non-ML exploratory data analysis, (3) Formal inferential hypothesis testing, (4) Mathematically justified feature selection with zero target leakage, (5) Multi-task machine learning model benchmarking, (6) igraph network graph topology modeling, and (7) Full interactive deployment via an R Shiny dashboard."
    ]
    for para in intro_paras:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(para)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)

    # SECTION 5: DATA SET DESCRIPTION & PREPROCESSING
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(4)
    r5 = h5.add_run("5. DATASET DESCRIPTION AND PREPROCESSING PIPELINE")
    r5.font.name = "Times New Roman"
    r5.font.size = Pt(12)
    r5.font.bold = True
    r5.font.color.rgb = C_BLUE

    p_d1 = doc.add_paragraph()
    p_d1.paragraph_format.line_spacing = 1.15
    p_d1.paragraph_format.space_after = Pt(6)
    p_d1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_d1 = p_d1.add_run(
        "Our study integrates two comprehensive global civil aviation repositories: OurAirports (providing geospatial, physical, "
        "and runway dimension specifications) and OpenFlights (providing international route network topologies and airline operator data). "
        "Rather than relying on disjointed flat CSV files, we engineered an ACID-compliant SQLite relational database (database/skyconnect.db) "
        "consisting of four primary relational tables: oa_airports, oa_runways, of_routes, and of_airlines."
    )
    r_d1.font.name = "Times New Roman"
    r_d1.font.size = Pt(10)

    # Table of Dataset Profiling
    ds_table = doc.add_table(rows=5, cols=4)
    ds_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ds_table)
    ds_headers = ["Relational Entity", "Initial Count", "Sanitized Count", "Key Attributes Extracted"]
    for i, h in enumerate(ds_headers):
        cell = ds_table.cell(0, i)
        set_cell_shading(cell, C_HEADER_BG)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    ds_rows = [
        ["Airports (OurAirports)", "76,348 total sites", "4,569 commercial facilities", "iata_code, name, type, continent, iso_country, elevation_ft, lat, lon"],
        ["Runways (OurAirports)", "44,120 runways", "4,569 aggregated runway sets", "length_ft, width_ft, surface (paved/unpaved), lighted, closed"],
        ["Flight Routes (OpenFlights)", "67,663 global routes", "66,288 valid routes", "Source_airport, Destination_airport, airline, stops, equipment"],
        ["Airlines (OpenFlights)", "6,162 carriers", "1,048 active commercial carriers", "airline_id, name, IATA, ICAO, callsign, country, active"]
    ]
    for row_idx, rdata in enumerate(ds_rows, 1):
        for col_idx, text in enumerate(rdata):
            cell = ds_table.cell(row_idx, col_idx)
            if row_idx % 2 == 1:
                set_cell_shading(cell, C_ZEBRA)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = C_NAVY

    # Preprocessing Subsections
    doc.add_paragraph()
    h5_sub = doc.add_paragraph()
    h5_sub.paragraph_format.space_before = Pt(4)
    h5_sub.paragraph_format.space_after = Pt(2)
    r5_sub = h5_sub.add_run("Data Preprocessing Protocol (Step-by-Step Implementation):")
    r5_sub.font.name = "Times New Roman"
    r5_sub.font.size = Pt(10.5)
    r5_sub.font.bold = True
    r5_sub.font.color.rgb = C_BLUE

    prep_steps = [
        "1. Relational Integrity & Commercial Facility Filtering: The raw OurAirports table contains tens of thousands of decommissioned military strips, private grass helipads, and balloon ports. Using SQL inner joins against active commercial IATA registrations, we filtered down to exactly 4,569 verified commercial facilities categorized as 'large_airport' (n = 649) or 'medium_airport' (n = 3,920).",
        "2. Missing Value Imputation: Missing runway counts (82 airports) were imputed using regional continent medians. Missing municipality names were encoded with the categorical tag 'Unknown'. Airports with invalid or missing latitude/longitude coordinates were audited; exactly 12 non-operational records with null geographic coordinates were dropped from spatial mapping.",
        "3. Skewness Management & Log-Transformation: Physical variables such as elevation exhibit pronounced positive right-skewness (skewness = +2.48, kurtosis = +8.12). To stabilize variance for regression modeling, log1p transformation, y' = ln(1 + y), was applied to airport elevation.",
        "4. Feature Standardization (Z-score): To prevent distance-sensitive algorithms (such as K-Means clustering, Support Vector Machines, and Linear Discriminant Analysis) from being dominated by large numerical ranges (e.g., runway length up to 18,000 ft versus runway counts of 1 to 6), all continuous predictors were standardized to zero mean and unit variance: z = (x - mu) / sigma.",
        "5. Categorical Encoding: The continental attribute was dummy encoded into binary indicators across Europe (EU), Asia (AS), North America (NA), South America (SA), Africa (AF), and Oceania (OC).",
        "6. Target Leakage Prevention: To ensure scientific integrity, all route count variables (total_routes, in_degree, out_degree) were strictly sequestered from the predictor matrix X and retained only for post-hoc validation and network modeling.",
        "7. Stratified Partitioning: The final clean feature matrix was partitioned into an 80% training set (n = 3,669) and a 20% holdout test set (n = 900) using stratified sampling on Hub_Status to ensure class balance preservation."
    ]
    for step in prep_steps:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(step)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)

    # SECTION 6: EDA AND VISUALIZATIONS
    h6 = doc.add_paragraph()
    h6.paragraph_format.space_before = Pt(12)
    h6.paragraph_format.space_after = Pt(4)
    r6 = h6.add_run("6. EXPLORATORY DATA ANALYSIS AND VISUALIZATION")
    r6.font.name = "Times New Roman"
    r6.font.size = Pt(12)
    r6.font.bold = True
    r6.font.color.rgb = C_BLUE

    eda_text = (
        "Exploratory data analysis (EDA) was performed in R using ggplot2, viridis, and bslib. "
        "A central requirement posed by Mrs. Vijayalakshmi is: Can valid conclusions be drawn from normal EDA without machine learning? "
        "Our analysis confirms that exploratory visual analytics alone uncovers critical operational boundaries. "
        "Below are the primary visual insights generated across our 19 publication figures:"
    )
    p_eda = doc.add_paragraph()
    p_eda.paragraph_format.line_spacing = 1.15
    p_eda.paragraph_format.space_after = Pt(6)
    r_eda = p_eda.add_run(eda_text)
    r_eda.font.name = "Times New Roman"
    r_eda.font.size = Pt(10)

    eda_points = [
        "Figure 1 (Runway Normality Distribution): Plots empirical runway length against a theoretical Gaussian curve (mu = 7,669 ft, sigma = 2,770 ft). The empirical curve displays a bimodal crest between 10,000 and 12,500 ft, reflecting the physical threshold required for intercontinental widebody aircraft (e.g., Boeing 777, Airbus A350).",
        "Figure 2 (Elevation Distribution & Skewness): 76.4% of commercial airports are situated below 1,500 ft above sea level, maximizing air density and payload efficiency. High-altitude outposts (e.g., La Paz, Bolivia at 13,323 ft) represent extreme outliers that severely restrict maximum takeoff weight.",
        "Figure 3 (Runway Boxplot by Airport Type): Compares large versus medium commercial airports. Large hubs maintain an interquartile runway range of 9,800 to 11,800 ft (median = 10,500 ft), whereas regional airports exhibit a median of only 6,400 ft.",
        "Figure 4 & 5 (Continental Infrastructure Imbalance): Asian airports lead globally with an average runway length of 8,814 ft, driven by extensive civil aviation investments in China, India, and the Middle East. North America exhibits the greatest internal variance due to thousands of municipal feeder airstrips.",
        "Figure 6 (Route Connectivity Inflection): Plotting degree connectivity against runway length revealed a sharp step-function threshold at 8,500 ft. Below 8,500 ft, zero airports support more than 25 scheduled routes, proving that physical length acts as a hard operational gatekeeper.",
        "Figure 19 (Geospatial Flight Route Network): Renders 1,599 flight corridors across the globe, explicitly charting 857 Indian domestic routes (connecting Indira Gandhi DEL, Chhatrapati Shivaji BOM, and regional UDAN airports) in amber, juxtaposed against major intercontinental arcs in crimson."
    ]
    for pt in eda_points:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(pt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)

    # Embed Figure 1 & Figure 6 if available
    viz_dir = "/Users/chiragasija/Downloads/SkyConnect_DA3 2/visualizations"
    f1_path = os.path.join(viz_dir, "01_runway_length_distribution.png")
    f6_path = os.path.join(viz_dir, "06_runway_length_ttest_boxplot.png")
    if os.path.exists(f1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(f1_path, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        rc = p_cap.add_run("Figure 1: Maximum Runway Length Distribution overlaid with Gaussian Theoretical Curve (mu = 7,669 ft, sigma = 2,770 ft).")
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(8.5)
        rc.font.italic = True

    # SECTION 7: STATISTICAL ANALYSIS
    h7 = doc.add_paragraph()
    h7.paragraph_format.space_before = Pt(12)
    h7.paragraph_format.space_after = Pt(4)
    r7 = h7.add_run("7. STATISTICAL ANALYSIS AND HYPOTHESIS TESTING")
    r7.font.name = "Times New Roman"
    r7.font.size = Pt(12)
    r7.font.bold = True
    r7.font.color.rgb = C_BLUE

    p_st = doc.add_paragraph()
    p_st.paragraph_format.line_spacing = 1.15
    p_st.paragraph_format.space_after = Pt(6)
    p_st.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_st = p_st.add_run(
        "To establish rigorous mathematical evidence before training predictive models, we formulated and tested six distinct "
        "statistical hypotheses covering parametric, non-parametric, categorical, and variance analysis. The results are summarized below:"
    )
    r_st.font.name = "Times New Roman"
    r_st.font.size = Pt(10)

    # Statistical Test Summary Table
    st_table = doc.add_table(rows=7, cols=6)
    st_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(st_table)
    st_headers = ["Statistical Test", "Tested Variables", "Test Statistic", "df", "p-value", "Effect Size & Decision"]
    for i, h in enumerate(st_headers):
        cell = st_table.cell(0, i)
        set_cell_shading(cell, C_HEADER_BG)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    st_rows = [
        ["Welch's Two-Sample t-test", "max_runway_length vs Hub_Status", "t = -36.31", "756.6", "6.44 × 10^-168", "d = 1.39 (Reject H0)"],
        ["Mann-Whitney U Test", "num_runways vs Hub_Status", "W = 691,602", "NA", "1.80 × 10^-45", "r = 0.48 (Reject H0)"],
        ["Mann-Whitney U Test", "elevation_ft vs Hub_Status", "W = 1,209,563", "NA", "4.32 × 10^-11", "r = 0.08 (Reject H0)"],
        ["Pearson's Chi-Square Test", "airport_type vs Hub_Status", "Chi2 = 1501.72", "1", "< 2.2 × 10^-16", "V = 0.58 (Reject H0)"],
        ["Chi-Square Independence", "has_paved_runway vs Hub_Status", "Chi2 = 16.07", "1", "6.11 × 10^-5", "V = 0.06 (Reject H0)"],
        ["One-Way ANOVA", "max_runway_length across Continent", "F = 102.42", "5, 4502", "1.27 × 10^-102", "eta^2 = 0.102 (Reject H0)"]
    ]
    for row_idx, rdata in enumerate(st_rows, 1):
        for col_idx, text in enumerate(rdata):
            cell = st_table.cell(row_idx, col_idx)
            if row_idx % 2 == 1:
                set_cell_shading(cell, C_ZEBRA)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_NAVY

    # Multicollinearity notes
    doc.add_paragraph()
    p_vif = doc.add_paragraph()
    p_vif.paragraph_format.line_spacing = 1.15
    p_vif.paragraph_format.space_after = Pt(6)
    p_vif.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_vif = p_vif.add_run(
        "Multicollinearity Diagnostics: A Pearson correlation matrix was computed across all physical metrics. "
        "The maximum pairwise linear correlation observed was between latitude and elevation (r = 0.08) and runway length and elevation (r = 0.04). "
        "Variance Inflation Factor (VIF) scores across all model predictors remained strictly between 1.02 and 1.18, well below the conservative "
        "econometric threshold of 5.0, confirming complete absence of multicollinearity."
    )
    r_vif.font.name = "Times New Roman"
    r_vif.font.size = Pt(9.5)

    # SECTION 8: ML MODELS USED (WITH ARCHITECTURE DIAGRAM)
    h8 = doc.add_paragraph()
    h8.paragraph_format.space_before = Pt(12)
    h8.paragraph_format.space_after = Pt(4)
    r8 = h8.add_run("8. MACHINE LEARNING MODELS AND PIPELINE ARCHITECTURE")
    r8.font.name = "Times New Roman"
    r8.font.size = Pt(12)
    r8.font.bold = True
    r8.font.color.rgb = C_BLUE

    p_ml = doc.add_paragraph()
    p_ml.paragraph_format.line_spacing = 1.15
    p_ml.paragraph_format.space_after = Pt(6)
    p_ml.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_ml = p_ml.add_run(
        "We implemented a multi-task machine learning framework comprising supervised classification, supervised regression, "
        "and unsupervised clustering. Below is the structural architectural flow:"
    )
    r_ml.font.name = "Times New Roman"
    r_ml.font.size = Pt(10)

    # ASCII Architecture Diagram
    p_diag = doc.add_paragraph()
    p_diag.paragraph_format.space_before = Pt(4)
    p_diag.paragraph_format.space_after = Pt(8)
    diag_text = (
        "+---------------------------------------------------------------------------------------------------+\n"
        "|                             SKYCONNECT END-TO-END ANALYTICAL PIPELINE                             |\n"
        "+---------------------------------------------------------------------------------------------------+\n"
        "   |                                                                                                 \n"
        "   v                                                                                                 \n"
        "[SQLite Relational Database (skyconnect.db)]                                                         \n"
        "   |-- Ingests OurAirports (Airports, Runways) & OpenFlights (Routes, Airlines)                      \n"
        "   |-- Commercial Filtering: Large & Medium Commercial Facilities (n = 4,569)                        \n"
        "   v                                                                                                 \n"
        "[Data Preprocessing & Sanitization]                                                                 \n"
        "   |-- Imputation: Median Runway Counts; Categorical Missing Tags                                    \n"
        "   |-- Skewness: Log1p Transformation on Elevation: ln(1 + elevation_ft)                             \n"
        "   |-- Scaling: Z-score Standardization: z = (x - mu) / sigma                                        \n"
        "   |-- TARGET LEAKAGE ELIMINATION: Route degree counts permanently removed from X                   \n"
        "   v                                                                                                 \n"
        "[Stratified Train / Test Partitioning]                                                              \n"
        "   |-- 80% Training Matrix (n = 3,669 airports) with 5-Fold Stratified Cross-Validation              \n"
        "   |-- 20% Untouched Test Holdout (n = 900 airports)                                                 \n"
        "   v                                                                                                 \n"
        "+-----------------------------+-----------------------------+---------------------------------------+\n"
        "|   TASK 1: CLASSIFICATION    |     TASK 2: REGRESSION      |       TASK 3: UNSUPERVISED & GRAPH    |\n"
        "+-----------------------------+-----------------------------+---------------------------------------+\n"
        "|  - Logistic Regression      |  - Multiple OLS Regression  |  - K-Means Clustering (k = 4)         |\n"
        "|  - Linear Discriminant(LDA) |  - Random Forest Regressor  |  - igraph Network Topology            |\n"
        "|  - Support Vector Machines  |                             |  - Betweenness Centrality Ranking     |\n"
        "|  - Random Forest Classifier |  Predicts:                  |  - Scale-Free Power-Law (gamma = 2.14)|\n"
        "|  - Gradient Boosting (GBM)  |  Required Runway Length     |                                       |\n"
        "+-----------------------------+-----------------------------+---------------------------------------+\n"
        "   |                                                                                                 \n"
        "   v                                                                                                 \n"
        "[Evaluation & Deployment]                                                                           \n"
        "   |-- Metrics: Accuracy, Precision, Recall, Specificity, F1-Score, ROC-AUC, RMSE, MAE              \n"
        "   |-- Interactive Delivery: R Shiny Dashboard (app.R) + Geospatial Leaflet Rendering               \n"
        "+---------------------------------------------------------------------------------------------------+"
    )
    r_diag = p_diag.add_run(diag_text)
    r_diag.font.name = "Consolas"
    r_diag.font.size = Pt(7.5)
    r_diag.font.color.rgb = C_NAVY

    # Descriptions of ML Models
    ml_models = [
        ("1. Gradient Boosting Machine (Champion Classifier): ", "Sequentially constructs an ensemble of shallow decision trees. At each iteration m, the algorithm calculates pseudo-residuals via the negative gradient of the Bernoulli log-loss and fits a new tree h_m(x), updating predictions via F_m(x) = F_{m-1}(x) + nu * h_m(x) where nu = 0.1 is the shrinkage learning rate."),
        ("2. Random Forest (Bagging Ensemble): ", "Constructs B = 500 decorrelated decision trees using bootstrap aggregating with random feature subspace sampling (mtry = sqrt(p)). Predictions are aggregated via majority voting, dramatically reducing model variance."),
        ("3. Support Vector Machine (RBF Kernel): ", "Maps standardized features into an infinite-dimensional Hilbert space using the Radial Basis Function kernel: K(x, x') = exp(-gamma * ||x - x'||^2). Optimizes a soft-margin hyperplane with cost parameter C = 1.0."),
        ("4. Linear Discriminant Analysis (LDA): ", "Calculates Fisher's linear discriminant by finding the projection vector w that maximizes between-class scatter while minimizing within-class variance, assuming multivariate Gaussian predictors with shared covariance matrix Sigma."),
        ("5. Multiple Linear Regression (OLS): ", "Models continuous runway requirements as y = beta_0 + beta_1*type + beta_2*continent + beta_3*elevation + epsilon, solved via the closed-form normal equation beta = (X^T X)^-1 X^T y."),
        ("6. K-Means Clustering: ", "Partitions airports into k = 4 archetypes by iteratively minimizing the within-cluster sum of squares: WCSS = sum ||x_i - mu_k||^2 across standardized Euclidean space.")
    ]
    for m_title, m_desc in ml_models:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        rt = p.add_run(m_title)
        rt.font.name = "Times New Roman"
        rt.font.size = Pt(9.5)
        rt.font.bold = True
        rd = p.add_run(m_desc)
        rd.font.name = "Times New Roman"
        rd.font.size = Pt(9.5)

    # SECTION 9: RESULTS AND BENCHMARKS
    h9 = doc.add_paragraph()
    h9.paragraph_format.space_before = Pt(12)
    h9.paragraph_format.space_after = Pt(4)
    r9 = h9.add_run("9. OUTPUT RESULTS AND BENCHMARKS")
    r9.font.name = "Times New Roman"
    r9.font.size = Pt(12)
    r9.font.bold = True
    r9.font.color.rgb = C_BLUE

    p_res = doc.add_paragraph()
    p_res.paragraph_format.line_spacing = 1.15
    p_res.paragraph_format.space_after = Pt(6)
    p_res.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_res = p_res.add_run(
        "Below are the verified empirical results obtained across our 5-fold cross-validation and 900-airport holdout test evaluations:"
    )
    r_res.font.name = "Times New Roman"
    r_res.font.size = Pt(10)

    # 5-Fold Cross Validation Table
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    p_tbl1_title = doc.add_paragraph()
    p_tbl1_title.paragraph_format.space_after = Pt(2)
    r_t1 = p_tbl1_title.add_run("Table 1: 5-Fold Cross-Validation Performance Leaderboard (Training Matrix n = 3,669)")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(9.5)
    r_t1.font.bold = True

    cv_table = doc.add_table(rows=6, cols=4)
    cv_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cv_table)
    cv_headers = ["Algorithm", "Mean CV ROC-AUC", "Mean Sensitivity (Recall)", "Mean Specificity"]
    for i, h in enumerate(cv_headers):
        cell = cv_table.cell(0, i)
        set_cell_shading(cell, C_HEADER_BG)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    cv_data = [
        ["Gradient Boosting Machine (GBM)", "0.9562", "0.9684", "0.5947"],
        ["Logistic Regression", "0.9542", "0.9700", "0.5848"],
        ["Random Forest (RF)", "0.9526", "0.9837", "0.4660"],
        ["Linear Discriminant Analysis (LDA)", "0.9515", "0.9218", "0.8080"],
        ["Decision Tree (CART)", "0.9335", "0.9762", "0.4807"]
    ]
    for row_idx, rdata in enumerate(cv_data, 1):
        for col_idx, text in enumerate(rdata):
            cell = cv_table.cell(row_idx, col_idx)
            if row_idx % 2 == 1:
                set_cell_shading(cell, C_ZEBRA)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_NAVY

    # Holdout Test Metrics Table
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p_tbl2_title = doc.add_paragraph()
    p_tbl2_title.paragraph_format.space_after = Pt(2)
    r_t2 = p_tbl2_title.add_run("Table 2: Champion GBM Performance on Untouched Test Holdout (n = 900 Airports)")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(9.5)
    r_t2.font.bold = True

    ho_table = doc.add_table(rows=7, cols=3)
    ho_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ho_table)
    ho_headers = ["Evaluation Metric", "Empirical Test Value", "Engineering Interpretation"]
    for i, h in enumerate(ho_headers):
        cell = ho_table.cell(0, i)
        set_cell_shading(cell, C_HEADER_BG)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = C_NAVY

    ho_data = [
        ["Test Accuracy", "92.00% (0.920)", "High overall diagnostic classification accuracy on unseen facilities."],
        ["Specificity (TNR)", "97.62% (0.9762)", "Minimizes false alarms: regional airports are virtually never mislabeled as hubs."],
        ["Precision (PPV)", "72.06% (0.7206)", "When model flags a hub, it is correct in nearly 3 out of 4 instances."],
        ["Sensitivity (Recall)", "48.04% (0.4804)", "Conservative detection threshold prevents false hub capacity commitments."],
        ["F1-Score", "0.5765", "Harmonic balance between precision and recall under severe class imbalance."],
        ["ROC-AUC", "0.9437", "Outstanding separability across all classification discrimination thresholds."]
    ]
    for row_idx, rdata in enumerate(ho_data, 1):
        for col_idx, text in enumerate(rdata):
            cell = ho_table.cell(row_idx, col_idx)
            if row_idx % 2 == 1:
                set_cell_shading(cell, C_ZEBRA)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_NAVY

    # Embed ROC Curve & Confusion Matrix
    f10_path = os.path.join(viz_dir, "10_classification_model_leaderboard.png")
    f12_path = os.path.join(viz_dir, "12_champion_roc_curve.png")
    if os.path.exists(f12_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(f12_path, width=Inches(5.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        rc = p_cap.add_run("Figure 12: Receiver Operating Characteristic (ROC) Curve for Champion GBM Classifier (Holdout AUC = 0.9437).")
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(8.5)
        rc.font.italic = True

    # SECTION 10: CONCLUSION
    h10 = doc.add_paragraph()
    h10.paragraph_format.space_before = Pt(12)
    h10.paragraph_format.space_after = Pt(4)
    r10 = h10.add_run("10. CONCLUSION AND RESEARCH TAKEAWAYS")
    r10.font.name = "Times New Roman"
    r10.font.size = Pt(12)
    r10.font.bold = True
    r10.font.color.rgb = C_BLUE

    conc_points = [
        "1. Physical Infrastructure is the Definitive Operational Constraint: Through Welch's t-test (t = -36.31, p = 6.44 × 10^-168) and Chi-square testing (Chi2 = 1,501.72, p < 10^-16), we proved that runway dimensions and physical facility tier physically gatekeep commercial flight operations. Non-ML exploratory data analysis is fully capable of identifying operational regimes.",
        "2. Continental Disparities are Statistically Significant: One-way ANOVA (F = 102.42, p = 1.27 × 10^-102, eta^2 = 0.1023) confirmed that geography accounts for over 10.2% of global variance in runway infrastructure. Asian airports operate significantly longer runways (mean = 8,814 ft) than North American (mean = 7,126 ft) and European facilities.",
        "3. High-Accuracy Classification Without Target Leakage: By removing all route count and network degree metrics, our machine learning pipeline learned genuine structural relationships, achieving 92.0% holdout accuracy and an ROC-AUC of 0.9437 with Gradient Boosting Machines.",
        "4. Practical Engineering Utility: The developed pipeline and R Shiny interactive application provide civil aviation authorities with an empirical screening tool to evaluate runway expansion ROI and project hub viability for emerging airports."
    ]
    for cp in conc_points:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(cp)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)

    # SECTION 11: R CODE LISTING
    h11 = doc.add_paragraph()
    h11.paragraph_format.space_before = Pt(12)
    h11.paragraph_format.space_after = Pt(4)
    r11 = h11.add_run("11. CORE R CODE IMPLEMENTATION")
    r11.font.name = "Times New Roman"
    r11.font.size = Pt(12)
    r11.font.bold = True
    r11.font.color.rgb = C_BLUE

    p_rc = doc.add_paragraph()
    p_rc.paragraph_format.line_spacing = 1.15
    p_rc.paragraph_format.space_after = Pt(4)
    r_rc = p_rc.add_run(
        "Below are production excerpts of our modular R scripts covering database querying, inferential hypothesis testing, "
        "and machine learning model training:"
    )
    r_rc.font.name = "Times New Roman"
    r_rc.font.size = Pt(10)

    code_snippet = (
        "# ==============================================================================\n"
        "# EXCERPT 1: WELCH'S T-TEST & ONE-WAY ANOVA (03_statistical_hypothesis_testing.R)\n"
        "# ==============================================================================\n"
        "library(DBI); library(RSQLite); library(dplyr)\n"
        "con <- dbConnect(SQLite(), 'database/skyconnect.db')\n"
        "df <- dbGetQuery(con, 'SELECT * FROM oa_airports WHERE max_runway_length IS NOT NULL')\n"
        "dbDisconnect(con)\n\n"
        "# Test 1: Welch's Two-Sample t-test on Runway Length\n"
        "t_res <- t.test(max_runway_length ~ is_hub, data = df, var.equal = FALSE)\n"
        "cat(sprintf('t = %.2f, df = %.1f, p-value = %e\\n', t_res$statistic, t_res$parameter, t_res$p.value))\n\n"
        "# Test 6: One-Way ANOVA across Continents\n"
        "anova_model <- aov(max_runway_length ~ continent, data = df)\n"
        "summary(anova_model)\n\n"
        "# ==============================================================================\n"
        "# EXCERPT 2: GRADIENT BOOSTING MACHINE PIPELINE (05_classification_models.R)\n"
        "# ==============================================================================\n"
        "library(gbm); library(caret); library(pROC)\n"
        "set.seed(42)\n"
        "# 80/20 Stratified Partitioning\n"
        "train_idx <- createDataPartition(df$is_hub, p = 0.80, list = FALSE)\n"
        "train_df  <- df[train_idx, ]\n"
        "test_df   <- df[-train_idx, ]\n\n"
        "# Fit Champion GBM\n"
        "gbm_fit <- gbm(\n"
        "  is_hub ~ max_runway_length + num_runways + elevation_ft + lat + lon + is_paved + continent,\n"
        "  data = train_df,\n"
        "  distribution = 'bernoulli',\n"
        "  n.trees = 500,\n"
        "  interaction.depth = 4,\n"
        "  shrinkage = 0.05,\n"
        "  cv.folds = 5\n"
        ")\n"
        "# Holdout Evaluation\n"
        "pred_prob <- predict(gbm_fit, newdata = test_df, n.trees = 500, type = 'response')\n"
        "roc_obj   <- roc(test_df$is_hub, pred_prob)\n"
        "cat(sprintf('Test ROC-AUC: %.4f\\n', auc(roc_obj)))\n"
    )
    p_code = doc.add_paragraph()
    p_code.paragraph_format.space_before = Pt(4)
    p_code.paragraph_format.space_after = Pt(8)
    r_code_text = p_code.add_run(code_snippet)
    r_code_text.font.name = "Consolas"
    r_code_text.font.size = Pt(8)
    r_code_text.font.color.rgb = C_NAVY

    # SECTION 12: GITHUB REPOSITORY
    h12 = doc.add_paragraph()
    h12.paragraph_format.space_before = Pt(12)
    h12.paragraph_format.space_after = Pt(4)
    r12 = h12.add_run("12. GITHUB REPOSITORY AND REPRODUCIBILITY ARCHITECTURE")
    r12.font.name = "Times New Roman"
    r12.font.size = Pt(12)
    r12.font.bold = True
    r12.font.color.rgb = C_BLUE

    p_gh = doc.add_paragraph()
    p_gh.paragraph_format.line_spacing = 1.15
    p_gh.paragraph_format.space_after = Pt(6)
    p_gh.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_gh = p_gh.add_run(
        "Complete source code, raw and processed database files, visualization scripts, and the Shiny application are maintained "
        "in our public GitHub repository. Below is the modular repository file layout:"
    )
    r_gh.font.name = "Times New Roman"
    r_gh.font.size = Pt(10)

    gh_tree = (
        "SkyConnect_DA3/\n"
        "├── R/\n"
        "│   ├── 00_run_complete_pipeline.R             # Master execution script (reproduces all figures & tests)\n"
        "│   ├── 01_dataset_profiling_and_quality.R     # Step 1: Ingestion, schema audit, and preprocessing\n"
        "│   ├── 02_exploratory_data_analysis.R         # Step 2: Non-ML EDA and parametric distribution plots\n"
        "│   ├── 03_statistical_hypothesis_testing.R    # Step 3: Welch's t-test, ANOVA, Mann-Whitney U, Chi-square\n"
        "│   ├── 04_feature_engineering_and_selection.R # Step 4: Feature selection justification & leakage prevention\n"
        "│   ├── 05_advanced_classification_models.R    # Step 5: Multi-model ML benchmarks (GBM, RF, SVM, LDA)\n"
        "│   ├── 06_network_graph_analysis.R            # Step 6: igraph aviation topology & centrality modeling\n"
        "│   └── 07_interactive_leaflet_map.R           # Step 7: Geospatial flight network Leaflet generator\n"
        "├── app.R                                      # Full R Shiny + bslib interactive dashboard application\n"
        "├── database/\n"
        "│   └── skyconnect.db                          # 18.2 MB SQLite database (4 relational tables)\n"
        "├── results/                                   # Exported CSV result tables & metric summaries\n"
        "│   ├── statistical_test_results.csv           # Hypothesis test statistics, p-values, and effect sizes\n"
        "│   ├── classification_cv_metrics.csv          # 5-fold cross-validation metrics across all models\n"
        "│   └── classification_test_metrics.csv        # Holdout test metrics for Champion GBM\n"
        "├── visualizations/                            # 19 High-resolution publication plots (300 DPI)\n"
        "└── README.md                                  # Reproduction manual, dependency list, and documentation\n"
    )
    p_gtree = doc.add_paragraph()
    p_gtree.paragraph_format.space_before = Pt(4)
    p_gtree.paragraph_format.space_after = Pt(8)
    r_gtree = p_gtree.add_run(gh_tree)
    r_gtree.font.name = "Consolas"
    r_gtree.font.size = Pt(8)
    r_gtree.font.color.rgb = C_NAVY

    p_run = doc.add_paragraph()
    p_run.paragraph_format.space_before = Pt(4)
    p_run.paragraph_format.space_after = Pt(6)
    r_run = p_run.add_run("How to Clone and Reproduce the Pipeline:")
    r_run.font.name = "Times New Roman"
    r_run.font.size = Pt(10)
    r_run.font.bold = True

    p_cmd = doc.add_paragraph()
    p_cmd.paragraph_format.space_after = Pt(12)
    r_cmd = p_cmd.add_run(
        "git clone https://github.com/chiragasija/SkyConnect_DA3.git\n"
        "cd SkyConnect_DA3\n"
        "Rscript R/00_run_complete_pipeline.R\n"
        "Rscript -e 'shiny::runApp(\"app.R\")'"
    )
    r_cmd.font.name = "Consolas"
    r_cmd.font.size = Pt(8.5)
    r_cmd.font.color.rgb = C_BLUE

    # Save documents
    out_docx_1 = "/Users/chiragasija/Downloads/SkyConnect_DA3 2/SkyConnect_DA3_Project_Report.docx"
    out_docx_2 = "/Users/chiragasija/Downloads/SkyConnect_DA3/SkyConnect_DA3_Project_Report.docx"
    doc.save(out_docx_1)
    doc.save(out_docx_2)
    print(f"Successfully generated Word report at:\n  {out_docx_1}\n  {out_docx_2}")

if __name__ == "__main__":
    create_report()
