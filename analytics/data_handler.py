from datasets import Dataset
from typing import Any, Dict, Union
import pandas as pd
import json
import os
import zipfile
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

class data_handler:
    @staticmethod
    def handle_external_dataset(file_path: str) -> Dict[str, Any]:
     
        # Initialize result dictionary
        result = {
            "file_path": file_path,
            "type": None,
            "metadata": {},
            "analysis_insights": {},
            "examples": [],
            "data": None,
            "errors": []
        }

        try:
            # Normalize the file path
            file_path = os.path.abspath(file_path)

            # CSV and Parquet handling
            if file_path.endswith(('.csv', '.parquet')):
                try:
                    # Load dataset
                    dataset = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_parquet(file_path)
                    
                    result["type"] = "tabular"
                    result["data"] = dataset
                    
                    # Metadata extraction
                    result["metadata"] = {
                        "num_rows": len(dataset),
                        "columns": list(dataset.columns),
                        "column_types": dict(dataset.dtypes)
                    }
                    
                    # Tabular Analysis
                    result["analysis_insights"] = {
                        "summary_statistics": dataset.describe(include='all').to_dict(),
                        "missing_values": dataset.isnull().sum().to_dict(),
                        "unique_value_counts": {col: dataset[col].nunique() for col in dataset.columns}
                    }
                    
                    # Examples
                    result["examples"] = dataset.head(5).to_dict(orient="records")

                except Exception as e:
                    result["errors"].append(f"Tabular data processing error: {str(e)}")

            # JSON handling
            elif file_path.endswith('.json'):
                try:
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                    
                    dataset = pd.json_normalize(json_data)
                    
                    result["type"] = "json"
                    result["data"] = json_data
                    
                    # JSON Metadata and Analysis
                    result["metadata"] = {
                        "num_entries": len(json_data) if isinstance(json_data, list) else 1,
                        "keys": list(json_data.keys()) if isinstance(json_data, dict) else [],
                        "structure": "list" if isinstance(json_data, list) else "dict"
                    }
                    
                    # JSON Analysis Insights
                    result["analysis_insights"] = {
                        "depth": len(str(json_data).split('{')),
                        "key_types": {k: type(v).__name__ for k, v in (json_data.items() if isinstance(json_data, dict) else {})},
                        "total_size_bytes": len(str(json_data).encode('utf-8'))
                    }
                    
                    # Examples
                    result["examples"] = dataset.head(5).to_dict(orient="records")

                except Exception as e:
                    result["errors"].append(f"JSON processing error: {str(e)}")

            # ZIP file handling (Images and Videos)
            elif file_path.endswith('.zip'):
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        temp_dir = "temp_extracted"
                        os.makedirs(temp_dir, exist_ok=True)
                        zip_ref.extractall(temp_dir)
                        extracted_files = os.listdir(temp_dir)

                    # Image dataset
                    if all(f.lower().endswith(('png', 'jpg', 'jpeg')) for f in extracted_files):
                        result["type"] = "image"
                        
                        # Load and analyze images
                        images = []
                        image_insights = {
                            "total_images": len(extracted_files),
                            "image_sizes": [],
                            "color_distributions": []
                        }
                        
                        for img_file in extracted_files[:5]:  # Limit to first 5 images
                            img_path = os.path.join(temp_dir, img_file)
                            img = cv2.imread(img_path)
                            
                            if img is not None:
                                images.append(img)
                                
                                # Image insights
                                image_insights["image_sizes"].append({
                                    "filename": img_file,
                                    "shape": img.shape,
                                    "mean_color": cv2.mean(img)[:3]
                                })
                                
                                # Color distribution
                                color_hist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
                                image_insights["color_distributions"].append({
                                    "filename": img_file,
                                    "histogram_shape": color_hist.shape
                                })
                        
                        result["data"] = images
                        result["analysis_insights"] = image_insights
                        result["metadata"] = {
                            "num_files": len(extracted_files),
                            "file_types": list(set(os.path.splitext(f)[1] for f in extracted_files))
                        }

                    # Video dataset
                    elif all(f.lower().endswith(('mp4', 'avi', 'mkv')) for f in extracted_files):
                        result["type"] = "video"
                        
                        # Video analysis
                        videos = []
                        video_insights = {
                            "total_videos": len(extracted_files),
                            "video_details": []
                        }
                        
                        for vid_file in extracted_files[:5]:  # Limit to first 5 videos
                            vid_path = os.path.join(temp_dir, vid_file)
                            cap = cv2.VideoCapture(vid_path)
                            
                            # Video metadata
                            fps = cap.get(cv2.CAP_PROP_FPS)
                            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            
                            # Read first frame
                            ret, first_frame = cap.read()
                            
                            if ret:
                                videos.append(first_frame)
                                video_insights["video_details"].append({
                                    "filename": vid_file,
                                    "fps": fps,
                                    "frame_count": frame_count,
                                    "resolution": f"{width}x{height}",
                                    "first_frame_mean_color": cv2.mean(first_frame)[:3]
                                })
                            
                            cap.release()
                        
                        result["data"] = videos
                        result["analysis_insights"] = video_insights
                        result["metadata"] = {
                            "num_files": len(extracted_files),
                            "file_types": list(set(os.path.splitext(f)[1] for f in extracted_files))
                        }

                    # Clean up temporary directory
                    for f in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, f))
                    os.rmdir(temp_dir)

                except Exception as e:
                    result["errors"].append(f"ZIP file processing error: {str(e)}")

            else:
                result["errors"].append("Unsupported file type. Supported types are .csv, .parquet, .json, and .zip (image or video).")

        except Exception as e:
            result["errors"].append(f"General processing error: {str(e)}")

        return result