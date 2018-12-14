# Matthew N. Brown copyright 2007

# Here is an example program in wich
# balls hit walls and other balls:
#
# This program draws circles using:   pygame.draw.circle
#
# You can copy this program on to
# your own computer and run it.
#

import os, sys

 ## INIT STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################
def HE_HE_init():
    global screen, big_black_rect, APPLICATION_w_size, APPLICATION_z_size
    global WOW_pi_divided_by_180, WOW_180_divided_by_pi
    pygame.init()
    random.seed()
    APPLICATION_w_size = 700
    APPLICATION_z_size = 500
    ##### To close window while in fullscreen, press Esc while holding shift. #######
    screen = pygame.display.set_mode((APPLICATION_w_size, APPLICATION_z_size))
    #screen = pygame.display.set_mode((APPLICATION_w_size, APPLICATION_z_size), FULLSCREEN)
    pygame.display.set_caption("They bwounce off bwalls? Matthew N. Brown copyright 2007")
    pygame.mouse.set_visible(1)
    big_black_rect = pygame.Surface(screen.get_size())
    big_black_rect = big_black_rect.convert()
    big_black_rect.fill((0, 0, 0))
    screen.blit(big_black_rect, (0, 0))
    #fonty = pygame.font.Font(None, 36)
    fonty = pygame.font.SysFont("Times New Roman", 25)
    fonty.set_bold(0)
    IMAGEE = fonty.render('Loading . . .', 1, (0, 250, 10))
    screen.blit(IMAGEE, (100, 200)); del IMAGEE
    pygame.display.flip()
    pygame.mixer.init(22050, -16, True, 1024)
    WOW_pi_divided_by_180 = math.pi / 180.0
    WOW_180_divided_by_pi = 180.0 / math.pi
    set_up_key_variables()
    Lets_ROLL()
 ## INIT STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################

 ## SAVE LEVEL?!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################
def write_to_file_WEEE_STRANGE(file_namey, data):
    noq = '\n'
    filey = open(file_namey, 'w')
    for d in data:
     filey.write(   str(d) + noq)
 ## SAVE LEVEL?!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################

 ## SMALL FUNCTIONS STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################
     ### some functions: ###
def distance_2D (w1, z1, w2, z2):
    return math.sqrt(math.pow(float(w1) - float(w2), 2) + math.pow(float(z1) - float(z2), 2))
def rect_touching_rect(w1, z1, wol1, zol1, w2, z2, wol2, zol2):
    w2 -= w1
    z2 -= z1
    ww1 = -wol2
    zz1 = -zol2
    return (w2 > ww1 and w2 < wol1 and z2 > zz1 and z2 < zol1)
def rect_touching_rect2(w1, z1, wol1, zol1, w2, z2, wol2, zol2):
    w2 -= w1
    z2 -= z1
    ww1 = -wol2
    zz1 = -zol2
    return (w2 >= ww1 and w2 <= wol1 and z2 >= zz1 and z2 <= zol1)
def positive(n):
    if n < 0: n = -n; return n
def int_randy(range, add):
    return int((random.random() * range) + add)
def randy(range, add):
    return (random.random() * range) + add
def freaky_rect_switcharoo_2D(pw, pz, pwol, pzol, buffy_the_fat):
    buffy_the_fat2 = buffy_the_fat * 2
    if pwol > 0:
     gw = pw; gwol = pwol
    else:
     gw = pwol + pw; gwol = pw - gw
    if pzol > 0:
     gz = pz; gzol = pzol
    else:
     gz = pzol + pz; gzol = pz - gz
    return [gw - buffy_the_fat, gz - buffy_the_fat, gwol + buffy_the_fat2, gzol + buffy_the_fat2]
def points_rotated_by_angle_2D(points_wz, axis_w, axis_z, angle):
    rotated_points_wz = []
    angle = -angle -90
    angle_times_WOW_pi_divided_by_180 = angle * WOW_pi_divided_by_180
    c1 = math.cos(angle_times_WOW_pi_divided_by_180)
    s1 = math.sin(angle_times_WOW_pi_divided_by_180)
    for pointy in points_wz:
     xt = pointy[0] - axis_w
     yt = pointy[1] - axis_z
     rotated_points_wz += [(-xt * s1) + (yt * c1) + axis_w, (-xt * c1) - (yt * s1) + axis_z]
    return rotated_points_wz
def point_rotated_by_angle_2D(point_w, point_z, axis_w, axis_z, angle):
    angle = -angle -90
    angle_times_WOW_pi_divided_by_180 = angle * WOW_pi_divided_by_180
    c1 = math.cos(angle_times_WOW_pi_divided_by_180)
    s1 = math.sin(angle_times_WOW_pi_divided_by_180)
    xt = point_w - axis_w
    yt = point_z - axis_z
    return (-xt * s1) + (yt * c1) + axis_w, (-xt * c1) - (yt * s1) + axis_z
def arc_tangent_2D(point_w, point_z):
    return math.atan2(point_w, point_z) * WOW_180_divided_by_pi + 180
def arc_tangent_2D_2(point_w, point_z):
    return -math.atan2(point_w, point_z) * WOW_180_divided_by_pi + 180
def ball_to_ball_wzkol_bounce(V1, m1, V2, m2, ball1_is_to_the_left):
    if (ball1_is_to_the_left and V1 >= V2) or (not ball1_is_to_the_left and V1 <= V2):
     Rv1 = V1 - V2
     Rv2 = 0 #V2 - V2
     NewV1 = ((m1 - m2) / float(m1 + m2)) * float(Rv1) + V2
     NewV2 = (( 2 * m1) / float(m1 + m2)) * float(Rv1) + V2
     return NewV1, NewV2
    else:
     return V1, V2
def Find_where_ball_stops_on_line_w(ball_w, ball_z, ball_wol, ball_zol, ball_rad, line_w, line_rad):
    did_collide = False
    totally = ball_rad + line_rad
    b1 = line_w + totally
    b2 = line_w - totally
    New_ball_w = ball_w + ball_wol
    New_ball_z = ball_z + ball_zol
    if   ball_w >= b1 and ball_wol < 0 and New_ball_w < b1: New_ball_w = b1; did_collide = True
    elif ball_w <= b2 and ball_wol > 0 and New_ball_w > b2: New_ball_w = b2; did_collide = True
    else:
     if ball_w > b2 and ball_w < b1:
      if   ball_w > line_w and ball_wol < 0:
       New_ball_w = ball_w; New_ball_z = ball_z
       did_collide = True
      elif ball_w < line_w and ball_wol > 0:
       New_ball_w = ball_w; New_ball_z = ball_z
       did_collide = True
     return New_ball_w, New_ball_z, did_collide
    New_ball_z = (float(ball_zol) / float(ball_wol) * float(New_ball_w - ball_w)) + float(ball_z)
    return New_ball_w, New_ball_z, did_collide
def find_where_ball_collides_on_a_wall(
                                       ball_w, ball_z,
                                       ball_wol, ball_zol,
                                       ball_rad,
                                       wall_type,
                                       wall_w1, wall_z1,
                                       wall_w2, wall_z2,
                                       wall_rad):
    toetoadly = ball_rad + wall_rad
    did_collide = False
    New_ball_w = ball_w + ball_wol
    New_ball_z = ball_z + ball_zol
    angle_hit_at = None
    Relate_ball_w = ball_w - wall_w1
    Relate_ball_z = ball_z - wall_z1
    Relate_wall_w2 = wall_w2 - wall_w1
    Relate_wall_z2 = wall_z2 - wall_z1
    arc_tangeriney = arc_tangent_2D(Relate_wall_w2, Relate_wall_z2)
    Rotate_Relate_ball_w, Rotate_Relate_ball_z, Rotate_Relate_wall_w2, Rotate_Relate_wall_z2 = points_rotated_by_angle_2D(((Relate_ball_w, Relate_ball_z), (Relate_wall_w2, Relate_wall_z2)), 0, 0, arc_tangeriney)
    Rotate_ball_wol, Rotate_ball_zol = point_rotated_by_angle_2D(ball_wol, ball_zol, 0, 0, arc_tangeriney)
    Rotate_Relate_ball_collide_w, Rotate_Relate_ball_collide_z, did_hit_weird_line = Find_where_ball_stops_on_line_w(Rotate_Relate_ball_w, Rotate_Relate_ball_z, Rotate_ball_wol, Rotate_ball_zol, ball_rad, 0, wall_rad)
    if Rotate_Relate_ball_w > -toetoadly and Rotate_Relate_ball_w < toetoadly:
     HE_HE_strange_popper_z = Rotate_Relate_ball_z
    else:
     HE_HE_strange_popper_z = Rotate_Relate_ball_collide_z
    Rotate_angle_hit_at = None
    if   HE_HE_strange_popper_z < Rotate_Relate_wall_z2:
       if ball_is_going_towards_point(Rotate_Relate_ball_w, Rotate_Relate_ball_z, Rotate_ball_wol, Rotate_ball_zol, 0, Rotate_Relate_wall_z2):
        p1_touched, p1_collide_w, p1_collide_z, p1_angle_hit_at = find_where_ball_collides_on_another_ball(Rotate_Relate_ball_w, Rotate_Relate_ball_z, Rotate_ball_wol, Rotate_ball_zol, ball_rad, 0, Rotate_Relate_wall_z2, wall_rad)
        if p1_touched:
         Rotate_Relate_ball_collide_w = p1_collide_w
         Rotate_Relate_ball_collide_z = p1_collide_z
         Rotate_angle_hit_at = p1_angle_hit_at
         did_collide = True
    elif HE_HE_strange_popper_z > 0:
       if ball_is_going_towards_point(Rotate_Relate_ball_w, Rotate_Relate_ball_z, Rotate_ball_wol, Rotate_ball_zol, 0, 0):
        p2_touched, p2_collide_w, p2_collide_z, p2_angle_hit_at = find_where_ball_collides_on_another_ball(Rotate_Relate_ball_w, Rotate_Relate_ball_z, Rotate_ball_wol, Rotate_ball_zol, ball_rad, 0, 0, wall_rad)
        if p2_touched:
         Rotate_Relate_ball_collide_w = p2_collide_w
         Rotate_Relate_ball_collide_z = p2_collide_z
         Rotate_angle_hit_at = p2_angle_hit_at
         did_collide = True
    else:
       if did_hit_weird_line:
        did_collide = True
        if Rotate_Relate_ball_collide_w < 0: Rotate_angle_hit_at = 90
        else: Rotate_angle_hit_at = 270
    if did_collide:
     arc_tangeriney_2 = -arc_tangeriney
     angle_hit_at = Rotate_angle_hit_at + arc_tangeriney
     New_ball_w, New_ball_z = point_rotated_by_angle_2D(Rotate_Relate_ball_collide_w, Rotate_Relate_ball_collide_z, 0, 0, arc_tangeriney_2)
     New_ball_w += wall_w1
     New_ball_z += wall_z1
    return did_collide, New_ball_w, New_ball_z, angle_hit_at  #, is_moving_towards
def zol_at_angle(wol, zol, angle):
    rotated_wol, rotated_zol = point_rotated_by_angle_2D(wol, zol, 0, 0, angle)
    return rotated_zol
def wzol_bounce_at_angle(wol, zol, angle, multi):
    rotated_wol, rotated_zol = point_rotated_by_angle_2D(wol, zol, 0, 0, angle)
    if rotated_zol > 0: rotated_zol = -rotated_zol * multi
    return point_rotated_by_angle_2D(rotated_wol, rotated_zol, 0, 0, -angle)
def ball_is_going_towards_point(ball_w, ball_z, ball_wol, ball_zol, point_w, point_z):
    angley = arc_tangent_2D(ball_w - point_w, ball_z - point_z)
    rotated_wol, rotated_zol = point_rotated_by_angle_2D(ball_wol, ball_zol, 0, 0, angley)
    return rotated_zol > 0
def find_where_ball_collides_on_another_ball (
                                               ball1_w, ball1_z,
                                               ball1_wol, ball1_zol,
                                               ball1_rad,
                                               ball2_w, ball2_z,
                                               ball2_rad
                                             ):
    totally = ball1_rad + ball2_rad
    dis_from_each_other = math.sqrt(math.pow(float(ball1_w) - float(ball2_w), 2) + math.pow(float(ball1_z) - float(ball2_z), 2))
    if dis_from_each_other < totally:
     angley = arc_tangent_2D(ball1_w - ball2_w, ball1_z - ball2_z)
     return True, ball1_w, ball1_z, angley
    else:
        they_did_touch = False
        New_ball1_w = ball1_w + ball1_wol
        New_ball1_z = ball1_z + ball1_zol
        angle_hit_at = None
        Relate_ball1_w = ball1_w - ball2_w
        Relate_ball1_z = ball1_z - ball2_z
        Relate_ball2_w = 0
        Relate_ball2_z = 0
        arcy_tangeriney = arc_tangent_2D(ball1_wol, ball1_zol)
        Rotated_Relate_ball1_w, Rotated_Relate_ball1_z, Rotated_ball1_wol, Rotated_ball1_zol = points_rotated_by_angle_2D(((Relate_ball1_w, Relate_ball1_z), (ball1_wol, ball1_zol)), 0, 0, arcy_tangeriney)
        did_collidey = False
        if Rotated_Relate_ball1_z > 0 and (Rotated_Relate_ball1_w > -totally and Rotated_Relate_ball1_w < totally):
         Rotated_Relate_ball1_collide_w = Rotated_Relate_ball1_w # + Rotated_ball1_wol
         HE_HE = math.pow(Rotated_Relate_ball1_w, 2) - math.pow(totally, 2)
         if HE_HE < 0: HE_HE = -HE_HE
         Rotated_Relate_ball1_collide_z = math.sqrt(HE_HE)
         Rotated_Relate_ball1_z__PLUS__Rotated_ball1_zol = Rotated_Relate_ball1_z + Rotated_ball1_zol
         if Rotated_Relate_ball1_collide_z < Rotated_Relate_ball1_z__PLUS__Rotated_ball1_zol:
          collision_wol = Rotated_ball1_wol
          collision_zol = Rotated_ball1_zol
          Rotated_Relate_ball1_collide_z = Rotated_Relate_ball1_z__PLUS__Rotated_ball1_zol
          angley_to_hit = None
         else:
          did_collidey = True
          they_did_touch = True
          angley_to_hit = arc_tangent_2D(Rotated_Relate_ball1_collide_w, Rotated_Relate_ball1_collide_z)
        else:
         angley_to_hit = None
         collision_wol = Rotated_ball1_wol
         collision_zol = Rotated_ball1_zol
         Rotated_Relate_ball1_collide_w = Rotated_Relate_ball1_w + Rotated_ball1_wol
         Rotated_Relate_ball1_collide_z = Rotated_Relate_ball1_z + Rotated_ball1_zol
        if did_collidey:
         arcy_tangeriney_2 = -arcy_tangeriney
         angle_hit_at = angley_to_hit + arcy_tangeriney
         New_ball1_w, New_ball1_z = point_rotated_by_angle_2D(Rotated_Relate_ball1_collide_w, Rotated_Relate_ball1_collide_z, 0, 0, arcy_tangeriney_2)
         New_ball1_w += ball2_w
         New_ball1_z += ball2_z
    return they_did_touch, New_ball1_w, New_ball1_z, angle_hit_at  #, New_ball1_wol, New_ball1_zol
     ### some functions: ###

 ## GRAPHICS STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################
def chilly_font(size):
    fonti = pygame.font.SysFont("Times New Roman", size)
    return fonti
def chilly_font_Italicy(size):
    fonti = pygame.font.SysFont("Times New Roman", size)
    fonti.set_italic(1)
    return fonti
def draw_loading_messagey(stringy): # Draw loading message
    pygame.mouse.set_visible(1)
    fonty = chilly_font(26)
    IMAGEE = fonty.render(stringy, 0, (0, 255, 0), (0, 0, 0))
    screen.blit(IMAGEE, (200, 250))
    del IMAGEE
    pygame.display.flip()
           ## GRAPHICS STUFF: ##
#########################################################################################

 ## KEYS AND MOUSE STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################
def set_up_key_variables():
     global ky_held, ky_first_held, ky_time_last_pressed
     global mowse_w, mowse_z, mowse_inn
     global mowse_left_pressed, mowse_right_pressed, mowse_left_held, mowse_right_held
     mowse_left_held = False
     mowse_right_held = False
     mowse_left_pressed = False
     mowse_right_pressed = False
     mowse_w = 0
     mowse_z = 0
     mowse_inn = 0
     ky_held = []
     ky_first_held = []
     ky_time_last_pressed = []
     m = -1
     while m < 500:
      m += 1
      ky_held              += [0]
      ky_first_held        += [0]
      ky_time_last_pressed += [0]
def clear_all_kys():
    global mowse_left_pressed, mowse_right_pressed, mowse_left_held, mowse_right_held
    mowse_left_held = False
    mowse_right_held = False
    mowse_left_pressed = False
    mowse_right_pressed = False
    m = -1
    while (m < 500):
     m += 1; ky_held[m] = 0; ky_first_held[m] = 0; ky_time_last_pressed[m] = 0
def clear_these_ky_first_held(list_keys_numbers):
    for k in list_keys_numbers:
     ky_first_held[k] = 0
def clear_first_held_kys():
    m = -1
    while (m < 500):
     m += 1; ky_first_held[m] = 0
def old_style_ky(n):
    return (ky_first_held_CEV(n) or (ky_held[n] and ky_time_last_pressed[n] < time.time() - .3))
def ky_first_held_CEV(n):
    if (ky_first_held[n]):
     ky_first_held[n] = 0; return 1
    else:
     return 0
def mowse_in_rect (w, z, wol, zol):
    return (mowse_w >= w and mowse_z >= z and mowse_w <= w + wol and mowse_z <= z + zol)
def mowse_in_circle (w, z, rad):
    dia = rad * 2
    if mowse_in_rect(w - rad, z - rad, w + dia, z + dia):
     return (distance_2D(mowse_w, mowse_z, w, z) < rad)
    else:
     return 0
    ## CHECK FOR: KEYBOARD, MOUSE, JOYSTICK, AND OTHERY INPUTY: ##
def check_for_keys():
        global mowse_w, mowse_z, mowse_inn, mowse_left_pressed, mowse_right_pressed, mowse_left_held, mowse_right_held, APPLICATION_w_size, APPLICATION_z_size
        global loopy
        global unicodey
        mowse_left_pressed = False
        mowse_right_pressed = False
        unicodey = ''
        for e in pygame.event.get():
          if e.type == QUIT:
            loopy = 0
          elif e.type == ACTIVEEVENT:
            mowse_inn = (e.gain and (e.state == 1 or e.state == 6))
          elif e.type == KEYDOWN:
            ky_held[e.key] = 1
            ky_first_held[e.key] = 1
            ky_time_last_pressed[e.key] = time.time()
            unicodey = e.unicode
          elif e.type == KEYUP:
            ky_held[e.key] = 0
          elif e.type == MOUSEMOTION:
            mowse_w = e.pos[0]
            mowse_z = e.pos[1]
            if mowse_w >= 0 and mowse_w <= APPLICATION_w_size and mowse_z >= 0 and mowse_z <= APPLICATION_z_size:
             mowse_inn = 1
            else:
             mowse_inn = 0
          elif e.type == MOUSEBUTTONUP:
            if e.button == 1: mowse_left_held = 0
            if e.button == 3: mowse_right_held = 0
          elif e.type == MOUSEBUTTONDOWN:
            mowse_left_pressed  = (e.button == 1)
            mowse_right_pressed = (e.button == 3)
            mowse_left_held =  mowse_left_held or e.button == 1
            mowse_right_held = mowse_right_held or e.button == 3
          elif e.type == JOYAXISMOTION:
            pass
          elif e.type == JOYBALLMOTION:
            pass
          elif e.type == JOYHATMOTION:
            pass
          elif e.type == JOYBUTTONUP:
            pass
          elif e.type == JOYBUTTONDOWN:
            pass
          elif e.type == VIDEORESIZE:
            print (e)
            print ("What happened!?")
            #global big_black_rect, screen
            #APPLICATION_w_size = e.size[0]
            #APPLICATION_z_size = e.size[1]
            #screen = pygame.display.set_mode((APPLICATION_w_size, APPLICATION_z_size))#, RESIZABLE)
            #big_black_rect = pygame.Surface(screen.get_size())
            #big_black_rect = big_black_rect.convert()
            #big_black_rect.fill((0, 100, 200))
          elif e.type == VIDEOEXPOSE:
            pass
          elif e.type == USEREVENT:
            pass
        if ky_held[27] and (ky_held[303] or ky_held[304]): loopy = 0
    ## CHECK FOR: KEYBOARD, MOUSE, JOYSTICK, AND OTHERY INPUTY: ##
 ## KEYS AND MOUSE STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################

#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################


 ## MAIN LOOPY STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#########################################################################################
def ball_is_going_towards_ball(Bn1, Bn2):
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_mass, ball_RECT
    arc_tangerine = arc_tangent_2D(ball_w[Bn1] - ball_w[Bn2], ball_z[Bn1] - ball_z[Bn2])
    woly1, zoly1 = point_rotated_by_angle_2D(ball_wol[Bn1], ball_zol[Bn1], 0, 0, arc_tangerine)
    return zoly1 > 0
def ball_is_relatively_going_towards_ball(Bn1, Bn2):
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_mass, ball_RECT
    arc_tangerine = arc_tangent_2D(ball_w[Bn1] - ball_w[Bn2], ball_z[Bn1] - ball_z[Bn2])
    woly1, zoly1, woly2, zoly2 = points_rotated_by_angle_2D(((ball_wol[Bn1], ball_zol[Bn1]), (ball_wol[Bn2], ball_zol[Bn2])), 0, 0, arc_tangerine)
    return zoly1 > 0 and zoly1 > zoly2  # zoly2 < zoly1 or zoly2 > zoly1 # zoly1 + zoly2 > 0
    #return zoly1 > 0 or zoly1 > zoly2
def Make_two_balls_hit_at_angle(Bn1, Bn2, angle):
    global bounce_friction
    #print angle
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_mass, ball_RECT
    woly1, zoly1, woly2, zoly2 = points_rotated_by_angle_2D(((ball_wol[Bn1], ball_zol[Bn1]), (ball_wol[Bn2], ball_zol[Bn2])), 0, 0, angle)
    V1 = zoly1 * bounce_friction
    V2 = zoly2 * bounce_friction
    zoly1, zoly2 = ball_to_ball_wzkol_bounce(V1, ball_mass[Bn1], V2, ball_mass[Bn2], True)
    ball_wol[Bn1], ball_zol[Bn1], ball_wol[Bn2], ball_zol[Bn2] = points_rotated_by_angle_2D(((woly1, zoly1), (woly2, zoly2)), 0, 0, -angle)
    updatey_ball_quick_rect(Bn1)
    updatey_ball_quick_rect(Bn2)
def updatey_ball_quick_rect(B):
    dia = ball_rad[B] * 2 + 4
    ball_squar[B] = [ball_w[B] - ball_rad[B] - 2, ball_z[B] - ball_rad[B] - 2, dia, dia]
    ball_RECT[B] = freaky_rect_switcharoo_2D(ball_w[B], ball_z[B], ball_wol[B], ball_zol[B], ball_rad[B] + 4)
def minus_ball_thing(n):
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_angle, ball_angleol, ball_squar, ball_mass, ball_RECT
    if ball_max >= 0:
     del ball_w      [n]
     del ball_z      [n]
     del ball_wol    [n]
     del ball_zol    [n]
     del ball_rad    [n]
     del ball_color  [n]
     del ball_squar  [n]
     del ball_angle  [n]
     del ball_angleol[n]
     del ball_mass   [n]
     del ball_RECT   [n]
     ball_max -= 1
def add_ball_thing(w, z, wol, zol, rad, color, angle, angleol, mass_thing, rect_thing):
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_squar, ball_angle, ball_angleol, ball_mass, ball_RECT
    ball_max += 1
    ball_w       += [w]
    ball_z       += [z]
    ball_wol     += [wol]
    ball_zol     += [zol]
    ball_rad     += [rad]
    ball_color   += [color]
    ball_angle   += [angle]
    ball_angleol += [angleol]
    dia = rad * 2
    ball_squar += [[w - rad, z - rad, dia, dia]]
    if mass_thing == True:
     ball_mass += [4 / 3 * math.pi * rad * rad * rad]
    else:
     ball_mass += [mass_thing]
    if rect_thing == True:
     ball_RECT += [None]
     updatey_ball_quick_rect(ball_max)
     #ball_RECT += [freaky_rect_switcharoo_2D(w, z, wol, zol, rad)]
    else:
     ball_RECT += [rect_thing]
def minus_wall_thing(WAL):
    global wall_max, wall_type, wall_w1, wall_z1, wall_w2, wall_z2, wall_rad, wall_color, wall_RECT
    if wall_max >= 0:
     del wall_type   [WAL]
     del wall_w1     [WAL]
     del wall_z1     [WAL]
     del wall_w2     [WAL]
     del wall_z2     [WAL]
     del wall_rad    [WAL]
     del wall_color  [WAL]
     del wall_RECT   [WAL]
     wall_max        -= 1
def add_wall_thing(type, w1, z1, w2, z2, rad, color_thing, rect_thing):
    global wall_max, wall_type, wall_w1, wall_z1, wall_w2, wall_z2, wall_rad, wall_color, wall_RECT
    wall_max    += 1
    wall_type   += [type]
    wall_w1     += [w1]
    wall_z1     += [z1]
    wall_w2     += [w2]
    wall_z2     += [z2]
    wall_rad    += [rad]
    if color_thing == True:
     if   type == 1: color_thing = (220, 220, 220)
     elif type == 2: color_thing = (240, 140, 130)
     elif type == 3: color_thing = (100, 255, 100)
     elif type == 4: color_thing = (255, 100, 100)
     elif type == 5: color_thing = (100, 100, 255)
    wall_color  += [color_thing]
    if rect_thing == True:
     wall_RECT   += [freaky_rect_switcharoo_2D(w1 - 2, z1 - 2, w2 - w1 + 4, z2 - z1 + 4, rad)]
    else:
     wall_RECT   += [rect_thing]
def reset_stuff():
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_angle, ball_angleol, ball_squar, ball_mass, ball_RECT
    global wall_max, wall_type, wall_w1, wall_z1, wall_w2, wall_z2, wall_rad, wall_color, wall_RECT
    global levely
    if levely == 1:
     ball_max     = -1
     ball_w       = []
     ball_z       = []
     ball_wol     = []
     ball_zol     = []
     ball_rad     = []
     ball_color   = []
     ball_angle   = []
     ball_angleol = []
     ball_squar   = []
     ball_mass    = []
     ball_RECT    = []
     #add_ball_thing(350, 300, 0, 0, 18, (230, 230, 250), 0, 0, True, True)
     #add_ball_thing(150, 400, 0, 0, 40, (220, 210, 255), 0, 0, True, True)
     #add_ball_thing(300, 150, 0, 0, 62, (110, 106, 255), 0, 0, True, True)
     add_ball_thing(220, 200, 0, 0, 50, (180, 226, 255), 180, 0, True, True)
     wall_max    = -1
     wall_type   = []
     wall_w1     = []
     wall_z1     = []
     wall_w2     = []
     wall_z2     = []
     wall_rad    = []
     wall_color  = []
     wall_RECT   = []
     add_wall_thing(1, 160, 250, 300, 270,  1, True, True)
     add_wall_thing(1, 500, 270, 600, 310,  1, True, True)
     add_wall_thing(1, 200, 450, 600, 450, 10, True, True)
     add_wall_thing(1, 300, 350, 400, 370,  5, True, True)
     add_wall_thing(1, 300, 100, 400, 100, 20, True, True)
     add_wall_thing(1, 650, 140, 700, 200,  6, True, True)
     add_wall_thing(1, 650, 140, 600,  40,  6, True, True)
     add_wall_thing(1, 150, 340, 150, 340, 30, True, True)
     add_wall_thing(1,  40, 200,  40, 200, 30, True, True)
     add_wall_thing(1,  30, 30,  30, 30, 10, True, True)
     add_wall_thing(1,  30, 30,  30, 30, 10, True, True)
     add_wall_thing(1,  30, 30,  30, 30, 10, True, True)
     add_wall_thing(1,  30, 30,  30, 30, 10, True, True)
     add_wall_thing(1,  30, 30,  30, 30, 10, True, True)
     add_wall_thing(1,  0, 0, APPLICATION_w_size, 0, 5, True, True)
     add_wall_thing(1,  0, 0, 0, APPLICATION_z_size, 5, True, True)
     add_wall_thing(1,  0, APPLICATION_z_size, APPLICATION_w_size, APPLICATION_z_size, 5, True, True)
     add_wall_thing(1,  APPLICATION_w_size, 0, APPLICATION_w_size, APPLICATION_z_size, 5, True, True)
    elif levely == 2:
     ball_max = 1
     ball_w = [323.62638473709342, 384.72135876760257]
     ball_z = [298.67896746658624, 109.24043981044279]
     ball_wol = [-0.27396932987421913, 7.133321987715842]
     ball_zol = [-0.38420912894762504, 1.6564147490246901]
     ball_rad = [15, 28]
     ball_color = [(137, 244, 234), (138, 221, 217)]
     ball_angle = [51.908780125668613, 294.77431504891717]
     ball_angleol = [-1.2400074168431123, 17.698615258690229]
     ball_squar = [[306.62638473709342, 281.67896746658624, 34, 34], [354.72135876760257, 79.240439810442794, 60, 60]]
     ball_mass = [10602.875205865552, 68964.24193160313]
     ball_RECT = [[304.35241540721921, 279.2947583376386, 38.273969329874205, 38.384209128947646], [352.72135876760257, 77.240439810442794, 71.133321987715846, 65.656414749024691]]
     wall_max = 17
     wall_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
     wall_w1 = [189, 290, 166, 14, 697, 562, 643, 3, 0, 223, 117, 695, 497, 497, 0, 0, 0, 700]
     wall_z1 = [284, 316, 436, 499, 446, 0, 128, 225, 106, 310, 155, 210, 159, 159, 0, 0, 500, 0]
     wall_w2 = [222, 446, 697, 157, 377, 681, 679, 49, 383, 287, 5, 448, 376, 546, 700, 0, 700, 700]
     wall_z2 = [301, 314, 478, 432, 487, 99, 98, 416, 171, 324, 225, 323, 147, 179, 0, 500, 500, 500]
     wall_rad = [1, 1, 10, 5, 20, 6, 6, 30, 30, 10, 10, 10, 10, 10, 5, 5, 5, 5]
     wall_color = [(220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220)]
     wall_RECT = [[186, 281, 39, 23], [287, 313, 162, 4], [154, 424, 555, 66], [7, 429, 157, 73], [359, 424, 356, 85], [554, -8, 135, 115], [635, 94, 52, 38], [-29, 193, 110, 255], [-32, 74, 447, 129], [211, 298, 88, 38], [-3, 143, 128, 94], [440, 198, 263, 137], [368, 139, 137, 28], [485, 147, 73, 44], [-7, -7, 714, 14], [-7, -7, 14, 514], [-7, 493, 714, 14], [693, -7, 14, 514]]
    elif levely == 3:
     ball_max = 2
     ball_w = [425.0, 492.31837629165733, 98.512856261065167]
     ball_z = [126.0, 422.24553778829392, 430.4902396760661]
     ball_wol = [-12.0, 2.6816237083426699, 6.487143738934833]
     ball_zol = [-3.0, -1.245537788293916, -21.490239676066096]
     ball_rad = [15, 28, 21]
     ball_color = [(137, 244, 234), (138, 221, 217), (136, 235, 236)]
     ball_angle = [93.833857527468922, 75.681742520058592, 323.2915629772819]
     ball_angleol = [-0.87655530207419896, 0.30220691772972269, 1.1825329351046094]
     ball_squar = [[408.0, 109.0, 34, 34], [462.31837629165733, 392.24553778829392, 60, 60], [75.512856261065167, 407.4902396760661, 46, 46]]
     ball_mass = [10602.875205865552, 68964.24193160313, 29094.28956489508]
     ball_RECT = [[394.0, 104.0, 50.0, 41.0], [460.31837629165733, 389.0, 66.68162370834267, 65.245537788293916], [73.512856261065167, 384.0, 56.487143738934833, 71.490239676066096]]
     wall_max = 17
     wall_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
     wall_w1 = [189, 290, 166, 14, 697, 562, 643, 3, 0, 223, 117, 695, 497, 497, 0, 0, 0, 700]
     wall_z1 = [284, 316, 436, 499, 446, 0, 128, 225, 106, 310, 155, 210, 159, 159, 0, 0, 500, 0]
     wall_w2 = [222, 446, 697, 157, 377, 681, 679, 49, 383, 287, 5, 480, 376, 546, 700, 0, 700, 700]
     wall_z2 = [301, 314, 478, 432, 487, 99, 98, 416, 171, 324, 225, 325, 147, 179, 0, 500, 500, 500]
     wall_rad = [1, 1, 10, 5, 20, 6, 6, 30, 30, 10, 10, 10, 10, 10, 5, 5, 5, 5]
     wall_color = [(220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220)]
     wall_RECT = [[186, 281, 39, 23], [287, 313, 162, 4], [154, 424, 555, 66], [7, 429, 157, 73], [359, 424, 356, 85], [554, -8, 135, 115], [635, 94, 52, 38], [-29, 193, 110, 255], [-32, 74, 447, 129], [211, 298, 88, 38], [-3, 143, 128, 94], [472, 198, 231, 139], [368, 139, 137, 28], [485, 147, 73, 44], [-7, -7, 714, 14], [-7, -7, 14, 514], [-7, 493, 714, 14], [693, -7, 14, 514]]
    elif levely == 4:
     ball_max = 15
     ball_w = [60.722554805471077, 452.1573538490178, 80.244575784959252, 38.90004863123329, 526.62934623960155, 561.76077439217966, 51.00641675327735, 476.21179724447387, 74.019911348330012, 104.13986580489509, 77.672785567417591, 97.908669417930454, 492.31309851379422, 107.55531577343871, 25.677250467589708, 408.28461679522843]
     ball_z = [123.53309256655999, 426.85562864865636, 446.98025958602022, 145.55077237791539, 432.36880616921724, 419.52605372165829, 185.76812996010321, 398.60172712183214, 227.90675893521163, 330.14246403509031, 280.7917430301959, 382.77488932204739, 431.7008452670733, 426.72875393133694, 108.86075181750218, 420.07030113046562]
     ball_wol = [0.58974898201312453, 0.29357826379544644, -0.7453458908661944, -0.26977452024547638, -0.13077525550683244, 0.35703289164546842, 0.25581836770201244, -0.16968524576896582, -0.96858759109981474, 0.020541831638986374, 0.21623640500730243, 0.16869582232640204, -0.32778500262837312, -1.0423733543425631, 0.078384075232750969, 0.070169924397188832]
     ball_zol = [2.5202528491916918, -0.067935899483811957, 1.0209651395893582, 1.5519551597452736, 0.37674466231734333, 0.7179102343171756, 1.2098558443319702, -0.21937811619009639, 1.6292902773669935, 0.95366629391114355, 0.99836183708718151, 0.65985328138026611, 0.72997687518744558, -0.33325230167901332, 1.8584237502130836, 1.1180771215980612]
     ball_rad = [12, 20, 14, 19, 14, 23, 23, 13, 25, 28, 28, 25, 20, 20, 20, 24]
     ball_color = [(132, 202, 208), (130, 220, 228), (133, 230, 241), (133, 200, 224), (138, 244, 248), (134, 176, 212), (132, 246, 206), (136, 191, 201), (130, 247, 204), (135, 190, 248), (136, 196, 244), (137, 246, 211), (132, 176, 232), (139, 200, 204), (135, 204, 206), (137, 234, 248)]
     ball_angle = [250.64218161257492, 228.50285566079282, 169.93029421257162, 93.92451866434908, 160.53385135173758, 101.81391124171368, 58.682544988047297, 42.833392250734839, 278.96920717602609, 157.52451729820555, 104.82808146227505, 319.29094377305643, 8.3988066326588289, 61.303383965779759, 262.01723832271352, 187.75853100116501]
     ball_angleol = [-11.145052526574146, 0.73910476098485844, -1.916370769365741, 7.8109934129380036, 1.2564621818214414, -0.21633250902344123, 0.96094866236460608, 18.696614939999161, -2.7765510174821686, -0.46915418861267033, 1.3615127061730832, 0.55215997018655683, 0.83188571652892485, -2.1096665563746759, 4.3536534603644128, 0.77565328887569629]
     ball_squar = [[46.722554805471077, 109.53309256655999, 28, 28], [430.1573538490178, 404.85562864865636, 44, 44], [64.244575784959252, 430.98025958602022, 32, 32], [17.90004863123329, 124.55077237791539, 42, 42], [510.62934623960155, 416.36880616921724, 32, 32], [536.76077439217966, 394.52605372165829, 50, 50], [26.00641675327735, 160.76812996010321, 50, 50], [461.21179724447387, 383.60172712183214, 30, 30], [47.019911348330012, 200.90675893521163, 54, 54], [74.139865804895095, 300.14246403509031, 60, 60], [47.672785567417591, 250.7917430301959, 60, 60], [70.908669417930454, 355.77488932204739, 54, 54], [470.31309851379422, 409.7008452670733, 44, 44], [85.555315773438707, 404.72875393133694, 44, 44], [3.6772504675897082, 86.860751817502177, 44, 44], [382.28461679522843, 394.07030113046562, 52, 52]]
     ball_mass = [5428.6721054031623, 25132.741228718347, 8620.5302414503913, 21548.184010972389, 8620.5302414503913, 38223.757816227015, 38223.757816227015, 6902.0790599367756, 49087.385212340516, 68964.24193160313, 68964.24193160313, 49087.385212340516, 25132.741228718347, 25132.741228718347, 25132.741228718347, 43429.376843225298]
     tempy = [[24.00641675327735, 158.76812996010321, 54.255818367702012, 55.209855844331969], [459.04211199870491, 381.38234900564203, 34.16968524576896, 34.219378116190114], [44.051323757230193, 198.90675893521163, 58.968587591099819, 59.629290277366991], [72.139865804895095, 298.14246403509031, 64.02054183163898, 64.953666293911141], [45.672785567417591, 248.7917430301959, 64.216236405007308, 64.998361837087188], [68.908669417930454, 353.77488932204739, 58.168695822326399, 58.659853281380265], [467.98531351116583, 407.7008452670733, 48.327785002628389, 48.729976875187447], [82.512942419096149, 402.39550162965793, 49.042373354342558, 48.333252301679011], [1.6772504675897082, 84.860751817502177, 48.078384075232748, 49.858423750213085], [380.28461679522843, 392.07030113046562, 56.070169924397192, 57.118077121598063]]
     ball_RECT = [[44.722554805471077, 107.53309256655999, 32.589748982013127, 34.520252849191692], [428.1573538490178, 402.78769274917255, 48.293578263795446, 48.067935899483814], [61.499229894093062, 428.98025958602022, 36.74534589086619, 37.020965139589357], [15.630274110987813, 122.55077237791539, 46.269774520245477, 47.551955159745276], [508.49857098409473, 414.36880616921724, 36.130775255506819, 36.376744662317343], [534.76077439217966, 392.52605372165829, 54.357032891645467, 54.717910234317173]] + tempy
     del tempy
     wall_max = 17
     wall_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
     wall_w1 = [189, 196, 166, 14, 697, 562, 643, 0, 326, 51, 18, 695, 497, 497, 0, 0, 0, 700]
     wall_z1 = [284, 221, 436, 499, 446, 0, 128, 201, 62, 9, 182, 210, 159, 159, 0, 0, 500, 0]
     wall_w2 = [220, 297, 697, 157, 377, 681, 679, 49, 304, 139, 0, 480, 376, 524, 700, 0, 700, 700]
     wall_z2 = [244, 218, 478, 432, 487, 99, 98, 416, 161, 315, 126, 325, 147, 176, 0, 500, 500, 500]
     wall_rad = [1, 1, 10, 5, 20, 6, 6, 30, 30, 10, 10, 10, 10, 10, 5, 5, 5, 5]
     wall_color = [(220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220)]
     wall_RECT = [[186, 245, 37, 38], [193, 218, 107, 3], [154, 424, 555, 66], [7, 429, 157, 73], [359, 424, 356, 85], [554, -8, 135, 115], [635, 94, 52, 38], [-32, 169, 113, 279], [276, 30, 78, 163], [39, -3, 112, 330], [-8, 118, 34, 72], [472, 198, 231, 139], [368, 139, 137, 28], [485, 147, 51, 41], [-7, -7, 714, 14], [-7, -7, 14, 514], [-7, 493, 714, 14], [693, -7, 14, 514]]
    elif levely == 5:
     ball_max = 15
     ball_w = [563.2380017184845, 135.5091931534665, 435.09697027584525, 132.51126304855137, 158.80356877160969, 486.49890666361813, 28.0454597909272, 469.94449157610796, 253.77058846375945, 33.311743878553251, 651.08671805489632, 467.4560139814393, 420.90145867058521, 248.83956419449743, 98.267666685148598, 670.85536291962285]
     ball_z = [340.3499477728684, 192.53572614832325, 274.00276170743837, 474.72360924550071, 248.04392629767023, 199.66234253741388, 291.77486188629132, 98.828156873677884, 261.79870802935454, 452.90721309179793, 434.31611085503482, 422.84067516142846, 143.71750465032488, 474.55563009909457, 63.407930077910926, 97.5392796541895]
     ball_wol = [-0.12736934788998625, -0.34670289908297647, -0.62730956112551528, -0.01316352118701539, -0.36875760413492498, 0.3253705975573648, -0.43186646985168864, 0.029829055857965088, -0.051399766840351885, 0.31143213467472303, 0.91261705660387604, -0.39289683694945782, 0.6973192899270082, -0.026739395385515136, 0.47773812365404217, -0.14449244329674141]
     ball_zol = [0.2651067487506561, 0.33747092449158278, -0.20330004911815291, 0.11263669365628809, 0.62183969591811039, 0.220324713577495, 0.12382039798193512, -0.062689280803922554, 0.13756798955280808, 0.8702172500111478, -0.031277763984301599, 0.28378328194527458, 0.1666190295210413, 0.056074468995401638, 0.75422143538357722, 0.14790083350095956]
     ball_rad = [12, 20, 14, 19, 14, 23, 23, 13, 25, 28, 28, 25, 20, 20, 20, 24]
     ball_color = [(132, 202, 208), (130, 220, 228), (133, 230, 241), (133, 200, 224), (138, 244, 248), (134, 176, 212), (132, 246, 206), (136, 191, 201), (130, 247, 204), (135, 190, 248), (136, 196, 244), (137, 246, 211), (132, 176, 232), (139, 200, 204), (135, 204, 206), (137, 234, 248)]
     ball_angle = [103.32400188884675, 316.71158855283181, 66.797426175129175, 35.509394217326573, 15.886531654813545, 0.61656478963343941, 195.33151301725019, 152.08747184390086, 199.80989069184068, 131.62120808048311, 339.38767654500623, 158.21789358507957, 322.31233400906359, 97.437869538449633, 179.6312883714439, 134.41162557033078]
     ball_angleol = [0.54118695268280415, -1.0009948706990461, -0.42583251039327935, -0.049119552546591096, -1.7234897593393199, 0.1278122582140804, -0.33925087348758332, 0.98916269599321738, 0.054177225060088277, 0.93648329222661952, 2.0855948904138386, -1.2792816321392795, 1.9343475351789952, -0.094694117658838645, 1.3328174529019678, 1.0390947956294083]
     ball_squar = [[549.2380017184845, 326.3499477728684, 28, 28], [113.5091931534665, 170.53572614832325, 44, 44], [419.09697027584525, 258.00276170743837, 32, 32], [111.51126304855137, 453.72360924550071, 42, 42], [142.80356877160969, 232.04392629767023, 32, 32], [461.49890666361813, 174.66234253741388, 50, 50], [3.0454597909272003, 266.77486188629132, 50, 50], [454.94449157610796, 83.828156873677884, 30, 30], [226.77058846375945, 234.79870802935454, 54, 54], [3.3117438785532514, 422.90721309179793, 60, 60], [621.08671805489632, 404.31611085503482, 60, 60], [440.4560139814393, 395.84067516142846, 54, 54], [398.90145867058521, 121.71750465032488, 44, 44], [226.83956419449743, 452.55563009909457, 44, 44], [76.267666685148598, 41.407930077910926, 44, 44], [644.85536291962285, 71.5392796541895, 52, 52]]
     ball_mass = [5428.6721054031623, 25132.741228718347, 8620.5302414503913, 21548.184010972389, 8620.5302414503913, 38223.757816227015, 38223.757816227015, 6902.0790599367756, 49087.385212340516, 68964.24193160313, 68964.24193160313, 49087.385212340516, 25132.741228718347, 25132.741228718347, 25132.741228718347, 43429.376843225298]
     tempy = [[140.43481116747478, 230.04392629767023, 36.368757604134913, 36.621839695918112], [459.49890666361813, 172.66234253741388, 54.325370597557367, 54.220324713577497], [0.61359332107551268, 264.77486188629132, 54.431866469851684, 54.123820397981937], [452.94449157610796, 81.765467592873961, 34.029829055857967, 34.062689280803923], [224.7191886969191, 232.79870802935454, 58.051399766840348, 58.137567989552807], [1.3117438785532514, 420.90721309179793, 64.311432134674718, 64.870217250011152], [619.08671805489632, 402.28483309105053, 64.912617056603878, 64.031277763984292], [438.06311714448987, 393.84067516142846, 58.392896836949433, 58.283783281945276], [396.90145867058521, 119.71750465032488, 48.697319289927009, 48.166619029521044], [224.81282479911192, 450.55563009909457, 48.026739395385505, 48.056074468995405], [74.267666685148598, 39.407930077910926, 48.477738123654042, 48.754221435383577], [642.71087047632614, 69.5392796541895, 56.144492443296713, 56.147900833500962]]
     ball_RECT = [[547.11063237059454, 324.3499477728684, 32.127369347889953, 32.265106748750654], [111.16249025438353, 168.53572614832325, 48.34670289908297, 48.337470924491583], [416.46966071471974, 255.79946165832024, 36.627309561125514, 36.203300049118127], [109.49809952736436, 451.72360924550071, 46.01316352118701, 46.112636693656285]] + tempy
     del tempy
     wall_max = 17
     wall_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
     wall_w1 = [135, 120, 230, 14, 531, 562, 441, 128, 403, 51, 504, 518, 377, 447, 0, 0, 0, 700]
     wall_z1 = [265, 216, 439, 499, 339, 0, 217, 104, 306, 9, 441, 210, 168, 127, 0, 0, 500, 0]
     wall_w2 = [227, 288, 697, 157, 456, 665, 476, 432, 61, 139, 633, 547, 435, 537, 700, 0, 700, 700]
     wall_z2 = [262, 200, 478, 432, 302, 141, 228, 77, 334, 315, 295, 193, 178, 114, 0, 500, 500, 500]
     wall_rad = [1, 1, 10, 5, 20, 6, 6, 30, 30, 10, 10, 10, 10, 10, 5, 5, 5, 5]
     wall_color = [(220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220), (220, 220, 220)]
     wall_RECT = [[132, 262, 98, 3], [117, 201, 174, 14], [218, 427, 491, 63], [7, 429, 157, 73], [438, 284, 111, 73], [554, -8, 119, 157], [433, 209, 51, 27], [96, 49, 368, 83], [33, 274, 398, 92], [39, -3, 112, 330], [492, 287, 153, 162], [506, 185, 53, 33], [365, 156, 82, 34], [435, 106, 114, 29], [-7, -7, 714, 14], [-7, -7, 14, 514], [-7, 493, 714, 14], [693, -7, 14, 514]]
def draw_walls_on_big_black_rect():
    global wall_max, wall_type, wall_w1, wall_z1, wall_w2, wall_z2, wall_rad, wall_color, wall_RECT
    global big_black_rect
    global LIN_selected, CLICKER, CLICKER2
    if CLICKER:
     if LIN_selected != -1:
      nnn = LIN_selected[0]
      if LIN_selected[1] == 1:
       wall_w1[nnn] = mowse_w
       wall_z1[nnn] = mowse_z
      else:
       wall_w2[nnn] = mowse_w
       wall_z2[nnn] = mowse_z
      w1 = wall_w1[nnn]
      z1 = wall_z1[nnn]
      w2 = wall_w2[nnn]
      z2 = wall_z2[nnn]
      rad = wall_rad[nnn]
      wall_RECT[nnn] = freaky_rect_switcharoo_2D(w1 - 2, z1 - 2, w2 - w1 + 4, z2 - z1 + 4, rad)
    wl = -1
    while wl < wall_max:
     wl += 1
     w1 = wall_w1[wl]
     z1 = wall_z1[wl]
     w2 = wall_w2[wl]
     z2 = wall_z2[wl]
     rad = wall_rad[wl]
     collyu = wall_color[wl]
     pygame.draw.line(big_black_rect, collyu, (w1, z1), (w2, z2), rad * 2)
     pygame.draw.circle(big_black_rect, collyu, (w1, z1), rad)
     pygame.draw.circle(big_black_rect, collyu, (w2, z2), rad)
     #pygame.draw.rect(big_black_rect, (200, 200, 200), wall_RECT[wl], 1)
     if CLICKER2:
      if mowse_in_rect(wall_RECT[wl][0], wall_RECT[wl][1], wall_RECT[wl][2], wall_RECT[wl][3]):
       if   mowse_in_circle(w1, z1, rad+3): selected = -1; LIN_selected = [wl, 1]
       elif mowse_in_circle(w2, z2, rad+3): selected = -1; LIN_selected = [wl, 2]
def Lets_ROLL():
    global loopy
    global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_angle, ball_angleol, ball_squar, ball_mass, ball_RECT
    global wall_max, wall_type, wall_w1, wall_z1, wall_w2, wall_z2, wall_rad, wall_color, wall_RECT
    global bounce_friction, air_friction, gravity, rock_and_ROLLY
    global LIN_selected, CLICKER, CLICKER2
    global levely
    levely = 3
    bounce_friction = 0.8
    #bounce_friction = 1.0
    air_friction = 0.999
    #air_friction = 1.0
    gravity = 0.5
    rock_and_ROLLY = math.pi / 8 * 180 #24
    reset_stuff()
    fontyyy = chilly_font_Italicy(24)
    PRESS_SPACE_BAR_TO_MOVE_immy = fontyyy.render('Press SPACE BAR to start motion.', 0, (100, 200, 100))
    PRESS_SPACE_BAR_TO_STOP_immy = fontyyy.render('Press SPACE BAR to stop motion.', 0, (200, 100, 100))
    PRESS_ENTER_TO_RESET_immy    = fontyyy.render('Press ENTER to reset.', 0, (150, 150, 150))
    PRESS_MINUS_TO_MINUS_immy    = fontyyy.render('Press - to delete a ball.', 0, (150, 150, 150))
    PRESS_ADD_TO_ADD_immy        = fontyyy.render('Press + to add a ball.', 0, (150, 150, 150))
    LEFT_CLICK_TO_immy           = fontyyy.render('Left click on a "ghost ball" to change its speed.', 0, (150, 150, 150))
    RIGHT_CLICK_TO_immy          = fontyyy.render('Right click on a ball to stop its motion.', 0, (150, 150, 150))
    PRESS_S_TO_immy              = fontyyy.render('Press S to stop all balls.', 0, (150, 150, 150))
    PRESS_PAGE_UP_TO_immy        = fontyyy.render('Press Page Up to change the level.', 0, (150, 150, 150))
    #message_1_immy
    del fontyyy
    #calculate_for_sure = True
    selected = -1
    LIN_selected = -1
    move_stuff = True
    t = time.time() + .01
    CLICKER = False
    CLICKER2 = False
    loopy = 1
    while loopy:
          big_black_rect.fill((0, 0, 0))
          draw_walls_on_big_black_rect()
          screen.blit(big_black_rect, (0, 0))
          check_for_keys()
          CLICKER    = mowse_left_held
          CLICKER2   = mowse_left_pressed
          CLICKER_2  = mowse_right_held
          CLICKER2_2 = mowse_right_pressed
          if ky_first_held_CEV(32): move_stuff = not move_stuff
          if ky_first_held_CEV(13): reset_stuff()
          if ky_first_held_CEV(280):
           levely += 1
           if levely > 5: levely = 1
           reset_stuff()
          if ky_first_held_CEV(115): # S
            M = -1
            while M < ball_max:
             M += 1
             ball_wol[M] = 0
             ball_zol[M] = 0
             updatey_ball_quick_rect(M)
          if ky_first_held_CEV(45) or ky_first_held_CEV(269): # -
           minus_ball_thing(0)
          if ky_first_held_CEV(61) or ky_first_held_CEV(270): # +
           add_ball_thing(350 + randy(40, -20), 400 + randy(40, -20), randy(40, -20), randy(40, -20), int_randy(20, 10), (int_randy(10, 130), int_randy(80, 170), int_randy(50, 200)), 0, 0, True, True)
          if ky_first_held_CEV(49):
           listy  = ['Level_save']
           listy += ['ball_max = ' + str(ball_max)]
           listy += ['ball_w = ' + str(ball_w)]
           listy += ['ball_z = ' + str(ball_z)]
           listy += ['ball_wol = ' + str(ball_wol)]
           listy += ['ball_zol = ' + str(ball_zol)]
           listy += ['ball_rad = ' + str(ball_rad)]
           listy += ['ball_color = ' + str(ball_color)]
           listy += ['ball_angle = ' + str(ball_angle)]
           listy += ['ball_angleol = ' + str(ball_angleol)]
           listy += ['ball_squar = ' + str(ball_squar)]
           listy += ['ball_mass = ' + str(ball_mass)]
           listy += ['ball_RECT = ' + str(ball_RECT)]
           listy += ['wall_max = ' + str(wall_max)]
           listy += ['wall_type = ' + str(wall_type)]
           listy += ['wall_w1 = ' + str(wall_w1)]
           listy += ['wall_z1 = ' + str(wall_z1)]
           listy += ['wall_w2 = ' + str(wall_w2)]
           listy += ['wall_z2 = ' + str(wall_z2)]
           listy += ['wall_rad = ' + str(wall_rad)]
           listy += ['wall_color = ' + str(wall_color)]
           listy += ['wall_RECT = ' + str(wall_RECT)]
           ##write_to_file_WEEE_STRANGE("Level_Save.dat", listy)
           del listy
          if CLICKER2:
           allow_selectey_thing = True
          else:
           allow_selectey_thing = False
           if not CLICKER:
            selected = -1
            LIN_selected = -1
          to_be_selected = selected
          M = -1
          while M < ball_max:
           M += 1
           if move_stuff:
            move_ball(M)
           wwol = int(ball_w[M] + ball_wol[M])
           zzol = int(ball_z[M] + ball_zol[M])
           pygame.draw.circle(screen, ball_color[M], (int(ball_w[M]), int(ball_z[M])), ball_rad[M])
           blpw, blpz = point_rotated_by_angle_2D(0, -ball_rad[M], 0, 0, ball_angle[M])
           pygame.draw.line(screen, (100, 100, 100), (int(ball_w[M] + blpw), int(ball_z[M] + blpz)), (int(ball_w[M]), int(ball_z[M])))
           if not move_stuff:
            pygame.draw.circle(screen, (100, 100, 250), (wwol, zzol), ball_rad[M], 1)
            pygame.draw.circle(screen, (100, 100, 150), (wwol, zzol), int(ball_rad[M] * 1.0), 1)
            pygame.draw.circle(screen, (150, 150, 200), (wwol, zzol), int(ball_rad[M] * 0.8), 1)
            pygame.draw.circle(screen, (200, 200, 250), (wwol, zzol), int(ball_rad[M] * 0.5), 1)
            pygame.draw.line(screen, (100, 160, 250), (int(ball_w[M]), int(ball_z[M])), (wwol, zzol))
            pygame.draw.rect(screen, (130, 130, 130), ball_RECT[M], 1)
            pygame.draw.rect(screen, (140, 140, 140), ball_squar[M], 1)
           if allow_selectey_thing:
            if mowse_in_rect(ball_RECT[M][0], ball_RECT[M][1], ball_RECT[M][2], ball_RECT[M][3]):
             if mowse_in_circle(wwol, zzol, ball_rad[M]):
              to_be_selected = M
              LIN_selected = -1
           if CLICKER_2:
            if mowse_in_rect(ball_squar[M][0], ball_squar[M][1], ball_squar[M][2], ball_squar[M][3]):
             if mowse_in_circle(ball_w[M], ball_z[M], ball_rad[M]):
              ball_wol[M] = 0
              ball_zol[M] = 0
              ball_angleol[M] = 0
              updatey_ball_quick_rect(M)
           if CLICKER:
            if selected == M:
             if move_stuff:
              mowseyy_w = mowse_w
              mowseyy_z = mowse_z
              bw1 = ball_rad[M]
              bz1 = ball_rad[M]
              bw2 = APPLICATION_w_size - ball_rad[M]
              bz2 = APPLICATION_z_size - ball_rad[M]
              if mowseyy_w < bw1: mowseyy_w = bw1
              if mowseyy_w > bw2: mowseyy_w = bw2
              if mowseyy_z < bz1: mowseyy_z = bz1
              if mowseyy_z > bz2: mowseyy_z = bz2
              ww = mowseyy_w - ball_w[M]
              zz = mowseyy_z - ball_z[M]
              #dissy = distance_2D(0, 0, ww, zz)
              ball_wol[M] = ww # / 2.0 # / dissy
              ball_zol[M] = zz # / 2.0 # / dissy
             else:
              ball_wol[M] = mowse_w - ball_w[M]
              ball_zol[M] = mowse_z - ball_z[M]
             updatey_ball_quick_rect(M)
          selected = to_be_selected
          if not move_stuff:
           screen.blit(PRESS_SPACE_BAR_TO_MOVE_immy, (10, 10))
          else:
           screen.blit(PRESS_SPACE_BAR_TO_STOP_immy, (10, 10))
          screen.blit(PRESS_MINUS_TO_MINUS_immy, (10, 30))
          screen.blit(PRESS_ADD_TO_ADD_immy, (10, 50))
          screen.blit(PRESS_ENTER_TO_RESET_immy, (10, 70))
          screen.blit(LEFT_CLICK_TO_immy, (10, 90))
          screen.blit(RIGHT_CLICK_TO_immy, (10, 110))
          screen.blit(PRESS_S_TO_immy, (10, 130))
          screen.blit(PRESS_PAGE_UP_TO_immy, (10, 150))
          pygame.display.flip()
          while t > time.time(): pass
          t = time.time() + .01
 # Try_Again_HE_HE Is weird!! maybe It should be deleted!!
def move_ball(M):
            ball_angle[M] += ball_angleol[M]
            if   ball_angle[M] > 359: ball_angle[M] -= 360
            elif ball_angle[M] <   0: ball_angle[M] += 361
            #movey_bally_speciality(M, ball_wol[M], ball_zol[M], 10)
            movey_bally_speciality(M, ball_wol[M], ball_zol[M], 10)
            ball_zol[M] += gravity
            updatey_ball_quick_rect(M)
def movey_bally_speciality(M, wol_special, zol_special, Try_Again_HE_HE):
            global loopy
            global ball_max, ball_w, ball_z, ball_wol, ball_zol, ball_rad, ball_color, ball_angle, ball_angleol, ball_squar, ball_mass, ball_RECT
            global wall_max, wall_type, wall_w1, wall_z1, wall_w2, wall_z2, wall_rad, wall_color, wall_RECT
            global bounce_friction, air_friction, gravity, rock_and_ROLLY
            distance_is_supposed_to_be_at = distance_2D(0, 0, wol_special, zol_special)
            wa = ball_w[M]
            za = ball_z[M]
            #will_be_w = wa + ball_wol[M]
            #will_be_z = za + ball_zol[M]
            will_be_w = wa + wol_special
            will_be_z = za + zol_special
            LIN_collide_max = -1
            LIN_collide_w    = []
            LIN_collide_z     = []
            LIN_collide_ang    = []
            LIN_collide_dis     = []
            LL = -1
            while LL < wall_max:
              LL += 1
              if rect_touching_rect2(ball_RECT[M][0], ball_RECT[M][1], ball_RECT[M][2], ball_RECT[M][3], wall_RECT[LL][0], wall_RECT[LL][1], wall_RECT[LL][2], wall_RECT[LL][3]):
                  #print 'weee'
                  did_collide, New_ball_w, New_ball_z, angle_hit_at = find_where_ball_collides_on_a_wall(wa, za, wol_special, zol_special, ball_rad[M], wall_type[LL], wall_w1[LL], wall_z1[LL], wall_w2[LL], wall_z2[LL], wall_rad[LL])
                  if did_collide:
                   #print 'collide'
                   #print str(New_ball_w), str(New_ball_z)
                   LIN_collide_max += 1
                   LIN_collide_w    += [New_ball_w]
                   LIN_collide_z     += [New_ball_z]
                   LIN_collide_ang    += [angle_hit_at]
                   LIN_collide_dis     += [distance_2D(wa, za, New_ball_w, New_ball_z)]
            HEH_collide_max = -1
            HEH_collide_w    = []
            HEH_collide_z     = []
            HEH_collide_ang    = []
            HEH_collide_dis     = []
            HEH_collide_ball_hit = []
            M2 = -1
            while M2 < ball_max:
             M2 += 1
             if M2 != M:
              if rect_touching_rect2(ball_RECT[M][0], ball_RECT[M][1], ball_RECT[M][2], ball_RECT[M][3], ball_squar[M2][0], ball_squar[M2][1], ball_squar[M2][2], ball_squar[M2][3]):
                  #they_did_touch, New_ball1_w, New_ball1_z, angle_hit_at = find_where_ball_collides_on_another_ball(wa, za, ball_wol[M], ball_zol[M], ball_rad[M], ball_w[M2], ball_z[M2], ball_rad[M2])
                  they_did_touch, New_ball1_w, New_ball1_z, angle_hit_at = find_where_ball_collides_on_another_ball(wa, za, wol_special, zol_special, ball_rad[M], ball_w[M2], ball_z[M2], ball_rad[M2])
                  if they_did_touch:
                   HEH_collide_max += 1
                   HEH_collide_w    += [New_ball1_w]
                   HEH_collide_z     += [New_ball1_z]
                   HEH_collide_ang    += [angle_hit_at]
                   HEH_collide_dis     += [distance_2D(wa, za, New_ball1_w, New_ball1_z)]
                   HEH_collide_ball_hit += [M2]
            current_dis = distance_is_supposed_to_be_at
            Wall_to_hit_at_angley = None
            Grr = -1
            while Grr < LIN_collide_max:
             Grr += 1
             #print LIN_collide_dis[Grr], current_dis
             if LIN_collide_dis[Grr] < current_dis:
               #print 'weee!'
               Wall_to_hit_at_angley = LIN_collide_ang[Grr]
               current_dis = LIN_collide_dis[Grr]
               will_be_w = LIN_collide_w[Grr]
               will_be_z = LIN_collide_z[Grr]
            Ball_to_hit = None
            Ball_to_hit_at_angley = None
            Heh = -1
            while Heh < HEH_collide_max:
             Heh += 1
             if HEH_collide_dis[Heh] < current_dis:
              if ball_is_going_towards_ball(M, HEH_collide_ball_hit[Heh]):
               if ball_is_relatively_going_towards_ball(M, HEH_collide_ball_hit[Heh]):
                Ball_to_hit = HEH_collide_ball_hit[Heh]
                Ball_to_hit_at_angley = HEH_collide_ang[Heh]
               else:
                Ball_to_hit = None
                Ball_to_hit_at_angley = None
               current_dis = HEH_collide_dis[Heh]
               will_be_w = HEH_collide_w[Heh]
               will_be_z = HEH_collide_z[Heh]
            if Ball_to_hit != None:
             Make_two_balls_hit_at_angle(M, Ball_to_hit, Ball_to_hit_at_angley)
            else:
             #if   bouncey == 1: ball_wol[M] = -ball_wol[M] * bounce_friction
             #elif bouncey == 2: ball_zol[M] = -ball_zol[M] * bounce_friction
             if Wall_to_hit_at_angley != None:
              ball_wol[M], ball_zol[M] = wzol_bounce_at_angle(ball_wol[M], ball_zol[M], Wall_to_hit_at_angley, bounce_friction)
              ball_angleol[M] = zol_at_angle(ball_wol[M], ball_zol[M], Wall_to_hit_at_angley + 90) / ball_rad[M] * rock_and_ROLLY
            ball_w[M] = will_be_w
            ball_z[M] = will_be_z
            if ball_w[M] < 0 or ball_w[M] > APPLICATION_w_size or ball_z[M] < 0 or ball_z[M] > APPLICATION_z_size:
             #print str(M) + "   ", str(wa), str(za)
             print (str(M) + "   ", str(ball_w[M]), str(ball_z[M]), str(ball_rad[M]))
            ball_wol[M] *= air_friction
            ball_zol[M] *= air_friction
            updatey_ball_quick_rect(M)
            if current_dis < distance_is_supposed_to_be_at:
             if Try_Again_HE_HE > 0:
              distance_to_travel_next = distance_is_supposed_to_be_at - current_dis
              disy_HE_HE = distance_2D(0, 0, ball_wol[M], ball_zol[M])
              next_wol = ball_wol[M]
              next_zol = ball_zol[M]
              movey_bally_speciality(M, next_wol, next_zol, Try_Again_HE_HE - 1)

           ## Woah... Finally! Were near the end of the program! ##
if __name__ == '__main__':
  import math
  import pygame
  import random
  import time
  import gc
  import copy
  from   pygame.locals import *
  if not pygame.font: print ('Warning, fonts disabled?')
  if not pygame.mixer: print ('Warning, sound disabled?')
  HE_HE_init()
           ## THE END! ##