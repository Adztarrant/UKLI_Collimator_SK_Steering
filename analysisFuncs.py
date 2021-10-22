import math
from array import array
import sys

def GetDotProduct(p1,p2):
    '''Calculate the dot product between two given vectors'''
    dotprod = 0
    for i in range(len(p1)):
        dotprod += p1[i]*p2[i]
    return dotprod

def GetModulus(vec):
    '''Calculate the modulus of a given vector'''
    tot = 0
    for n in vec:
        tot += (n*n)
    mod = math.sqrt(tot)
    return mod

def GetHitAngle(start,end,tar,pos):
    '''Takes the start, end, target position coordinates [x,y,z], and the injector position and returns the
    angle between the injector and hit PMT.'''
    # Calculate vector from injector to target
    x_ht = start[0]-tar[0]
    y_ht = start[1]-tar[1]
    z_ht = start[2]-tar[2]
    vec_ht = [x_ht,y_ht,z_ht]
    # Calculate vector from injector to hit PMT
    x_it = start[0]-end[0]
    y_it = start[1]-end[1]
    z_it = start[2]-end[2]
    vec_it = [x_it,y_it,z_it]

    # Calculate angle between vectors
    # cos(theta) = u.v / |u||v|
    dot_prod = GetDotProduct(vec_ht, vec_it)
    mod_ht = GetModulus(vec_ht)
    mod_it = GetModulus(vec_it)

    costheta = dot_prod/(mod_ht*mod_it)
    theta = math.acos(costheta)

    return theta

def GetTimeOfFlight(start,end,speed):
    '''Takes start and end position vectors [x,y,z] and the speed of light in water
    in cm/ns. Returns the time of flight and distance between the two positions.'''
    x = start[0]-end[0]
    y = start[1]-end[1]
    z = start[2]-end[2]
    c = speed # speed of light in water (cm/ns)
    r = math.sqrt((x*x)+(y*y)+(z*z)) # distance travelled (cm)
    TOF = (r/c) # time of flight in ns

    return TOF,r

def GetRSqCor(theta):
    '''Takes angle in radians and returns the angular correction'''
    cor = 1/((math.cos(theta))*(math.cos(theta)))

    return cor

def GetAttCor(r,z):
    '''Takes the distance travelled and the offset in z, returns the attenuation correction
    resulting from different path lengths.'''
    L = 9800 # attenuation length in cm
    cor = math.exp(-z/L)/math.exp(-r/L)
    return cor

def GetSolidAngleCor(angle):
    '''Takes the incident angle and returns correction due to solid angle of PMT.'''
    cor = 1/(1-(abs(angle)/math.pi))
    return cor

def GetGainVals(run_num,gain_cor,test):
    '''Finds the 5 separate gain corrections (based on PMT production year) for a
    particular run number. Test should be true or false.'''
    sk4gain = [0.992057, 1.00184, 0.989083, 0.98216, 0.987678] # as determined at start of sk4
    gains = array('d',[])
    num = "0"+str(run_num)
    try:
        gainFile = open(gain_cor,"r")
    except IOError:
        print "ERROR: Could not find PMT gain table! Exiting..."
        sys.exit(1)
    ### Need to find the closest normal run if using a test mode run, as test mode runs not in gaincor table
    if test:
        max_diff = 10000 # maximum separation between actual run number and that used for gain correction
        for line in gainFile:
            vals = line.split(' ')
            dummy_run = int(vals[0][-5:])
            if abs(run_num - dummy_run)<max_diff:
                max_diff = abs(run_num - dummy_run)
                used_run = dummy_run
        if max_diff>100:
            print "Info: Running in Test mode. This run number is "+str(run_num)
            print "ERROR: No normal run within 100 runs is found. Exiting..."
            sys.exit(0)
        gainFile.seek(0)
        num = "0"+str(used_run)
        print "INFO: Running in Test Mode. This run number is "+str(run_num)+".Closest normal run number is "+str(used_run)
        print "INFO: Will use gain correction table information from run "+str(used_run)
        
    for line in gainFile:
        vals = line.split(' ')
        ents = len(vals)
        if vals[0]==num:
            gains.append((float(vals[ents-5])-float(sk4gain[0]))/float(sk4gain[0]))
            gains.append((float(vals[ents-4])-float(sk4gain[1]))/float(sk4gain[1]))
            gains.append((float(vals[ents-3])-float(sk4gain[2]))/float(sk4gain[2]))
            gains.append((float(vals[ents-2])-float(sk4gain[3]))/float(sk4gain[3]))
            gains.append((float(vals[ents-1])-float(sk4gain[4]))/float(sk4gain[4]))
            gains.append(0) # for the PMTs with no production year information
            break
    gainFile.close()
    if len(gains)<5:
        print "ERROR: Run number "+num+" not found in gain correction table"
        print "EXITING..."
        sys.exit(1)
    else:
        print "SUCCESS: Run number "+num+" located in gain table"
        for i in range(len(gains)):
            print "INFO: Gain correction for production period "+str(i+1)+" is "+str(gains[i])
        return gains

def LoadProdYear(prod_year_tab):
    '''Parses the PMT production year table so information is available for all PMT numbers.'''
    pmt_IDs = array('i',[])
    prod_years = array('i',[])
    prodFile = open(prod_year_tab,'r')
    for line in prodFile:
        h = []
        vals = line.split(' ')
        for val in vals:
            if val!='':
                h.append(val)
        pmt_IDs.append(int(h[0]))
        year = int(h[1].split('.')[0])
        if year==1992 or year==1993 or year==1994 or year==1995:
            grp = 0
        elif year==1996 or year==1997:
            grp = 1
        elif year==2003:
            grp = 2
        elif year==2004:
            grp = 3
        elif year==2005:
            grp = 4
        elif year==0:
            grp = 5
        else:
            print "Unrecognised year in PMT production year table"
            print "EXITING..."
            sys.exit(1)
        prod_years.append(grp)
    return pmt_IDs,prod_years
