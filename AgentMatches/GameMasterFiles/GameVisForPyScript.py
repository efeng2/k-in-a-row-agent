print("Loading seed file GameVisForPyScript.py")

'''GameVisForPyScript.py
    Initializes some display stuff, and then provides the
    render_state method for turning a state description
    into a Canvas-graphics rendering.

Development plan as of Nov. 16 at 11:00 AM:

1. Write a function that gets the game board dimensions N and M
and is callable from WebGameClient whenever the user changes
the game type.  Connect it to a Selection element on the page.


 Verify that Python variables hold the size of the CANVAS object.

'''

import js  # Comes from the main HTML page and the script it contains.
from pyodide.ffi import create_proxy, to_js

CTX = None
CANVAS = None

c_side = 32 # Based on the pixels dimensions of component .png images.
def set_up_gui(n, m):
  '''Do any pre-session setup that might be
  needed, like computing constantss.'''
  global CTX, CANVAS 

  CTX = js.CTX
  CANVAS = js.CANVAS
  CANVAS.width = m*c_side
  CANVAS.height = n*c_side
  
  #print("In GameVisForPyScript.py, finished call to set_up_gui.")
  
def cx_from_x(x):
  # Converts a state's x value to a canvas x.
  return x * SCALE_X + ACTUAL_ORIGIN_X

def cy_from_y(y):
  # Converts a state's x value to a canvas x.
  return y * SCALE_Y + ACTUAL_ORIGIN_Y


def render_state_canvas_graphics(s):
    CTX.clearRect(0, 0, CANVAS.width, CANVAS.height)
    # loop through the squares, drawing each one.

    board = s.board

    cy = 0
    for row in board:

        cx = 0
        for item in row:
            
             draw_image(cx, cy, item)
             cx += c_side

        cy += c_side

def draw_text(cx, cy, item):
    w = c_side; h = c_side
    CTX.fillStyle = "red"
    CTX.font = "bold 30px serif"
    #CTX.textAlign = 'left'
    CTX.textAlign = 'center'
    CTX.fillText(item, cx + w/2, cy + h/2)
    #CTX.drawText(item, cy, cy)

#    renderCommentary("It is "+who+"'s turn to move.\n")
def draw_image(cx, cy, item):
  w = c_side; h = c_side
  image = {"X": "X128", "O": "O128", " ": "gray128", "-": "black128"}[item]
  img = image+".png"
  #js.OLD_get_and_use_image(img, create_proxy(lambda img: CTX.drawImage(img, cx, cy, w, h)))
  Im = js.Image.new();
  Im.src = "GameMasterFiles/img/"+img
  Im.onload = create_proxy(lambda dummy: CTX.drawImage(Im, cx, cy, w, h))
  
