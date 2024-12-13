from tasks import collect_data
from preprocess_data import preprocess_data
from analyze_data import analyze_data
import asyncio
import subprocess
from kmeans_clustering import kmeans_with_sentiment
from sentiment_analysis import perform_sentiment_analysis

def main():
    """Main function to run the project."""
    # Step 1: Collect data
    print("Starting data collection...")
    if not asyncio.get_event_loop().is_running():
        # If no event loop is running, use asyncio.run()
        posts = asyncio.run(collect_data(subreddit_name="technology", limit=100))
    else:
        # If an event loop is running, directly await the coroutine
        posts = asyncio.get_event_loop().run_until_complete(collect_data(subreddit_name="technology", limit=100))
    asyncio.run(collect_data(subreddit_name="technology", limit=100))
    print("Data collection complete.")
    
    # Step 2: Preprocess data
    print("Starting data preprocessing...")
    preprocess_data()
    print("Data preprocessing complete.")
    
    # Step 3: Analyze data
    print("Starting data analysis...")
    analyze_data()
    print("Data analysis complete.")

    # Step 4: Perform sentiment analysis
    print("Performing sentiment analysis...")
    perform_sentiment_analysis()

    print("Workflow completed successfully.")

    # Step 5: K means Clustering
    '''
    print("Performing Kmeans Clustering")
    result = subprocess.run(["python", "kmeans_clust.py"], capture_output=True, text=True)
    print(result.stdout)  # Print output of the clustering script
    '''
    print("Performing Kmeans Clustering")
    kmeans_with_sentiment(n_clusters=3)
    print("finished")  # Print output of the clustering script


if __name__ == "__main__":
    main()
