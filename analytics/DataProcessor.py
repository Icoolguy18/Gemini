import json
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np  

class JsonAnalysis:
    def __init__(self, data):
        self.data = data

    def perform_analysis(self):
        """
        Perform basic analysis on JSON data.
        """
        if isinstance(self.data, dict):
            # Convert JSON to DataFrame if it's a dictionary
            json_df = pd.json_normalize(self.data)
            print("\nConverted JSON to DataFrame:")
            print(json_df.head())
            
            # Basic Info
            print("\nBasic Info:")
            print(json_df.info())
            
            # Descriptive Statistics
            print("\nDescriptive Statistics:")
            print(json_df.describe())
        
        else:
            print("The data provided is not a valid JSON object.")


class ImageAnalysis:
    def __init__(self, image):
        self.image = image

    def perform_analysis(self):
        """
        Perform basic analysis on image data.
        """
        if self.image is not None:
            # Display image
            plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            plt.title("Image Preview")
            plt.axis('off')
            plt.show()

            # Basic image statistics
            print(f"Image Shape: {self.image.shape}")
            print(f"Image Size: {self.image.size} pixels")
            print(f"Image Channels: {self.image.shape[2] if len(self.image.shape) > 2 else 1}")

            # Convert to grayscale and display histogram
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            plt.hist(gray_image.ravel(), bins=256, color='gray')
            plt.title("Grayscale Histogram")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")
            plt.show()

        else:
            print("The image data is invalid or empty.")


class TabularAnalyzer:
    """
    A class for performing basic analysis on tabular datasets (CSV or Parquet).
    """
    def __init__(self, file_path: str):
        """
        Initialize the TabularAnalyzer with the dataset file path.

        Args:
            file_path (str): Path to the tabular dataset.
        """
        self.file_path = file_path
        self.dataset = None

    def load_dataset(self):
        """
        Load the dataset from the file path.
        """
        print("\nLoading tabular dataset...")
        self.dataset = pd.read_csv(self.file_path) if self.file_path.endswith(".csv") else pd.read_parquet(self.file_path)

    def display_basic_info(self):
        """
        Display basic information about the dataset.
        """
        if self.dataset is not None:
            print("\nDataset Columns and Types:")
            print(self.dataset.dtypes)

            print("\nFirst Few Rows:")
            print(self.dataset.head())
        else:
            print("Dataset not loaded. Please load the dataset first.")

    def display_summary_statistics(self):
        """
        Display summary statistics of the dataset.
        """
        if self.dataset is not None:
            print("\nSummary Statistics:")
            print(self.dataset.describe(include="all"))
        else:
            print("Dataset not loaded. Please load the dataset first.")


class VideoAnalysis:
    def __init__(self, video):
        self.video = video

    def perform_analysis(self):
        """
        Perform basic analysis on video data.
        """
        if isinstance(self.video, np.ndarray):
            # Display the first frame (if loaded)
            plt.imshow(cv2.cvtColor(self.video, cv2.COLOR_BGR2RGB))
            plt.title("First Frame of Video")
            plt.axis('off')
            plt.show()

        else:
            print("The video data is invalid or empty.")
