import ROOT

def getTH1F(name,bins,xlow,xhigh,title,xaxislabel,yaxislabel):
    plot = ROOT.TH1F(name,name,bins,xlow,xhigh)
    plot.SetTitle(title)
    plot.GetXaxis().SetTitle(xaxislabel)
    plot.GetYaxis().SetTitle(yaxislabel)
    plot.SetMarkerStyle(8)
    plot.SetMarkerSize(0.1)
    plot.SetLineColor(1)
    plot.SetMarkerColor(1)
    plot.Sumw2()
    return plot

def getTH2F(name,bins,xlow,xhigh,ylow,yhigh,title,xaxislabel,yaxislabel):
    plot = ROOT.TH2F(name,name,bins,xlow,xhigh,bins,ylow,yhigh)
    plot.SetTitle(title)
    plot.GetXaxis().SetTitle(xaxislabel)
    plot.GetYaxis().SetTitle(yaxislabel)
    plot.SetMarkerStyle(8)
    plot.SetMarkerSize(0.1)
    return plot

def getTH3F(name,bins,xlow,xhigh,ylow,yhigh,zlow,zhigh,title,xaxislabel,yaxislabel):
    plot = ROOT.TH3F(name,name,bins,xlow,xhigh,bins,ylow,yhigh,bins,zlow,zhigh)
    plot.SetTitle(title)
    plot.GetXaxis().SetTitle(xaxislabel)
    plot.GetYaxis().SetTitle(yaxislabel)
    plot.SetMarkerStyle(8)
    plot.SetMarkerSize(0.1)
    return plot
    
def GetPlots(pos):
    ### TOF from injector
    TOFInjPlot = getTH1F('TOFInjPlot',2000,0,2000,'t-TOF(inj) time','Time (ns)','Hits')

    ### TOF from target
    TOFTarPlot = getTH1F('TOFTarPlot',2000,0,2000,'t-TOF(tar) time','Time (ns)','Hits')
    TOFHaloPlot = getTH1F('TOFHaloPlot',2000,0,2000,'t-TOF(tar) time','Time (ns)','Hits')

    ### 2D Beam spot plot
    #QwBeamSpot = getTH2F('QwBeamSpot',36,-1820.0,1820.0,-1820.0,1820.0,'Beam spot','x position (cm)','y position (cm)')
    QwBeamSpot = getTH2F('QwBeamSpot',100,-1820.0,1820.0,-1820.0,1820.0,'Beam spot','x position (cm)','y position (cm)')
    



    ### 1D Beam spot plot
    #QwZPosBeam = getTH1F('QwZPosBeam',1000,-1820.0,1820.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits')
    #QwZPosBeam = getTH1F('QwPosBeam',1000,-1700.0,1700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits')
    #QwZPosBeam = getTH1F('QwZPosBeam',20,-1112.0,-380.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits')
    if pos==1:
        QwZPosBeam = getTH1F('QwZPosBeam',50,700.0,1700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B1
        QwZPosBeam_tOff = getTH1F('QwZPosBeam_tOff',50,700.0,1700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B1
        QwZPosBeam_tFocus = getTH1F('QwZPosBeam_tFocus',50,700.0,1700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B1
#        QwZPosBeam_tDeepFocus = getTH1F('QwZPosBeam_tDeepFocus',25,700.0,1700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B1
    if pos==2:
        QwZPosBeam = getTH1F('QwZPosBeam',50,250.0,1250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B2
        QwZPosBeam_tOff = getTH1F('QwZPosBeam_tOff',50,250.0,1250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B2
        QwZPosBeam_tFocus = getTH1F('QwZPosBeam_tFocus',50,250.0,1250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B2
#        QwZPosBeam_tDeepFocus = getTH1F('QwZPosBeam_tDeepFocus',25,250.0,1250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B2
    if pos==3:
        QwZPosBeam = getTH1F('QwZPosBeam',50,-750.0,250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B3
        QwZPosBeam_tOff = getTH1F('QwZPosBeam_tOff',50,-750.0,250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B3
        QwZPosBeam_tFocus = getTH1F('QwZPosBeam_tFocus',50,-750.0,250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B3
#        QwZPosBeam_tDeepFocus = getTH1F('QwZPosBeam_tDeepFocus',25,-750.0,250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B3
    if pos==4:
        QwZPosBeam = getTH1F('QwZPosBeam',50,-1250.0,-250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B4
        QwZPosBeam_tOff = getTH1F('QwZPosBeam_tOff',50,-1250.0,-250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B4
        QwZPosBeam_tFocus = getTH1F('QwZPosBeam_tFocus',50,-1250.0,-250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B4
#        QwZPosBeam_tDeepFocus = getTH1F('QwZPosBeam_tDeepFocus',25,-1250.0,-250.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B4
        #QwZPosBeam =  getTH1F('QwZPosBeam',50,-1000,-400.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B4
    if pos==5:
        QwZPosBeam = getTH1F('QwZPosBeam',50,-1700.0,-700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B5
        QwZPosBeam_tOff = getTH1F('QwZPosBeam_tOff',50,-1700.0,-700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B5
        QwZPosBeam_tFocus = getTH1F('QwZPosBeam_tFocus',50,-1700.0,-700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B5
#        QwZPosBeam_tDeepFocus = getTH1F('QwZPosBeam_tDeepFocus',25,-1700.0,-700.0,'Charge weighted z position of hits','Hit PMT z position (cm)', 'Qw Hits') #B5

    ###1D beam spot plot y direction
    #QwPosBeamY = getTH1F('QwPosBeamY',1000,-1700.0,1700.0,'Charge weighted y position of hits','Hit PMT y position (cm)', 'Qw Hits')
    #QwPosBeamY = getTH1F('QwPosBeamY',50,-1700.0,1700.0,'Charge weighted y position of hits','Hit PMT y position (cm)', 'Qw Hits')
    #QwPosBeamY = getTH1F('QwPosBeamY',50,-1000.0,0.0,'Charge weighted y position of hits','Hit PMT y position (cm)', 'Qw Hits') #B1 B2
    QwPosBeamY = getTH1F('QwPosBeamY',50,-1400.0,-400.0,'Charge weighted y position of hits','Hit PMT y position (cm)', 'Qw Hits') #B3 B4 B5
    QwPosBeamYbin = getTH1F('QwPosBeamYbin',22,-1400.0,-400.0,'Charge weighted y position of hits','Hit PMT y position (cm)', 'Qw Hits') #B3 B4 B5
    QwPosBeamY_monCorr = getTH1F('QwPosBeamY_monCorr',50,-1400.0,-400.0,'Charge weighted and monitor corrected y position of hits','Hit PMT y position (cm)', 'Qw Hits') #B3 B4 B5
    QwPosBeamYbin_monCorr = getTH1F('QwPosBeamYbin_monCorr',22,-1400.0,-400.0,'Charge weighted and monitor corrected y position of hits','Hit PMT y position (cm)', 'Qw Hits') #B3 B4 B5

    ####1D beam spot plot x direction
    #QwPosBeamX = getTH1F('QwPosBeamX',1000,-1700.0,1700.0,'Charge weighted x position of hits','Hit PMT x position (cm)', 'Qw Hits')
    QwPosBeamX = getTH1F('QwPosBeamX',50,-1700.0,-1000.0,'Charge weighted x position of hits','Hit PMT x position (cm)', 'Qw Hits')
    QwPosBeamX_tOff = getTH1F('QwPosBeamX_tOff',50,-1700.0,-1000.0,'Charge weighted x position of hits','Hit PMT x position (cm)', 'Qw Hits')
    QwPosBeamX_tFocus = getTH1F('QwPosBeamX_tFocus',50,-1700.0,-1000.0,'Charge weighted x position of hits','Hit PMT x position (cm)', 'Qw Hits')
    QwPosBeamXbin = getTH1F('QwPosBeamXbin',25,-1700.0,-700.0,'Charge weighted x position of hits','Hit PMT x position (cm)', 'Qw Hits')
    QwPosBeamX_monCorr = getTH1F('QwPosBeamX_monCorr',50,-1700.0,-1000.0,'Charge weighted and monitor corrected x position of hits','Hit PMT x position (cm)', 'Qw Hits')
    QwPosBeamXbin_monCorr = getTH1F('QwPosBeamXbin_monCorr',25,-1700.0,-700.0,'Charge weighted and monitor corrected x position of hits','Hit PMT x position (cm)', 'Qw Hits')

    QwPosBeamH = getTH1F('QwPosBeamH',25,-500.0,750.0,'Charge weighted horizontal position of hits','Hit PMT Horizontal position (cm)', 'Qw Hits')
    QwPosBeamH_tOff = getTH1F('QwPosBeamH_tOff',25,-500.0,750.0,'Charge weighted horizontal position of hits','Hit PMT Horizontal position (cm)', 'Qw Hits')
    QwPosBeamH_tFocus = getTH1F('QwPosBeamH_tFocus',25,-500.0,750.0,'Charge weighted horizontal position of hits','Hit PMT Horizontal position (cm)', 'Qw Hits')
    ### 1D Beam spot plot by angle
    QwAngBeam = getTH1F('QwAngBeam',36,-90,90,'Charge weighted angle of hits','Hit PMT angle from injector (degs)', 'Qw Hits')
    QwCosAngBeam_tOff = getTH1F('QwCosAngBeam_tOff',50,0.0,1,'Charge weighted angle of hits','Hit PMT cos(angle) from injector', 'Qw Hits')
    QwCosAngBeamFront_tOff = getTH1F('QwCosAngBeamFront_tOff',50,0.85,1.0,'Charge weighted angle of hits','Hit PMT cos(angle) from injector', 'Qw Hits')
    QwCosAngBeamZoomFront_tOff = getTH1F('QwCosAngBeamZoomFront_tOff',50,0.5,1,'Charge weighted angle of hits','Hit PMT cos(angle) from injector', 'Qw Hits')
    QwCosAngBeam_tFocus = getTH1F('QwCosAngBeam_tFocus',50,0.0,1,'Charge weighted angle of hits','Hit PMT cos(angle) from injector', 'Qw Hits')
    QwCosAngBeamFront_tFocus = getTH1F('QwCosAngBeamFront_tFocus',50,0.85,1.0,'Charge weighted angle of hits','Hit PMT cos(angle) from injector', 'Qw Hits')
    QwCosAngBeamZoomFront_tFocus = getTH1F('QwCosAngBeamZoomFront_tFocus',50,0.5,1,'Charge weighted angle of hits','Hit PMT cos(angle) from injector', 'Qw Hits')
    AngBeam = getTH1F('AngBeam',36,-90,90,'Angle of hits','Hit PMT angle from injector (degs)', 'Hits')

    ### TOF from target for selected PMTs
    ZTBAPlot = getTH1F('ZTBAPlot',2000,0,2000,'t-TOF(tar) for hits in z region','t-TOF(target) (ns)','Hits')
    #ZTBAPlot = getTH1F('ZTBAPlot',2000,0,2000,'t-TOF(tar) for hits in z region','t-TOF(target) (ns)','Hits')
    #ZTBAPlot = getTH1F('ZTBAPlot',200,0,2000,'t-TOF(tar) for hits in z region','t-TOF(target) (ns)','Hits')

    ### time vs hits 
    tvhits = getTH1F('tvhits',2000,0,2000,'time vs hits in z region','time (ns)','Hits')

    
    ###TOF of hits vs z-position
    zposvTOF = getTH1F('zposvTOF',2000,0,2000,'Hit PMT z pos vs t-TOF(tar)','Hit PMT z position','t-TOF(target) (ns)')
    ### 3D beam
    Qw3DBeam = getTH3F('Qw3DBeam',52,-1820.0,1820.0,-1820.0,1820.0,-1820.0,1820.0,'Beam spot','x position (cm)', 'y position (cm)')

    ### Total charge in tank outside 2m exclusion
    QinTank = getTH1F('QinTank',2000,0,2000,'t-TOF(tar) for all hits outside 2m','t-TOF(target) (ns)','Qw Hits')

    ### Total charge outside beam
    QoutBeam = getTH1F('QoutBeam',2000,0,2000,'t-TOF(tar) for all hits outside 2m, outside beam','t-TOF(target) (ns)','Qw Hits')

    ### Total charge inside beam
    QinBeam = getTH1F('QinBeam',2000,0,2000,'t-TOF(tar) for all hits outside 2m, inside beam','t-TOF(target) (ns)','Qw Hits')

    ### Total charge in specific z region
    QinZRegion = getTH1F('QinZRegion',2000,0,2000,'t-TOF(tar) for hits outside 2m in z region','t-TOF(target) (ns)','Qw Hits')

    ### Charge outside beam in z region
    QinZoutBeam = getTH1F('QinZoutBeam',2000,0,2000,'t-TOF(tar) for hits outside 2m, outside beam, in z region','t-TOF(target) (ns)','Qw Hits')

    return TOFInjPlot,TOFTarPlot,TOFHaloPlot,QwBeamSpot,QwZPosBeam,QwZPosBeam_tOff,QwZPosBeam_tFocus,QwPosBeamY,QwPosBeamYbin,QwPosBeamY_monCorr,QwPosBeamYbin_monCorr,QwPosBeamX,QwPosBeamX_tOff,QwPosBeamX_tFocus,QwPosBeamXbin,QwPosBeamX_monCorr,QwPosBeamXbin_monCorr,QwPosBeamH,QwPosBeamH_tOff,QwPosBeamH_tFocus,QwAngBeam,QwCosAngBeam_tOff,QwCosAngBeamFront_tOff,QwCosAngBeamZoomFront_tOff,QwCosAngBeam_tFocus,QwCosAngBeamFront_tFocus,QwCosAngBeamZoomFront_tFocus,AngBeam,ZTBAPlot,tvhits,zposvTOF,Qw3DBeam,QinTank,QoutBeam,QinBeam,QinZRegion,QinZoutBeam
