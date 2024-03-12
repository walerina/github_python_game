level_map = [
'XX                   W      ',
'XX                   W      ',
'XXX B                W      ',
'XXXPB  XXX           WXX    ',
'X                    W   X   ',
'XXXX        EXX      WBXX   ',
'XXXX      FXX        WB X   ',
'XXX    XXXXXXXXXXXXXXWXX    ',
'XXX  E X  XXXXXXXXXX  XXX   ',
'XXXXXXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

level_map2 = [ 
'XXX                   W    X',
'XXP                   W    X',
'X                     W    X',
'XXF F  BBB  E         W    X',
'X XXXXX   XXX         W    X',
'             XX       W    X',
'               X      W    X',
'                X    XXX   X',
'                 XXXXXXXXXXX',
'                            ',
'                            ']

level_map3 = [
' XXX                    W  X',
' X       XX             W  X',
' XXP     XX       EBEBEBW  X',
' X       F              W  X',
' XXXXXXXXXXXXXXX        WX X',
'   X          X BBBBBBBB  X',
'    X       XXXXX      X    ',
'     XXXXXXX     XXXXXX     ',
'                            ',
'                            ',
'                            ']

level_maps = [level_map, level_map2, level_map3]

tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size