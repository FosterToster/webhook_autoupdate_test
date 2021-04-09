from dataclasses import dataclass
from typing import Callable, Union, Any

@dataclass
class GithubWebhookHandler():
    repository_name: str
    prod_branch_name:str = 'master'
    message_hook:str = 'Merge pull request'
    on_update: Union[Callable(Any), None] = None
    on_restart: Union[Callable(Any), None] = None
    on_before_update: Union[Callable(Any), None] = None
    on_after_update: Union[Callable(Any), None] = None
    on_integrity_check: Union[Callable(Any), None] = None
    dataset: Union(dict, None) = None

    
            