# Source: https://www.programcreek.com/python/?CodeExample=select+folder
# Example: 11

from tkinter import filedialog
from tkinter import Tk
    
def select_folder(title='Select folder', initialdir='.'):
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title, 
                                          initialdir=initialdir)
    root.destroy()
    return folder_path 

if __name__ == '__main__':
    
    sf = select_folder(initialdir='.')
    if sf:
        print(f'Selected folder:\n{sf}')
    else:
        print('Selection cancelled!')