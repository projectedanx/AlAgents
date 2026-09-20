import torch
import torch.nn as nn
import torch.fft

class PNS5ModalAttention(nn.Module):
    """
    S5-Modal Attention Mechanism using FFT-optimized circular convolution for value accumulation.
    Natively supports paraconsistent non-separable conjunctions (PNS5 logic).
    """
    def __init__(self, embed_dim: int, num_heads: int):
        """
        Initializes the PNS5 Modal Attention module.

        Args:
            embed_dim (int): The total embedding dimension.
            num_heads (int): The number of attention heads.
        """
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        assert self.head_dim * num_heads == self.embed_dim, "embed_dim must be divisible by num_heads"

        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
        """
        Forward pass for PNS5 Modal Attention.

        Args:
            query (torch.Tensor): Shape (batch_size, seq_len, embed_dim)
            key (torch.Tensor): Shape (batch_size, seq_len, embed_dim)
            value (torch.Tensor): Shape (batch_size, seq_len, embed_dim)

        Returns:
            torch.Tensor: Attended values, shape (batch_size, seq_len, embed_dim)
        """
        batch_size, seq_len, _ = query.size()

        # Linear projections and reshape for multi-head
        # Shape: (batch_size, num_heads, seq_len, head_dim)
        Q = self.q_proj(query).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_proj(key).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_proj(value).view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # Standard scaled dot-product attention scores
        # Shape: (batch_size, num_heads, seq_len, seq_len)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        attn_weights = torch.softmax(scores, dim=-1)

        # --- PNS5 Fourier-Domain Value Accumulation ---
        # 1. Transform Values to frequency domain
        V_freq = torch.fft.fft(V, dim=-1) # Shape: (batch_size, num_heads, seq_len, head_dim)

        # 2. Prepare identity element in frequency domain (vector of ones)
        ones_freq = torch.ones_like(V_freq)

        # We need to accumulate the product across the sequence length (the 'j' index in attention).
        # output_i = prod_j ( alpha_{i,j} * V_j_freq + (1 - alpha_{i,j}) * 1_freq )

        # Expand dims for broadcasting
        # attn_weights shape: (batch_size, num_heads, seq_len_q, seq_len_k, 1)
        attn_weights = attn_weights.unsqueeze(-1)

        # V_freq shape: (batch_size, num_heads, 1, seq_len_k, head_dim)
        V_freq_exp = V_freq.unsqueeze(2)
        ones_freq_exp = ones_freq.unsqueeze(2)

        # Calculate the interpolated frequency representation for each query-key pair
        # Shape: (batch_size, num_heads, seq_len_q, seq_len_k, head_dim)
        interp_freq = attn_weights * V_freq_exp + (1.0 - attn_weights) * ones_freq_exp

        # Multiply across the key sequence dimension (dim=3) to perform circular convolution of the attended values
        # Shape: (batch_size, num_heads, seq_len_q, head_dim)
        accum_freq = torch.prod(interp_freq, dim=3)

        # 3. Inverse FFT back to spatial domain
        out = torch.fft.ifft(accum_freq, dim=-1).real

        # --- Reshape and Output Projection ---
        # Shape: (batch_size, seq_len, embed_dim)
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.embed_dim)

        return self.out_proj(out)

if __name__ == "__main__":
    # Simple test for testability and syntax check
    batch_size = 2
    seq_len = 4
    embed_dim = 16
    num_heads = 4

    attention = PNS5ModalAttention(embed_dim=embed_dim, num_heads=num_heads)

    # Dummy inputs
    q = torch.randn(batch_size, seq_len, embed_dim)
    k = torch.randn(batch_size, seq_len, embed_dim)
    v = torch.randn(batch_size, seq_len, embed_dim)

    output = attention(q, k, v)

    print(f"Input shape: {q.shape}")
    print(f"Output shape: {output.shape}")
    assert output.shape == (batch_size, seq_len, embed_dim), "Output shape mismatch"
    print("PNS5ModalAttention forward pass successful.")
