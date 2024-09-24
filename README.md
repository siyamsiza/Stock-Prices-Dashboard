
---

# Stock Prices Dashboard

This Streamlit app provides real-time stock data from Yahoo Finance, allowing users to explore stock prices, visualize trends, and perform basic feature engineering on selected stock data.

## Features

- **Navigation Sidebar**: The sidebar includes different sections for interacting with the app:
  - Domain Knowledge
  - Data Extraction
  - Data Preview
  - Data Summary
  - Data Visualization
  - Feature Engineering
  - Conclusion
  - Downloads

- **Domain Knowledge**: Provides an introduction to stocks and their relevance in financial markets.

- **Data Extraction**: Users can select a company from a predefined list (e.g., Apple, Tesla, Google) and extract stock data using the Yahoo Finance API. Extracted data includes historical stock prices and trading volumes.

- **Data Preview**: Displays a preview of the stock data, including the number of rows and columns, along with checks for missing values.

- **Data Summary**: Provides statistical summaries of stock prices (e.g., Open, Close, High, Low) and visualizes price distributions for each.

- **Data Visualization**: Users can interact with an interactive Plotly chart of stock prices over time. Additional charts using Matplotlib and Seaborn are available for stock closing prices and trading volume over time.

- **Feature Engineering**: Example feature engineering includes calculating a 30-day moving average of the stock's closing price and visualizing it alongside the closing price. A heatmap is also generated to explore correlations between different stock attributes.

- **Conclusion**: The Stock Prices Dashboard provides an insightful and interactive platform for investors and analysts to explore the complexities of stock data. From extracting data on major corporations to visualizing trends through engaging charts, the app empowers users to make informed decisions based on comprehensive analyses. Whether you are a seasoned investor or just starting your journey in the world of finance, this dashboard serves as a valuable tool to deepen your insights and foster better decision-making in your investment endeavors.

- **Downloads**: Allows you to download the stock dataset used in the dashboard.
  
## Libraries Used

- `streamlit`: For building the interactive web app.
- `yfinance`: For extracting real-time stock data.
- `pandas`: For data manipulation.
- `numpy`: For numerical operations.
- `matplotlib` and `seaborn`: For plotting stock data.
- `plotly`: For interactive stock charts.
- `warnings`: To suppress irrelevant warnings.

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/siyamsiza/Stock-Prices-Dashboard.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Stock-Prices-Dashboard
   ```

3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

5. Open your browser and navigate to the URL provided by Streamlit to interact with the app.

## Customizations

This app can be easily customized to include more companies, additional technical indicators, and more detailed analysis of stock data.

## Author

Siya Msiza

---
