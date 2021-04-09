from dataclasses import dataclass
from typing import Callable, Union, Any

@dataclass
class GithubWebhookHandler():
    def __init__(self,
        repository_name: str,
        main_branch_name:str = 'master',
        production_branch_name:str = 'mas/prod',
        message_hook:str = 'Merge pull request',
        on_before_update: Union[Callable, None] = None,
        on_update: Union[Callable, None] = None,
        on_after_update: Union[Callable, None] = None,
        on_restart: Union[Callable, None] = None,
    ):

        self.repository_name = repository_name 
        self.main_branch_name = main_branch_name 
        self.production_branch_name = production_branch_name 
        self.message_hook = message_hook 
        self.on_before_update = on_before_update 
        self.on_update = on_update 
        self.on_after_update = on_after_update 
        self.on_restart = on_restart 


    def before_update(self):
        if not (self.on_before_update is None):
            return self.on_before_update(self)

    
    def update(self):
        if not (self.on_update is None):
            return self.on_update(self)


    def after_update(self):
        if not (self.on_after_update is None):
            return self.on_after_update(self)


    def restart(self):
        if not (self.on_restart is None):
            return self.on_restart(self)

    
    

    
            