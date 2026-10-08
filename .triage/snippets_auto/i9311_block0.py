import torch

test = torch.nn.Parameter(torch.rand(2, 10, 1, 3))
test = test.repeat(1, 1, 3, 1)[:, :, 0, :]
