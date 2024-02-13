import torch
import torch.nn as nn

class hand_LSTM(nn.Module):
    def __init__(self, num_layers=1):
        super(hand_LSTM, self).__init__()
        self.lstm1 = nn.LSTM(67, 128, num_layers, batch_first=True, bidirectional=True)
        self.layer_norm1 = nn.LayerNorm(256)
        self.dropout1 = nn.Dropout(0.1)
        
        self.lstm2 = nn.LSTM(256, 64, num_layers, batch_first=True, bidirectional=True)
        self.layer_norm2 = nn.LayerNorm(128)
        self.dropout2 = nn.Dropout(0.1)
        
        self.lstm3 = nn.LSTM(128, 32, num_layers, batch_first=True, bidirectional=True)
        self.layer_norm3 = nn.LayerNorm(64)
        self.dropout3 = nn.Dropout(0.1)
        
        self.attention = nn.Linear(64, 1)
        self.fc = nn.Linear(64, 2)
        
    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.layer_norm1(x)
        x = self.dropout1(x)
        
        x, _ = self.lstm2(x)
        x = self.layer_norm2(x)
        x = self.dropout2(x)
        
        x, _ = self.lstm3(x)
        x = self.layer_norm3(x)
        x = self.dropout3(x)
        
        # Attention 메커니즘
        attention_weights = torch.softmax(self.attention(x), dim=1)
        x = torch.sum(attention_weights * x, dim=1)
        
        x = self.fc(x)
        return x