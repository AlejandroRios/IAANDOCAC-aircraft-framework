"""
File name :
Author    : 
Email     : aarc.88@gmail.com
Date      : 
Last edit :
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - This function calculates the cabine dimensions
    - Reference PreSTO-Cabin - https://www.fzt.haw-hamburg.de/pers/Scholz/PreSTo/PreSTo-Cabin_Documentation_10-11-15.pdf
Inputs:
    -
Outputs:
    - 
TODO's:
    - 

"""
########################################################################################
"IMPORTS"
########################################################################################

########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################
def fuselage_cross_section(container_type,aisles_number,seats_number,cabin_height,
    seat_width,aisle_width,height_to_width_ratio):

    in_to_m = 0.0254

    # Seat dimensions economy class
    armrest_top = 22   #[inch]
    armrest_bottom = 7    # [inch]
    armrest_width = 2*in_to_m # armrest width
    armrest_top_height = armrest_top*in_to_m
    armrest_bottom_height = armrest_bottom*in_to_m

    seat_cushion_thickness_YC = 0.14 # [m] YC - economy class
    seat_cushion_width_YC = seat_width
    double_container = 'no'
    backrest_height    = 0.59 # [m]
    floor_thickness    = 0.117# [m]
    aux = ((armrest_top_height-armrest_bottom_height)-seat_cushion_thickness_YC)/2
    seat_cushion_height = aux + armrest_bottom_height

    # Default values (95% american male)
    pax_distance_head_wall = 0.06 # [m]
    pax_distance_shoulder_wall = 0.04 # [m]
    pax_shoulder_breadth = 0.53 # [m]
    pax_eye_height = 0.87 # [m]
    pax_midshoulder_height = 0.70 # [m]

    delta_z_symmetry_inferior = -1
    delta_z_symmetry_superior = 2
    points_number = 20
    seat_delta_width_floor = 0.025

    iterations         = 12

    if double_container is 'no':
        if container_type is 'none':
            lowerdeck_width_top = 0
            lowerdeck_width_bottom = 0  
            lowerdeck_height = 0 
        elif container_type is 'LD1':
            lowerdeck_width_bottom = 1.56   
            lowerdeck_width_top = 2.44
            lowerdeck_height = 1.68
        elif container_type is 'LD11':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 3.28
            lowerdeck_height = 1.68   
        elif container_type is  'LD2':
            lowerdeck_width_bottom = 1.19   
            lowerdeck_width_top = 1.66
            lowerdeck_height = 1.68  
        elif container_type is  'LD26':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.16
            lowerdeck_height = 1.68 
        elif container_type is 'LD29':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.82
            lowerdeck_height = 1.68
        elif container_type is  'LD3':
            lowerdeck_width_bottom = 1.56   
            lowerdeck_width_top = 2.11
            lowerdeck_height = 1.68
        elif container_type is 'LD3-45':
            lowerdeck_width_bottom = 1.56   
            lowerdeck_width_top = 2.11
            lowerdeck_height = 1.19
        elif container_type is  'LD3-45R':
            lowerdeck_width_bottom = 1.56   
            lowerdeck_width_top = 1.66
            lowerdeck_height = 1.19
        elif container_type is  'LD3-45W':
            lowerdeck_width_bottom = 1.43   
            lowerdeck_width_top = 2.53
            lowerdeck_height = 1.14
        elif container_type is  'LD39':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.82
            lowerdeck_height = 1.68
        elif container_type is  'LD4':
            lowerdeck_width_bottom = 2.44   
            lowerdeck_width_top = 2.54
            lowerdeck_height = 1.68
        elif container_type is  'LD6':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.16
            lowerdeck_height = 1.68
        elif container_type is  'LD8':
            lowerdeck_width_bottom = 2.44   
            lowerdeck_width_top = 3.28
            lowerdeck_height = 1.68
        elif container_type is  'LD9':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 3.28
            lowerdeck_height = 1.68
    else:
        if container_type is  'None':
            lowerdeck_width_top = 0
            lowerdeck_width_bottom = 0  
            lowerdeck_height = 0  
        elif container_type is  'LD1':
            lowerdeck_width_bottom = 3.22   
            lowerdeck_width_top = 4.77
            lowerdeck_height = 1.68
        elif container_type is  'LD11':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 3.28
            lowerdeck_height = 1.68   
        elif container_type is  'LD2':
            lowerdeck_width_bottom = 2.49   
            lowerdeck_width_top = 3.22
            lowerdeck_height = 1.68  
        elif container_type is  'LD26':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.16
            lowerdeck_height = 1.68 
        elif container_type is  'LD29':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.82
            lowerdeck_height = 1.68
        elif container_type is  'LD3':
            lowerdeck_width_bottom = 3.22   
            lowerdeck_width_top = 4.11
            lowerdeck_height = 1.68
        elif container_type is  'LD3-45':
            lowerdeck_width_bottom = 3.22   
            lowerdeck_width_top = 4.11
            lowerdeck_height = 1.19
        elif container_type is  'LD3-45R':
            lowerdeck_width_bottom = 1.56   
            lowerdeck_width_top = 1.66
            lowerdeck_height = 1.19
        elif container_type is  'LD3-45W':
            lowerdeck_width_bottom = 1.43   
            lowerdeck_width_top = 2.53
            lowerdeck_height = 1.14
        elif container_type is  'LD39':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.82
            lowerdeck_height = 1.68
        elif container_type is  'LD4':
            lowerdeck_width_bottom = 2.44   
            lowerdeck_width_top = 2.54
            lowerdeck_height = 1.68
        elif container_type is  'LD6':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 4.16
            lowerdeck_height = 1.68
        elif container_type is  'LD8':
            lowerdeck_width_bottom = 2.44   
            lowerdeck_width_top = 3.28
            lowerdeck_height = 1.68
        elif container_type is  'LD9':
            lowerdeck_width_bottom = 3.18   
            lowerdeck_width_top = 3.28
            lowerdeck_height = 1.68

    if aisles_number == 1:
        seats_number = max(seats_number,2) # minor number of rows is 3
        seats_number = min(seats_number,6) # major number of rows is 9
    elif aisles_number == 2:
        seats_number = max(seats_number,6)# minor number of rows is 3
        seats_number = min(seats_number,9) # major number of rows is 9

    number_of_seats_abreast = seats_number

    if aisles_number == 1:
        left_fuselage_seats = math.ceil(number_of_seats_abreast/2)
        right_fuselage_seats = number_of_seats_abreast - left_fuselage_seats
    else:
        if seats_number == 6:
            left_fuselage_seats = 2
            right_fuselage_seats = 2
            center_fuselage_seats = 2
        elif seats_number == 7:
            left_fuselage_seats = 2
            right_fuselage_seats = 2
            center_fuselage_seats = 3
        elif seats_number == 8:
            left_fuselage_seats = 3
            right_fuselage_seats = 3
            center_fuselage_seats = 2
        elif seats_number == 9:
            left_fuselage_seats = 3
            right_fuselage_seats = 3
            center_fuselage_seats = 3

    # Calculate the width coordinates for the various points
    w0 = 0.5*cabin_height*aisles_number
    w4 = number_of_seats_abreast*seat_cushion_width_YC + aisles_number*aisle_width + (number_of_seats_abreast - aisles_number + 1)*armrest_width
    y_last_seat = 0.5*(w4 - seat_cushion_width_YC - 2*armrest_width)
    w1 = 2*y_last_seat
    w2 = 2*(pax_distance_head_wall + 0.084 + y_last_seat)
    w3 = 2*(pax_distance_shoulder_wall + pax_shoulder_breadth/2 + y_last_seat)
    w5 = w4
    w6 = w4 - 2*seat_delta_width_floor - 2*armrest_width
    w7 = lowerdeck_width_top
    w8 = lowerdeck_width_top
    w9 = lowerdeck_width_bottom

    while iterations >0:
        iterations = iterations - 1
        
        k = 0
        k_minimum = points_number
        result_z_symmetry_minimum = 1000
        k_minimum2 = points_number
        result_z_symmetry_minimum2 = 1000

        while k <= points_number:
            delta_z_symmetry = k*(delta_z_symmetry_superior - delta_z_symmetry_inferior)/points_number + delta_z_symmetry_inferior
            h0 = cabin_height - delta_z_symmetry
            h1 = pax_eye_height + seat_cushion_height - delta_z_symmetry + 0.126 + pax_distance_head_wall
            h2 = pax_eye_height + seat_cushion_height - delta_z_symmetry
            h3 = pax_midshoulder_height + seat_cushion_height - delta_z_symmetry
            h4 = armrest_top_height - delta_z_symmetry
            h5 = armrest_bottom_height - delta_z_symmetry
            h6 = -delta_z_symmetry
            h7 = -delta_z_symmetry - floor_thickness
            




    
            


        



    





    

    








    return
########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################