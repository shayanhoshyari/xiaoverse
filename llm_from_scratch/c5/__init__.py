import tensorflow  # noqa
import tiktoken
import torch

import llm_from_scratch.c2  # noqa
import llm_from_scratch.c4  # noqa


def text_to_token_ids(text: str, tokenizer: tiktoken.Encoding) -> torch.Tensor:
    encoded = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)  # 1
    return encoded_tensor


def token_ids_to_text(token_ids: torch.Tensor, tokenizer: tiktoken.Encoding) -> str:
    flat = token_ids.squeeze(0)  # 2
    return tokenizer.decode(flat.tolist())
