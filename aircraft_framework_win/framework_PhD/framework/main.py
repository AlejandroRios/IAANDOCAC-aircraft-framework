# from utilities.logger import get_logger
# from CPACS2AVL.CPACS2AVL import *
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))


from FRAMEWORK_PhD.Economics.crew_salary import crew_salary

MTOW = 10

print(crew_salary(MTOW))