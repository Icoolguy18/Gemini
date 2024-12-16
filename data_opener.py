from datasets import Dataset
from typing import Any, Dict, Union
import pandas as pd
import json
import os
import zipfile
from PIL import Image
import cv2

class data_handler:
    def handle_external_dataset(file_path: str) -> Dict[str, Any]:
        """
        Loads an external dataset file, understands its structure, and stores relevant dataset information.

        Args:
            file_path (str): The path to the dataset file.

        Returns:
            Dict[str, Any]: A dictionary containing metadata, column types, and examples from the dataset.
        """
        try:
            dataset_info = {
                "file_path": file_path,
                "type": None,
                "metadata": {},
                "examples": []
            }

            if file_path.endswith('.csv'):
                dataset = pd.read_csv(file_path)
                dataset_info["type"] = "tabular"
                dataset_info["metadata"] = {
                    "num_rows": len(dataset),
                    "columns": list(dataset.columns)
                }
                dataset_info["examples"] = dataset.head(5).to_dict(orient="records")

            elif file_path.endswith('.parquet'):
                dataset = pd.read_parquet(file_path)
                dataset_info["type"] = "tabular"
                dataset_info["metadata"] = {
                    "num_rows": len(dataset),
                    "columns": list(dataset.columns)
                }
                dataset_info["examples"] = dataset.head(5).to_dict(orient="records")

            elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                dataset = pd.json_normalize(json_data)
                dataset_info["type"] = "json"
                dataset_info["metadata"] = {
                    "num_rows": len(dataset),
                    "columns": list(dataset.columns)
                }
                dataset_info["examples"] = dataset.head(5).to_dict(orient="records")

            elif file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall("temp_extracted")
                    extracted_files = os.listdir("temp_extracted")

                if all(f.lower().endswith(('png', 'jpg', 'jpeg')) for f in extracted_files):
                    dataset_info["type"] = "image"
                    dataset_info["metadata"] = {"num_files": len(extracted_files)}
                    dataset_info["examples"] = extracted_files[:5]
                    # Optionally load a few images
                    for img_file in extracted_files[:5]:
                        img_path = os.path.join("temp_extracted", img_file)
                        img = Image.open(img_path)
                        dataset_info["examples"].append({"file_name": img_file, "size": img.size})

                elif all(f.lower().endswith(('mp4', 'avi', 'mkv')) for f in extracted_files):
                    dataset_info["type"] = "video"
                    dataset_info["metadata"] = {"num_files": len(extracted_files)}
                    dataset_info["examples"] = extracted_files[:5]
                    # Optionally load metadata for a few videos
                    for vid_file in extracted_files[:5]:
                        vid_path = os.path.join("temp_extracted", vid_file)
                        cap = cv2.VideoCapture(vid_path)
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        duration = frame_count / fps if fps else 0
                        dataset_info["examples"].append({"file_name": vid_file, "fps": fps, "duration": duration})
                        cap.release()

                # Cleanup temporary files
                for f in extracted_files:
                    os.remove(os.path.join("temp_extracted", f))
                os.rmdir("temp_extracted")

            else:
                raise ValueError("Unsupported file type. Supported types are .csv, .parquet, .json, and .zip (image or video).")

            return dataset_info

        except Exception as e:
            print(f"Error loading dataset: {e}")
            return {"error": str(e)}

    