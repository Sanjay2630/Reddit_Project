import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import json
import os

# Load data
def load_cleaned_data(input_path="data/cleaned_data.json"):
    """Load cleaned data for clustering."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} not found. Please preprocess the data first.")

    with open(input_path, "r", encoding="utf-8") as file:
        cleaned_data = json.load(file)

    df = pd.DataFrame(cleaned_data)
    return df

# Prepare numeric features
def prepare_numeric_features(df):
    """Extract and scale numeric features for clustering."""
    features = df[["score", "Normalized Upvotes"]].fillna(0)
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    return scaled_features

# Prepare text embeddings
def prepare_text_embeddings(df, column="Cleaned Title"):
    """Generate text embeddings using Sentence-BERT."""
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and efficient model
    text_data = df[column].fillna("").tolist()
    embeddings = model.encode(text_data)
    return embeddings

# Perform K-Means clustering
def perform_kmeans(features, n_clusters=5):
    """Apply K-Means clustering."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(features)
    return kmeans, labels

# Elbow Method for optimal K
def plot_elbow_method(features, max_k=10):
    """Plot the Elbow Method to determine optimal K."""
    distortions = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(features)
        distortions.append(kmeans.inertia_)
    plt.plot(range(1, max_k + 1), distortions, marker="o")
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Distortion")
    plt.title("Elbow Method for Optimal K")
    plt.show()

# Save clustered data
def save_clustered_data(df, labels, output_path="data/clustered_data.json"):
    """Save clustered data to a JSON file."""
    df["Cluster"] = labels
    clustered_data = df.to_dict(orient="records")
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(clustered_data, outfile, indent=4)
    print(f"Clustered data saved to {output_path}")

# Visualize clusters
def visualize_clusters(features, labels):
    """Visualize clusters in 2D using PCA."""
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(features)
    plt.scatter(reduced_features[:, 0], reduced_features[:, 1], c=labels, cmap="viridis")
    plt.colorbar(label="Cluster")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("Clusters Visualized in 2D")
    plt.show()

# Main function
def main():
    """Main function to execute K-Means clustering."""
    print("Loading cleaned data...")
    df = load_cleaned_data()

    print("Preparing features...")
    numeric_features = prepare_numeric_features(df)
    text_embeddings = prepare_text_embeddings(df)

    # Combine numeric and text features
    combined_features = np.hstack((numeric_features, text_embeddings))

    print("Determining the optimal number of clusters...")
    plot_elbow_method(combined_features)

    print("Performing K-Means clustering...")
    optimal_k = 5  # You can adjust this based on the Elbow Method
    kmeans_model, cluster_labels = perform_kmeans(combined_features, n_clusters=optimal_k)

    print("Saving clustered data...")
    save_clustered_data(df, cluster_labels)

    print("Visualizing clusters...")
    visualize_clusters(combined_features, cluster_labels)

    print("K-Means clustering complete.")

if __name__ == "__main__":
    main()
