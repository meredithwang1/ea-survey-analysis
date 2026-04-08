import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import re
import plotly.express as px
import plotly.graph_objects as go

# Define filler words to remove from text analysis
FILLER_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
    'from', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
    'that', 'this', 'these', 'those', 'which', 'who', 'what', 'where', 'when', 'why', 'how',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'her', 'its', 'our', 'their', 'what\'s', 'don\'t', 'doesn\'t',
    'didn\'t', 'won\'t', 'can\'t', 'couldn\'t', 'shouldn\'t', 'wouldn\'t', 'hasn\'t', 'haven\'t',
    'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t', 'not', 'no', 'any', 'some', 'all', 'each',
    'every', 'both', 'either', 'neither', 'more', 'most', 'many', 'much', 'few', 'less',
    'very', 'too', 'so', 'such', 'just', 'only', 'even', 'also', 'well', 'now', 'here',
    'there', 'then', 'today', 'tomorrow', 'yesterday', 'please', 'thank', 'thanks', 'answer',
    'question', 'minute', 'minutes', 'sentence', 'sentences', 'etc', 's', 't', 're', 'll',
    'i\'m','than','across','about','like','com','single','concierge','pull','stie','within','once',
    'without','work'
}

def clean_text_for_analysis(text):
    """Remove filler words and clean text for analysis"""
    if pd.isna(text):
        return ""
    
    # Convert to lowercase and remove special characters
    text = str(text).lower()
    # Keep letters, numbers, hyphens, and apostrophes
    text = re.sub(r'[^a-z0-9\s\-\']', ' ', text)
    # Split into words
    words = text.split()
    # Filter out filler words and short words
    words = [w for w in words if w not in FILLER_WORDS and len(w) > 2]
    return ' '.join(words)

def extract_key_phrases(text, top_n=15):
    """Extract the most common phrases (1-3 words) from text"""
    cleaned = clean_text_for_analysis(text)
    words = [w for w in cleaned.split() if w.strip()]
    
    if not words or len(words) < 2:
        return Counter()
    
    # Extract phrases: 2-grams and 3-grams using simple loops
    phrases = []
    
    # Add 2-grams
    for i in range(len(words) - 1):
        bigram = ' '.join(words[i:i+2])
        phrases.append(bigram)
    
    # Add 3-grams
    for i in range(len(words) - 2):
        trigram = ' '.join(words[i:i+3])
        phrases.append(trigram)
    
    # Filter out phrases that contain only very common single words
    meaningful_phrases = []
    for phrase in phrases:
        phrase_words = phrase.split()
        # Skip phrases that contain only filler words
        if not all(word in FILLER_WORDS for word in phrase_words):
            meaningful_phrases.append(phrase)
    
    # Get most common phrases
    phrase_freq = Counter(meaningful_phrases).most_common(top_n)
    
    return phrase_freq

def filter_meaningful_words(words, min_length=4):
    """Filter out single words that are not very meaningful"""
    # Additional filtering for single words beyond filler words
    less_meaningful = {
        'need', 'make', 'take', 'give', 'come', 'know', 'think', 'feel', 'want', 'get',
        'see', 'look', 'use', 'find', 'help', 'work', 'play', 'game', 'time', 'way',
        'thing', 'part', 'point', 'place', 'case', 'kind', 'type', 'sort', 'form',
        'level', 'area', 'team', 'role', 'task', 'step', 'plan', 'goal', 'idea',
        'issue', 'problem', 'solution', 'result', 'effect', 'impact', 'change',
        'process', 'system', 'tool', 'feature', 'function', 'service', 'support',
        'customer', 'user', 'player', 'people', 'group', 'company', 'business',
        'market', 'product', 'service', 'content', 'data', 'information', 'knowledge',
        'experience', 'quality', 'value', 'cost', 'price', 'rate', 'score', 'number',
        'amount', 'size', 'scale', 'range', 'list', 'set', 'group', 'class', 'type'
    }
    
    filtered = []
    for word in words:
        if (len(word) >= min_length and 
            word not in FILLER_WORDS and 
            word not in less_meaningful):
            filtered.append(word)
    
    return filtered

def create_word_frequency_chart(text_series, question_title):
    """Create a visualization of word and phrase frequency"""
    all_text = ' '.join(text_series.dropna().astype(str))
    cleaned = clean_text_for_analysis(all_text)
    words = [w for w in cleaned.split() if w.strip()]
    
    if not words:
        st.info("No meaningful words found in responses for analysis.")
        return
    
    # Get meaningful single words
    meaningful_words = filter_meaningful_words(words)
    single_word_freq = Counter(meaningful_words).most_common(8) if meaningful_words else []
    
    # Get phrases
    phrase_freq = extract_key_phrases(all_text, 7)
    
    # Combine single words and phrases
    combined_freq = single_word_freq + phrase_freq
    
    if combined_freq:
        # Sort by frequency and take top 15
        combined_freq = sorted(combined_freq, key=lambda x: x[1], reverse=True)[:15]
        items, counts = zip(*combined_freq)
        
        # Create blue color gradient based on frequency values
        # Normalize counts to 0-1 range for color mapping
        min_count = min(counts)
        max_count = max(counts)
        normalized_counts = [(c - min_count) / (max_count - min_count) if max_count > min_count else 0.5 for c in counts]
        
        # Map to blue color scale: light blue (low) to dark blue (high)
        # RGB values: light blue (100, 150, 255) to dark blue (0, 51, 153)
        colors = [f'rgba({int(100 - 100*norm)}, {int(150 - 99*norm)}, {int(255 - 102*norm)}, 0.8)' for norm in normalized_counts]
        
        fig = go.Figure(data=[
            go.Bar(x=counts, y=items, orientation='h', marker_color=colors)
        ])
        fig.update_layout(
            title="Top Words & Phrases in Responses",
            xaxis_title="Frequency",
            yaxis_title="Words/Phrases",
            height=500,
            margin=dict(l=200)
        )
        st.plotly_chart(fig, width='stretch')
        
        # Add legend explanation
        st.caption("🔵 Light blue = Lower frequency | Dark blue = Higher frequency")

def create_word_cloud(text_series, question_title):
    """Create a word cloud from text responses including phrases"""
    all_text = ' '.join(text_series.dropna().astype(str))
    cleaned = clean_text_for_analysis(all_text)
    
    if not cleaned.strip():
        st.info("No meaningful words found for word cloud.")
        return
    
    # Get meaningful single words
    words = [w for w in cleaned.split() if w.strip()]
    meaningful_words = filter_meaningful_words(words)
    
    # Get phrases and repeat them based on frequency for word cloud
    phrase_freq = extract_key_phrases(all_text, 20)
    
    # Create text for word cloud: single words + repeated phrases
    cloud_text = ' '.join(meaningful_words)
    
    # Add phrases multiple times based on their frequency
    for phrase, freq in phrase_freq:
        cloud_text += (' ' + phrase) * min(freq, 3)  # Repeat up to 3 times
    
    if not cloud_text.strip():
        st.info("No meaningful content found for word cloud.")
        return
    
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                             colormap='viridis', max_words=66, 
                             collocations=False).generate(cloud_text)
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        # ax.set_title(f"Word Cloud - {question_title}", fontsize=28, fontweight='bold')
        ax.axis('off')
        st.pyplot(fig, width='stretch')
        
        # Show top phrases
        if phrase_freq:
            st.subheader("Top Phrases")
            phrase_df = pd.DataFrame(phrase_freq[:10], columns=['Phrase', 'Frequency'])
            st.dataframe(phrase_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Could not generate word cloud: {e}")

# Load data
st.title("📊 Survey Analysis Dashboard")
st.markdown("Comprehensive analysis of EA workshop attendee survey responses with visualizations and key insights")

try:
    df = pd.read_csv('survey_data.csv', index_col=0, encoding='latin-1')
except FileNotFoundError:
    st.error("survey_data.csv not found. Please make sure the file is in the same directory.")
    st.stop()
except Exception as e:
    try:
        df = pd.read_csv('survey_data.csv', index_col=0, encoding='utf-8', errors='ignore')
    except:
        st.error(f"Error reading CSV file: {e}")
        st.stop()

# Display basic info
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Responses", len(df))
with col2:
    st.metric("Completion Rate", f"{(df['Complete'] == 'Completed').sum() / len(df) * 100:.1f}%")
with col3:
    st.metric("Survey Questions", 12)

st.divider()

# Define survey questions (columns I through T, displayed as questions 1-12)
# Excel columns: I=8, J=9, K=10, L=11, M=12, N=13, O=14, P=15, Q=16, R=17, S=18, T=19
question_columns = {
    1: 'What is your role today, and how do you currently interact with player support, player-facing knowledge, or content as part of your work?',
    2: 'Vision for AI Concierge: Which player moments are most important for AI Concierge to support?',
    3: 'Experience Expectations: What does a high-quality vs low-quality AI Concierge experience look like?',
    4: 'Risks: What risks or concerns come to mind with an AI-driven player experience?',
    5: 'Success Metrics: What would success look like for AI Concierge?',
    6: 'Fan Care vs. IT vs. Game Studios Roles: How do you see these teams contributing?',
    7: 'Knowledge Sources - Internal: What knowledge sets support the AI Concierge?',
    8: 'Third Party Content: How do you feel about using third-party content?',
    9: 'AI Readiness: On a scale of 1-10, how ready is existing knowledge?',
    10: 'AI Readiness Explanation: Why did you select that number?',
    11: 'Responsible AI: What safety or review measures are in place?',
    12: 'Gaps & Dependencies: What are the biggest gaps or blockers?'
}

# Get the actual column names
actual_columns = df.columns.tolist()

# Map question numbers to actual column indices
col_mapping = {}
for i, number in enumerate(range(1, 13)):
    # Columns start at index 7 for column I (0-indexed)
    if 7 + i < len(actual_columns):
        col_mapping[number] = actual_columns[7 + i]

st.header("Survey Questions & Analysis")

# Create tabs for each question
with st.expander("📋 View All Questions", expanded=False):
    for number, question in question_columns.items():
        st.write(f"**Question {number}. {question}**")

# Analyze each question
for question_num in range(1, 13):
    if question_num not in col_mapping:
        continue
    
    col_name = col_mapping[question_num]
    question_text = question_columns[question_num]
    
    st.header(f"Question {question_num}: {question_text}")
    
    # Get responses
    responses = df[col_name].dropna()
    
    if len(responses) == 0:
        st.warning("No responses for this question")
        continue
    
    # Special handling for numerical question (Question 9)
    if question_num == 9:
        try:
            # Try to convert to numeric
            numeric_responses = pd.to_numeric(responses, errors='coerce').dropna()
            
            if len(numeric_responses) > 0:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Mean", f"{numeric_responses.mean():.2f}")
                with col2:
                    st.metric("Median", f"{numeric_responses.median():.2f}")
                with col3:
                    st.metric("Std Dev", f"{numeric_responses.std():.2f}")
                with col4:
                    st.metric("Sample Size", len(numeric_responses))
                
                # Create visualizations for numerical data
                col1, col2 = st.columns(2)
                
                with col1:
                    # Bar chart of distribution
                    fig = go.Figure(data=[
                        go.Histogram(x=numeric_responses, nbinsx=10, marker_color='rgba(25, 118, 210, 0.8)')
                    ])
                    fig.update_layout(
                        title="Distribution of Responses",
                        xaxis_title="Rating (1-10)",
                        yaxis_title="Count",
                        height=400
                    )
                    st.plotly_chart(fig, width='stretch')
                
                with col2:
                    # Box plot
                    fig = go.Figure(data=[
                        go.Box(y=numeric_responses, marker_color='lightseagreen')
                    ])
                    fig.update_layout(
                        title="Box Plot of Responses",
                        yaxis_title="Rating (1-10)",
                        height=400
                    )
                    st.plotly_chart(fig, width='stretch')
        except Exception as e:
            st.warning(f"Could not analyze as numerical data: {e}")
    else:
        # Text analysis for non-numerical questions
        st.subheader("Key Themes & Word Frequency")
        
        col1, col2 = st.columns(2)
        
        with col1:
            create_word_frequency_chart(responses, question_text)
        
        with col2:
            create_word_cloud(responses, question_text)
        
        # Show sample responses
        with st.expander("View Sample Responses"):
            for idx, response in enumerate(responses.head(3), 1):
                st.write(f"**Response {idx}:**")
                st.write(response)
                st.divider()
    
    st.divider()

# Summary section
st.header("📈 Overall Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Response Quality")
    completion = (df['Complete'] == 'Completed').sum() / len(df) * 100
    progress = st.progress(completion / 100)
    st.write(f"Completed Survey Rate: {completion:.1f}%")

with col2:
    st.subheader("Response Coverage")
    coverage_data = []
    for letter in ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
        if letter in col_mapping:
            col_name = col_mapping[letter]
            non_null = df[col_name].notna().sum()
            coverage_data.append(non_null)
    
    avg_coverage = np.mean(coverage_data)
    st.metric("Average Response Rate", f"{avg_coverage / len(df) * 100:.1f}%")

st.info("💡 **Analysis Note:** Text responses have been cleaned to remove filler words for meaningful analysis. Visualizations include word frequency charts and word clouds to identify key themes and frequently mentioned concepts.")
