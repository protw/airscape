## Checks whether input values has changed

def changed():
    par_names = list(in_pars.keys())
    ch = False
    new_pars = pin_wait_change(par_names)
    for par_name in par_names:
        if new_pars['name'] == par_name:
            pin['par_name'] = new_pars['value']
            ch = True
    return ch
