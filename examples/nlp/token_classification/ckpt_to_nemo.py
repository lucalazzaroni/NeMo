import sys
sys.path = ["/home/apeganov/NeMo"] + sys.path

import argparse
from pathlib import Path

import torch
from omegaconf import OmegaConf

from nemo.collections.nlp.models import MTEncDecModel, PunctuationCapitalizationModel


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", "-c", type=Path, help="Path to checkpoint to encapsulate.", required=True)
    parser.add_argument("--nemo", "-n", type=Path, help="Path to output nemo file", required=True)
    parser.add_argument("--cfg", "-f", type=Path, help="Path to config file", required=True)
    parser.add_argument(
        "--model_class",
        "-t",
        choices=["PunctuationCapitalizationModel", "MTEncDecModel"],
        default="PunctuationCapitalizationModel",
    )
    args = parser.parse_args()
    args.ckpt = args.ckpt.expanduser()
    args.nemo = args.nemo.expanduser()
    args.cfg = args.cfg.expanduser()
    return args


def main():
    args = get_args()
    cfg = OmegaConf.load(args.cfg)
    cls = MTEncDecModel if args.model_class == "MTEncDecModel" else PunctuationCapitalizationModel
    model = cls(cfg.model)
    ckpt = torch.load(args.ckpt)
    model.load_state_dict(ckpt['state_dict'], strict=False)
    # model = cls.load_from_checkpoint(args.ckpt, cfg=cfg.model, strict=False)
    model.save_to(args.nemo)


if __name__ == "__main__":
    main()
