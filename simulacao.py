import tkinter as tk
from tkinter import W, E, SW, NSEW, EW

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.lines import Line2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


from numpy.lib.function_base import append

import  PIL.Image
from PIL import ImageTk, ImageDraw

import math

from time import time




animationOn = False

x = 0.0

p011 = Line2D([],[])
yp1 = []
t = []
xmax = 10.0


p012 = Line2D([],[])
yp2 = []
t2 = []

animacaoSistemaWidth = 1300
animacaoSistemaHeight = 300
size = 50
calibri = PIL.ImageFont.truetype(r"misc/Calibri.ttf",14)
imMola = PIL.Image.open("misc/mola.jpg")

constanteElastica = 50
massaBloco = 5
xZero = 400
vZero = 0

cont1 = 0
cont2 = 0
cont3 = False

omega = math.sqrt(constanteElastica/massaBloco)
amplitude = math.sqrt(xZero**2 + (vZero/omega)**2)
if xZero != 0:
    constanteFase = math.atan(-vZero/(xZero*omega))
elif vZero < 0:
    constanteFase = math.pi/2
elif vZero > 0:
    constanteFase = -math.pi/2
else:
    constanteFase = 0

i = 1

def defineVariaveis():
    global constanteElastica, massaBloco, amplitude, xZero, vZero, omega, constanteFase, tempo

    constanteElastica = float(entradaConstanteElastica.get())
    massaBloco = float(entradaMassaBloco.get())
    xZero = float(entradaPosicaoInicial.get())
    vZero = float(entradaVelocidadeInicial.get())



    tempo=0
    omega = math.sqrt(constanteElastica/massaBloco)
    amplitude = float(math.sqrt(xZero**2 + (vZero/omega)**2))
    if xZero != 0:
        constanteFase = math.atan(-vZero/(xZero*omega))
    elif vZero < 0:
        constanteFase = math.pi/2
    elif vZero > 0:
        constanteFase = -math.pi/2
    else:
        constanteFase = 0


def troca():
    global animationOn, start, cont1, cont2, cont3
    if animationOn == False:
        animationOn = True
        if cont1 !=0:
            cont2 += time() - cont1
            print(cont2)
        if not cont3:
            start = time()
            cont3 = True
        
        att()
    else:
        cont1 = time()
        animationOn = False


def att():
    global animationOn, x
    x = time() - start - cont2
    if animationOn:
        
        attGraph1()
        attGraph2()
        attSystemAnimated()
        
        root.after(1,att)
    
def limpaGrafico1():
    global p011, t, yp1
    del(plotGraphPosition.lines[0])

    t=[]
    yp1=[]
    p011, = plotGraphPosition.plot(t, yp1,'b-')
    if amplitude !=0:
        plotGraphPosition.set_ylim(-amplitude-amplitude/20,amplitude+amplitude/20)
    else:
        plotGraphPosition.set_ylim(-1,1)
    plotGraphPosition.set_xlim(0,10.0)
    attGraph1()
    
def limpaGrafico2():
    global p012, t2, yp2
    del(plotGraphPositionVelocity.lines[0])

    t2=[]
    yp2=[]
    p012, = plotGraphPositionVelocity.plot(t2, yp2,'b-')
    if amplitude != 0 and omega != 0:
        plotGraphPositionVelocity.set_ylim(-omega*amplitude-(omega*amplitude)/20,omega*amplitude+(omega*amplitude)/20)
        plotGraphPositionVelocity.set_xlim(-amplitude - amplitude/20,amplitude + amplitude/20)
    else:
        plotGraphPositionVelocity.set_ylim(-1,-1)
        plotGraphPositionVelocity.set_xlim(-1,1)
    attGraph2()

def attGraph1():
    global x, yp1, t, p011, xmax, p021

    tmpp1 = (vZero/omega)*math.sin(omega*x)+xZero*math.cos(omega*x)
    yp1 = append(yp1,tmpp1)
    t = append(t,x)


    p011.set_data(t,yp1)
    canvasGraficoPosicao.draw()



    if x>= xmax-1.00:
        p011.axes.set_xlim(x-xmax+1.0,x+1.0)


def attGraph2():
    global x, yp2, t2, p012

    tmpp1 = (vZero/omega)*math.sin(omega*x)+xZero*math.cos(omega*x)
    tmpp2 = vZero*math.cos(omega*x)-xZero*omega*math.sin(omega*x)
    
    yp2 = append(yp2,tmpp1)
    t2 = append(t2,tmpp2)

    p012.set_data(yp2,t2)

    canvasGraficoSenoidal2.draw()

def attSystemAnimated():

    newIm = PIL.Image.new( "RGB", (animacaoSistemaWidth, animacaoSistemaHeight), (255, 255, 255))
    draw = ImageDraw.Draw(newIm)
    draw.line([20,animacaoSistemaHeight/2 + 2*size,animacaoSistemaWidth,animacaoSistemaHeight/2 + 2*size], fill=(0,0,0), width=2)
    draw.line([20,-animacaoSistemaHeight, 20,animacaoSistemaHeight/2 + 2*size], fill=(0,0,0), width=2)
    (cX, cY) = (animacaoSistemaWidth/2, animacaoSistemaHeight/2)


    print(amplitude)

    if amplitude !=0:

        deslocamento = (vZero/omega)*math.sin(omega*x)+xZero*math.cos(omega*x)

        deslocamentoNormalizado = (((deslocamento+amplitude)/(2*amplitude))*800)-400

        draw.text([400+cX+size/5,cY+2*size+size/3], text=str(round(amplitude,2)) + "m", fill=(0,0,0), font=calibri)
        draw.text([-400+cX+size/5,cY+2*size+size/3], text=str(round(-amplitude,2)) + "m", fill=(0,0,0), font=calibri)
        draw.rectangle( [cX+deslocamentoNormalizado, cY+size, cX+size+deslocamentoNormalizado, cY+2*size], (99, 72, 49))
        novo = imMola.resize(size=(int(cX+deslocamentoNormalizado-17), size))
        newIm.paste(novo,(22,int(cY + size)))

    else:
        draw.rectangle( [cX, cY+size, cX+size, cY+2*size], (99, 72, 49))
        novo = imMola.resize(size=(int(cX-17), size))
        newIm.paste(novo,(22,int(cY + size)))

    draw.text([cX+size/4,cY+2*size+size/3], text=" 0.0m", fill=(0,0,0), font=calibri)
    newPhoto = ImageTk.PhotoImage(newIm)
    labelAnimacaoSistema.configure(image = newPhoto)
    labelAnimacaoSistema.image = newPhoto

def seta():
    global animationOn, x, cont3, cont1, cont2
    animationOn = False
    cont1 = 0
    cont2 = 0
    cont3 = False
    defineVariaveis()
    x = 0
    limpaGrafico1()
    limpaGrafico2()
    attSystemAnimated()

class Application(tk.Tk):
    

    def __init__(self, *args, **kwargs):
        global p011, canvasGraficoPosicao, figureGraphPosition, plotGraphPosition
        global p012, canvasGraficoSenoidal2, plotGraphPositionVelocity
        global labelAnimacaoSistema
        global entradaConstanteElastica, entradaMassaBloco, entradaPosicaoInicial, entradaVelocidadeInicial
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "Simulação de Sistema Massa-Mola")
        
        container = tk.Frame(self,bg="#BDC3C7")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1) 
        
        self.resizable(0,0)

        # sets figure
        figureGraphPosition = Figure(figsize=(8.32,3.54), dpi=100)
        plotGraphPosition = figureGraphPosition.add_subplot(111)
        

        # adds distance to bottom edge
        figureGraphPosition.subplots_adjust(bottom=0.15)

        # sets initial xy-limits
        plotGraphPosition.set_ylim(-420,420)
        plotGraphPosition.set_xlim(0,10.0)

        # sets grid on
        plotGraphPosition.grid(True)

        # sets title and label names
        plotGraphPosition.set_title("Posição x Tempo")
        plotGraphPosition.set_xlabel("Tempo (s)")
        plotGraphPosition.set_ylabel("Posição (m)")


        # set plots
        p011, = plotGraphPosition.plot(t, yp1,'b-')




       

        canvasGraficoPosicao = FigureCanvasTkAgg(figureGraphPosition,container)
        
        

        canvasGraficoPosicao.draw()
        canvasGraficoPosicao.get_tk_widget().grid(row=1, column=0, columnspan=2, sticky="we",padx=(14,7),pady=(7,14))
      
        
        figureGraphPositionVelocity = Figure(figsize=(4.16,3.54), dpi=100)
        plotGraphPositionVelocity = figureGraphPositionVelocity.add_subplot(111)
        
        

        # adds distance to bottom edge
        figureGraphPositionVelocity.subplots_adjust(bottom=0.15)
        figureGraphPositionVelocity.subplots_adjust(left=0.25)

        # sets initial xy-limits

        plotGraphPositionVelocity.set_ylim(-omega*amplitude-(omega*amplitude)/20,omega*amplitude+(omega*amplitude)/20)
        plotGraphPositionVelocity.set_xlim(-amplitude - amplitude/20,amplitude + amplitude/20)

        # sets grid on
        plotGraphPositionVelocity.grid(True)

        # sets title and label names
        plotGraphPositionVelocity.set_title("Velocidade x Posição")
        plotGraphPositionVelocity.set_xlabel("Posição (m)")
        plotGraphPositionVelocity.set_ylabel("Velocidade (m/s)")


        # set plots
        p012, = plotGraphPositionVelocity.plot(t2, yp2,'b-')

        


        canvasGraficoSenoidal2 = FigureCanvasTkAgg(figureGraphPositionVelocity,container)
        canvasGraficoSenoidal2.draw()
        canvasGraficoSenoidal2.get_tk_widget().grid(row=1, column=2, sticky="we",padx=(7,14),pady=(7,14))

        im = PIL.Image.new("RGB",(animacaoSistemaWidth,animacaoSistemaHeight),(255, 255, 255))
        photo = ImageTk.PhotoImage(im)

        labelAnimacaoSistema = tk.Label(container, image=photo)#, height = 20)
        labelAnimacaoSistema.image = photo
        labelAnimacaoSistema.grid(row=0,column=0, columnspan=3, sticky="we",padx=(14,14),pady=(14,7))

        
        frameObtemDados = tk.Frame(container, bg="#BDC3C7", width=320)
        frameObtemDados.grid(row=0, column=3, rowspan=2, sticky="ns",padx=(7,14),pady=(14,14))

        labelTitulo = tk.Label(frameObtemDados, bg='#BDC3C7', text="Simulação de\nSistema Massa-Mola", font="Bahnschrift 18 bold", justify="center", width=21)
        labelTitulo.grid(row=0, column=0, columnspan=15,rowspan=3, pady= (10,5))




        labelAdicioneValoresFisicos = tk.Label(frameObtemDados, bg='#BDC3C7', text="  Adicione valores físicos:", font="Bahnschrift 13", anchor=W)
        labelAdicioneValoresFisicos.grid(row=3, column=0, columnspan=15,pady=(5,5), sticky="WE")

        labelConstanteElastica = tk.Label(frameObtemDados, bg='#BDC3C7', text="k", font="Bahnschrift 14 bold", anchor=E)
        labelConstanteElastica.grid(row=4,column=0, pady=(5,5), sticky="WE")

        descricaoConstanteElastica = tk.Label(frameObtemDados, bg='#BDC3C7', text="(constante elástica\nda mola)", font="Bahnschrift 8 italic", anchor=SW)
        descricaoConstanteElastica.grid(row=4,column=1,columnspan=8, pady=(5,5), sticky=NSEW)

        entradaConstanteElastica = tk.Entry(frameObtemDados, width=9)
        entradaConstanteElastica.grid(row=4, column=9, columnspan=4, pady=(5,5), sticky=NSEW)
        entradaConstanteElastica.insert(0,50)

        unidadeConstanteElastica = tk.Label(frameObtemDados,  bg='#BDC3C7', text="N/m", font="Bahnschrift 13", anchor=W)
        unidadeConstanteElastica.grid(row=4, column=13, columnspan=2, padx=(0,5))




        labelMassaBloco = tk.Label(frameObtemDados, bg='#BDC3C7', text="m", font="Bahnschrift 14 bold", anchor=E)
        labelMassaBloco.grid(row=5,column=0, pady=(5,5), sticky=EW)

        descricaoMassaBloco = tk.Label(frameObtemDados, bg='#BDC3C7', text="(massa do bloco)", font="Bahnschrift 8 italic", anchor=SW)
        descricaoMassaBloco.grid(row=5,column=1,columnspan=8, pady=(5,5), padx=(0,5), sticky=NSEW)

        entradaMassaBloco = tk.Entry(frameObtemDados, width=0)
        entradaMassaBloco.grid(row=5, column=9, columnspan=4, pady=(5,5), sticky=NSEW)
        entradaMassaBloco.insert(0,5)

        unidadeMassa = tk.Label(frameObtemDados,  bg='#BDC3C7', text="kg", font="Bahnschrift 13", anchor=W)
        unidadeMassa.grid(row=5, column=13, columnspan=2, padx=(0,5))




        labelAdicioneValoresFisicos = tk.Label(frameObtemDados, bg='#BDC3C7', text="  Defina as condições iniciais:", font="Bahnschrift 13", anchor=W)
        labelAdicioneValoresFisicos.grid(row=6, column=0, columnspan=15,pady=(5,5), sticky="WE")

        labelPosicaoInicial = tk.Label(frameObtemDados, bg='#BDC3C7', text="x(0)", font="Bahnschrift 14 bold", anchor=E)
        labelPosicaoInicial.grid(row=7,column=0, pady=(5,5), sticky=EW)

        descricaoPosicaoInicial = tk.Label(frameObtemDados, bg='#BDC3C7', text="(posição inicial\ndo bloco)", font="Bahnschrift 8 italic", anchor=SW)
        descricaoPosicaoInicial.grid(row=7,column=1,columnspan=8, pady=(5,5), sticky=NSEW)

        entradaPosicaoInicial = tk.Entry(frameObtemDados, width=9)
        entradaPosicaoInicial.grid(row=7, column=9, columnspan=4, pady=(5,5), sticky=NSEW)
        entradaPosicaoInicial.insert(0,400)

        unidadePosicaoInicial = tk.Label(frameObtemDados,  bg='#BDC3C7', text="m", font="Bahnschrift 13", anchor=W)
        unidadePosicaoInicial.grid(row=7, column=13, columnspan=2, padx=(0,5))




        labelVelocidadeInicial = tk.Label(frameObtemDados, bg='#BDC3C7', text="v(0)", font="Bahnschrift 14 bold", anchor=E)
        labelVelocidadeInicial.grid(row=8,column=0, pady=(5,10), sticky=EW)

        descricaoVelocidadeInicial = tk.Label(frameObtemDados, bg='#BDC3C7', text="(velocidade inicial\n do bloco)", font="Bahnschrift 8 italic", anchor=SW)
        descricaoVelocidadeInicial.grid(row=8,column=1,columnspan=8, pady=(5,10), sticky=NSEW)

        entradaVelocidadeInicial = tk.Entry(frameObtemDados, width=9)
        entradaVelocidadeInicial.grid(row=8, column=9, columnspan=4, pady=(5,10), sticky=NSEW)
        entradaVelocidadeInicial.insert(0,0)

        unidadeMassa = tk.Label(frameObtemDados,  bg='#BDC3C7', text="m/s", font="Bahnschrift 13", anchor=W)
        unidadeMassa.grid(row=8, column=13, columnspan=2, padx=(0,5), pady=(5,10))




        botao = tk.Button(frameObtemDados, text="Setar", justify="center", font="Bahnschrift 11", command=seta)
        botao.grid(row=9, column=0, columnspan=7, pady=(15,10), sticky=NSEW, padx=(10,10))

        botao = tk.Button(frameObtemDados, text="Rodar/Pausar", justify="center", font="Bahnschrift 11", command=troca)
        botao.grid(row=9, column=7, columnspan=8, pady=(15,10), sticky=NSEW, padx=(0,10))

        



root = Application()

attSystemAnimated()

root.mainloop()