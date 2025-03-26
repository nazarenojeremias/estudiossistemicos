import sys, pickle, os, math
import pip
import time
import numpy as np

# Se importa el modulo powerfactory, ubicado en el directorio de instalacion
import powerfactory as pf

def report_3F(f,oBar, operacion):
    if not (oBar.IsOutOfService()):
        CC3F.shcobj=oBar
        CC3F.Execute()
        bSkss=oBar.GetAttribute('m:Skss')
        bIkss=oBar.GetAttribute('m:Ikss')
        bIb=oBar.GetAttribute('m:Ib')
        bIk=oBar.GetAttribute('m:Ik')
        bIth=oBar.GetAttribute('m:Ith')
        bX=oBar.GetAttribute('m:X')
        bR=oBar.GetAttribute('m:R')
        kdc = 0
        bIasy = 0
        bip = 0
        bidc = 0
        bXtoR = 0
        if bR!=0:
            bXtoR=bX/bR
        if bIkss !=0 and bXtoR !=0:
            bip = bIkss*math.sqrt(2)*(1+1*math.exp(-(math.pi)/bXtoR))
            bIasy =  bIkss*((1+2*math.exp(-(8*(math.pi))/bXtoR)))**0.5
            bidc =  bIkss*math.sqrt(2)*((math.exp(-4*(math.pi)/bXtoR)))
            kdc = (bidc/(bIb*(2**0.5)))*100
    else:
        bSkss= 0
        bIkss= 0
        bip=0
        bidc=0
        bIb=0
        bIk=0
        bIth=0
        bIasy=0
        bXtoR=0
        kdc = 0


    if oBar.cpSubstat:
        SE_name = oBar.cpSubstat.loc_name
    else:
        SE_name = oBar.loc_name
    Bus_name = oBar.loc_name
    Tension=oBar.uknom
    f.write('%s;%s;%s;%s;%3.2f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f; \n' %('3F',operacion,
        SE_name,Bus_name,Tension,bSkss,bIkss,bip,bidc,bIb,bIk,bIth,bIasy,bXtoR,kdc))

def report_1F2F2FT(f,falla,oBar, operacion):
    if not (oBar.IsOutOfService()):
        falla.shcobj=oBar
        falla.Execute()
        bSkssA=oBar.GetAttribute('m:Skss:A')
        bSkssB=oBar.GetAttribute('m:Skss:B')
        bSkssC=oBar.GetAttribute('m:Skss:C')
        bSkss=np.array([bSkssA,bSkssB,bSkssC]) #XXX
        bSkssMax = bSkss.max()
        bIkssA=oBar.GetAttribute('m:Ikss:A')
        bIkssB=oBar.GetAttribute('m:Ikss:B')
        bIkssC=oBar.GetAttribute('m:Ikss:C')
        bIkss=np.array([bIkssA,bIkssB,bIkssC]) #XXX
        bIkssMax = bIkss.max()
        bipMax = 0
        bIbA=oBar.GetAttribute('m:Ib:A')
        bIbB=oBar.GetAttribute('m:Ib:B')
        bIbC=oBar.GetAttribute('m:Ib:C')
        bIb=np.array([bIbA,bIbB,bIbC]) #XXX
        bIbMax = bIb.max()
        bIkA=oBar.GetAttribute('m:Ik:A')
        bIkB=oBar.GetAttribute('m:Ik:B')
        bIkC=oBar.GetAttribute('m:Ik:C')
        bIk=np.array([bIkA,bIkB,bIkC]) #XXX
        bIkMax = bIk.max()
        bIthA=oBar.GetAttribute('m:Ith:A')
        bIthB=oBar.GetAttribute('m:Ith:B')
        bIthC=oBar.GetAttribute('m:Ith:C')
        bIth=np.array([bIthA,bIthB,bIthC]) #XXX
        bIthMax = bIth.max()
        bRk0=oBar.GetAttribute('m:R0')
        bRk1=oBar.GetAttribute('m:R1')
        bRk2=oBar.GetAttribute('m:R2')
        bXk0=oBar.GetAttribute('m:X0')
        bXk1=oBar.GetAttribute('m:X1')
        bXk2=oBar.GetAttribute('m:X2')              
        bUA=oBar.GetAttribute('m:U:A')
        bUB=oBar.GetAttribute('m:U:B')
        bUC=oBar.GetAttribute('m:U:C')
        bphiA=oBar.GetAttribute('m:phiu:A')
        bphiB=oBar.GetAttribute('m:phiu:B')
        bphiC=oBar.GetAttribute('m:phiu:C')
        i0x3=oBar.GetAttribute('m:I0x3')
        idc = 0
        kdc = 0      
        sumRk = 0
        sumXk = 0
        Iasy = 0
        bipMax = 0
        XR=0
        if falla.loc_name == 'CC1F':
            sumRk = bRk0 + bRk1 + bRk2
            sumXk = bXk0 + bXk1 + bXk2
        elif falla.loc_name == 'CC2F':
            sumRk = bRk1 + bRk2
            sumXk = bXk1 + bXk2
        elif falla.loc_name == 'CC2TF':
                Z0=bRk0+bXk0*1j
                if abs(Z0)<10000:
                    Z1=bRk1+bXk1*1j
                    Z2=bRk2+bXk2*1j
                    Zcc = (Z1*Z2 + Z0*Z1 + Z0*Z2)/(math.sqrt(3)*Z2)
                    sumRk=Zcc.real
                    sumXk=Zcc.imag
                else:
                    sumRk = bRk1 + bRk2
                    sumXk = bXk1 + bXk2
                    app.PrintPlain("") 
                    app.PrintWarn("XR2FT de Barra %s se calcula como XR2F" %oBar)
                    app.PrintPlain("")
        if sumRk != 0:
            XR =  abs(sumXk / sumRk)
            if XR == 0:
                idc = 0
                Iasy = 0
                bipMax = 0
            else:
                if bIkssMax !=0:
                    bipMax = bIkssMax*math.sqrt(2)*(1+1*math.exp(-(math.pi)/XR))
                    Iasy =  bIkssMax*((1+2*math.exp(-(8*(math.pi))/XR)))**0.5
                    idc =  bIkssMax*math.sqrt(2)*((math.exp(-4*(math.pi)/XR)))
                    kdc = (idc/(bIbMax*(2**0.5)))*100
    else:
        bSkssMax=0
        bIkssMax=0
        bipMax=0
        idc=0
        bIbMax=0
        bIkMax=0
        bIthMax=0
        Iasy=0
        kdc=0
        XR=0
        i0x3=0
        idc = 0      
        sumRk = 0
        sumXk = 0
            

    if oBar.cpSubstat:
        SE_name = oBar.cpSubstat.loc_name
    else:
        SE_name = oBar.loc_name
    Bus_name = oBar.loc_name
    Tension=oBar.uknom
    f.write('%s;%s;%s;%s;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f;%3.3f; \n' %(falla.loc_name,operacion,SE_name,
    Bus_name,Tension,bSkssMax, bIkssMax, bipMax, 
    idc, bIbMax, bIkMax, bIthMax, Iasy, kdc, XR, i0x3, sumRk,sumXk))

def IccBarras3f(CC3F,sBar,sPro,identificador, vpath_csv, name_StCas,Sce):
    CC3F.iopt_mde = iopt_mde
    CC3F.Ta = Ta
    CC3F.Tk = Tk
    CC3F.Rf = Rf
    CC3F.Xf = Xf
    if iopt_mde:
        CC3F.cfac = cfac
    dirN=('%s%s%s-%s%s' %(vpath_csv,'\Reporte_CC3F',identificador,name_StCas,'.csv'))
    f = open(dirN,'w+')
    f.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s \n' %('Tipo de Icc',
    'Operacion','Subestacion','Barra',
    'Nivel de Tension','Skss','Ikss','ip',
    'idc','Ib','Ik','Ith','Iasy','X/R','kDC'))
    app.EchoOff()
    operacion = 'C/P'
    for oPro in sPro:
        oElem_Pro=oPro.obj_id
        oElem_Pro.outserv=0
    for oBar in sBar:
        oBar = oBar.obj_id
        report_3F(f,oBar,operacion)
    Sce.Deactivate(0)
    Sce.Activate()
    operacion = 'S/P'
    if (len(sPro)) !=0:
        for oPro in sPro:
            oElem_Pro=oPro.obj_id
            oElem_Pro.outserv=1
        for oBar in sBar:
            oBar = oBar.obj_id
            report_3F(f,oBar,operacion)
    Sce.Deactivate(0)
    Sce.Activate()
    app.EchoOn()
    f.close()
    f = open(dirN,'r+')
    texto = f.read()
    texto = texto.replace('.',',')
    f.seek(0)
    f.writelines(texto)
    f.close()

def IccBarras1f2f2ft(CC2F,CC2TF,CC1F,sBar,sPro,identificador, vpath_csv, name_StCas,Sce):
    fallas = [CC2F,CC2TF,CC1F]
    for falla in fallas:
        falla.iopt_mde = iopt_mde
        falla.Ta = Ta
        falla.Tk = Tk
        falla.Rf = Rf
        falla.Xf = Xf
        if iopt_mde:
            falla.cfac = cfac

    dirN=('%s%s%s-%s%s' %(vpath_csv,'\Reporte_1F2F2TF',identificador,name_StCas,'.csv'))
    f = open(dirN,'w+')
    f.write('%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s \n' 
    %('Tipo de Icc','Subestacion','Operacion','Barra','Nivel de Tension',
    'Skss', 'Ikss','ip','idc', 'Ib', 'Ik', 'Ith', 'Iasy', 'kdc', 'X/R','i0x3','SumRk','SumXk'))

    app.EchoOff()
    operacion = 'C/P'
    for oPro in sPro:
        oElem_Pro=oPro.obj_id
        oElem_Pro.outserv=0
    for falla in fallas:
        for oBar in sBar:
            oBar = oBar.obj_id
            report_1F2F2FT(f,falla,oBar,operacion)
    Sce.Deactivate(0)
    Sce.Activate()
    operacion = 'S/P'
    if (len(sPro)) !=0:
        for oPro in sPro:
            oElem_Pro=oPro.obj_id
            oElem_Pro.outserv=1
        for falla in fallas:
            for oBar in sBar:
                oBar = oBar.obj_id
                report_1F2F2FT(f,falla,oBar,operacion)
    Sce.Deactivate(0)
    Sce.Activate()

    app.EchoOn()
    f.close()
    f = open(dirN,'r+')
    texto = f.read()
    texto = texto.replace('.',',')
    f.seek(0)
    f.writelines(texto)
    f.close()


app = pf.GetApplication()
script = app.GetCurrentScript()
for i in script.GetContents():
    if i.loc_name == 'Barras':
        sBar = i.GetContents()
    if i.loc_name == 'Proyecto':
        sPro = i.GetContents()
    if i.loc_name == 'CC3F':
        CC3F = i
    if i.loc_name == 'CC2F':
        CC2F = i
    if i.loc_name == 'CC2TF':
        CC2TF = i
    if i.loc_name == 'CC1F':
        CC1F = i
    if i.loc_name == 'StudyCases':
        StudyCases = i

identificador = script.identificador
Ruta=script.ruta

iopt_mde = script.Method
Ta = script.BreakTime
Tk = script.FaultClearingTime
Rf = script.Zfalla_Rf
Xf = script.Zfalla_Xf
cfac = script.Tension
vpath_csv = script.ruta

StudyCases = StudyCases.Get()

for i in StudyCases:
    i.Activate()
    Sce = app.GetActiveScenario()
    name_StCas = i.loc_name
    if script.F3F:
        IccBarras3f(CC3F,sBar,sPro,identificador, vpath_csv, name_StCas,Sce)
    if script.F1F2F2TF:
        IccBarras1f2f2ft(CC2F,CC2TF,CC1F,sBar,sPro,identificador, vpath_csv, name_StCas,Sce)