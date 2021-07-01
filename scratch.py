import bigDumbBird
from icecream import ic 
file = '/users/machew/documents/eagle/projects/dummy/dummy2.brd'

board = bigDumbBird.Board (file)

ic (board.getTotalSMDArea ())
