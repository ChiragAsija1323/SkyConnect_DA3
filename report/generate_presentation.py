#!/usr/bin/env python3
"""
SkyConnect DA-3 Presentation Generator
Generates a 16:9 widescreen academic PowerPoint deck (.pptx)
Embedded with real visualization plots, exact statistical test statistics,
speaker badges (Chirag Asija & Saanvi Gupta 50/50 split), and embedded presenter notes.
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(viz_dir, output_path):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Academic Color Palette
    C_NAVY_DARK = RGBColor(15, 23, 42)     # #0F172A
    C_BLUE_PRIMARY = RGBColor(30, 58, 138)  # #1E3A8A
    C_BLUE_LIGHT = RGBColor(239, 246, 255)  # #EFF6FF
    C_SLATE_DARK = RGBColor(51, 65, 85)     # #334155
    C_SLATE_MUTED = RGBColor(100, 116, 139) # #64748B
    C_BORDER = RGBColor(226, 232, 240)      # #E2E8F0
    C_WHITE = RGBColor(255, 255, 255)
    C_AMBER = RGBColor(217, 119, 6)         # #D97706
    C_RED = RGBColor(220, 38, 38)           # #DC2626
    C_GREEN = RGBColor(16, 185, 129)        # #10B981

    def set_slide_background(slide, color=RGBColor(248, 250, 252)):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category, speaker_name, speaker_id, speaker_time, slide_num):
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_AMBER

        # Main Title (Full Width)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(9.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_DARK

        # Clean Academic Slide Tracker Pill (No speaker names on slide)
        badge_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.7), Inches(0.45), Inches(1.8), Inches(0.45))
        badge_bg.fill.solid()
        badge_bg.fill.fore_color.rgb = C_BLUE_LIGHT
        badge_bg.line.color.rgb = RGBColor(191, 219, 254)
        badge_bg.line.width = Pt(1)

        badge_box = slide.shapes.add_textbox(Inches(10.7), Inches(0.48), Inches(1.8), Inches(0.4))
        tf_b = badge_box.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = f"Slide {slide_num} of 18"
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = C_BLUE_PRIMARY
        p_b.alignment = PP_ALIGN.CENTER

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf_f = footer_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "SkyConnect DA-3: Data Analytics using R | Faculty Guide: Mrs. Vijayalakshmi | VIT Chennai"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = C_SLATE_MUTED

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ==========================================================================
    # SLIDE 1: Title Slide (Both Speakers)
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, RGBColor(15, 23, 42)) # Deep Navy Hero

    # Accent Top Stripe
    stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_AMBER
    stripe.line.fill.background()

    # Title & Subtitle Card
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.3), Inches(2.6))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "SKYCONNECT DA-3"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(248, 250, 252)

    p2 = tf1.add_paragraph()
    p2.text = "A Statistically-Grounded Machine Learning Pipeline for Global Aviation Infrastructure & Airline Connectivity"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(147, 197, 253)
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "End-to-End Analytical Workflow: Data Quality Audit • Hypothesis Testing • Target Leakage Prevention • Multi-Model ML • igraph Network Analytics"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_before = Pt(12)

    # Authors Card Left (Chirag)
    c_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(5.3), Inches(1.8))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_card.line.color.rgb = RGBColor(71, 85, 105)
    c_box = s1.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(4.9), Inches(1.6))
    c_tf = c_box.text_frame
    cp1 = c_tf.paragraphs[0]
    cp1.text = "CHIRAG ASIJA"
    cp1.font.size = Pt(16)
    cp1.font.bold = True
    cp1.font.color.rgb = RGBColor(254, 215, 170)
    cp2 = c_tf.add_paragraph()
    cp2.text = "Reg. No: 24BDS1073\nCourse: Data Analytics using R\nRole: Parametric Statistics, Feature Engineering & ML"
    cp2.font.size = Pt(11)
    cp2.font.color.rgb = RGBColor(226, 232, 240)

    # Authors Card Right (Saanvi)
    s_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(4.5), Inches(5.3), Inches(1.8))
    s_card.fill.solid()
    s_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    s_card.line.color.rgb = RGBColor(71, 85, 105)
    s_box = s1.shapes.add_textbox(Inches(7.2), Inches(4.6), Inches(4.9), Inches(1.6))
    s_tf = s_box.text_frame
    sp1 = s_tf.paragraphs[0]
    sp1.text = "SAANVI GUPTA"
    sp1.font.size = Pt(16)
    sp1.font.bold = True
    sp1.font.color.rgb = RGBColor(254, 215, 170)
    sp2 = s_tf.add_paragraph()
    sp2.text = "Reg. No: 24BDS1023\nCourse: Data Analytics using R\nRole: Data Profiling, ANOVA, Clustering & igraph Network"
    sp2.font.size = Pt(11)
    sp2.font.color.rgb = RGBColor(226, 232, 240)

    # Footer note
    guide_box = s1.shapes.add_textbox(Inches(1.0), Inches(6.65), Inches(11.3), Inches(0.4))
    g_tf = guide_box.text_frame
    gp = g_tf.paragraphs[0]
    gp.text = "Faculty Guide: Mrs. Vijayalakshmi | Academic Year: 2026–2027 | VIT Chennai"
    gp.font.size = Pt(11)
    gp.font.color.rgb = RGBColor(148, 163, 184)
    gp.alignment = PP_ALIGN.CENTER

    add_notes(s1, "Chirag: Good day everyone, and respected faculty guide Mrs. Vijayalakshmi. My name is Chirag Asija (24BDS1073), and alongside my co-researcher Saanvi Gupta (24BDS1023), we present SkyConnect DA-3: A Statistically-Grounded Machine Learning Pipeline for Global Aviation Infrastructure and Airline Connectivity. Today, we will present our end-to-end analytical study across 18 slides in exactly 14 minutes.")

    # Helper function for split content + plot slides
    def create_split_slide(title, category, speaker_name, speaker_id, speaker_time, slide_num,
                           bullets, image_filename, stat_cards=None, notes=""):
        slide = prs.slides.add_slide(blank_layout)
        set_slide_background(slide)
        add_header(slide, title, category, speaker_name, speaker_id, speaker_time, slide_num)

        # Left Container (Content & Metrics)
        card_w = Inches(5.9)
        card_h = Inches(5.35)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1)

        # Bullets in Left Container
        box = slide.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.5), Inches(3.6))
        tf = box.text_frame
        tf.word_wrap = True

        for i, b in enumerate(bullets):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b[0]
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = C_NAVY_DARK
            p.space_before = Pt(8) if i > 0 else Pt(0)

            p_sub = tf.add_paragraph()
            p_sub.text = b[1]
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = C_SLATE_DARK

        # Stat cards at bottom of left container if provided
        if stat_cards:
            start_y = 5.3
            card_width = 5.5 / len(stat_cards)
            for j, sc in enumerate(stat_cards):
                sc_shape = slide.shapes.add_shape(
                    MSO_SHAPE.ROUNDED_RECTANGLE,
                    Inches(1.0 + j * card_width + j * 0.1), Inches(start_y),
                    Inches(card_width - 0.1), Inches(1.25)
                )
                sc_shape.fill.solid()
                sc_shape.fill.fore_color.rgb = C_BLUE_LIGHT
                sc_shape.line.color.rgb = RGBColor(191, 219, 254)
                sc_tf = sc_shape.text_frame
                sc_tf.word_wrap = True
                scp1 = sc_tf.paragraphs[0]
                scp1.text = sc[0]
                scp1.font.size = Pt(9)
                scp1.font.bold = True
                scp1.font.color.rgb = C_SLATE_MUTED
                scp2 = sc_tf.add_paragraph()
                scp2.text = sc[1]
                scp2.font.size = Pt(14)
                scp2.font.bold = True
                scp2.font.color.rgb = C_BLUE_PRIMARY
                scp3 = sc_tf.add_paragraph()
                scp3.text = sc[2]
                scp3.font.size = Pt(9)
                scp3.font.color.rgb = C_SLATE_DARK

        # Right Container (Image)
        img_path = os.path.join(viz_dir, image_filename)
        if os.path.exists(img_path):
            img_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.45), Inches(5.6), Inches(5.35))
            img_card.fill.solid()
            img_card.fill.fore_color.rgb = C_WHITE
            img_card.line.color.rgb = C_BORDER
            img_card.line.width = Pt(1)

            # Insert Image
            slide.shapes.add_picture(img_path, Inches(7.0), Inches(1.55), Inches(5.4), Inches(5.15))

        add_notes(slide, notes)
        return slide

    # ==========================================================================
    # SLIDE 2: Problem Motivation & Aviation Context (Chirag - 1:00 min)
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Motivation & Real-World Aviation Bottlenecks", "Context & Objectives", "Chirag Asija", "24BDS1073", "1:00 min", 2)

    # 3 Structured Highlight Cards
    card_data = [
        ("THE POST-PANDEMIC CAPACITY CRISIS",
         "Global air passenger traffic has surged beyond 4.5 billion annual travelers. Major international hubs like London Heathrow, Atlanta, and Frankfurt face acute runway saturation, slot restrictions, and cascading airspace delays.",
         "Operational Reality", C_RED),
        ("THE CORE RESEARCH QUESTION",
         "Can the physical infrastructure of an airport—runway length, runway count, paved surface, altitude, and geographic coordinates—statistically predict whether it can function as a global international transit hub, WITHOUT knowing its route numbers?",
         "Core Hypothesis", C_BLUE_PRIMARY),
        ("THE REAL-WORLD INDUSTRY VALUE",
         "Airlines and civil aviation authorities can evaluate emerging airports for new intercontinental hubs or strategic alliance connections purely based on civil engineering specifications and geographic viability.",
         "Actionable Impact", C_AMBER)
    ]
    for idx, (ctitle, cdesc, ctag, col) in enumerate(card_data):
        c_x = Inches(0.8 + idx * 3.95)
        c_shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, Inches(1.6), Inches(3.8), Inches(4.8))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = C_WHITE
        c_shape.line.color.rgb = C_BORDER
        c_shape.line.width = Pt(1)

        # Header bar in card
        hbar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x + Inches(0.2), Inches(1.8), Inches(3.4), Inches(0.35))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = col
        hbar.line.fill.background()
        h_tf = hbar.text_frame
        hp = h_tf.paragraphs[0]
        hp.text = ctag.upper()
        hp.font.size = Pt(10)
        hp.font.bold = True
        hp.font.color.rgb = C_WHITE
        hp.alignment = PP_ALIGN.CENTER

        c_box = s2.shapes.add_textbox(c_x + Inches(0.2), Inches(2.3), Inches(3.4), Inches(3.8))
        ctf = c_box.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = ctitle
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = C_NAVY_DARK

        cp2 = ctf.add_paragraph()
        cp2.text = cdesc
        cp2.font.size = Pt(11)
        cp2.font.color.rgb = C_SLATE_DARK
        cp2.space_before = Pt(10)

    add_notes(s2, "Chirag: The motivation behind SkyConnect DA-3 stems from the severe post-pandemic capacity crisis in global air transportation. Airlines open new routes and airports expand terminals every year. However, our fundamental research question asks: Can physical infrastructure—runway length, surface paving, elevation, and geographic coordinates—statistically determine whether an airport can function as an international transit hub, completely independent of flight traffic numbers? In real data science, machine learning models should never be applied arbitrarily. Before training a single algorithm, we must mathematically understand our data and prove underlying relationships.")

    # ==========================================================================
    # SLIDE 3: Teacher's Mandate & Analytical Roadmap (Saanvi - 1:00 min)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Adhering to Faculty Guidelines: End-to-End Analytical Workflow", "Course Rubric", "Saanvi Gupta", "24BDS1023", "1:00 min", 3)

    steps = [
        ("Step 1: Learning the Dataset", "Understand physical attributes, audit missing values, scales of measurement, skewness & kurtosis.", C_BLUE_PRIMARY),
        ("Step 2: Non-ML Exploratory Analysis", "Pure visual discovery using standard academic plots (histograms, boxplots, GAM smoothers).", C_SLATE_DARK),
        ("Step 3: Statistical Hypothesis Testing", "Rigorously test relationships using Welch's t-test, Mann-Whitney U, Chi-Square, ANOVA, & VIF.", C_AMBER),
        ("Step 4: Statistically-Grounded Features", "Mathematically justify feature selection by effect size & strictly enforce Target Leakage Prevention.", C_GREEN),
        ("Step 5: Multi-Task Machine Learning", "5-fold cross-validated Classification (GBM, RF, LDA, CART, Logistic), Regression & K-Means.", C_RED),
        ("Step 6: Technical Innovation (igraph)", "Aviation network modeling: Degree, Betweenness, Google PageRank, & Louvain Communities.", C_BLUE_PRIMARY)
    ]
    for k, (stitle, sdesc, scol) in enumerate(steps):
        row = k // 3
        col = k % 3
        bx = Inches(0.8 + col * 3.95)
        by = Inches(1.6 + row * 2.5)

        b_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.8), Inches(2.25))
        b_card.fill.solid()
        b_card.fill.fore_color.rgb = C_WHITE
        b_card.line.color.rgb = C_BORDER
        b_card.line.width = Pt(1)

        b_box = s3.shapes.add_textbox(bx + Inches(0.15), by + Inches(0.15), Inches(3.5), Inches(1.95))
        btf = b_box.text_frame
        btf.word_wrap = True
        bp1 = btf.paragraphs[0]
        bp1.text = stitle
        bp1.font.size = Pt(13)
        bp1.font.bold = True
        bp1.font.color.rgb = scol

        bp2 = btf.add_paragraph()
        bp2.text = sdesc
        bp2.font.size = Pt(10.5)
        bp2.font.color.rgb = C_SLATE_DARK
        bp2.space_before = Pt(8)

    add_notes(s3, "Saanvi: Thank you, Chirag. To answer our research question, we adhered strictly to our faculty guide Mrs. Vijayalakshmi's instructions by structuring our study into a rigorous 6-step analytical workflow: learning the dataset first, performing non-ML exploratory analysis, conducting formal hypothesis testing, scientifically justifying feature engineering, training machine learning models, and delivering network innovation with igraph.")

    # ==========================================================================
    # SLIDE 4: Dataset Architecture & Data Quality Audit (Saanvi - 1:00 min)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Step 1: Dataset Architecture & Data Quality Audit", "Data Profiling", "Saanvi Gupta", "24BDS1023", "1:00 min", 4)

    # Left: Database & Cleaning
    d_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    d_card.fill.solid()
    d_card.fill.fore_color.rgb = C_WHITE
    d_card.line.color.rgb = C_BORDER
    d_box = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.4), Inches(5.0))
    dtf = d_box.text_frame
    dtf.word_wrap = True

    dp1 = dtf.paragraphs[0]
    dp1.text = "1. SQLite Relational Database (skyconnect.db)"
    dp1.font.size = Pt(13)
    dp1.font.bold = True
    dp1.font.color.rgb = C_NAVY_DARK

    dp2 = dtf.add_paragraph()
    dp2.text = "• Ingested 67,663 global routes and 4,569 commercial airports.\n• Joined OurAirports infrastructure (runway dimensions, surface, elevation) with OpenFlights route topology."
    dp2.font.size = Pt(11)
    dp2.font.color.rgb = C_SLATE_DARK

    dp3 = dtf.add_paragraph()
    dp3.text = "2. Resolving the North America ('NA') Trap"
    dp3.font.size = Pt(13)
    dp3.font.bold = True
    dp3.font.color.rgb = C_RED
    dp3.space_before = Pt(10)

    dp4 = dtf.add_paragraph()
    dp4.text = "• Standard R read_csv parses 'NA' as NA_character_.\n• We enforced a continent repair script preserving North America's 1,349 airports from being dropped."
    dp4.font.size = Pt(11)
    dp4.font.color.rgb = C_SLATE_DARK

    dp5 = dtf.add_paragraph()
    dp5.text = "3. Missing Value Imputation & Outlier Audit"
    dp5.font.size = Pt(13)
    dp5.font.bold = True
    dp5.font.color.rgb = C_BLUE_PRIMARY
    dp5.space_before = Pt(10)

    dp6 = dtf.add_paragraph()
    dp6.text = "• Imputed 47 missing elevations via continental medians.\n• Audited Tukey's 1.5×IQR outliers: 11.0% elevation outliers, 13.9% route outliers (extreme skewness)."
    dp6.font.size = Pt(11)
    dp6.font.color.rgb = C_SLATE_DARK

    # Right: Data Quality Table
    t_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    t_card.fill.solid()
    t_card.fill.fore_color.rgb = C_WHITE
    t_card.line.color.rgb = C_BORDER

    t_box = s4.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.0))
    ttf = t_box.text_frame
    ttf.word_wrap = True
    tp1 = ttf.paragraphs[0]
    tp1.text = "DATA QUALITY AUDIT & SCALE CLASSIFICATION"
    tp1.font.size = Pt(12)
    tp1.font.bold = True
    tp1.font.color.rgb = C_AMBER

    tp2 = ttf.add_paragraph()
    tp2.text = "Variable             | Type       | Scale of Measurement | Missing\n--------------------------------------------------------------\nairport_ident        | character  | Identifier / Text    | 0 (0.0%)\niata_code            | character  | Identifier / Text    | 0 (0.0%)\nairport_type         | character  | Categorical Nominal  | 0 (0.0%)\nlatitude_deg         | numeric    | Continuous Ratio     | 0 (0.0%)\nlongitude_deg        | numeric    | Continuous Ratio     | 0 (0.0%)\nelevation_ft         | numeric    | Continuous Ratio     | 47 (1.0%)\ncontinent            | character  | Categorical Nominal  | 0 (0.0%)\nnum_runways          | integer    | Discrete Ratio       | 0 (0.0%)\nmax_runway_length    | numeric    | Continuous Ratio     | 0 (0.0%)\nhas_paved_runway     | binary     | Binary Nominal       | 0 (0.0%)\ntotal_routes         | integer    | Discrete Ratio       | 0 (0.0%)"
    tp2.font.size = Pt(9.5)
    tp2.font.color.rgb = C_NAVY_DARK
    tp2.space_before = Pt(8)

    tp3 = ttf.add_paragraph()
    tp3.text = "Key Takeaway: The analytical cohort is 100% complete across all 4,508 operational commercial facilities."
    tp3.font.size = Pt(10.5)
    tp3.font.bold = True
    tp3.font.color.rgb = C_GREEN
    tp3.space_before = Pt(12)

    add_notes(s4, "Saanvi: In Step 1, we executed a rigorous Data Quality Audit. We extracted 4,569 commercial airports from our SQLite database. Every variable was classified by its formal scale of measurement. We resolved the critical North America continent code trap where the two-letter ISO code 'NA' was improperly read as missing. We imputed 47 missing elevation records using continent-specific medians, and audited distribution skewness and extreme outliers using Tukey's 1.5 times Interquartile Range rule.")

    # ==========================================================================
    # SLIDE 5: EDA 1: Runway Normality & Elevation Skewness (Chirag - 1:05 min)
    # ==========================================================================
    create_split_slide(
        title="Step 2: Runway Length Distribution & Elevation Skewness",
        category="Exploratory Data Analysis (Non-ML)",
        speaker_name="Chirag Asija", speaker_id="24BDS1073", speaker_time="1:05 min", slide_num=5,
        bullets=[
            ("1. Runway Length: Parametric Normality Curve",
             "Max runway length averages 7,669 ft (SD = 2,770 ft). The empirical distribution exhibits bimodality: a primary peak at 6,000 ft (regional feeder airfields) and a secondary peak at 11,000 ft (wide-body intercontinental operations). Overall skewness is mild at 0.07."),
            ("2. Elevation: Extreme Positive Skewness",
             "Elevation exhibits massive right-skewness of 2.94 and excess kurtosis of 11.41. 75% of commercial airports operate below 1,276 ft, but high-altitude exceptions reach 14,472 ft in mountainous regions (e.g., Daocheng Yading in Tibet, El Alto in Bolivia)."),
            ("3. Physical Infrastructure Takeaway",
             "Runway lengths allow parametric modeling, whereas elevation requires non-parametric ranking due to heavy-tailed kurtosis.")
        ],
        image_filename="01_runway_length_distribution.png",
        stat_cards=[
            ("MEAN RUNWAY", "7,670 ft", "SD = 2,770 ft"),
            ("SKEWNESS", "0.07", "Near-symmetric"),
            ("ELEVATION KURT", "11.41", "Heavy-tailed peak")
        ],
        notes="Chirag: Moving to Step 2: Exploratory Data Analysis without any machine learning. Looking at Figure 1, we plotted the distribution of maximum runway lengths overlaid with a parametric Gaussian curve and kernel density estimation. Runway lengths follow a bimodal distribution with peaks at 6,000 feet for regional aviation and 11,000 feet for wide-body operations, showing slight positive skewness of 0.07. Airport elevation exhibits massive right-skewness of 2.94 and excess kurtosis of 11.41. Over 75% of airports sit below 1,276 feet, but extreme outliers reach 14,472 feet."
    )

    # ==========================================================================
    # SLIDE 6: EDA 2: Airport Classification & Route Non-Linearity (Chirag - 1:00 min)
    # ==========================================================================
    create_split_slide(
        title="Step 2: Airport Classification Boxplot & Route Inflection Point",
        category="Exploratory Data Analysis (Non-ML)",
        speaker_name="Chirag Asija", speaker_id="24BDS1073", speaker_time="1:00 min", slide_num=6,
        bullets=[
            ("1. Runway Boxplots by Airport Classification",
             "Figure 3 demonstrates a massive physical divide: Large airports maintain a median runway length of 10,170 ft (IQR: 8,800 - 11,800 ft), whereas Medium airports plateau at a median of 5,900 ft. Notched boxplot intervals do not overlap, demonstrating visual significance."),
            ("2. Non-Linear Route Inflection Point (GAM Smoother)",
             "Figure 5 reveals a steep non-linear threshold: facilities under 7,500 ft rarely support more than 20 routes. Once runway length crosses 10,000 ft (enabling fully-laden Boeing 777/A350 departures), route connectivity increases exponentially."),
            ("3. Academic Proof",
             "This non-linear inflection provides visual evidence that physical infrastructure dictates route capacity.")
        ],
        image_filename="03_runway_by_airport_type_boxplot.png",
        stat_cards=[
            ("LARGE APT MEDIAN", "10,170 ft", "Wide-body capable"),
            ("MEDIUM MEDIAN", "5,900 ft", "Regional turboprops"),
            ("THRESHOLD", "10,000 ft", "Exponential routes")
        ],
        notes="Chirag: In Figure 3, our notched boxplots show a massive physical divide: large international airports maintain median runway lengths exceeding 10,000 feet, whereas medium airports plateau around 6,000 feet. The non-overlapping notches indicate that this physical difference is highly significant. In Figure 5, our generalized additive model smoother reveals a steep non-linear inflection point: airports under 7,500 feet rarely support more than 20 routes, but once runway length exceeds 10,000 feet, connectivity explodes."
    )

    # ==========================================================================
    # SLIDE 7: EDA 3: Continental Infrastructure Breakdown (Saanvi - 1:00 min)
    # ==========================================================================
    create_split_slide(
        title="Step 2: Continental Infrastructure Disparities & Variances",
        category="Exploratory Data Analysis (Non-ML)",
        speaker_name="Saanvi Gupta", speaker_id="24BDS1023", speaker_time="1:00 min", slide_num=7,
        bullets=[
            ("1. Regional Imbalance in Aviation Infrastructure",
             "Figure 4 highlights global infrastructure disparity: Asia and Europe operate the longest average commercial runways (means of 8,600 ft and 8,100 ft), driven by wide-body international trunk corridors."),
            ("2. Oceania & South America Disadvantage",
             "Oceania operates the shortest average commercial runways (mean = 5,865 ft), reflecting archipelago island-hopping operations and regional turboprop reliance."),
            ("3. North America Density vs Diversity",
             "North America possesses the largest absolute number of commercial facilities (N = 1,349), but exhibits wide variance between regional general aviation strips and massive multi-runway hubs like Dallas-Fort Worth and Chicago O'Hare.")
        ],
        image_filename="04_continental_infrastructure_breakdown.png",
        stat_cards=[
            ("ASIA MEAN", "8,600 ft", "Intercontinental lead"),
            ("OCEANIA MEAN", "5,865 ft", "Archipelago hops"),
            ("NORTH AMERICA", "1,349 apts", "Largest volume")
        ],
        notes="Saanvi: Continuing our exploratory analysis, Figure 4 examines continental infrastructure disparities with 95% confidence intervals. Asia and Europe lead the world with the longest average commercial runways, while Oceania and South America operate shorter runways suited for regional hops. North America possesses the largest absolute number of commercial facilities (1,349), but exhibits wide variance between small regional strips and massive multi-runway hubs like Dallas and Chicago."
    )

    # ==========================================================================
    # SLIDE 8: Statistical Hypothesis Testing 1: Parametric Tests (Chirag - 1:15 min)
    # ==========================================================================
    create_split_slide(
        title="Step 3: Parametric Welch's t-test & Mann-Whitney U Tests",
        category="Statistical Hypothesis Testing",
        speaker_name="Chirag Asija", speaker_id="24BDS1073", speaker_time="1:15 min", slide_num=8,
        bullets=[
            ("Test 1: Welch's Two-Sample t-test on Runway Length",
             "• Null Hypothesis H0: Mean runway length of Hubs = Mean of Regular Airports.\n• Result: t = -36.31, df = 756.6, p-value = 6.44 × 10^-168.\n• Finding: Mean Regular = 7,391 ft vs Mean Hub = 10,749 ft.\n• Effect Size: Cohen's d = 1.39 (Extremely Large Effect). Decisive rejection of H0."),
            ("Test 2: Mann-Whitney U Test on Number of Runways",
             "• Non-parametric evaluation for discrete counts.\n• Result: W = 691,602, p-value = 1.80 × 10^-45. Rank-Biserial r = 0.48.\n• Hubs require multi-runway configurations to manage simultaneous flight movements."),
            ("Test 3: Mann-Whitney U Test on Airport Elevation",
             "• Result: W = 1,209,563, p-value = 4.32 × 10^-11 (Small effect size).")
        ],
        image_filename="06_runway_length_ttest_boxplot.png",
        stat_cards=[
            ("WELCH'S t", "-36.31", "p = 6.44e-168"),
            ("COHEN'S d", "1.39", "Large Effect Size"),
            ("MANN-WHITNEY", "W = 691,602", "p = 1.80e-45")
        ],
        notes="Chirag: In Step 3, we subjected our observations to rigorous inferential statistics to test five formal hypotheses. Hypothesis 1: We hypothesized that international hubs require significantly longer runways than non-hubs. Because variances between groups were unequal, we conducted Welch's Two-Sample t-test. As shown in Figure 6, with a t-statistic of -36.31 and a p-value of 6.44 times 10 to the negative 168, we decisively rejected the null hypothesis. Major hubs average 10,749 feet compared to 7,391 feet for regular airports, with a Cohen's d of 1.39, representing a massive effect size. Mann-Whitney U tests also proved hubs require multi-runway configurations at p = 1.8 times 10 to the negative 45."
    )

    # ==========================================================================
    # SLIDE 9: Statistical Hypothesis Testing 2: ANOVA & Independence (Saanvi - 1:15 min)
    # ==========================================================================
    create_split_slide(
        title="Step 3: Categorical Chi-Square & One-Way Continental ANOVA",
        category="Statistical Hypothesis Testing",
        speaker_name="Saanvi Gupta", speaker_id="24BDS1023", speaker_time="1:15 min", slide_num=9,
        bullets=[
            ("Test 4: Pearson's Chi-Square Test of Independence",
             "• Airport Classification vs Hub Status: χ² = 1,501.7, df = 1, p < 2.2 × 10^-16, Cramér's V = 0.58 (Exceptionally strong association).\n• Paved Runway vs Hub Status: χ² = 16.07, df = 1, p = 6.11 × 10^-5. 99.7% of hubs feature paved surfaces vs 87.2% of non-hubs."),
            ("Test 5: One-Way ANOVA across 6 Continents",
             "• Model: max_runway_length ~ continent (Figure 7).\n• Result: F(5, 4502) = 102.42, p-value = 1.27 × 10^-102.\n• Eta-Squared η² = 0.102 (10.2% of global runway variance is dictated by continental geography alone).\n• Post-Hoc Tukey HSD: Confirmed Asia & Europe differ significantly from Oceania & South America (p_adj < 0.001).")
        ],
        image_filename="07_anova_continental_runway_cis.png",
        stat_cards=[
            ("CHI-SQUARE χ²", "1,501.7", "Cramér's V = 0.58"),
            ("ANOVA F", "102.42", "p = 1.27e-102"),
            ("ETA-SQUARED", "10.2%", "Continental variance")
        ],
        notes="Saanvi: Thank you, Chirag. Hypothesis 3 evaluated categorical independence using Pearson's Chi-Square Test. The association between physical airport classification and hub status yielded a chi-square of 1,501.7 with a Cramér's V of 0.58, confirming an exceptionally strong relationship. In Hypothesis 4, we conducted a One-Way ANOVA across all six continents. The test returned an F-statistic of 102.42 with a p-value of 1.27 times 10 to the negative 102 and an eta-squared of 0.102. This proves that 10.2% of global runway variance is dictated purely by continental geography."
    )

    # ==========================================================================
    # SLIDE 10: Multicollinearity Diagnostics & Correlation (Saanvi - 1:00 min)
    # ==========================================================================
    create_split_slide(
        title="Step 3: Multicollinearity Diagnostics & Correlation Matrix",
        category="Statistical Hypothesis Testing",
        speaker_name="Saanvi Gupta", speaker_id="24BDS1023", speaker_time="1:00 min", slide_num=10,
        bullets=[
            ("1. Pearson Correlation Matrix Heatmap (Figure 8)",
             "• Evaluated linear collinearity across all physical infrastructure metrics.\n• Highest pairwise correlation: max_runway_length and num_runways (r = 0.31), representing a healthy, non-redundant relationship.\n• Elevation exhibits minimal correlation with runway length (r = -0.04), indicating independent variation across global topographies."),
            ("2. Variance Inflation Factors (VIF) Audit",
             "• Tested: max_runway_length (1.10), num_runways (1.14), elevation_ft (1.05), latitude (1.09), longitude (1.13).\n• Max VIF = 1.14, strictly below the collinearity threshold of 5.0.\n• Proof: Predictors are completely non-redundant and stable for machine learning.")
        ],
        image_filename="08_correlation_matrix_heatmap.png",
        stat_cards=[
            ("MAX PAIRWISE r", "0.31", "Runway & Counts"),
            ("MAX VIF", "1.14", "Threshold < 5.0"),
            ("COLLINEARITY", "ZERO", "Stable Predictors")
        ],
        notes="Saanvi: In Hypothesis 5, we evaluated multicollinearity. Looking at Figure 8, the highest pairwise correlation is between runway length and runway count at r = 0.31, representing a healthy relationship. Furthermore, we computed Variance Inflation Factors across all candidate numerical predictors. All VIF scores remained strictly below 1.15, well under the multicollinearity threshold of 5.0, proving zero redundancy among our features and guaranteeing numerical stability for ML."
    )

    # ==========================================================================
    # SLIDE 11: Feature Engineering & Target Leakage Prevention (Chirag - 1:00 min)
    # ==========================================================================
    create_split_slide(
        title="Step 4: Statistically-Grounded Feature Selection & Leakage Prevention",
        category="Feature Engineering",
        speaker_name="Chirag Asija", speaker_id="24BDS1073", speaker_time="1:00 min", slide_num=11,
        bullets=[
            ("1. Mathematical Basis for Feature Selection",
             "Mandated by our faculty guide: On what scientific basis were features selected? We constructed a formal Justification Matrix (Figure 9) ranking predictors by p-value (p < 0.001) and effect size (Cohen's d = 1.39, Cramér's V = 0.58)."),
            ("2. Strict Target Leakage Prevention (Crucial Requirement)",
             "• In our database, total_routes is an operational outcome of being a hub.\n• If total_routes were included to predict hub status, the model would suffer from trivial target leakage and fail in real-world planning.\n• We strictly EXCLUDED total_routes from the modeling feature matrix!"),
            ("3. Final Feature Matrix (4,508 Operational Airports)",
             "Predictors: max_runway_length, num_runways, has_paved_runway, airport_type, elevation_ft, latitude_deg, longitude_deg, continent.")
        ],
        image_filename="09_statistical_feature_ranking.png",
        stat_cards=[
            ("TARGET LEAKAGE", "0% LEAKAGE", "total_routes excluded"),
            ("PRIMARY DRIVER", "Runway Length", "Cohen's d = 1.39"),
            ("TRAIN/TEST SPLIT", "80 / 20", "Stratified Partition")
        ],
        notes="Chirag: Step 4 answers the critical question mandated by our faculty guide: On what scientific basis were features selected? Instead of picking predictors randomly, we constructed a formal Feature Justification Matrix, visualized in Figure 9. Predictors were mathematically ranked using their statistical p-values, Cohen's d, and Cramér's V effect sizes. Most importantly, we enforced strict Target Leakage Prevention. Total routes is an operational outcome of being a hub; including it would cause trivial target leakage. We strictly excluded route counts, forcing models to learn solely from physical infrastructure and geography."
    )

    # ==========================================================================
    # SLIDE 12: Machine Learning Methodology & Architecture (Saanvi - 1:00 min)
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Step 5: Multi-Task Machine Learning Suite Architecture", "ML Methodology", "Saanvi Gupta", "24BDS1023", "1:00 min", 12)

    ml_cards = [
        ("TASK 1: SUPERVISED CLASSIFICATION",
         "Objective: Predict Hub Status (Hub vs Regular) without knowing flight counts.\n\n5 Algorithms Benchmarked:\n• Gradient Boosting Machine (GBM)\n• Random Forest (500 trees)\n• Logistic Regression\n• Linear Discriminant Analysis (LDA)\n• Decision Trees (CART)\n\nValidation: 5-Fold Stratified Cross-Validation on 3,608 training airports, tested on 900 unseen holdout airports.",
         C_BLUE_PRIMARY),
        ("TASK 2: SUPERVISED REGRESSION",
         "Objective: Predict physical runway length requirements from geographic coordinates and airport classification.\n\nAlgorithm: Multiple Linear Regression\nFormula: max_runway_length ~ airport_type + continent + elevation_ft + latitude + longitude\n\nValidation: 4-panel regression diagnostic analysis (Residuals vs Fitted, Normal Q-Q, Scale-Location, Cook's Leverage).",
         C_AMBER),
        ("TASK 3: UNSUPERVISED CLUSTERING",
         "Objective: Discover natural airport archetypes using unsupervised geometry.\n\nAlgorithm: K-Means Clustering\nCluster Selection: Within-Cluster Sum of Squares (WCSS) Elbow & Silhouette analysis (Optimal K = 3).\n\nDiscovered Archetypes:\n1. Global Megahubs\n2. Regional Gateways\n3. Domestic Feeder Airfields",
         C_GREEN)
    ]
    for idx, (mtitle, mdesc, mcol) in enumerate(ml_cards):
        cx = Inches(0.8 + idx * 3.95)
        mshape = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.6), Inches(3.8), Inches(4.8))
        mshape.fill.solid()
        mshape.fill.fore_color.rgb = C_WHITE
        mshape.line.color.rgb = C_BORDER
        mshape.line.width = Pt(1)

        hbar = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.2), Inches(1.8), Inches(3.4), Inches(0.35))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = mcol
        hbar.line.fill.background()
        htf = hbar.text_frame
        hp = htf.paragraphs[0]
        hp.text = mtitle.split(":")[0]
        hp.font.size = Pt(10)
        hp.font.bold = True
        hp.font.color.rgb = C_WHITE
        hp.alignment = PP_ALIGN.CENTER

        mbox = s12.shapes.add_textbox(cx + Inches(0.2), Inches(2.3), Inches(3.4), Inches(3.9))
        mtf = mbox.text_frame
        mtf.word_wrap = True
        mp1 = mtf.paragraphs[0]
        mp1.text = mtitle.split(":")[1].strip()
        mp1.font.size = Pt(13)
        mp1.font.bold = True
        mp1.font.color.rgb = C_NAVY_DARK

        mp2 = mtf.add_paragraph()
        mp2.text = mdesc
        mp2.font.size = Pt(10)
        mp2.font.color.rgb = C_SLATE_DARK
        mp2.space_before = Pt(8)

    add_notes(s12, "Saanvi: With our features mathematically vetted, Step 5 deployed an end-to-end Machine Learning suite. We partitioned our 4,508 operational commercial airports into an 80% stratified training set of 3,608 airports and a 20% unseen holdout test set of 900 airports. We framed a multi-task learning architecture: Supervised Classification comparing 5 distinct algorithms with 5-fold cross-validation, Supervised Multiple Linear Regression predicting physical runway requirements, and Unsupervised K-Means clustering to discover natural airport archetypes.")

    # ==========================================================================
    # SLIDE 13: Supervised Classification Results & Champion Model (Chirag - 1:15 min)
    # ==========================================================================
    create_split_slide(
        title="Step 5: Classification Leaderboard & Champion Model (GBM)",
        category="Machine Learning Results",
        speaker_name="Chirag Asija", speaker_id="24BDS1073", speaker_time="1:15 min", slide_num=13,
        bullets=[
            ("1. Multi-Model Benchmark on 900 Unseen Holdout Airports",
             "• Gradient Boosting Machine (GBM): Accuracy = 92.0%, Specificity = 97.6%, AUC = 0.9437 (CHAMPION).\n• Random Forest (500 trees): Accuracy = 91.8%, Specificity = 96.9%, AUC = 0.9322.\n• Logistic Regression: Accuracy = 89.2%, AUC = 0.9124.\n• Linear Discriminant Analysis (LDA): Accuracy = 88.6%, AUC = 0.9080.\n• Decision Tree (CART): Accuracy = 89.0%, AUC = 0.8415."),
            ("2. Confusion Matrix Diagnostics (Figure 11)",
             "On the 900 holdout airports, GBM achieved 778 True Negatives, 50 True Positives, with only 19 False Positives (high specificity prevents misallocating infrastructure investment)."),
            ("3. Feature Importance (Figure 12)",
             "Airport type (51.2%), max runway length (24.8%), and runway count (11.5%) drive over 87% of predictive power.")
        ],
        image_filename="10_classification_model_leaderboard.png",
        stat_cards=[
            ("GBM ACCURACY", "92.0%", "Holdout N = 900"),
            ("GBM SPECIFICITY", "97.6%", "778 / 797 TN"),
            ("CHAMPION AUC", "0.9437", "Outstanding Discrim.")
        ],
        notes="Chirag: Evaluating on our 900 unseen holdout airports yielded outstanding results, shown in Figures 10, 11, and 12. Our champion model was the Gradient Boosting Machine, achieving an overall accuracy of 92.0%, a specificity of 97.6%, and an Area Under the ROC Curve of 0.9437. Random Forest followed closely with an AUC of 0.9322. Feature importance diagnostics in Figure 12 confirmed that physical airport classification, maximum runway length, and runway count contributed over 87% of predictive power."
    )

    # ==========================================================================
    # SLIDE 14: Regression Diagnostics & K-Means Clusters (Chirag - 1:00 min)
    # ==========================================================================
    create_split_slide(
        title="Step 5: Runway Length Regression & K-Means Archetypes",
        category="Machine Learning Results",
        speaker_name="Chirag Asija", speaker_id="24BDS1073", speaker_time="1:00 min", slide_num=14,
        bullets=[
            ("1. Multiple Linear Regression for Runway Requirements",
             "• Formula: max_runway_length ~ airport_type + continent + elevation_ft + lat + lon.\n• Performance: R² = 0.455, Adjusted R² = 0.454, F(10, 4497) = 376.1, p < 10^-300.\n• Residual Diagnostics (Figure 13): Residuals show homoscedastic dispersion and Normal Q-Q alignment across operational ranges."),
            ("2. K-Means Cluster Archetypes (Figure 14, Optimal K = 3)",
             "• Cluster 1: Global Megahubs (N = 514) — Mean Runway 10,800 ft, Multi-runway, Mean 180 routes.\n• Cluster 2: Regional Gateways (N = 1,420) — Mean Runway 8,200 ft, Paved, Mean 32 routes.\n• Cluster 3: Domestic Feeder Airfields (N = 2,574) — Mean Runway 5,600 ft, Single runway, Local hops.")
        ],
        image_filename="14_kmeans_cluster_archetypes.png",
        stat_cards=[
            ("REGRESSION R²", "0.455", "F = 376.1, p < 1e-300"),
            ("OPTIMAL CLUSTERS", "K = 3", "Megahubs / Gateways"),
            ("RESIDUAL DIAG", "Normal Q-Q", "Homoscedastic")
        ],
        notes="Chirag: In our regression analysis, our multiple linear regression model predicted runway length with an R-squared of 0.455 and F-statistic of 376.1. The diagnostic residual panels confirmed that the normality and homoscedasticity assumptions held true. Furthermore, K-Means clustering with K = 3 naturally grouped airports into three distinct archetypes: Global Intercontinental Megahubs, Regional Gateways, and Domestic Feeder Airfields."
    )

    # ==========================================================================
    # SLIDE 15: Technical Innovation: Aviation Network Graph Analysis (Saanvi - 1:15 min)
    # ==========================================================================
    create_split_slide(
        title="Step 6: Technical Innovation — igraph Aviation Network Analysis",
        category="Technical Complexity",
        speaker_name="Saanvi Gupta", speaker_id="24BDS1023", speaker_time="1:15 min", slide_num=15,
        bullets=[
            ("1. Modeling Aviation as a Mathematical Graph (igraph)",
             "Modeled 66,288 directed route edges across 3,388 vertex airports. Directly satisfies the university rubric for analytical innovation."),
            ("2. Graph Centrality Findings (Figures 15 & 17)",
             "• Degree Centrality: Frankfurt (FRA, 990), Paris CDG (966), Atlanta (ATL, 924) lead in direct connections.\n• Betweenness Centrality: Identified Anchorage, Alaska (ANC, 0.0702) and Dubai (DXB, 0.0388) as the critical global bridges connecting disparate continents.\n• Google PageRank: Atlanta (0.0076) and Chicago (0.0068) represent the most authoritative global transit nodes."),
            ("3. Louvain Community Detection (Figure 18)",
             "Discovered continental airline alliance sub-networks with a high modularity Q of 0.66.")
        ],
        image_filename="17_betweenness_vs_pagerank_scatter.png",
        stat_cards=[
            ("TOP BRIDGE", "Anchorage (ANC)", "Betweenness = 0.0702"),
            ("TOP PAGERANK", "Atlanta (ATL)", "PR = 0.0076"),
            ("MODULARITY Q", "0.66", "Louvain Alliance Clust.")
        ],
        notes="Saanvi: For our project's technical innovation—earning top marks for analytical complexity—we modeled global aviation as an authentic Mathematical Network Graph using the igraph package in R, covering 66,288 directed routes. As shown in Figures 15 through 18, we computed Degree Centrality where Frankfurt and Paris lead, Betweenness Centrality which identified Anchorage, Alaska and Dubai as critical bridges connecting East-West transit, Google PageRank where Atlanta and Chicago emerged as most authoritative, and Louvain Community Detection which discovered airline alliance sub-networks with modularity Q = 0.66."
    )

    # ==========================================================================
    # SLIDE 16: LIVE DEMO: Automated Pipeline & Leaflet Map (Both - 2:00 min)
    # ==========================================================================
    create_split_slide(
        title="Step 7: Live Demonstration — Dual RStudio Plots & Interactive Leaflet Map",
        category="Live Demonstration",
        speaker_name="Chirag & Saanvi", speaker_id="Both", speaker_time="2:00 min", slide_num=16,
        bullets=[
            ("1. Part A: RStudio Plots Pane (Publication Static Map)",
             "• Figure 19 renders directly in RStudio Plots Pane via ggplot2.\n• Plots 1,599 flight corridors (742 global intercontinental corridors in crimson red + 857 Indian domestic & international gateway routes in vibrant amber).\n• Hub circles sized proportionally to route capacity."),
            ("2. Part B: RStudio Viewer Pane (Interactive Leaflet Map)",
             "• 100% Free OpenStreetMap & Esri Topographic tiles (zero API key watermarks).\n• Toggleable layers: Indian Routes, Global Corridors, Indian Airports, Major Global Hubs, Regional Facilities.\n• Rich HTML popups display: IATA, route count, runway dimensions, elevation, and hub status on click."),
            ("3. Single Command Reproducibility",
             "Running source('R/00_run_complete_pipeline.R') executes all 7 scripts in under 70 seconds.")
        ],
        image_filename="19_global_flight_routes_map.png",
        stat_cards=[
            ("FLIGHT ARCS", "1,599 routes", "857 Indian + 742 Global"),
            ("LEAFLET TILES", "OpenStreetMap", "100% Free & Open"),
            ("RUN TIME", "< 70 seconds", "Complete pipeline")
        ],
        notes="Chirag: Now we transition to our live demo. In RStudio, running source('R/00_run_complete_pipeline.R') reproduces our entire analytical pipeline sequentially in under 70 seconds. The static publication map in Figure 19 renders in the Plots pane.\n\nSaanvi: And in the Viewer pane, our interactive Leaflet map allows users to explore 1,599 flight corridors across every continent. Zooming into India shows full domestic trunk routes and international connections to London, New York, Frankfurt, and Dubai with rich interactive HTML popups."
    )

    # ==========================================================================
    # SLIDE 17: GitHub Repository Walkthrough (Chirag - 0:30 min)
    # ==========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "Project Architecture & Reproducible GitHub Repository", "Reproducibility", "Chirag Asija", "24BDS1073", "0:30 min", 17)

    gh_dirs = [
        ("📁 R/", "Modular pipeline scripts:\n• 00_run_complete_pipeline.R\n• 01_dataset_profiling_and_quality.R\n• 02_exploratory_data_analysis.R\n• 03_statistical_hypothesis_testing.R\n• 04_feature_engineering.R\n• 05_machine_learning_suite.R\n• 06_network_graph_analysis.R\n• 07_interactive_leaflet_map.R"),
        ("📁 database/ & data/", "• database/skyconnect.db (17MB SQLite)\n• data/raw/ (OpenFlights & OurAirports)\n• data/processed/ (cohorts & partitions)\n• train_features.csv (3,608 rows)\n• test_features.csv (900 rows)"),
        ("📁 visualizations/ & results/", "• 19 Publication-grade 300-DPI Figures\n• 19_interactive_global_aviation_map.html\n• 10 CSV result tables:\n  - data_quality_audit.csv\n  - statistical_test_results.csv\n  - classification_metrics.csv\n  - feature_justification_matrix.csv"),
        ("📁 models/ & report/", "• Serialized R models (.rds files):\n  - model_gbm.rds\n  - model_random_forest.rds\n  - model_logistic.rds\n  - model_lda.rds\n  - model_decision_tree.rds\n• Presentation script & viva guide")
    ]
    for idx, (gtitle, gdesc) in enumerate(gh_dirs):
        gx = Inches(0.8 + idx * 2.95)
        gshape = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, gx, Inches(1.6), Inches(2.85), Inches(4.8))
        gshape.fill.solid()
        gshape.fill.fore_color.rgb = C_WHITE
        gshape.line.color.rgb = C_BORDER
        gshape.line.width = Pt(1)

        gbox = s17.shapes.add_textbox(gx + Inches(0.15), Inches(1.75), Inches(2.55), Inches(4.4))
        gtf = gbox.text_frame
        gtf.word_wrap = True
        gp1 = gtf.paragraphs[0]
        gp1.text = gtitle
        gp1.font.size = Pt(13)
        gp1.font.bold = True
        gp1.font.color.rgb = C_BLUE_PRIMARY

        gp2 = gtf.add_paragraph()
        gp2.text = gdesc
        gp2.font.size = Pt(10)
        gp2.font.color.rgb = C_SLATE_DARK
        gp2.space_before = Pt(8)

    add_notes(s17, "Chirag: Our project is hosted under a clean, industry-standard modular repository structure. The R/ directory contains all 7 modular pipeline scripts. The database/ folder houses our 17MB SQLite database. The visualizations/ folder contains all 19 high-resolution 300-DPI publication figures plus the standalone interactive HTML map. The results/ folder stores all exported CSV tables for statistical tests, VIF, and ML metrics. And our comprehensive README details reproducible execution instructions.")

    # ==========================================================================
    # SLIDE 18: Academic Conclusions & Acknowledgements (Saanvi - 0:45 min)
    # ==========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18, RGBColor(15, 23, 42))

    # Accent Stripe
    stripe18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    stripe18.fill.solid()
    stripe18.fill.fore_color.rgb = C_AMBER
    stripe18.line.fill.background()

    c_box18 = s18.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.5))
    ctf18 = c_box18.text_frame
    ctf18.word_wrap = True

    cp1 = ctf18.paragraphs[0]
    cp1.text = "ACADEMIC CONCLUSIONS & RESEARCH TAKEAWAYS"
    cp1.font.size = Pt(26)
    cp1.font.bold = True
    cp1.font.color.rgb = RGBColor(248, 250, 252)

    concl_points = [
        ("1. Physical Infrastructure is Definitive", "Welch's t-test (p < 10^-167) and Chi-Square (p < 10^-16) mathematically prove that runway dimensions and paved surfaces dictate global hub viability."),
        ("2. Continental Inequality is Statistically Significant", "One-Way ANOVA (F = 102.42, p < 10^-101) confirms that geography drives 10.2% of global runway variance, revealing systematic disparities in Africa and Oceania."),
        ("3. High-Accuracy Prediction with Zero Target Leakage", "By excluding total_routes, our Gradient Boosting Machine predicted international hub status with 92.0% accuracy, 97.6% specificity, and AUC = 0.9437 purely from civil engineering features."),
        ("4. Network Topology Identifies Critical Bridges", "igraph Betweenness analysis proved that transit bridges like Anchorage and Dubai are as vital to global aviation as mega-origin hubs like Atlanta and London Heathrow.")
    ]
    for ctitle, cdesc in concl_points:
        cp_title = ctf18.add_paragraph()
        cp_title.text = ctitle
        cp_title.font.size = Pt(13)
        cp_title.font.bold = True
        cp_title.font.color.rgb = RGBColor(254, 215, 170)
        cp_title.space_before = Pt(10)

        cp_sub = ctf18.add_paragraph()
        cp_sub.text = cdesc
        cp_sub.font.size = Pt(11)
        cp_sub.font.color.rgb = RGBColor(203, 213, 225)

    thanks_box = s18.shapes.add_textbox(Inches(1.0), Inches(6.4), Inches(11.3), Inches(0.6))
    ttf18 = thanks_box.text_frame
    tp = ttf18.paragraphs[0]
    tp.text = "Sincere Gratitude to our Faculty Guide: Mrs. Vijayalakshmi | Presenters: Chirag Asija & Saanvi Gupta | Thank You!"
    tp.font.size = Pt(12)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor(147, 197, 253)
    tp.alignment = PP_ALIGN.CENTER

    add_notes(s18, "Saanvi: To conclude, our study conclusively demonstrates that physical airport infrastructure and geographic positioning are definitive determinants of global aviation hub viability. Our normal EDA and statistical tests proved that runway lengths (p < 10^-167) and continental location (p < 10^-101) establish physical operational thresholds, while our machine learning models proved that physical predictors alone predict hub status with 92% accuracy with zero target leakage. We express our sincere gratitude to our faculty guide, Mrs. Vijayalakshmi, for her invaluable guidance and rigorous academic standards throughout this capstone project. Thank you.")

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    viz_dir = "/Users/chiragasija/Downloads/SkyConnect_DA3 2/visualizations"
    out_dir = "/Users/chiragasija/Downloads/SkyConnect_DA3 2/report"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "SkyConnect_DA3_Presentation.pptx")
    create_deck(viz_dir, out_file)
