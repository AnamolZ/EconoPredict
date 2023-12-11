# EconoPredict
The core of EconoPredict lies in its ability to analyze historical data and calculate potential price drops and rises. It’s not just about prediction, it’s about providing a comprehensive understanding of the stock market dynamics. EconoPredict is a state-of-the-art financial analysis tool designed to provide investors with a comprehensive understanding of stock market dynamics. The platform employs advanced machine learning techniques, specifically utilizing Long Short-Term Memory (LSTM) models, to analyze historical data. Going beyond mere prediction, EconoPredict equips users with actionable insights into potential price drops and rises.

**Key Features:**

1. **LSTM Machine Learning Model:**
   - The core of EconoPredict relies on the sophisticated LSTM machine learning model. This model excels at capturing intricate patterns within historical stock market data, enabling accurate predictions of future price movements. This approach enhances the platform's predictive capabilities, providing users with valuable insights for informed decision-making.

2. **Real-time Stock Market Insights:**
   - EconoPredict offers real-time stock market insights, ensuring users have access to the most up-to-date information. By leveraging advanced algorithms and the power of LSTM, the platform provides a dynamic view of market trends, helping investors stay ahead of market shifts.

3. **Visualizing Historical Price Trends:**
   - The platform enables users to visualize historical price trends for leading companies that significantly influence the financial landscape. Through interactive and visually captivating charts, investors can explore the past performance of stocks, gaining a deeper understanding of market behavior.

4. **Google Finance API Integration:**
   - EconoPredict seamlessly integrates with the Google Finance API to fetch and process financial data. This integration ensures the accuracy and reliability of the information presented on the platform. Users can trust the data provided, allowing them to make well-informed investment decisions with confidence.

5. **Next-Day Price Prediction:**
   - One of the standout features of EconoPredict is its ability to predict the next-day stock prices. By leveraging the power of LSTM and analyzing historical data, the platform offers users valuable insights into potential price movements, aiding them in planning and adjusting their investment strategies.

6. **Past 1-Month Data Details:**
   - EconoPredict displays detailed information for the past 1 month, including high, low, close, open, and volume details. This feature provides users with a granular view of recent stock performance, further enhancing their ability to make informed decisions.

7. **User Empowerment:**
   - EconoPredict is meticulously crafted to empower investors. The user-friendly interface, coupled with sophisticated data analysis, provides a seamless experience for users of varying expertise levels. The platform's goal is to democratize financial insights, making them accessible to a broad audience.

### Docker Installation
   ```bash
docker pull err0rz/econ
docker run -p 127.0.0.1:8000:8000 err0rz/econ:latest
```

### Installation
1. Clone the repository: `git clone https://github.com/AnamolZ/EconoPredict.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run main: `python -m uvicorn main:app --host 127.0.0.1 --port 8000`

In conclusion, EconoPredict stands at the intersection of finance and technology, offering investors a powerful tool to navigate the complexities of the stock market. By combining advanced machine learning models, real-time data, and intuitive visualization, the platform empowers users to make informed investment decisions in an ever-changing financial landscape.

## Contributing to the Econo Predict Community

We welcome contributions to the Econo Predict project. Feel free to fork the repository, engage in discussions, and submit pull requests to enhance its features and functionality.

## Open-Source License

Econo Predict is licensed under the MIT License, an open-source license that fosters collaboration and innovation. This license grants you the freedom to use, modify, and distribute Google Finance for any purpose, empowering you to contribute to its growth and development.
