from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


def prompt_user_autocomplete( msg, alist ):
    answer = ''
    while True:
        completer = WordCompleter( alist )
        
        print()
        answer = prompt( msg , completer = completer)
        print()

        if answer in alist:
            break
    
    return answer