from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load the dataset
dataset_path = "nasa_battery_data/metadata.csv"
data = pd.read_csv(dataset_path)

# Debug: Print dataset info
print(data.head())
print(data.describe())

# Create a sequential Cycle_Index if test_id is constant
if data['test_id'].nunique() <= 1:
    print("Warning: test_id has constant values. Creating sequential Cycle_Index.")
    data['Cycle_Index'] = range(1, len(data) + 1)
else:
    data.rename(columns={'test_id': 'Cycle_Index'}, inplace=True)

# Check for constant values
print("Unique Re values:", data['Re'].nunique())
print("Unique Rct values:", data['Rct'].nunique())
print("Unique Capacity values:", data['Capacity'].nunique())

# Select necessary columns
data = data[['Cycle_Index', 'Capacity', 'Re', 'Rct']]

# Create plots
@app.route("/")
def index():
    # Re Plot with Dark Theme and White Line
    fig_re = px.line(data, x='Cycle_Index', y='Re', title="Electrolyte Resistance (Re) vs Cycle Index")
    fig_re.update_traces(line=dict(color='white', width=3))  # White Line Color
    fig_re.update_layout(template='plotly_dark', plot_bgcolor='black', paper_bgcolor='black')

    re_html = pio.to_html(fig_re, full_html=False)

    # Rct Plot with Dark Theme and Green Line
    fig_rct = px.line(data, x='Cycle_Index', y='Rct', title="Charge Transfer Resistance (Rct) vs Cycle Index")
    fig_rct.update_traces(line=dict(color='green', width=3))  # Green Line Color
    fig_rct.update_layout(template='plotly_dark', plot_bgcolor='black', paper_bgcolor='black')

    rct_html = pio.to_html(fig_rct, full_html=False)

    # Capacity Plot with Dark Theme and White Line
    fig_capacity = px.line(data, x='Cycle_Index', y='Capacity', title="Battery Capacity vs Cycle Index")
    fig_capacity.update_traces(line=dict(color='white', width=3))  # White Line Color
    fig_capacity.update_layout(template='plotly_dark', plot_bgcolor='black', paper_bgcolor='black')

    capacity_html = pio.to_html(fig_capacity, full_html=False)

    return render_template("index.html", re_plot=re_html, rct_plot=rct_html, capacity_plot=capacity_html)

if __name__ == "__main__":
    app.run(debug=True)
