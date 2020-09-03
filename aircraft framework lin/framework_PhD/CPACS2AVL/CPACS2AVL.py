'''
This functions takes cpacs file and write AVL input file.
'''

import os
import sys
import linecache
import subprocess
import cpacsfunctions as cpsf
import numpy as np


# from tigl3.tigl3wrapper import Tigl3, TiglBoolean
# from tixi3.tixi3wrapper import Tixi3

# tixi = Tixi3()
# tigl = Tigl3()

# version = tigl.getVersion()
# print(version)



MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
cpacs_path = os.path.join(MODULE_DIR,'ToolInput','D150_v30.xml')
cpacs_out_path = os.path.join(MODULE_DIR,'ToolOutput','D150_v30.xml')

tixi = cpsf.open_tixi(cpacs_path)
tigl = cpsf.open_tigl(tixi)


tigl_version= tigl.getVersion()
print('Tigl version :',tigl_version)

model_xpath = '/cpacs/vehicles/aircraft/model/'
profiles_xpath = '/cpacs/vehicles/profiles/'
vehicles_xpath = '/cpacs/vehicles/'
toolspecific_xpath = '/cpacs/toolspecific/AVL/'



n_wings = tigl.getWingCount()

Cref = tigl.wingGetMAC(tigl.wingGetUID(1))
Sref = tigl.wingGetReferenceArea(1,1)
b    = tigl.wingGetSpan(tigl.wingGetUID(1))

avl_file_name = 'avl_file.avl'

# aircraft_name = cpsf.copy_branch(tixi,model_xpath+'uID')
aircraft_name = 'aircraft'

file = open(avl_file_name,'w')
file.write(aircraft_name+'\n')
file.write('0.0\n')
file.write('0 0 0\n')
file.write('{:.3f} {:.3f} {:.3f}\n'.format(Sref,Cref[0],b))
file.write('0.0 0.0 0.0\n')
file.write('0.1\n')

Nchord = cpsf.get_value(tixi,toolspecific_xpath+ 'vlm_autopanels_c/')
Cspace = cpsf.get_value(tixi,toolspecific_xpath+ 'vlm_distpanels_c/')
Nspan = cpsf.get_value(tixi,toolspecific_xpath+ 'vlm_autopanels_s/')
Sspace = cpsf.get_value(tixi,toolspecific_xpath+ 'vlm_distpanels_c/')

for i in range(1,n_wings+1):

    n_segments = tigl.wingGetSectionCount(i)
    wing_name = tigl.wingGetUID(i)


    component_segment_UID = tigl.wingGetComponentSegmentUID(i,1)
    n_component_segment = tigl.getControlSurfaceCount(component_segment_UID)
    n_control_surfaces = tigl.getControlSurfaceCount(component_segment_UID)
 
    file.write('SURFACE\n')
    file.write(wing_name+'\n')
    file.write('{:.1f} {:.1f} {:.1f} {:.1f}\n'.format(Nchord,Cspace,Nspan,Sspace))

    # Check symmetry in plane x-z = 2 
    if tigl.wingGetSymmetry(i) == 2:
        file.write('YDUPLICATE \n')
        file.write('0 \n')

    incidence = cpsf.get_value(tixi,model_xpath+ 
                               'wings/wing['+str(i)+']/transformation/rotation/y')

    file.write('ANGLE \n')
    file.write('{:.1f} \n'.format(incidence))

    file.write('SCALE \n')
    file.write('1.0 1.0 1.0 \n')

    translate_x = cpsf.get_value(tixi,model_xpath+ 
                               'wings/wing['+str(i)+']/transformation/translation/x')
    translate_y= cpsf.get_value(tixi,model_xpath+ 
                               'wings/wing['+str(i)+']/transformation/translation/y')
    translate_z = cpsf.get_value(tixi,model_xpath+ 
                               'wings/wing['+str(i)+']/transformation/translation/z')                                                      
    file.write('TRANSLATE \n')
    file.write('{:.5f} {:.5f} {:.5f} \n'.format(translate_x,translate_y,translate_z))

    print('======================================================')
    # test_xpath ='/cpacs/vehicles/aircraft/model/'
    # print(tixi.checkElement(model_xpath+ 'wings/wing/name'))
    # print(tixi.checkAttribute(model_xpath+ 'wings/','teste'))
    # print(tixi.uIDCheckExists('D150_InnerFlap'))
    # print(tixi.getTextElement(model_xpath+ 'wings/wing['+str(1)+']/name'))
    # print(tixi.getTextElement(model_xpath+ 'wings/wing['+str(1)+']/componentSegments/componentSegment[1]/name'))
    # print(tixi.getNamedChildrenCount(model_xpath+ 'wings','wing'))
    # print(tixi.getChildNodeName(model_xpath+ 'wings/wing[1]/',2))

    try:
        print('control surfaces TE:',tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/controlSurfaces/trailingEdgeDevices/'))
    except:
        print('No TE controls')

    try:    
        print('control surfaces LE:',tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/controlSurfaces/spoilers/'))
    except:
        print('No LE controls')

    try:
        print('control surfaces Type:',tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/controlSurfaces/'))
    except:
        print('No controls')


    # print('number of tanks:', tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/wingFuelTanks/'))
    print('======================================================')

    # n_control_surface_types = tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/controlSurfaces/')
    # n_LE_control_surfaces = tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/controlSurfaces/spoilers/')
    # n_TE_control_surfaces = tixi.getNumberOfChilds(model_xpath+ 'wings/wing['+str(i)+']/componentSegments/componentSegment/controlSurfaces/trailingEdgeDevices/')



    vector_section_x = []
    vector_section_y = []
    vector_section_z = []
    for j in range(1,n_segments+1):
        file.write('SECTION \n')

        ''' Most examples in cpacs uses positioning to define the position of the wing sections leading edge cooridinates.
        Following the examples, becomes necessary to calculate the x, y and z coordinates from length, sweep and dihedral angles.
        '''
        positioning_length = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/positionings/positioning['+str(j)+']/length')
        positioning_sweep_angle = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/positionings/positioning['+str(j)+']/sweepAngle')  
        positiong_dihedral_angle = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/positionings/positioning['+str(j)+']/dihedralAngle')

        section_z_aux = positioning_length*np.sin(positiong_dihedral_angle*np.pi/180)
        ca_aux = positioning_length*np.cos(positiong_dihedral_angle*np.pi/180)
        section_y_aux = ca_aux*np.cos(positioning_sweep_angle*np.pi/180)
        section_x_aux = section_y_aux*np.tan(positioning_sweep_angle*np.pi/180)

        '''Once positioning is defined CPACS also allows to perform a tranformation of the wing sections taking as reference 
        the positionig cooridinates. This increment on coordinates values must be considered and sum to obtaing the global 
        values for the construction of AVL file.
        '''
        section_x_aux0 = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/sections/section['+str(j)+']/transformation/translation/x')
        section_y_aux0 = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/sections/section['+str(j)+']/transformation/translation/y')   
        section_z_aux0 = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/sections/section['+str(j)+']/transformation/translation/z')

        vector_section_x.append(section_x_aux + section_x_aux0)
        vector_section_y.append(section_y_aux + section_y_aux0)
        vector_section_z.append(section_z_aux + section_z_aux0)

        if j == 1:
            section_x = vector_section_x[j-1]
            section_y = vector_section_y[j-1]
            section_z = vector_section_z[j-1]
        else:
            section_x = sum(vector_section_x)
            section_y = sum(vector_section_y)
            section_z = sum(vector_section_z)
                                    
        incidence_section = cpsf.get_value(tixi,model_xpath+
                                           'wings/wing['+str(i)+']/sections/section['+str(j)+']/transformation/rotation/y')

        chord_section = cpsf.get_value(tixi,model_xpath+
                                     'wings/wing['+str(i)+']/sections/section['+str(j)+']/'+
                                      'elements/element[1]/transformation/scaling/x')

        if tigl.wingGetSymmetry(i) == 2:
            file.write('{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} \n'.format(section_x,section_y,section_z,chord_section,incidence_section))
        else:
            file.write('{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} \n'.format(section_x,section_z,section_y,chord_section,incidence_section))

        airfoil = cpsf.get_value(tixi,model_xpath+
                                'wings/wing['+str(i)+']/sections/section['+str(j)+']/elements/element/airfoilUID')

        file.write('AFILE \n')
        file.write(airfoil+'\n')



        
        

file.close()  


def cd0Eval():
    p = subprocess.Popen('avl < avl_run.run',shell = True)
    try:
        p.wait(50)
    except subprocess.TimeoutExpired:
        p.kill()        
   
    line = linecache.getline('st.st', 25)
    linecache.clearcache()
    if os.path.exists('st.st'):
        os.remove('st.st')
    
    return float(line.split(" ")[-1])

cd0 = cd0Eval()

xpath_write = '/cpacs/toolspecific/AVL/save_results/total_forces/CD_tot'

value_name = 'CD_tot'
value = float(cd0)


tixi_out = cpsf.open_tixi(cpacs_out_path)
tixi_out.updateDoubleElement(xpath_write,value,'%g')
tixi_out = cpsf.close_tixi(tixi_out,cpacs_out_path)
