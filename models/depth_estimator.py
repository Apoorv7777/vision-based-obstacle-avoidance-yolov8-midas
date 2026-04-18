import torch
import cv2
import numpy as np


class DepthEstimator:

    def __init__(self):

        print("Loading MiDaS model...")

        self.device = (
            "cpu"
        )

        # Load MiDaS small model
        self.model = torch.hub.load(
            "intel-isl/MiDaS",
            "MiDaS_small"
        )

        self.model.to(self.device)
        self.model.eval()

        # Load transforms
        midas_transforms = torch.hub.load(
            "intel-isl/MiDaS",
            "transforms"
        )

        self.transform = (
            midas_transforms.small_transform
        )

        print("Depth model loaded")

    def estimate_depth(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        input_batch = (
            self.transform(rgb_frame)
            .to(self.device)
        )

        with torch.no_grad():

            prediction = self.model(
                input_batch
            )

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=frame.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = (
            prediction.cpu().numpy()
        )

        # Normalize depth
        depth_map = cv2.normalize(
            depth_map,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        depth_map = depth_map.astype(
            np.uint8
        )

        return depth_map