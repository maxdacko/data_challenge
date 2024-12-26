import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

data_dir = "data/output/"
assets_dir = "assets/"
output_pdf = "results/Allowance_Discrepancies_Report.pdf"
images_dir = "results/images"


# Load datasets
backend_discrepancies = pd.read_csv(f"{data_dir}backend_discrepancies.csv")
schedule_discrepancies = pd.read_csv(f"{data_dir}schedule_discrepancies.csv")
period_frequency_discrepancies = pd.read_csv(f"{data_dir}period_frequency_discrepancies.csv")

# Helper function to save plots

def save_plot(filename, title, x_data, y_data, x_label, y_label):
    plt.figure(figsize=(10, 6))
    plt.bar(x_data, y_data)
    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Create visualizations
period_discrepancies_summary = (
    period_frequency_discrepancies
    .groupby(['frequency', 'day'])
    .size()
    .reset_index(name='count')
    .sort_values(by="count", ascending=False)
)
save_plot(
    f"{images_dir}/period_discrepancies.png",
    "Period and Frequency Discrepancies by Day and Frequency",
    period_discrepancies_summary['day'] + " (" + period_discrepancies_summary['frequency'] + ")",
    period_discrepancies_summary['count'],
    "Day and Frequency",
    "Count of Discrepancies"
)

backend_discrepancies_summary = (
    backend_discrepancies
    .groupby(['frequency', 'day'])
    .size()
    .reset_index(name='count')
    .sort_values(by="count", ascending=False)
)
save_plot(
    f"{images_dir}/backend_discrepancies.png",
    "Backend Discrepancies by Day and Frequency",
    backend_discrepancies_summary['day'] + " (" + backend_discrepancies_summary['frequency'] + ")",
    backend_discrepancies_summary['count'],
    "Day and Frequency",
    "Count of Discrepancies"
)

schedule_discrepancies_summary = (
    schedule_discrepancies
    .groupby(['frequency', 'day'])
    .size()
    .reset_index(name='count')
    .sort_values(by="count", ascending=False)
    .head(10)
)
save_plot(
    f"{images_dir}/schedule_discrepancies.png",
    "Schedule Discrepancies by Day and Frequency",
    schedule_discrepancies_summary['day'] + " (" + schedule_discrepancies_summary['frequency'] + ")",
    schedule_discrepancies_summary['count'],
    "Day and Frequency",
    "Count of Discrepancies"
)

# Generate PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Add logo
pdf.image(f"{assets_dir}/64022cf362115a3f47fe43e6_modakgreen.png", x=75, y=20, w=60)
pdf.ln(40)

# Add title
pdf.set_font("Arial", size=16, style="B")
pdf.cell(0, 10, txt="Data Engineering Challenge: Allowance Day Discrepancies", ln=True, align='C')
pdf.ln(10)

# Add introductory image
pdf.image(f"{assets_dir}/66a8f5c6f7fe510887a0fbb0_our-solution-image.png", x=50, y=70, w=100)
pdf.ln(140)  # Adjust to position text below the image

# Add insights section
pdf.set_font("Arial", size=14, style="B")
pdf.cell(0, 10, txt="Index", ln=True)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, txt="1. Introduction", ln=True)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, txt="2. Findings and Insights", ln=True)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, txt="3. Hypotheses and Explanations", ln=True)

pdf.set_font("Arial", size=12)
pdf.cell(0, 10, txt="4. Recommendations", ln=True)
pdf.ln(50)

# Add insights section
pdf.set_font("Arial", size=14, style="B")
pdf.cell(0, 10, txt="Introduction", ln=True)
pdf.ln(10)

# Add insights section
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="The goal of this assessment is to help identify and understand discrepancies in the next_payment_day and payment_date fields across the backend datasets. These fields play a key role in ensuring that recurring allowances are scheduled correctly, and addressing the issues found will be critical for improving the reliability of this feature.\n"
                "To tackle this challenge, I chose to break down the main problem into smaller, more manageable subproblems. This approach allowed me to focus on specific aspects of the data and analyze each one thoroughly, ensuring no detail was overlooked.\n"
                "One key step in my process involved making some enhancements to the base datasets. For example, I added a new column to the allowance_events JSON file. By using the event timestamp, allowance frequency, and scheduled day, I calculated the next payment date for each user. This adjustment was essential to align the events data with the backend tables and uncover any inconsistencies in how payment schedules were being generated.\n"
                "To streamline this entire process, everything presented here was automated through Python scripts. This means that if we ever need to repeat this analysis in the future, we can simply run the app.py script, and the entire workflow, including the generation of this PDF, will be executed automatically. This ensures not only consistency in the results but also significant time savings for any future investigations.")
pdf.ln(120)

# Add insights section
pdf.set_font("Arial", size=14, style="B")
pdf.cell(0, 10, txt="Findings and Insights", ln=True)
pdf.ln(10)

# Add insights section
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt="Now we are going to review the insights found in the discrepancies datasets that I created in the previous step!\nTo do so, we will be analysing each dataset on its own:")
pdf.ln(5)

# Add visualizations with context
pdf.set_font("Arial", size=12)

# Period and Frequency Discrepancies
pdf.cell(0, 10, txt="1. Period and Frequency Discrepancies", ln=True)
pdf.image(f"{images_dir}/period_discrepancies.png", x=10, w=190)
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "Key Findings:\n"
    "- 453 records where the frequency and day from backend data, does not align with the one in Allowance Events.\n"
    "- Most frequent discrepancies occur in:\n"
    "  - Weekly allowances on Fridays (69 cases).\n"
    "  - Monthly allowances on the first day (65 cases).\n"
    "  - Biweekly allowances on Fridays (54 cases).\n"

))
pdf.ln(100)

# Backend Discrepancies
pdf.cell(0, 10, txt="2. Backend Discrepancies", ln=True)
pdf.image(f"{images_dir}/backend_discrepancies.png", x=10, w=190)
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "Key Findings:\n"
    "- 1,608 records with mismatches between `next_payment_day` and calculated values.\n"
    "- Similar patterns to Period and Frequency Discrepancies but with larger numbers:\n"
    "  - Monthly allowances on the first day (284 cases).\n"
    "  - Weekly allowances on Fridays (279 cases).\n"
    "  - Biweekly allowances on Fridays (278 cases).\n"

))
pdf.ln(100)

# Schedule Discrepancies
pdf.cell(0, 10, txt="3. Schedule Discrepancies", ln=True)
pdf.image(f"{images_dir}/schedule_discrepancies.png", x=10, w=190)
pdf.ln(5)
pdf.multi_cell(0, 10, txt=(
    "Key Findings:\n"
    "- 53 records where `payment_date` differs from `next_payment_day`.\n"
    "- Similiar patterns to the other datasets, with friday being the most common case\n"
))
pdf.ln(120)

# Add hypotheses section
pdf.set_font("Arial", size=14, style="B")
pdf.cell(0, 10, txt="Hypotheses and Explanations", ln=True)
pdf.ln(10)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt=(
    "We can clearly see that in every single graphic, the most common discrepancies are on Fridays and the first day of the month, so we could consider the following hypotheses:\n\n"
    "1. Backend Logic Errors on Recurring Schedules:\n"
    "   - Pattern Observed: Fridays in weekly and biweekly schedules show disproportionately high discrepancies.\n"
    "   - Hypothesis: The backend logic for calculating the `next_payment_day` might have an off-by-one error or issues with day alignment. Weekends (Friday or nearby) could exacerbate this due to special processing for weekends or holidays.\n\n"
    "2. Fixed Date Errors for Monthly Allowances:\n"
    "   - Pattern Observed: Monthly schedules on the 'first day' of the month have significant discrepancies.\n"
    "   - Hypothesis: The 'first day' logic might fail when processing near month transitions, especially if the logic doesnt account for varying month lengths or time zones.\n\n"
    "3. Mismatches Between Event Logs and Backend Updates:\n"
    "   - Pattern Observed: Backend discrepancies are significantly high\n"
    "   - Hypothesis: Event logs, considered the source of truth, might not synchronize properly with backend updates. Concurrent updates could overwrite correct values, or delayed updates might result in stale `next_payment_day` values.\n"
    "4. Load and Scaling Issues:\n"
    "   - Pattern Observed: Concentration of discrepancies on popular days like Fridays.\n"
    "   - Hypothesis: Backend processes might face load or scaling issues on these high-frequency update days, leading to timing mismatches or skipped updates.\n\n"
))

# Add recommendations
pdf.set_font("Arial", size=14, style="B")
pdf.cell(0, 10, txt="Recommendations", ln=True)
pdf.ln(10)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, txt=(
    "This recommendations are aimed at addressing the root causes of discrepancies and improving system reliability:\n\n"
    "- Investigate Backend Logic: Dive into the code handling of day and frequency calculations, with particular attention to Fridays and `first day` configurations. Refactoring or adding test cases could help catch edge cases.\n\n"
    "- Audit Synchronization Processes: Review how event logs update backend tables to ensure proper alignment, for example, implementing stronger checks during synchronization could prevent delays and overwrite issues.\n\n"
    "- Conduct Load Testing: Simulate high-frequency updates on peak days (like Fridays) to identify performance bottlenecks and ensure the system can handle real-world load conditions.\n\n"
    "- Refine Day Transition Logic: Enhance algorithms for monthly day adjustments, especially for transitions involving months with different day counts.\n"
))

# Add conclusion with author attribution
pdf.ln(10)
pdf.set_font("Arial", size=10)
pdf.cell(0, 60, "Maximiliano Dacko", 0, 0, "C")

# Save the PDF
pdf.output(output_pdf)

print(f"PDF report saved as {output_pdf}")