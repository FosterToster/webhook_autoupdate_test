from dataclasses import dataclass
from typing import Callable, Union, Any

@dataclass
class GithubWebhookHandler():
    repository_name: str
    prod_branch_name:str = 'master'
    message_hook:str = 'Merge pull request'
    on_before_update: Union[Callable, None] = None
    on_update: Union[Callable, None] = None
    on_after_update: Union[Callable, None] = None
    on_restart: Union[Callable, None] = None
    dataset: Union[dict, None] = None

    
            