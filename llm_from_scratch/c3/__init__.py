import torch
from torch import nn


def softmax_naive(x):
    return torch.exp(x) / torch.exp(x).sum(dim=0)


# Same as Andrei-Karpathi's video
class MultiHeadAttention(nn.Module):
    """
    Implementation of MultiAttention Head.

    #1 Reduces the projection dim to match the desired output dim
    #2 Uses a Linear layer to combine head outputs
    #3 Tensor shape: (b, num_tokens, d_out)
    #4 We implicitly split the matrix by adding a num_heads dimension. Then we unroll the last dim: (b, num_tokens, d_out) -&gt; (b, num_tokens, num_heads, head_dim).
    #5 Transposes from shape (b, num_tokens, num_heads, head_dim) to (b, num_heads, num_tokens, head_dim)
    #6 Computes dot product for each head
    #7 Masks truncated to the number of tokens
    #8 Uses the mask to fill attention scores
    #9 Tensor shape: (b, num_tokens, n_heads, head_dim)
    #10 Combines heads, where self.d_out = self.num_heads * self.head_dim
    #11 Adds an optional linear projection”
    """

    def __init__(self, d_in, d_out, context_length, dropout, num_heads, qkv_bias=False):
        super().__init__()
        assert d_out % num_heads == 0, "d_out must be divisible by num_heads"

        self.d_out = d_out
        self.num_heads = num_heads
        self.head_dim = d_out // num_heads  # 1
        self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
        self.out_proj = nn.Linear(d_out, d_out)  # 2
        self.dropout = nn.Dropout(dropout)
        self.register_buffer(
            "mask", torch.triu(torch.ones(context_length, context_length), diagonal=1)
        )

    def forward(self, x):
        b, num_tokens, d_in = x.shape
        keys = self.W_key(x)  # 3
        queries = self.W_query(x)  # 3
        values = self.W_value(x)  # 3

        # b * num_tokens * d_out -> b * num_tokens * n_heads * head_dim
        keys = keys.view(b, num_tokens, self.num_heads, self.head_dim)  # 4
        values = values.view(b, num_tokens, self.num_heads, self.head_dim)
        queries = queries.view(b, num_tokens, self.num_heads, self.head_dim)

        # b * num_tokens * n_heads * head_dim -> b * n_heads * num_tokens * head_dim
        keys = keys.transpose(1, 2)  # 5
        queries = queries.transpose(1, 2)  # 5
        values = values.transpose(1, 2)  # 5

        # queries: b * n_heads * num_tokens * head_dim
        # keys.T :   b * n_heads * head_dim * num_tokens
        # =>
        # attn_scores: b * n_heads * num_tokens * num_tokens
        attn_scores = queries @ keys.transpose(2, 3)  # 6

        mask_bool = self.mask.bool()[:num_tokens, :num_tokens]  # 7
        attn_scores.masked_fill_(mask_bool, -torch.inf)  # 8

        attn_weights = torch.softmax(attn_scores / keys.shape[-1] ** 0.5, dim=-1)
        attn_weights = self.dropout(attn_weights)

        # attn_weights: b * n_heads * num_tokens * num_tokens
        # values      : b * n_heads * num_tokens * head_dim
        # =>
        # context_vec  : b * n_heads * num_tokens * head_dim
        # =>
        # context_vec  : b * num_tokens * n_heads * head_dim
        context_vec = (attn_weights @ values).transpose(1, 2)  # 9

        # contiguous arranges the memory in a good shape again
        # required by view.
        # before: b * num_tokens * n_heads * head_dim
        # after:  b * num_tokens * d_out
        context_vec = context_vec.contiguous().view(b, num_tokens, self.d_out)  # 10

        # in karpathy's video, he also added a dropout here.
        # for the book the drop_out is outside in the Transformer Block.

        # not sure what the point of this is. There is a layer norm and feed
        # forward network in the transformer block after here anyway. Also
        # karpathy does not have this.
        context_vec = self.out_proj(context_vec)  # 11

        return context_vec
