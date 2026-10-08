import torch
from torch import nn


def okay(module_or_parameter: nn.Parameter | torch.Tensor) -> None:
    if isinstance(module_or_parameter, nn.Parameter):
        param = module_or_parameter
        param.requires_grad = False
    elif isinstance(module_or_parameter, nn.Module):
        module = module_or_parameter
        module.eval()

        for param in module.parameters():
            param.requires_grad = False


def no_member_error(module_or_parameter: nn.Parameter | torch.Tensor) -> None:
    if isinstance((parameter := module_or_parameter), nn.Parameter):
        parameter.requires_grad = False
    elif isinstance((module := module_or_parameter), nn.Module):
        module.eval()  # pylint(no-member): Class 'module' has no 'eval' member

        for param in module.parameters():  # pylint(no-member): Class 'module' has no 'parameters' member
            param.requires_grad = False

