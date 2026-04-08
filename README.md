# Survey Analysis Dashboard

A comprehensive Streamlit application for analyzing survey responses with advanced text analysis, visualizations, and insights.

## Features

- 📊 **Survey Data Analysis**: Reads and analyzes survey responses from CSV files
- 🔍 **Advanced Text Analysis**: Extracts meaningful keywords and phrases (2-3 word combinations)
- 📈 **Interactive Visualizations**: Word clouds, frequency charts, and statistical plots
- 🎯 **Smart Filtering**: Removes filler words and focuses on meaningful insights
- 📋 **Question-by-Question Analysis**: Detailed breakdown for each survey question

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd survey-analysis-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run survey_analysis_app.py
```

## Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Create a GitHub repository** and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Connect your GitHub repository**:
   - Click "New app"
   - Select your repository
   - Set main file path to: `survey_analysis_app.py`
   - Click "Deploy"

4. **Upload your data**: Since `survey_data.csv` is in `.gitignore`, you'll need to upload it to Streamlit Cloud separately or include it in your repository if it's not sensitive data.

### Option 2: Heroku

1. Create a `Procfile`:
```
web: streamlit run survey_analysis_app.py --server.port $PORT --server.headless true
```

2. Update `requirements.txt` to include:
```
streamlit
pandas
numpy
matplotlib
seaborn
wordcloud
plotly
requests
gunicorn
```

3. Deploy to Heroku using their Git deployment method.

### Option 3: Other Platforms

- **Railway**: Connect your GitHub repo
- **Render**: Connect your GitHub repo
- **Fly.io**: Use their Docker deployment
- **Vercel**: For static deployments (limited interactivity)

## Data Requirements

The app expects a CSV file named `survey_data.csv` with:
- Survey questions in columns I through T
- One row per survey response
- UTF-8 encoding (or latin-1 as fallback)

## Configuration

- Modify `FILLER_WORDS` in the code to customize text filtering
- Adjust visualization parameters in the plotting functions
- Update question mappings in the `question_columns` dictionary

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

MIT License - feel free to use and modify as needed.