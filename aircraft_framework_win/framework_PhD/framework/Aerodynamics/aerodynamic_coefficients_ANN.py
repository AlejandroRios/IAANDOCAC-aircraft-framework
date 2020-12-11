"""
File name : aerodynamic coefficients
Author    : Alejandro Rios
Email     : aarc.88@gmail.com
Email     : aarc.88@gmail.com
Date      : September/2020
Last edit : September/2020
Language  : Python
Aeronautical Institute of Technology - Airbus Brazil

Description:
    - 
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
import numpy as np
import array
import scipy.io as spio
from sklearn.preprocessing import normalize
from framework.baseline_aircraft import *
########################################################################################
"CLASSES"
########################################################################################

########################################################################################
"""FUNCTIONS"""
########################################################################################


def loadmat(filename):
    '''
    this function should be called instead of direct snp.pio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict

def logical(varin):
    if varin == 0:
        varout = 0
    else:
        varout = 1
    return varout

def aerodynamic_coefficients_ANN(aircraft,altitude,mach,CL):
    alfag = 1
    fixed_AoA = 0
    CL_input = CL



    inputs_neural_network = {'mach':mach,
            'altitude':altitude,
            'angle_of_attack':alfag*np.pi/180,
            'aspect_ratio':aircraft['wing_aspect_ratio'],
            'taper_ratio':aircraft['wing_taper_ratio'] ,
            'leading_edge_sweep':aircraft['wing_sweep_c_4']*np.pi/180,
            'inboard_wing_dihedral':3*np.pi/180,
            'outboard_wing_dihedral':5*np.pi/180,
            'break_position':aircraft['semi_span_kink'],
            'wing_area':aircraft['wing_surface'],
            'wing_root_airfoil_incidence':aircraft['incidence_root']*np.pi/180,
            'wing_break_airfoil_incidence':aircraft['incidence_kink']*np.pi/180,
            'wing_tip_airfoil_incidence':aircraft['incidence_tip']*np.pi/180,
            'root_airfoil_leading_edge_radius':aircraft['leading_edge_radius'][0],
            'root_airfoil_thickness_ratio':aircraft['thickness_ratio'][0],
            'root_airfoil_thickness_line_angle_trailing_edge':aircraft['thickness_line_angle_trailing_edge'][0] ,
            'root_airfoil_thickness_to_chord_maximum_ratio':aircraft['thickness_to_chord_maximum_ratio'][0] ,
            'root_airfoil_camber_line_angle_leading_edge':aircraft['camber_line_angle_leading_edge'][0],
            'root_airfoil_camber_line_angle_trailing_edge':aircraft['camber_line_angle_trailing_edge'][0],
            'root_airfoil_maximum_camber':aircraft['maximum_camber'][0],
            'root_airfoil_camber_at_maximum_thickness_chordwise_position':aircraft['camber_at_maximum_thickness_chordwise_position'][0],
            'root_airfoil_maximum_camber_chordwise_position ':aircraft['maximum_camber_chordwise_position'][0] ,
            'break_airfoil_leading_edge_radius':aircraft['leading_edge_radius'][1],
            'break_airfoil_thickness_ratio':aircraft['thickness_ratio'][1],
            'break_airfoil_thickness_line_angle_trailing_edge':aircraft['thickness_line_angle_trailing_edge'][1],
            'break_airfoil_maximum_thickness_chordwise_position':aircraft['thickness_to_chord_maximum_ratio'][1] ,
            'break_airfoil_camber_line_angle_leading_edge':aircraft['camber_line_angle_leading_edge'][1],
            'break_airfoil_camber_line_angle_trailing_edge':aircraft['camber_line_angle_trailing_edge'][1],
            'break_airfoil_maximum_camber':aircraft['maximum_camber'][1],
            'break_airfoil_camber_at_maximum_thickness_chordwise_position':aircraft['camber_at_maximum_thickness_chordwise_position'][1],
            'break_airfoil_maximum_camber_chordwise_position ':aircraft['maximum_camber_chordwise_position'][1] ,
            'tip_airfoil_leading_edge_radius':aircraft['leading_edge_radius'][2],
            'tip_airfoil_thickness_ratio':aircraft['thickness_ratio'][2],
            'tip_airfoil_thickness_line_angle_trailing_edge':aircraft['thickness_line_angle_trailing_edge'][2],
            'tip_airfoil_maximum_thickness_chordwise_position':aircraft['thickness_to_chord_maximum_ratio'][2] ,
            'tip_airfoil_camber_line_angle_leading_edge':aircraft['camber_line_angle_leading_edge'][2],
            'tip_airfoil_camber_line_angle_trailing_edge':aircraft['camber_line_angle_trailing_edge'][2],
            'tip_airfoil_maximum_camber':aircraft['maximum_camber'][2],
            'tip_airfoil_camber_at_maximum_thickness_chordwise_position':aircraft['camber_at_maximum_thickness_chordwise_position'][2],
            'tip_airfoil_maximum_camber_chordwise_position ':aircraft['maximum_camber_chordwise_position'][2]}

    


    NN_induced = loadmat('Aerodynamics/NN_CDind.mat')
    NN_wave = loadmat('Aerodynamics/NN_CDwave.mat')
    NN_cd0 = loadmat('Aerodynamics/NN_CDfp.mat')
    NN_CL = loadmat('Aerodynamics/NN_CL.mat')

    CLout, Alpha, CDfp, CDwave, CDind, grad_CL, grad_CDfp,grad_CDwave, grad_CDind = ANN_aerodynamics_main(
        CL_input,inputs_neural_network,fixed_AoA,NN_induced,NN_wave,NN_cd0,NN_CL)

    CDfp = 1.04*CDfp
    CDwing = CDfp + CDwave + CDind

    return CDwing,CLout

def ANN_aerodynamics_main(CL_input,inputs_neural_network,CL_logical,NN_ind,NN_wave,NN_cd0,NN_CL):
    '''Soure: Ney Rafael Seccô and Bento Mattos
       Aeronautical Institute of Technology
    '''

    sizes = len(inputs_neural_network)
    # if sizes != 40 :
        # print('\n The number of input variables should be 40.')
        # print('\n Check the size of input_neural_network columns.')

    m = 1
    # DEFINE VARIABLE BOUNDS
    # Flight conditions
    mach = np.array([0.2, 0.85]) # 1 - Flight Mach number
    altitude = np.array([0, 13000]) # 2 - Flight altitude [m]
    alpha = np.array([-5, 10])*np.pi/180 # 3 - Angle of attack [rad]
    
    # Wing planform
    aspect_ratio = np.array([7, 12]) # 4 - Aspect ratio
    taper_ratio = np.array([0.2, 0.6])# 5 - Taper ratio
    leading_edge_sweep = np.array([10, 35])*np.pi/180 # 6 - Leading edge sweep angle np.array([rad])
    dihedral_inner_panel = np.array([0, 5])*np.pi/180 # 7 - Inner panel dihedral np.array([rad])
    dihedral_outer_panel = np.array([5, 10])*np.pi/180 # 8 - Outer panel dihedral np.array([rad])
    span_wise_kink_position = np.array([0.3, 0.6]) # 9 - Span-wise kink position np.array([span fraction])
    wing_area = np.array([50, 200]) # 10 - Wing area np.array([m?])

    # Airfoil incidences (realtive to fuselage centerline)
    incidence_root = np.array([0, 2])*np.pi/180# 11 - Root airfoil incidence np.array([rad])
    incidence_kink = np.array([-1, 1])*np.pi/180# 12 - Kink airfoil incidence np.array([rad])
    incidence_tip = np.array([-3, 0])*np.pi/180# 13 - Tip airfoil incidence np.array([rad])

    # Root airfoil
    rBA_root = np.array([0.02, 0.20])# 14 - Leading edge radius
    # EspBF_root = np.array([0.0025 0.0025])### - Trailing edge thickness (constant)
    t_c_root = np.array([0.10, 0.18])# 15 - Thickness ratio
    phi_root = np.array([-0.12, 0.05])*2# 16 - Thickness line angle at trailing edge
    X_tcmax_root = np.array([0.20, 0.46])# 17 - Maximum thickness chord-wise position
    theta_root = np.array([-0.20, 0.10])# 18 - Camber line angle at leading edge
    epsilon_root = np.array([-0.300, -0.005])# 19 - Camber line angle at trailing edge
    Ycmax_root = np.array([-0.05, 0.03])# 20 - Maximum camber
    YCtcmax_root = np.array([-0.05, 0.025])# 21 - Maximum camber at maximum thickness chord-wise position
    # Hte_root = np.array([0 0])### - Trailing edge height with respect to chord-line (constant)
    X_Ycmax_root = np.array([0.50, 0.80])# 22 - Maximum camber chord-wise position

    # Kink airfoil
    rBA_kink = np.array([0.03, 0.20])# 23 - Leading edge radius
    # EspBF_kink = np.array([0.0025 0.0025])### - Trailing edge thickness (constant)
    t_c_kink = np.array([0.08, 0.13])# 24 - Thickness ratio
    phi_kink = np.array([-0.12, 0.05])*2# 25 - Thickness line angle at trailing edge
    X_tcmax_kink = np.array([0.20, 0.46])# 26 - Maximum thickness chord-wise position
    theta_kink = np.array([-0.20, 0.10])# 27 - Camber line angle at leading edge
    epsilon_kink = np.array([-0.300, -0.005])# 28 - Camber line angle at trailing edge
    Ycmax_kink = np.array([0.00, 0.03])# 29 - Maximum camber
    YCtcmax_kink = np.array([0.000, 0.025])# 30 - Maximum camber at maximum thickness chord-wise position
    # Hte_kink = np.array([0 0]) - Trailing edge height with respect to chord-line (constant)
    X_Ycmax_kink = np.array([0.50, 0.80])# 31 - Maximum camber chord-wise position


    rBA_tip = np.array([0.03, 0.15])# 32 - Leading edge radius
    # EspBF_tip = np.array([0.0025 0.0025])### - Trailing edge thickness (constant)
    t_c_tip = np.array([0.08, 0.12])# 33 - Thickness ratio
    phi_tip = np.array([-0.12, 0.05])*2# 34 - Thickness line angle at trailing edge
    X_tcmax_tip = np.array([0.20, 0.46])# 35 - Maximum thickness chord-wise position
    theta_tip = np.array([-0.20, 0.10])# 36 - Camber line angle at leading edge
    epsilon_tip = np.array([-0.300, -0.005])# 37 - Camber line angle at trailing edge
    Ycmax_tip = np.array([0.00, 0.03])# 38 - Maximum camber
    YCtcmax_tip = np.array([0.000, 0.025])# 39 - Maximum camber at maximum thickness chord-wise position
    # Hte_tip = np.array([0 0]) - Trailing edge height with respect to chord-line (constant)
    X_Ycmax_tip = np.array([0.50, 0.80])# 40 - Maximum camber chord-wise position

    # intervals = np.concatenate((mach, 
    #                            altitude), axis=0)
    intervals = np.vstack((mach, 
                          altitude,
                          alpha,
                          aspect_ratio,
                          taper_ratio,
                          leading_edge_sweep,
                          dihedral_inner_panel,
                          dihedral_outer_panel,
                          span_wise_kink_position,
                          wing_area,
                          incidence_root,
                          incidence_kink,
                          incidence_tip,
                          rBA_root,
                          t_c_root,
                          phi_root,
                          X_tcmax_root,
                          theta_root,
                          epsilon_root,
                          Ycmax_root,
                          YCtcmax_root,
                          X_Ycmax_root,
                          rBA_kink,
                          t_c_kink,
                          phi_kink,
                          X_tcmax_kink,
                          theta_kink,
                          epsilon_kink,
                          Ycmax_kink,
                          YCtcmax_kink,
                          X_Ycmax_kink,
                          rBA_tip,
                          t_c_tip,
                          phi_tip,
                          X_tcmax_tip,
                          theta_tip,
                          epsilon_tip,
                          Ycmax_tip,
                          YCtcmax_tip,
                          X_Ycmax_tip))

    input_nn = list(inputs_neural_network.values())


    # for var_index in range(0,32):
        # if input_nn[var_index] < intervals[var_index,0] or  input_nn[var_index] > intervals[var_index,1]:

            # print('\n ==> Warning: variable %d out of boundary limits  \n', var_index)


    if CL_logical == 1:
        output_nn, grad_nn = ANN_internal_use(input_nn,NN_CL)

        CL = output_nn[0]
        grad_CL = grad_nn[0]
        Alpha = input_nn[2]

    else:

        Alpha = input_nn[2]
        # print(input_nn)
        output_nn,_ = ANN_internal_use(input_nn,NN_CL)
        CL1 = output_nn[0]
        input_nn[2] = Alpha + np.pi/180
        output_nn,_ = ANN_internal_use(input_nn,NN_CL)
        CL2 = output_nn[0]
        CL_alpha = (CL2-CL1)/(np.pi/180)
        CL0 = CL1-CL_alpha*Alpha
        Alphades = (CL_input-CL0)/CL_alpha
        input_nn[2] = Alphades
        output_nn,grad_nn = ANN_internal_use(input_nn,NN_CL)
        CL = output_nn[0]
        grad_CL = grad_nn[0]
        # print(output_nn)

    del(output_nn,grad_nn)

    output_nn,grad_nn = ANN_internal_use(input_nn,NN_wave)
    CD_wave = output_nn[0]

    CD_wave = max(CD_wave,np.zeros(np.shape(CD_wave)))
    grad_CD_wave = grad_nn
    grad_CD_wave = grad_CD_wave * (np.ones(len(grad_CD_wave))*logical(CD_wave))

    del(output_nn,grad_nn)

    output_nn,grad_nn = ANN_internal_use(input_nn,NN_cd0)

    CD_fp = output_nn[0]
    grad_CD_fp = grad_nn[0]

    del(output_nn,grad_nn)

    output_nn,grad_nn = ANN_internal_use(input_nn,NN_ind)

    CD_ind = output_nn[0]
    grad_CD_ind = grad_nn[0]

    del(output_nn,grad_nn)
    

    return CL, Alpha, CD_fp, CD_wave, CD_ind, grad_CL, grad_CD_fp,grad_CD_wave, grad_CD_ind

def  calculation_alfa(alfa,input_nn,NN,CLinput):

    # Gathering outputs
    input_nn = alfa

    output, doutput_dinput = ANN_internal_use(input_nn,NN)
    CL = output_nn
    delta_alfa = CL-CLinput
    
    return delta_alfa


def ANN_internal_use(input_nn,NN):
    output = {}
    doutput_dinput = {}

    for nn_index in range(0,1):
        
        output, doutput_dinput = feedfoward_gradients(input_nn, NN['NN']['theta1'], NN['NN']['theta2'], NN['NN']['theta3'], NN['NN']['Norm_struct'])


    return output, doutput_dinput

def feedfoward_gradients(inputs, theta1, theta2, theta3, norm_struct):


    input_norm =  normalize_internal(inputs,norm_struct['Mean_input'], norm_struct['Range_input'])

    # print(norm_struct['Range_input'])
    # mean_iiinputt = np.asarray(norm_struct['Mean_input'])
    # np.savetxt("a0.csv", mean_iiinputt, delimiter=",")
    m = 1

    if not theta3.size == 0:
        a0 = np.append(np.ones(m),input_norm)

        # print(a0)
        # np.savetxt("a0.csv", a0, delimiter=",")

        z1 = np.dot(theta1,a0) # DANGERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        a1 =  np.array(np.append(np.ones(m),2/(1+np.exp(-2*z1))-1), dtype=float)
        z2 = np.dot(theta2,a1)
        a2 = np.array(np.append(np.ones(m), 2/(1+np.exp(-2*z2))-1), dtype=float)
        output_norm = np.dot(theta3,a2)
        
    else:
        a0 = [np.ones(m), input_norm] 
        z1 = theta1*a0
        a1 = [np.ones(m), 2./(1+np.exp(-2*z1))-1]
        output_norm = theta2@a1

    doutput_norm_da2 = theta3[1:]*np.ones(m)
    doutput_norm_da1 = np.transpose(theta2[:, 1:])@(doutput_norm_da2*(1-a2[1:]*a2[1:]))
    doutput_norm_da0 = np.transpose(theta1[:, 1:])@(doutput_norm_da1*(1-a1[1:]*a1[1:]))


    output = denormalize_internal(output_norm, norm_struct['Mean_output'],norm_struct['Range_output'],)
    doutput_dinput = doutput_norm_da0*(np.tile(norm_struct['Range_output']*np.ones(m),40))/(norm_struct['Range_input']*np.ones(m))


    return output, doutput_dinput


def normalize_internal(X, mean, Range):
    # Number of training sets
    
    m = 1
    X = np.asarray(X)
    # Normalization
    X_norm = 2*(X - mean*np.ones(m))/(Range*np.ones(m))
    # print(X_norm)

    

    return X_norm

def denormalize_internal(X_norm, mean, Range):
    # Number of training sets
    m = 1
    # Denormalization
    # X = np.array([[1, 2, 3], [5, 0, 0]], dtype=object)
    X = X_norm*(Range*np.ones(m))/2 + mean*np.ones(m)
    return X

########################################################################################
"""MAIN"""
########################################################################################

########################################################################################
"""TEST"""
########################################################################################

