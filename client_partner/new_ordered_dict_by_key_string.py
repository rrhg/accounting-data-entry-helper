

def new_ordered_dict_by_key_string(d):
    ordered = {k:v for k,v in sorted( d.items(),key=lambda x: (x[0].lower(), x[0].islower() ) )} 
    return ordered




    # spent a few hours & couldnt get to prioritize all uppercase over lowercase (not just the first one) 
    # this the best could find which ignores case 
    # due to decoding unicode & how that works
    
    # Uppercase first but Ab was after Ad
    # ordered = {k:v for k,v in sorted( d.items(),key=lambda x:   2*ord(x[0][0].lower()) + x[0][0].islower()            )} 
    # https://stackoverflow.com/questions/57208803/how-to-sort-a-list-alphabetically-by-treating-same-letters-in-different-case-as


    # all upper case first then all lowercase
    # ordered = {k:v for k,v in sorted( d.items() )} 

    # ordered = dict(   OrderedDict( sorted( d.items(), key=lambda x: (x[0].lower(), x[0].islower() )     ) )  )


    # ordered = dict(   OrderedDict( sorted(d.items()) )   )
    # ordered = dict(   OrderedDict( d.items() )   )
    # ordered = dict(   OrderedDict( sorted( d.items(), key=str.lower() ) )  )

    # ordered = dict(   OrderedDict( sorted( d.items(), key=lambda x: x[0].lower()      ) )  )

    # ordered = dict(   OrderedDict( sorted( d.items(), key=lambda x: ( x[0].lower(), x[0] )     ) )  )

    # ordered = dict(   OrderedDict( sorted( d.items(), key=lambda x: ( x[0].lower(), x[0].islower()  )     ) )  )
   
   
    # s = sorted( d.items(), key=lambda x: ( x[0].lower(), x[0].islower()  )     )
    # ordered = dict(   OrderedDict( s )  )
    
    # ordered = dict(   OrderedDict( sorted( d.items(), key=lambda a: sum(([a[:i].lower(), a[:i]] for i in range(1, len(a)+1)),[])     ) )  )

    # ordered = dict(   
    #                 OrderedDict( sorted( d.items(),
    #                 key=lambda a: sum(([a[:i].lower(), a[:i]] for i in range(1, len(a)+1)),[])     
    #             ) )  )
    # ordered = dict(   
    #                 OrderedDict( sorted( d.items(),
    #                 key=lambda a: sum(([a[0].lower(), a[0]] for i in range(1, len(a)+1)),[])     
    #             ) )  )


    # print( sorted( d.items(), key=lambda x: ( x[0].lower(), x[0])  )  )
    # print( sorted( d.items(),    key=lambda a: sum(([a[0].lower(), a[0]] for i in range(1, len(a)+1)),[])           )  )
