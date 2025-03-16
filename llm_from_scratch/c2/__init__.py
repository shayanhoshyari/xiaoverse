from typing import Protocol
from pathlib import Path

import torch
import tiktoken
from torch.utils.data import Dataset, DataLoader

VERDICT_PATH = Path(__file__).with_name("the-verdict.txt")


class Tokenizer(Protocol):
    def encode(self, value: str) -> list[int]: ...
    def decode(self, value: list[int]) -> str: ...


class GPTDatasetV1(Dataset):
    def __init__(
        self, txt: str, tokenizer: Tokenizer, max_length: int, stride: int
    ) -> None:
        self.input_ids = list[torch.Tensor]()
        self.target_ids = list[torch.Tensor]()

        token_ids = tokenizer.encode(txt)  # 1

        for i in range(0, len(token_ids) - max_length, stride):  # 2
            input_chunk = token_ids[i : i + max_length]
            target_chunk = token_ids[i + 1 : i + max_length + 1]
            self.input_ids.append(torch.tensor(input_chunk))
            self.target_ids.append(torch.tensor(target_chunk))

    def __len__(self) -> int:  # 3
        return len(self.input_ids)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:  # 4
        return self.input_ids[idx], self.target_ids[idx]


def create_dataloader_v1(
    txt: str,
    batch_size: int = 4,
    max_length: int = 256,
    stride: int = 128,
    shuffle: bool = True,
    drop_last: bool = True,
    num_workers: int = 0,
) -> GPTDatasetV1:
    tokenizer = tiktoken.get_encoding("gpt2")  # 1
    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)  # 2
    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,  # 3
        num_workers=num_workers,  # 4
    )
    return dataloader
