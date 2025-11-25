
import matplotlib.pyplot as plt

def plot_category(df, ax):
    df['category'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title("Category Count")

def plot_price_dist(df, ax):
    df['price'].plot(kind='hist', ax=ax)
    ax.set_title("Price Distribution")

def plot_popularity(df, ax):
    df['popularity'].plot(kind='line', ax=ax)
    ax.set_title("Popularity Trend")
