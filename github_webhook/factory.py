from dataclasses import dataclass
from flask import Flask, request
from flask import Blueprint
from .handler import GithubWebhookHandler
from typing import List

class GithubException(Exception):
    pass

class Github():
    '''
    Static class that handles github webhooks

    Requires Flask application to be initialized.
    
    default route
    '''

    handlers: List[GithubWebhookHandler] = list()
    blueprint = Blueprint('github','github')
    __initialized: bool = False

    def __init__(self, app: Flask, route:str = '/github_webhook'):
        if self.__class__.__initialized:
            return None

        if app is None:
            raise GithubException('Flask application required')

        self.__class__.app = app
        self.__class__.webhook_handler = self.__class__.blueprint.route('/')(self.__class__.webhook_handler) 
        app.register_blueprint(self.__class__.blueprint, url_prefix=route)
        self.__class__.__initialized = True

    
    @staticmethod
    def webhook_handler():
        try:
            dataset = request.json
            ref = dataset['ref'].get()

            if ref is None:
                raise GithubException('ref is not found in the payload')
            if ref.find('refs/heads/') >= 0:
                branch = dataset['ref'].replace('refs/heads')
            else:
                raise GithubException('refs/heads/ not found for branch in the push payload')

            repository_dataset = dataset.get('repository')
            if repository_dataset is None:
                raise GithubException('repository dataset is not found in the payload')

            repo = repository_dataset['full_name']

            handler = Github.find_handler(repo, branch)
            
            if handler is None:
                raise GithubException(f'Handler for {repo}#{branch} is not registered')

            handler.dataset = dataset

            return Github.perform_handler(handler)
            
        except Exception as e:
            return f'{e.__class__.__name__}{str(e)}'

    
    @classmethod
    def perform_handler(handler:GithubWebhookHandler):
        results = dict()
        try:
            if not (handler.on_before_update is None):
                results.update({'before_update': str(handler.on_before_update(handler))})
            
            if not (handler.on_update is None):
                results.update({'update': str(handler.on_update(handler))})

            if not (handler.on_after_update is None):
                results.update({'after_update': str(handler.on_after_update(handler))})
        except Exception as e:
            raise
        else:
            return ';'.join(f'{k}={v}' for k,v in results.items())
        finally:
            if len(results) == 0:
                raise GithubException('Nothing was handled')


    @classmethod
    def find_handler(cls, repo, branch):
        for handler in cls.handlers:
            if handler.repository_name == repo and handler.prod_branch_name == branch:
                return handler


    @classmethod
    def new_handler(cls, repository_name, production_branch_name, **options):
        '''Initialize new github webhook handler for flask application

        :param message_hook: substring of head_commit.message which will cause update sequence if found. Default = "Merge pull request "

        :param on_update: callback function which will be called when update received. Note that it overrides default update sequence

        :param on_restart: callback function which will be called when restart needed. Overrides default restart sequence

        :param on_before_update: callback function which will be called before update sequence

        :param on_after_update: callback function which will be called after update sequence

        '''

        if not (cls.find_handler(repository_name, production_branch_name) is None):
            raise GithubException(f'Handler for repository {repository_name} and branch {production_branch_name} alredy created')



        cls.handlers.append(
            GithubWebhookHandler(
                repository_name, 
                production_branch_name, 
                options.get('message_hook', 'Merge pull request '),
                options.get('on_before_update'),
                options.get('on_update'),
                options.get('on_after_update'),
                options.get('on_restart')
            ))
        return cls.handlers[-1]
        



    # @classmethod
    # def find_handler(cls, branch_name):
    #     for handler in cls.handlers



    


