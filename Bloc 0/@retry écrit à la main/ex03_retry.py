import functools
import time


class EchecApresRetries(Exception):
    """Levée quand toutes les tentatives ont échoué."""


def retry(*, essais=3, attente=0.5, exceptions, dormir=time.sleep):
    def decorateur(func):
        functools.wraps(func)

        def enveloppe(*args, **kwargs):
            dernier_erreur = None
            for tentative in range(essais):
                try:
                    func(*args, **kwargs)
                except exceptions as e:
                    derniere_erreur = e
                    if tentative < essais - 1:
                        dormir(attente * 2**tentative)
                raise EchecApresRetries(
                    f"{func.__name__} a échoué après {essais} tentatives"
                ) from derniere_erreur
            return enveloppe

        return decorateur
