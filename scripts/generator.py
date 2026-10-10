from torch import nn

class Generator(nn.Module):
    def __init__(self, latent_dim=100, features=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, features*8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(features*8), nn.ReLU(True),
            nn.ConvTranspose2d(features*8, features*4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(features*4), nn.ReLU(True),
            nn.ConvTranspose2d(features*4, features*2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(features*2), nn.ReLU(True),
            nn.ConvTranspose2d(features*2, features, 4, 2, 1, bias=False),
            nn.BatchNorm2d(features), nn.ReLU(True),
            nn.ConvTranspose2d(features, 3, 4, 2, 1, bias=False), nn.Tanh())
    def forward(self, z):
        return self.net(z)

