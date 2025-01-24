from pathlib import Path
import os
import torch
from model import OCRModel

def load_models(path: str = "./results/final-models"):
    """ function to load all final models in the directory ./results/final-models  """

    models_path = Path(path)
    models = []
    for model_file in os.listdir(models_path):
        model_path = models_path/model_file
        if model_path.suffix.lower() in [".pt", ".pth"]:
            device = torch.device( 'cuda:0' if torch.cuda.is_available() else 'cpu' )
            model = torch.load(model_path, map_location=torch.device(device.type), weights_only=False)
            models.append(model)
    return models


def average_models(path: str = "./results/final-models"):

    models: list[OCRModel] = load_models(path)
    model_count = len(models)
    print(f"Total model found: {model_count}")

    # averaging models
    models_state_dict =  [ m.state_dict() for m in models]
    avg_state_dict = {}
    for key in models_state_dict[0].keys():
        avg_state_dict[key] = sum([state_dict[key] for state_dict in models_state_dict]) / model_count

    return avg_state_dict


if __name__ == "__main__":
    state_dict = average_models()