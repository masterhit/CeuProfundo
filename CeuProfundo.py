#!/usr/bin/env python
# coding: utf-8

"""
# ## CARTA CELESTE - www.ceuprofundo.com

Versão 0.4.1


[PT-BR]
CeuProfundo plota cartas celestes retangulares e polares utilizando
dados de catálogos estelares e de objetos de céu profundo.
O tamanho e a resolução são ajustáveis para visualização e impressão.
A exibição de estrelas e objetos celestes pode ser desabilitada, criando
cartas em branco que podem ser utilizadas em atividades educacionais.

    Copyright (C) 2020  Wandeclayt M./N. Palivanas/CeuProfundo.com

    Este programa é um software livre: você pode redistribuí-lo e/ou
    modificá-lo sob os termos da Licença Pública Geral GNU, conforme
    publicado pela Free Software Foundation, seja a versão 3 da Licença
    ou (a seu critério) qualquer versão posterior.

    Este programa é distribuído na esperança de que seja útil,
    mas SEM QUALQUER GARANTIA; sem a garantia implícita de
    COMERCIALIZAÇÃO OU ADEQUAÇÃO A UM DETERMINADO PROPÓSITO. Veja a
    Licença Pública Geral GNU para obter mais detalhes.

    Você deve ter recebido uma cópia da Licença Pública Geral GNU
    junto com este programa. Se não, veja <https://www.gnu.org/licenses/>.

[EN]
CeuProfundo plots sky charts in rectangular and polar modes with data
from star and deep sky objects catalogs.
Size and resolution can be adjusted for viewing or printing.
Star and DSO exhibition can be toggled off to generate blank templates for
educational purposes.

    Copyright (C) 2020  Wandeclayt M./N. Palivanas/CeuProfundo.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


### CATALOGOS ###

Bright Star Catalog 5 (BSC5P)

The BSC5P database table contains data derived from the Bright Star Catalog,
5th Edition, preliminary, which is widely used as a source of basic
astronomical and astrophysical data for stars brighter than magnitude 6.5.
The database contains the identifications of included stars in several
other widely-used catalogs, double- and multiple-star identifications,
indication of variability and variable-star identifiers, equatorial
positions for B1900.0 and J2000.0, galactic coordinates, UBVRI photoelectric
photometric data when they exist, spectral types on the Morgan-Keenan (MK)
classification system, proper motions (J2000.0), parallax, radial- and
rotational-velocity data, and multiple-star information (number of components,
separation, and magnitude differences) for known non-single stars.

Hoffleit, D. and Warren, Jr., W.H., 1991, "The Bright Star Catalog,
5th Revised Edition (Preliminary Version)".


"""
import pandas as pd
import numpy as np
import argparse
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
#import matplotlib.font_manager
#import matplotlib.transforms as mtrans
from matplotlib.patches import ConnectionPatch, Circle
from matplotlib.gridspec import GridSpec
#from matplotlib.textpath import TextPath

# Argument Parser
ap = argparse.ArgumentParser(description='Ceu Profundo - Cartas Celestes',
                             prefix_chars='-',
                             prog='Ceu Profundo - Cartas Celestes')

ap.add_argument('-v', '--version', action='version', version='%(prog) s 0.4.1')
ap.add_argument('-S', '--Stars', action='store_true',
                help='Plota cartas com estrelas.')
ap.add_argument('-M', '--Messier', action='store_true',
                help='Plota cartas com objetos Messier.')
ap.add_argument('-C', '--Caldwell', action='store_true',
                help='Plota cartas com objetos Caldwell.')
ap.add_argument('-D', '--Dark', action='store_true',
                help='Usa fundo escuro.')
ap.add_argument('-r', '--retangular', action='store_true',
                help='Plota carta retangular.')
ap.add_argument('-s', '--sul', action='store_true',
                help='Plota carta polar sul.')
ap.add_argument('-n', '--norte', action='store_true',
                help='Plota carta polar norte.')
ap.add_argument('-d', '--dupla', action='store_true',
                help='Plota carta polar norte e sul.')
#ap.add_argument('-i', '--interativo', action='store_true',
#                help='Executa em modo interativo.')
#ap.add_argument('-a', '--all', action='store_true',
#                help='Plota todas as cartas.')
#ap.add_argument('-I', '--IC', action='store_true',
#                help='Plota cartas com objetos do Index Catalog.')
#ap.add_argument('-N', '--NGC', action='store_true',
#                help='Plota cartas com objetos NGC.')
ap.add_argument('-g', '--png', action='store_true',
                help='Muda extensão do arquivo de saída para .png.')

args = ap.parse_args()


# ARGUMENTOS
darkmode = args.Dark
stars = args.Stars
messier = args.Messier
caldwell = args.Caldwell
#ic = args.IC
polar_sul = args.sul
polar_norte = args.norte
polar_duplo = args.dupla
retangular = args.retangular
png = args.png

file_format = '.pdf'

#if args.all:  # GERA TODAS AS CARTAS
#    retangular = True
#    polar_sul = True
#    polar_norte = True
#    polar_duplo = True


# DEFINE SE A FAIXA ONDE OBJETOS PODEM SER OCULTADOS PELA LUA E' EXIBIDA
faixa_de_ocultacao = False

# DECLINACAO LIMITE PARA CARTAS RETANGULARES
declinacao_limite = 65

# TAMANHO/RESOLUCAO DO GRAFICO PARA IMPRESSAO
plot_size = 25
plot_dpi = 250

"""
###############################################################################
#
#                        DEFINICAO DE FUNCOES
#
###############################################################################
"""
#%%
# PARAMETROS DE TAMANHO DO PLOT DAS ESTRELAS
# magnitude=(plot_dpi/fator)*(base**-df.V)-limite
base = 0.6 * np.e
limite = 4
fator = 3
star_alpha = 0.4
alpha = star_background = 0.7


def StarMagnitude(StarCatalog):
    magnitude = (plot_dpi / fator) * (base ** -StarCatalog) - limite
    return(magnitude)


def ColorIndex(StarCatalog):
    color_index = 2.512 ** (- StarCatalog / 1.2)
    return(color_index)
###############################################################################


def StarsSul():
    magnitude = StarMagnitude(stars_south.V)
    if darkmode:
        circle = ax.patch
        circle.set_facecolor('black')
        plt.scatter(stars_south.RA * 2 * np.pi / 24,
                    90 + stars_south.DEC, c='white',
                    s=magnitude, alpha=star_background, zorder=2)
    plt.scatter(stars_south.RA * 2 * np.pi / 24,
                90 + stars_south.DEC,
                c=ColorIndex(stars_south.BminusV),
                cmap=plt.cm.RdYlBu, s=magnitude,
                alpha=star_alpha, zorder=3)
###############################################################################


def StarsNorte():
    magnitude = StarMagnitude(stars_north.V)
    color_index = ColorIndex(stars_north.BminusV)
    if darkmode:
        circle = ax.patch
        circle.set_facecolor('black')
        plt.scatter(stars_north.RA * 2 * np.pi / 24,
                    90 - stars_north.DEC,
                    c='white',
                    s=magnitude, alpha=star_background, zorder=2)
    plt.scatter(stars_north.RA * 2 * np.pi / 24,
                90 - stars_north.DEC,
                c=color_index,
                cmap=plt.cm.RdYlBu, s=magnitude,
                alpha=star_alpha, zorder=3)


#%%
###############################################################################
def header():
    ax = fig.add_subplot(gs[0, :])
    ax.axis('off')
    ax.text(0.5, 0, '',
            va='center', ha='center',
            fontsize=24, color='k')


###############################################################################
def rodape():
    ax = fig.add_subplot(gs[5, 0:1])
    image = plt.imread('ngc-1365.jpg')
    im = ax.imshow(image)
    patch = Circle((580, 460), radius=300, transform=ax.transData)
    im.set_clip_path(patch)
    ax.axis('off')


###############################################################################
    ax = fig.add_subplot(gs[5, 1:2])
    ax.set_title('MAGNITUDES')
    ax.set_ylim(8, -2)
    ax.set_xlim(-10, 10)
    ax.axis('off')
    x = np.zeros(8)
    y = np.arange(-1, 7, 1)
    plt.scatter(x, y, s=StarMagnitude(y), alpha=0.5)
    for i in y:
        ax.annotate(str(i), (1, i + 0.1))
###############################################################################
    ax = fig.add_subplot(gs[5, 2:3])
    ax.set_title('Objetos de Céu Profundo /\nDeep Sky Objects')
    ax.set_ylim(6, -1)
    ax.set_xlim(-1, 10)
    ax.axis('off')

    DSO_symbol = ('d', r'$\bigotimes$', '^', 's', r'$\emptyset$')

    DSO_name = ('Galáxia / Galaxy', 'Aglomerado Globular / Globular Cluster',
                'Aglomerado Aberto / Open Cluster', 'Nebulosa / Nebula',
                'Nebulosa Planetária / Planetary Nebula'
                )
    for i in range(0, 5, 1):
        plt.scatter(0, i, c='k', marker=DSO_symbol[i], s=60, alpha=0.5)
        ax.annotate(DSO_name[i], (1, i + 0.1))


###############################################################################
    ax = fig.add_subplot(gs[5, 3:4])
    ax.set_title('ALFABETO GREGO /\nGREEK ALPHABET')
    ax.axis('off')
    ax.text(0.25, 0.5,
            r"$\alpha$ - alpha" "\n"
            r"$\beta$ - beta" "\n"
            r"$\gamma$ - gamma" "\n"
            r"$\delta$ - delta" "\n"
            r"$\epsilon$ - epsilon" "\n"
            r"$\zeta$ - zeta" "\n"
            r"$\eta$ - eta" "\n"
            r"$\theta$ - theta" "\n"
            r"$\iota$ - iota" "\n"
            r"$\kappa$ - kappa" "\n"
            r"$\lambda$ - lambda" "\n"
            r"$\mu$ - mu" "\n"
            r"$\nu$ - nu" "\n",
            va="center", ha='left')
    ax.text(0.5, 0.5,
            r"$\xi$ - xi (ksi)" "\n"
            r"$o$ - omicron" "\n"
            r"$\pi$ - pi" "\n"
            r"$\rho$ - rho" "\n"
            r"$\sigma$ - sigma" "\n"
            r"$\tau$ - tau" "\n"
            r"$\upsilon$ - upsilon" "\n"
            r"$\phi$ - phi" "\n"
            r"$\chi$ - chi" "\n"
            r"$\psi$ - psi" "\n"
            r"$\omega$ - omega" "\n",
            va="center", ha='left')
###############################################################################
    ax = fig.add_subplot(gs[5, 4:7])
    ax.set_title('CONSTELAÇÕES / CONSTELLATIONS')
    ax.axis('off')
    ax.text(0, 0.5,
            "And - Andromeda\n"
            "Ant - Antlia\n"
            "Aps - Apus\n"
            "Aql - Aquila\n"
            "Aqr - Aquarius\n"
            "Ara - Ara\n"
            "Ari - Aries\n"
            "Aur - Auriga\n"
            "Boo - Boötes\n"
            "CMa - Canis Major\n"
            "CMi - Canis Minor\n"
            "CVn - Canes Venatici\n"
            "Cae - Caelum\n"
            "Cam - Camelopardalis\n"
            "Cap - Capricornus\n"
            "Car - Carina\n"
            "Cas - Cassiopeia\n"
            "Cen - Centaurus\n"
            "Cep - Cepheus\n"
            "Cet - Cetus\n"
            "Cha - Chamaeleon\n"
            "Cir - Circinus\n",
            va="center", ha='left')
    ax.text(0.2775, 0.5,
            "Cnc - Cancer\n"
            "Col - Columba\n"
            "Com - Coma Berenices\n"
            "CrA - Corona Australis\n"
            "CrB - Corona Borealis\n"
            "Crt - Crater\n"
            "Cru - Crux\n"
            "Crv - Corvus\n"
            "Cyg - Cygnus\n"
            "Del - Delphinus\n"
            "Dor - Dorado\n"
            "Dra - Draco\n"
            "Equ - Equuleus\n"
            "Eri - Eridanus\n"
            "For - Fornax\n"
            "Gem - Gemini\n"
            "Gru - Grus\n"
            "Her - Hercules\n"
            "Hor - Horologium\n"
            "Hya - Hydra\n"
            "Hyi - Hydrus\n"
            "Ind - Indus\n",
            va="center", ha='left')
    ax.text(0.55, 0.5,
            "Lac - Lacerta\n"
            "Leo - Leo\n"
            "LMi - Leo Minor\n"
            "Lep - Lepus\n"
            "Lib - Libra\n"
            "Lup - Lupus\n"
            "Lyn - Lynx\n"
            "Lyr - Lyra\n"
            "Men - Mensa\n"
            "Mic - Microscopium\n"
            "Mon - Monoceros\n"
            "Mus - Musca\n"
            "Nor - Norma\n"
            "Oct - Octans\n"
            "Oph - Ophiucus\n"
            "Ori - Orion\n"
            "Pav - Pavo\n"
            "Peg - Pegasus\n"
            "Per - Perseu\n"
            "Phe - Phoenix\n"
            "Pic - Pictor\n"
            "PsA - Pisces Austrinus\n",
            va="center", ha='left')
    ax.text(0.8250, 0.5,
            "Psc - Pisces\n"
            "Pup - Puppis\n"
            "Pyx - Pyxis\n"
            "Ret - Reticulum\n"
            "Scl - Sculptor\n"
            "Sco - Scorpius\n"
            "Sct - Scutum\n"
            "Ser - Serpens\n"
            "Sex - Sextans\n"
            "Sge - Sagitta\n"
            "Sgr - Sagittarius\n"
            "Tau - Taurus\n"
            "Tel - Telescopium\n"
            "TrA - Triangulum Australe\n"
            "Tri - Triangulum\n"
            "Tuc - Tucana\n"
            "UMa - Ursa Major\n"
            "UMi - Ursa Minor\n"
            "Vel - Vela\n"
            "Vir - Virgo\n"
            "Vol - Volans\n"
            "Vul - Vulpecula\n",
            va="center", ha='left')

###############################################################################
    ax = fig.add_subplot(gs[5, 7:])
    #creditos = "GNU Public License 3.0\n© 2020 Wandeclayt Melo"
    ax.axis('off')
    line0 = "Copyright © 2020 Wandeclayt Melo/\n"
    line1 = "Natália Palivanas.\n"
    line2 = "GNU General Public License 3.0\n\n"
    line3 = "www.ceuprofundo.com\n twitter: @ceuprofundo\n\n"
    line4 = "Generated with Python 3.7.6 and Matplotlib 3.2.1\n"
    line5 = "www.github.com/masterhit/CeuProfundo"

    ax.text(0.5, 0.5, line0 + line1 + line2 + line3 + line4 + line5,
            va="center", ha='center')


"""
    ax = fig.add_subplot(gs[5, 2:3])
    ax.set_title('ÍNDICE DE COR (B-V) /\nCOLOR INDEX (B-V)')
    ax.set_ylim(3, -2)
    ax.set_xlim(-10, 10)
    ax.axis('off')
    x = np.zeros(8)
    y = np.arange(-1.5, 2.5, 0.5)
    plt.scatter(x, y, s=StarMagnitude(-1),
                c=-y,
                cmap=plt.cm.RdYlBu, alpha=star_alpha)
    for i in y:
        ax.annotate(str(i), (1, i + 0.1))
"""

#%%

###############################################################################
###############################################################################
#
#                       CONSTELLATION LINES OVERLAY
#
###############################################################################
###############################################################################


def Line(StarA, StarB):
    con = ConnectionPatch(StarA, StarB, coordsA="data", coordsB="data",
                          arrowstyle="-", color="gray", alpha=0.5)
    ax.add_artist(con)


# AJUSTE/CONVERSAO DE COORDENADAS
def Coordenadas(RA, DEC):
    if retangular:
        #Nenhum ajuste em coordenadas retangulares: RA -> X
        RA_ajustado = RA
        #Nenhum ajuste em coordenadas retangulares: DEC -> Y
        DEC_ajustado = DEC
    else:
        #Conversao de Ascencao Reta para Radianos: RA -> theta
        RA_ajustado = RA * 2 * np.pi / 24
        #Ajuste de Origem da declinacao (0 no equador, 90 no polo): DEC -> r
        DEC_ajustado = 90 - abs(DEC)
    return (RA_ajustado, DEC_ajustado)


# ROTULOS DAS CONSTELACOES
def Const_Label(Const, RA, DEC):
    plt.annotate(Const, xy=Coordenadas(RA, DEC),
                 color='gray', alpha=0.8, fontsize='medium')


# ROTULOS DAS ESTRELAS
def Star_Label(Star, RA, DEC):
    plt.annotate(Star, xy=(Coordenadas(RA, DEC)),
                 color='gray', alpha=0.8, fontsize='medium')


"""
    # Greek Alphabet

    Alpha
    Beta
    Gamma
    Delta
    Epsilon
    Zeta
    Eta
    Theta
    Iota
    Kappa
    Lambda
    Mu
    Nu
    Xi
    Omicron
    Pi
    Rho
    Sigma
    Tau
    Upsilon
    Phi
    Chi
    Psi
    Omega

"""


def And():
    AlphaAnd = Coordenadas(0.139806, 29.090556)
    BetaAnd = Coordenadas(1.162194, 35.620556)
    GammaAnd = Coordenadas(2.065000, 42.329722)
    DeltaAnd = Coordenadas(0.655472, 30.860833)
    MuAnd = Coordenadas(0.945889, 38.499444)
    NuAnd = Coordenadas(0.830222, 41.078889)

    Line(AlphaAnd, DeltaAnd)
    Line(DeltaAnd, BetaAnd)
    Line(BetaAnd, GammaAnd)
    Line(BetaAnd, MuAnd)
    Line(MuAnd, NuAnd)

    Const_Label('And', 0.66, 35)
    Star_Label(r'$\alpha$', 0.14, 30.2)
    Star_Label(r'$\beta$', 1.16, 35)
    Star_Label(r'$\gamma$', 2.1, 42)
    Star_Label(r'$\delta$', 0.69, 31)
    Star_Label(r'$\mu$', 1, 39)
    Star_Label(r'$\nu$', 0.86, 42)


def Ant():
    _AlpAnt = Coordenadas(10.45252778, -31.06777778)
    _EpsAnt = Coordenadas(9.487416667, -35.95138889)
    _IotAnt = Coordenadas(10.94530556, -37.13777778)

    Line(_AlpAnt, _IotAnt)
    Line(_AlpAnt, _EpsAnt)

    Const_Label('Ant', 10.33, -35)
    Star_Label(r'$\alpha$', 10.42, -31.5)


def Apus():
    AlphaApodi = Coordenadas(14.80, -79.04)
    BetaApodi = Coordenadas(16.72, -77.52)
    GammaApodi = Coordenadas(16.56, -78.90)
    DeltaApodi = Coordenadas(16.34, -78.69)

    Line(AlphaApodi, DeltaApodi)
    Line(BetaApodi, DeltaApodi)
    Line(BetaApodi, GammaApodi)

    Const_Label('Aps', 15.66, -78)
    Star_Label(r'$\alpha$', 14.66, -76)
    Star_Label(r'$\beta$', 16.66, -77)


def Aql():
    _53AlpAql = Coordenadas(19.84638889, 8.868333332999999)
    _50GamAql = Coordenadas(19.771, 10.61333333)
    _17ZetAql = Coordenadas(19.09016667, 13.86333333)
    #_65TheAql = Coordenadas(20.18841667, 0.8213888889000001)
    _30DelAql = Coordenadas(19.42497222, 3.1147222219999997)
    #_16LamAql = Coordenadas(19.10413889, -4.8825)
    _60BetAql = Coordenadas(19.92188889, 6.4066666670000005)
    #_55EtaAql = Coordenadas(19.87455556, 1.005555556)
    #_12Aql = Coordenadas(19.028, -5.738888889)
    # _13EpsAql = Coordenadas(18.99372222, 15.06833333)

    Line(_17ZetAql, _50GamAql)
    Line(_50GamAql, _53AlpAql)
    Line(_53AlpAql, _60BetAql)
    Line(_53AlpAql, _30DelAql)
    Line(_30DelAql, Coordenadas(19.25, 0))
    Line(_60BetAql, Coordenadas(20.1, 0))

    Const_Label('Aql', 19.7, 3)
    Star_Label(r'$\alpha$', 19.85, 9.8)
    Star_Label(r'$\beta$', 19.92188889, 6.4066666670000005)
    Star_Label(r'$\gamma$', 19.771, 10.61333333)
    Star_Label(r'$\delta$', 19.42497222, 3.1147222219999997)
    Star_Label(r'$\epsilon$', 18.99372222, 15.06833333)
    Star_Label(r'$\zeta$', 19.09016667, 13.86333333)
    Star_Label(r'$\theta$', 20.18841667, 0.8213888889000001)


def AqlSouth():
    _65TheAql = Coordenadas(20.18841667, -0.8213888889000001)
    _16LamAql = Coordenadas(19.10413889, -4.8825)
    #_12Aql = Coordenadas(19.028, -5.738888889)

    Line(Coordenadas(19.25, 0), _16LamAql)
    Line(Coordenadas(20.1, 0), _65TheAql)

    Const_Label('Aql', 19.16, -8)


def Aqr():
    _22BetAqr = Coordenadas(21.52597222, -5.5711111110000004)
    _34AlpAqr = Coordenadas(22.09638889, -0.31972222219999996)
    _76DelAqr = Coordenadas(22.91083333, -15.82083333)
    _88Aqr = Coordenadas(23.15744444, -21.1725)
    _73LamAqr = Coordenadas(22.87691667, -7.579722222000001)
    _2EpsAqr = Coordenadas(20.79461111, -9.495833333)
    _48GamAqr = Coordenadas(22.36094444, -1.387222222)
    _98Aqr = Coordenadas(23.38283333, -20.10055556)
    #_71Tau2Aqr = Coordenadas(22.82652778, -13.5925)
    #_62EtaAqr = Coordenadas(22.58927778, -0.1175)
    #_43TheAqr = Coordenadas(22.28055556, -7.783333333)
    #_91Psi1Aqr = Coordenadas(23.26486111, -9.087777778)
    _90PhiAqr = Coordenadas(23.23872222, -6.048888889)
    _105Ome2Aqr = Coordenadas(23.71202778, -14.545)
    _6MuAqr = Coordenadas(20.87755556, -8.983333333)
    _69Tau1Aqr = Coordenadas(22.79522222, -14.05638889)

    Line(_2EpsAqr, _6MuAqr)
    Line(_6MuAqr, _22BetAqr)
    Line(_22BetAqr, _34AlpAqr)
    Line(_34AlpAqr, _48GamAqr)
    Line(_48GamAqr, _73LamAqr)
    Line(_73LamAqr, _90PhiAqr)
    Line(_90PhiAqr, _105Ome2Aqr)
    Line(_105Ome2Aqr, _98Aqr)
    Line(_98Aqr, _88Aqr)
    Line(_88Aqr, _76DelAqr)
    Line(_76DelAqr, _69Tau1Aqr)
    Line(_69Tau1Aqr, _73LamAqr)

    Const_Label('Aqr', 23.16, -12)
    Star_Label(r'$\alpha$', 22.09638889, -1.61972222219999996)
    Star_Label(r'$\beta$', 21.52597222, -5.5711111110000004)
    Star_Label(r'$\gamma$', 22.36094444, -1.387222222)
    Star_Label(r'$\delta$', 22.91083333, -15.82083333)
    Star_Label(r'$\epsilon$', 20.79461111, -9.495833333)
    Star_Label(r'$98$', 23.38283333, -20.10055556)
    Star_Label(r'$\eta$', 22.58927778, -1.3175)
    Star_Label(r'$\theta$', 22.28055556, -7.783333333)
    Star_Label(r'$\lambda$', 22.87691667, -7.579722222000001)
    Star_Label(r'$\mu$', 20.87755556, -8.983333333)
    Star_Label(r'$\tau^1$', 22.79522222, -14.05638889)
    Star_Label(r'$\tau^2$', 22.82652778, -13.5925)
    Star_Label(r'$\phi$', 23.23872222, -6.048888889)
    Star_Label(r'$\omega$', 23.71202778, -14.545)


def Ara():
    _BetAra = Coordenadas(17.42166667, -55.53)
    #_AlpAra = Coordenadas(17.53069444, -49.87611111)
    #_ZetAra = Coordenadas(16.977, -55.99027778)
    _TheAra = Coordenadas(18.11052778, -50.09166667)
    #_EtaAra = Coordenadas(16.82975, -59.04138889)
    _Eps1Ara = Coordenadas(16.99308333, -53.16055556)

    Line(_TheAra, _BetAra)
    Line(_BetAra, _Eps1Ara)

    Const_Label('Ara', 17.33, -54)


def Aries():
    AlphaArietis = Coordenadas(2.12, 23.46)
    BetaArietis = Coordenadas(1.91, 20.81)
    GammaArietis = Coordenadas(1.89, 19.29)

    Line(AlphaArietis, BetaArietis)
    Line(BetaArietis, GammaArietis)

    Const_Label('Ari', 2, 20)
    Star_Label(r'$\alpha$', 2.12, 23.46)
    Star_Label(r'$\beta$', 1.91, 20.81)
    Star_Label(r'$\gamma$', 1.89, 19.29)


def Aur():
    BetaTauri = Coordenadas(5.438194, 28.607500)
    AlphaAur = Coordenadas(5.278167, 45.998056)
    BetaAur = Coordenadas(5.992139, 44.947500)
    EtaAur = Coordenadas(5.108583, 41.234444)
    ThetaAur = Coordenadas(5.995361, 37.212500)
    IotaAur = Coordenadas(4.949889, 33.166111)

    Line(BetaTauri, ThetaAur)
    Line(ThetaAur, BetaAur)
    Line(BetaAur, AlphaAur)
    Line(AlphaAur, EtaAur)
    Line(EtaAur, IotaAur)
    Line(IotaAur, BetaTauri)

    Const_Label('Aur', 5.5, 43)
    Star_Label(r'$\alpha$', 5.278167, 45.998056)
    Star_Label(r'$\beta$', 5.992139, 44.947500)
    Star_Label(r'$\eta$', 5.108583, 41.234444)
    Star_Label(r'$\theta$', 5.995361, 37.212500)
    Star_Label(r'$\iota$', 4.949889, 33.166111)


def Bootes():

    AlphaBootis = Coordenadas(14.261028, 19.182500)
    BetaBootis = Coordenadas(15.032444, 40.390556)
    GammaBootis = Coordenadas(14.534639, 38.308333)
    DeltaBootis = Coordenadas(15.258389, 33.314722)
    EpsilonBootis = Coordenadas(14.749778, 27.074167)
    ZetaBootis = Coordenadas(14.685806, 13.728333)
    EtaBootis = Coordenadas(13.911417, 18.397778)
    RhoBootis = Coordenadas(14.530500, 30.371389)

    Line(AlphaBootis, EtaBootis)
    Line(AlphaBootis, ZetaBootis)
    Line(AlphaBootis, EpsilonBootis)
    Line(AlphaBootis, RhoBootis)
    Line(RhoBootis, GammaBootis)
    Line(GammaBootis, BetaBootis)
    Line(BetaBootis, DeltaBootis)
    Line(DeltaBootis, EpsilonBootis)

    Const_Label('Boo', 14.85, 32)
    Star_Label(r'$\alpha$', 14.2, 17.5)
    Star_Label(r'$\beta$', 15.032444, 40.390556)
    Star_Label(r'$\gamma$', 14.534639, 38.308333)
    Star_Label(r'$\delta$', 15.258389, 33.314722)
    Star_Label(r'$\epsilon$', 14.749778, 27.074167)
    Star_Label(r'$\zeta$', 14.685806, 13.728333)
    Star_Label(r'$\eta$', 13.911417, 18.397778)
    Star_Label(r'$\rho$', 14.450500, 30.371389)


def CMa():

    AlphaCMa = Coordenadas(6.752472, -16.716111)
    BetaCMa = Coordenadas(6.378333, -17.955833)
    GammaCMa = Coordenadas(7.062639, -15.633333)
    DeltaCMa = Coordenadas(7.139861, -26.393333)
    EpsilonCMa = Coordenadas(6.977083, -28.972222)
    #ZetaCMa = Coordenadas(6.338556, -30.063333)
    EtaCMa = Coordenadas(7.401583, -29.303056)
    ThetaCMa = Coordenadas(6.903167, -12.038611)
    IotaCMa = Coordenadas(6.935611, -17.054167)
    #KappaCMa  = Coordenadas(6.830694, -32.508611)
    #LambdaCMa  = Coordenadas(6.469472, -32.580000)

    Line(DeltaCMa, AlphaCMa)
    Line(DeltaCMa, EpsilonCMa)
    Line(DeltaCMa, EtaCMa)
    Line(AlphaCMa, IotaCMa)
    Line(IotaCMa, GammaCMa)
    Line(GammaCMa, ThetaCMa)
    Line(AlphaCMa, BetaCMa)

    Const_Label('CMa', 6.8, -25)
    Star_Label(r'$\alpha$', 6.73, -18)
    Star_Label(r'$\beta$', 6.378333, -17.955833)
    Star_Label(r'$\gamma$', 7.062639, -15.633333)
    Star_Label(r'$\delta$', 7.139861, -26.393333)
    Star_Label(r'$\epsilon$', 6.977083, -28.972222)
    Star_Label(r'$\eta$', 7.401583, -29.303056)


def CMi():
    AlphaCMi = Coordenadas(7.655028, 5.225000)
    BetaCMi = Coordenadas(7.452500, 8.289444)

    Line(AlphaCMi, BetaCMi)

    Const_Label('CMi', 7.6, 8)
    Star_Label(r'$\alpha$', 7.66, 4.6)


def CVn():
    _12Alp2CVn = Coordenadas(12.93380556, 38.31833333)
    _8BetCVn = Coordenadas(12.56236111, 41.3575)
    _20CVn = Coordenadas(13.29236111, 40.5725)

    Line(_12Alp2CVn, _8BetCVn)
    Line(_8BetCVn, _20CVn)

    Const_Label('CVn', 12.83, 43)
    Star_Label(r'$\alpha$', 12.93, 37)
    Star_Label(r'$\beta$', 12.56, 40)


def Cae():
    _AlpCae = Coordenadas(4.676027778, -41.86388889)
    _Gam1Cae = Coordenadas(5.073444444, -35.48333333)
    _BetCae = Coordenadas(4.700972222, -37.14444444)
    _DelCae = Coordenadas(4.513916667, -44.95388889)

    Line(_Gam1Cae, _BetCae)
    Line(_BetCae, _AlpCae)
    Line(_AlpCae, _DelCae)

    Const_Label('Cae', 4.83, -38)


def Cam():
    _10BetCam = Coordenadas(5.056972222, 60.44222222)
    _9AlpCam = Coordenadas(4.9008333330000005, 66.34277778)
    _7Cam = Coordenadas(4.954777778, 53.75222222)
    _GamCam = Coordenadas(3.8393055560000002, 71.33222222)
    _43Cam = Coordenadas(6.895055556, 68.88833333)
    _36Cam = Coordenadas(6.214194443999999, 65.71833333)

    Line(_GamCam, _9AlpCam)
    Line(_9AlpCam, _10BetCam)
    Line(_10BetCam, _7Cam)
    Line(_9AlpCam, _36Cam)
    Line(_36Cam, _43Cam)

    Const_Label('Cam', 5.33, 68)
    Star_Label(r'$\alpha$', 4.9008333330000005, 66.34277778)
    Star_Label(r'$\beta$', 5.056972222, 60.44222222)
    Star_Label(r'$\gamma$', 3.8393055560000002, 71.33222222)
    Star_Label(r'$7$', 4.954777778, 53.75222222)
    Star_Label(r'$43$', 6.895055556, 68.88833333)
    Star_Label(r'$36$', 6.214194443999999, 65.71833333)


def Cap():
    AlphaCapricorni = Coordenadas(20.294139, -12.508333)
    BetaCapricorni = Coordenadas(20.350194, -14.781389)
    GammaCapricorni = Coordenadas(21.668194, -16.662222)
    DeltaCapricorni = Coordenadas(21.784000, -16.127222)
    EpsilonCapricorni = Coordenadas(21.618000, -19.466111)
    ZetaCapricorni = Coordenadas(21.444444, -22.411389)
    ThetaCapricorni = Coordenadas(21.099111, -17.232778)
    IotaCapricorni = Coordenadas(21.370778, -16.834444)
    PsiCapricorni = Coordenadas(20.768250, -25.270833)
    OmegaCapricorni = Coordenadas(20.863694, -26.919167)

    Line(AlphaCapricorni, BetaCapricorni)
    Line(AlphaCapricorni, ThetaCapricorni)
    Line(BetaCapricorni, PsiCapricorni)
    Line(PsiCapricorni, OmegaCapricorni)
    Line(OmegaCapricorni, ZetaCapricorni)
    Line(ZetaCapricorni, EpsilonCapricorni)
    Line(EpsilonCapricorni, DeltaCapricorni)
    Line(DeltaCapricorni, GammaCapricorni)
    Line(GammaCapricorni, IotaCapricorni)
    Line(IotaCapricorni, ThetaCapricorni)

    Const_Label('Cap', 20.9, -22)
    Star_Label(r'$\alpha$', 20.294139, -12.508333)
    Star_Label(r'$\beta$', 20.350194, -14.781389)
    Star_Label(r'$\gamma$', 21.668194, -16.662222)
    Star_Label(r'$\delta$', 21.784000, -16.127222)
    Star_Label(r'$\epsilon$', 21.618000, -19.466111)
    Star_Label(r'$\zeta$', 21.444444, -22.411389)
    Star_Label(r'$\theta$', 21.099111, -17.232778)
    Star_Label(r'$\iota$', 21.370778, -16.834444)
    Star_Label(r'$\psi$', 20.768250, -25.270833)
    Star_Label(r'$\omega$', 20.863694, -26.919167)


def Car():
    _AlpCar = Coordenadas(6.399194444, -52.69583333)
    _BetCar = Coordenadas(9.22, -69.71722222)
    _EpsCar = Coordenadas(8.375222222, -59.50972222)
    _IotCar = Coordenadas(9.284833333, -59.27527778)
    _TheCar = Coordenadas(10.71594444, -64.39444444)
    #_UpsCar = Coordenadas(9.785027778, -65.07194444)
    _OmeCar = Coordenadas(10.22894444, -70.03805556)
    #_PCar = Coordenadas(10.53372222, -61.68527778)
    _ChiCar = Coordenadas(7.946305556, -52.98222222)
    _XCar = Coordenadas(11.14316667, -58.975)
    _ZCar = Coordenadas(11.109000000000002, -62.42416667)
    #_EtaCar = Coordenadas(10.751, -59.68416667)
    #_UpsCar = Coordenadas(9.785194444, -65.0725)

    Line(_AlpCar, _BetCar)
    Line(_BetCar, _OmeCar)
    Line(_OmeCar, _TheCar)
    Line(_TheCar, _ZCar)
    Line(_ZCar, _XCar)
    Line(_XCar, _IotCar)
    Line(_IotCar, _EpsCar)
    Line(_EpsCar, _ChiCar)
    Line(_ChiCar, _AlpCar)

    Const_Label('Car', 9.66, -65)
    Star_Label(r'$\alpha$', 6.4, -53.5)
    Star_Label(r'$\beta$', 9.22, -69.71722222)
    Star_Label(r'$\epsilon$', 8.375222222, -59.50972222)
    Star_Label(r'$\theta$', 10.71594444, -64.39444444)
    Star_Label(r'$\iota$', 9.284833333, -59.27527778)
    Star_Label(r'$\eta$', 10.7, -58)


def Cas():
    AlphaCas = Coordenadas(0.675139, 56.537222)
    BetaCas = Coordenadas(0.152972, 59.149722)
    GammaCas = Coordenadas(0.945139, 60.716667)
    DeltaCas = Coordenadas(1.430278, 60.235278)
    EpsilonCas = Coordenadas(1.906583, 63.670000)

    Line(AlphaCas, BetaCas)
    Line(AlphaCas, GammaCas)
    Line(DeltaCas, GammaCas)
    Line(DeltaCas, EpsilonCas)

    Const_Label('Cas', 1, 58)
    Star_Label(r'$\alpha$', 0.7, 57)
    Star_Label(r'$\beta$', 0.15, 61)


def Cen():
    AlphaCen = Coordenadas(14.66, -60.83)
    BetaCen = Coordenadas(14.06, -60.37)
    GammaCen = Coordenadas(12.69, -48.96)
    DeltaCen = Coordenadas(12.14, -50.72)
    EpsilonCen = Coordenadas(13.66, -53.46)
    ZetaCen = Coordenadas(13.92, -47.29)
    ThetaCen = Coordenadas(14.11, -36.37)
    IotaCen = Coordenadas(13.34, -36.71)
    NuCen = Coordenadas(13.82, -41.69)
    PiCen = Coordenadas(11.35, -54.49)
    Omicron1Cen = Coordenadas(11.53, -59.44)
    RhoCen = Coordenadas(12.19, -52.37)
    KapCen = Coordenadas(14.98602778, -42.10416667)
    PhiCen = Coordenadas(13.97119444, -42.10083333)
    EtaCen = Coordenadas(14.59177778, -42.15777778)

    Line(AlphaCen, BetaCen)
    Line(BetaCen, EpsilonCen)
    Line(EpsilonCen, GammaCen)
    Line(EpsilonCen, ZetaCen)
    Line(ZetaCen, NuCen)
    Line(GammaCen, DeltaCen)
    Line(NuCen, ThetaCen)
    Line(NuCen, IotaCen)
    Line(DeltaCen, PiCen)
    Line(GammaCen, RhoCen)
    Line(RhoCen, Omicron1Cen)
    Line(NuCen, PhiCen)
    Line(PhiCen, EtaCen)
    Line(EtaCen, KapCen)

    Const_Label('Cen', 13.3, -50)
    Star_Label(r'$\alpha$', 14.66, -61.5)
    Star_Label(r'$\beta$', 14.06, -61)
    Star_Label(r'$\epsilon$', 13.5, -53.46)
    Star_Label(r'$\gamma$', 12.69, -50)
    Star_Label(r'$\zeta$', 13.92, -47.3)
    Star_Label(r'$\mu$', 13.7, -42.5)
    Star_Label(r'$\delta$', 12.14, -49)
    Star_Label(r'$\rho$', 12.19, -52.45)
    Star_Label(r'$\eta$', 14.59177778, -42.15777778)
    Star_Label(r'$\theta$', 14.11, -36.37)
    Star_Label(r'$\iota$', 13.34, -36.71)
    Star_Label(r'$\kappa$', 14.98602778, -42.10416667)
    Star_Label(r'$\phi$', 13.97119444, -42.10083333)
    Star_Label(r'$\nu$', 13.82, -41.69)
    Star_Label(r'$o$', 11.53, -60.0)
    Star_Label(r'$\pi$', 11.35, -53.49)


def Cep():
    _5AlpCep = Coordenadas(21.30966667, 62.58555556)
    _35GamCep = Coordenadas(23.65577778, 77.6325)
    _8BetCep = Coordenadas(21.47766667, 70.56083333)
    _21ZetCep = Coordenadas(22.18091667, 58.20111111)
    #_3EtaCep = Coordenadas(20.75483333, 61.83888889)
    _32IotCep = Coordenadas(22.828000000000003, 66.20055556)

    Line(_5AlpCep, _8BetCep)
    Line(_8BetCep, _35GamCep)
    Line(_35GamCep, _32IotCep)
    Line(_32IotCep, _21ZetCep)
    Line(_32IotCep, _8BetCep)
    Line(_21ZetCep, _5AlpCep)

    Const_Label('Cep', 22.16, 65)
    Star_Label(r'$\alpha$', 21.3, 61.5)
    Star_Label(r'$\beta$', 21.29, 71.5)
    Star_Label(r'$\gamma$', 23.65577778, 77.6325)
    Star_Label(r'$\zeta$', 22.18091667, 58.20111111)
    Star_Label(r'$\eta$', 20.75483333, 61.83888889)
    Star_Label(r'$\iota$', 22.828000000000003, 66.20055556)


def Cet():
    _16BetCet = Coordenadas(0.7265, -17.98666667)
    _68OmiCet = Coordenadas(2.3224166669999997, -2.9775)
    _31EtaCet = Coordenadas(1.143166667, -10.18222222)
    _52TauCet = Coordenadas(1.734472222, -15.9375)
    _8IotCet = Coordenadas(0.32380555559999996, -8.823888889)
    _45TheCet = Coordenadas(1.400388889, -8.183333333)
    _55ZetCet = Coordenadas(1.857666667, -10.335)

    Line(_68OmiCet, _55ZetCet)
    Line(_55ZetCet, _52TauCet)
    Line(_52TauCet, _16BetCet)
    Line(_16BetCet, _8IotCet)
    Line(_8IotCet, _31EtaCet)
    Line(_31EtaCet, _45TheCet)
    Line(_45TheCet, _68OmiCet)
    Line(_68OmiCet, Coordenadas(2.658055556, 0))

    Const_Label('Cet', 1.5, 12)
    Star_Label(r'$o$', 2.34, -3.5)
    Star_Label(r'$\beta$', 0.72, -18.1)
    Star_Label(r'$\zeta$', 1.857666667, -10.335)
    Star_Label(r'$\eta$', 1.143166667, -10.18222222)
    Star_Label(r'$\theta$', 1.400388889, -8.183333333)
    Star_Label(r'$\iota$', 0.32380555559999996, -8.823888889)
    Star_Label(r'$\tau$', 1.734472222, -15.9375)


def CetNorth():
    _92AlpCet = Coordenadas(3.0380000000000003, 4.089722222)
    _86GamCet = Coordenadas(2.721666667, 3.235833333)
    _82DelCet = Coordenadas(2.658055556, 0.3286111111)
    _87MuCet = Coordenadas(2.7490277780000003, 10.11416667)
    _73Xi2Cet = Coordenadas(2.469305556, 8.46)
    _91LamCet = Coordenadas(2.99525, 8.9075)

    Line(_82DelCet, _86GamCet)
    Line(_86GamCet, _92AlpCet)
    Line(_92AlpCet, _91LamCet)
    Line(_91LamCet, _87MuCet)
    Line(_87MuCet, _73Xi2Cet)
    Line(_73Xi2Cet, _86GamCet)

    Const_Label('Cet', 2.7, 7)
    Star_Label(r'$\alpha$', 3.07, 3.8)


def Cha():

    _AlpCha = Coordenadas(8.308777778, -76.91972222)
    _GamCha = Coordenadas(10.59113889, -78.60777778)
    _BetCha = Coordenadas(12.30575, -79.31222222)
    #_TheCha = Coordenadas(8.344027778, -77.48444444)
    _Del2Cha = Coordenadas(10.763, -80.54027778)
    _EpsCha = Coordenadas(11.99369444, -78.22194444)

    Line(_AlpCha, _GamCha)
    Line(_GamCha, _Del2Cha)
    Line(_Del2Cha, _BetCha)
    Line(_BetCha, _EpsCha)
    Line(_EpsCha, _GamCha)

    Const_Label('Cha', 9.5, -77.5)
    Star_Label(r'$\alpha$', 8.3, -75)


def Cir():
    AlphaCircini = Coordenadas(14.71, -64.97)
    BetaCircini = Coordenadas(15.29, -58.80)
    GammaCircini = Coordenadas(15.39, -59.32)

    Line(AlphaCircini, BetaCircini)
    Line(AlphaCircini, GammaCircini)

    Const_Label('Cir', 15.33, -58)


def Cancer():

    AlphaCancri = Coordenadas(8.974778, 11.857778)
    BetaCancri = Coordenadas(8.275250, 9.185556)
    GammaCancri = Coordenadas(8.721417, 21.468611)
    DeltaCancri = Coordenadas(8.744750, 18.154167)
    IotaCancri = Coordenadas(8.778278, 28.760000)

    Line(AlphaCancri, DeltaCancri)
    Line(DeltaCancri, BetaCancri)
    Line(DeltaCancri, GammaCancri)
    Line(GammaCancri, IotaCancri)

    Const_Label('Cnc', 8.66, 17)
    Star_Label(r'$\alpha$', 8.974778, 11.857778)
    Star_Label(r'$\beta$', 8.275250, 9.185556)
    Star_Label(r'$\gamma$', 8.721417, 21.468611)
    Star_Label(r'$\delta$', 8.744750, 18.154167)
    Star_Label(r'$\iota$', 8.778278, 28.760000)


def Col():
    _AlpCol = Coordenadas(5.660805556000001, -34.07416667)
    _BetCol = Coordenadas(5.849333333, -35.76833333)
    _DelCol = Coordenadas(6.3685555560000005, -33.43638889)
    _EpsCol = Coordenadas(5.5201944439999995, -35.47055556)
    _EtaCol = Coordenadas(5.985777777999999, -42.81527778)
    _GamCol = Coordenadas(5.958944444, -35.28333333)

    Line(_EpsCol, _AlpCol)
    Line(_AlpCol, _BetCol)
    Line(_BetCol, _EtaCol)
    Line(_BetCol, _GamCol)
    Line(_GamCol, _DelCol)

    Const_Label('Col', 5.66, -37)
    Star_Label(r'$\alpha$', 5.66, -35)


def Com():
    _43BetCom = Coordenadas(13.19788889, 27.87805556)
    _15GamCom = Coordenadas(12.44897222, 28.26833333)
    _42AlpCom = Coordenadas(13.16647222, 17.52944444)

    Line(_42AlpCom, _43BetCom)
    Line(_43BetCom, _15GamCom)

    Const_Label('Com', 13, 25)
    Star_Label(r'$\alpha$', 13.10, 17.53)
    Star_Label(r'$\beta$', 13.2, 28.2)
    Star_Label(r'$\gamma$', 12.45, 28.3)


def CrA():
    _AlpCrA = Coordenadas(19.15786111, -37.90444444)
    _BetCrA = Coordenadas(19.16713889, -39.34083333)
    _DelCrA = Coordenadas(19.13913889, -40.49666667)
    _TheCrA = Coordenadas(18.55838889, -42.3125)
    _ZetCrA = Coordenadas(19.05191667, -42.09527778)
    _EpsCrA = Coordenadas(18.97872222, -37.1075)
    _GamCrA = Coordenadas(19.10697222, -37.06333333)
    #_LamCrA = Coordenadas(18.72969444, -38.32361111)
    #_MuCrA = Coordenadas(18.79572222, -40.40611111)
    _Eta1CrA = Coordenadas(18.81402778, -43.68)
    #_Eta2CrA = Coordenadas(18.82638889, -43.43388889)
    #_Kap2CrA = Coordenadas(18.55641667, -38.72611111)
    #_Kap1CrA = Coordenadas(18.55647222, -38.72027778)

    Line(_EpsCrA, _GamCrA)
    Line(_GamCrA, _AlpCrA)
    Line(_AlpCrA, _BetCrA)
    Line(_BetCrA, _DelCrA)
    Line(_DelCrA, _ZetCrA)
    Line(_ZetCrA, _Eta1CrA)
    Line(_Eta1CrA, _TheCrA)

    Const_Label('CrA', 18.83, -42)
    Star_Label(r'$\alpha$', 19.15786111, -38)
    Star_Label(r'$\beta$', 19.16713889, -40)
    Star_Label(r'$\gamma$', 19.10697222, -37.5)
    Star_Label(r'$\delta$', 19.13913889, -40.9)
    Star_Label(r'$\epsilon$', 18.97872222, -37.6)
    Star_Label(r'$\zeta$', 19.05191667, -42.6)
    Star_Label(r'$\eta$', 18.81402778, -44.1)


def CrB():
    _5AlpCrB = Coordenadas(15.57813889, 26.71472222)
    _3BetCrB = Coordenadas(15.46380556, 29.10583333)
    _8GamCrB = Coordenadas(15.71238889, 26.29555556)
    _4TheCrB = Coordenadas(15.54883333, 31.35916667)
    _13EpsCrB = Coordenadas(15.95980556, 26.87777778)
    _10DelCrB = Coordenadas(15.82658333, 26.06833333)
    #_16TauCrB = Coordenadas(16.14952778, 36.49083333)
    #_11KapCrB = Coordenadas(15.85386111, 35.6575)
    #_19XiCrB = Coordenadas(16.36827778, 30.89194444)
    _14IotCrB = Coordenadas(16.02405556, 29.85111111)
    """
    _7Zet2CrB = Coordenadas(15.65630556, 36.63583333)
    _6MuCrB = Coordenadas(15.5875, 39.01)
    _20Nu1CrB = Coordenadas(16.37261111, 33.79916667)
    _21Nu2CrB = Coordenadas(16.37477778, 33.70361111)
    _15RhoCrB = Coordenadas(16.01741667, 33.30361111)
    _12LamCrB = Coordenadas(15.92988889, 37.94694444)
    _1OmiCrB = Coordenadas(15.33569444, 29.61611111)
    _9PiCrB = Coordenadas(15.73313889, 32.51583333)
    _2EtaCrB = Coordenadas(15.38675, 30.28777778)
    _17SigCrB = Coordenadas(16.24466667, 33.85861111)
    _18UpsCrB = Coordenadas(16.27911111, 29.15027778)
    _7Zet1CrB = Coordenadas(15.65616667, 36.63666667)
    _2EtaCrB = Coordenadas(15.38675, 30.28777778)
    _17SigCrB = Coordenadas(16.24466667, 33.85833333)
    """
    Line(_14IotCrB, _13EpsCrB)
    Line(_13EpsCrB, _10DelCrB)
    Line(_10DelCrB, _8GamCrB)
    Line(_8GamCrB, _5AlpCrB)
    Line(_5AlpCrB, _3BetCrB)
    Line(_3BetCrB, _4TheCrB)

    Const_Label('CrB', 15.83, 28)
    Star_Label(r'$\alpha$', 15.57813889, 25.31472222)
    Star_Label(r'$\beta$', 15.46380556, 27.70583333)
    Star_Label(r'$\gamma$', 15.71238889, 24.89555556)
    Star_Label(r'$\delta$', 15.82658333, 24.66833333)
    Star_Label(r'$\epsilon$', 15.95980556, 25.47777778)
    Star_Label(r'$\theta$', 15.54883333, 29.75916667)
    Star_Label(r'$\iota$', 16.02405556, 28.45111111)


def Crt():
    _12DelCrt = Coordenadas(11.32236111, -14.77861111)
    _7AlpCrt = Coordenadas(10.99625, -18.29888889)
    _15GamCrt = Coordenadas(11.41469444, -17.68388889)
    _11BetCrt = Coordenadas(11.19430556, -22.82583333)
    _21TheCrt = Coordenadas(11.61136111, -9.802222222000001)
    _27ZetCrt = Coordenadas(11.74605556, -18.35083333)
    _14EpsCrt = Coordenadas(11.41016667, -10.85944444)
    #_13LamCrt = Coordenadas(11.38941667, -18.78)
    _30EtaCrt = Coordenadas(11.93358333, -17.15083333)

    Line(_30EtaCrt, _27ZetCrt)
    Line(_27ZetCrt, _15GamCrt)
    Line(_15GamCrt, _12DelCrt)
    Line(_12DelCrt, _14EpsCrt)
    Line(_14EpsCrt, _21TheCrt)
    Line(_12DelCrt, _7AlpCrt)
    Line(_7AlpCrt, _11BetCrt)
    Line(_11BetCrt, _15GamCrt)

    Const_Label('Crt', 11.15, -18)
    Star_Label(r'$\alpha$', 11, -18.5)
    Star_Label(r'$\beta$', 11.19, -23)
    Star_Label(r'$\gamma$', 11.41469444, -17.68388889)
    Star_Label(r'$\delta$', 11.32236111, -14.77861111)
    Star_Label(r'$\epsilon$', 11.41016667, -10.85944444)
    Star_Label(r'$\zeta$', 11.74605556, -18.35083333)
    Star_Label(r'$\eta$', 11.93358333, -17.15083333)
    Star_Label(r'$\theta$', 11.61136111, -9.802222222000001)


def Cru():
    #AlphaCrucis = (12.44*2*np.pi/24, 90-63.1)
    AlphaCrucis = Coordenadas(12.44, -63.1)
    GammaCrucis = Coordenadas(12.52, -57.1)
    BetaCrucis = Coordenadas(12.79, -59.7)
    DeltaCrucis = Coordenadas(12.25, -58.75)

    #Alpha-Gamma
    Line(AlphaCrucis, GammaCrucis)
    #Beta-Delta
    Line(BetaCrucis, DeltaCrucis)

    Const_Label('Cru', 12.5, -61)
    Star_Label(r'$\alpha$', 12.55, -63.1)
    Star_Label(r'$\beta$', 12.8, -58.5)
    Star_Label(r'$\gamma$', 12.52, -55.5)
    Star_Label(r'$\delta$', 12.1, -58.65)
    Star_Label(r'$\epsilon$', 12.25, -60.2)


def Crv():
    AlphaCrv = Coordenadas(12.14, -24.72)
    BetaCrv = Coordenadas(12.57, -23.40)
    GammaCrv = Coordenadas(12.26, -17.54)
    DeltaCrv = Coordenadas(12.50, -16.51)
    EpsilonCrv = Coordenadas(12.17, -22.62)

    Line(AlphaCrv, EpsilonCrv)
    Line(BetaCrv, DeltaCrv)
    Line(BetaCrv, EpsilonCrv)
    Line(GammaCrv, DeltaCrv)
    Line(GammaCrv, EpsilonCrv)

    Const_Label('Crv', 12.33, -20)
    Star_Label(r'$\alpha$', 12.14, -24.72)
    Star_Label(r'$\beta$', 12.57, -23.4)
    Star_Label(r'$\gamma$', 12.26, -17.54)
    Star_Label(r'$\delta$', 12.50, -16.51)
    Star_Label(r'$\epsilon$', 12.17, -22.62)


def Cygnus():
    AlphaCygni = Coordenadas(20.690528, 45.280278)
    BetaCygni = Coordenadas(19.512028, 27.959722)
    GammaCygni = Coordenadas(20.370472, 40.256667)
    DeltaCygni = Coordenadas(19.749583, 45.130833)
    EpsilonCygni = Coordenadas(20.770194, 33.970278)
    #ZetaCygni = Coordenadas(21.215611, 30.226944)
    EtaCygni = Coordenadas(19.938444, 35.083333)
    #ThetaCygni = Coordenadas(19.607361, 50.221111)

    Line(AlphaCygni, GammaCygni)
    Line(GammaCygni, DeltaCygni)
    Line(GammaCygni, EpsilonCygni)
    Line(GammaCygni, EtaCygni)
    Line(EtaCygni, BetaCygni)
    #Line(DeltaCygni,ThetaCygni)
    #Line(EpsilonCygni, ZetaCygni)

    Const_Label('Cyg', 20, 40)
    Star_Label(r'$\alpha$', 20.7, 46)
    Star_Label(r'$\beta$', 19.5, 29)
    Star_Label(r'$\gamma$', 20.370472, 40.256667)
    Star_Label(r'$\delta$', 19.749583, 45.130833)
    Star_Label(r'$\epsilon$', 20.770194, 33.970278)
    Star_Label(r'$\eta$', 19.938444, 35.083333)
    Star_Label(r'$\zeta$', 21.215611, 30.226944)
    Star_Label(r'$\theta$', 19.607361, 50.221111)


def Del():
    _6BetDel = Coordenadas(20.62583333, 14.59527778)
    _9AlpDel = Coordenadas(20.66063889, 15.91194444)
    _2EpsDel = Coordenadas(20.55355556, 11.30333333)
    _12Gam2Del = Coordenadas(20.77763889, 16.12416667)
    _11DelDel = Coordenadas(20.72430556, 15.07444444)

    Line(_2EpsDel, _6BetDel)
    Line(_6BetDel, _9AlpDel)
    Line(_9AlpDel, _12Gam2Del)
    Line(_12Gam2Del, _11DelDel)
    Line(_11DelDel, _6BetDel)

    Const_Label('Del', 20.66, 13)


def Dor():
    _AlpDor = Coordenadas(4.566611111, -55.045)
    _BetDor = Coordenadas(5.560416667, -62.48972222)
    #_GamDor = Coordenadas(4.267111111, -51.48666667)
    _DelDor = Coordenadas(5.746222222, -65.73555556)
    _36Dor = Coordenadas(5.901694443999999, -63.09)
    _ZetDor = Coordenadas(5.091833333, -57.47277778)

    Line(_AlpDor, _BetDor)
    Line(_BetDor, _DelDor)
    Line(_DelDor, _36Dor)
    Line(_36Dor, _BetDor)
    Line(_BetDor, _ZetDor)
    Line(_ZetDor, _AlpDor)

    Const_Label('Dor', 5, -58)
    Star_Label(r'$\alpha$', 4.66, -55)
    Star_Label(r'$\beta$', 5.66, -62.5)


def Dra():
    _33GamDra = Coordenadas(17.94344444, 51.48888889)
    _14EtaDra = Coordenadas(16.39986111, 61.51416667)
    _23BetDra = Coordenadas(17.50722222, 52.30138889)
    _57DelDra = Coordenadas(19.20925, 67.66166667)
    _22ZetDra = Coordenadas(17.14644444, 65.71472222)
    _12IotDra = Coordenadas(15.4155, 58.96611111)
    #_44ChiDra = Coordenadas(18.35094444, 72.73277778)
    _11AlpDra = Coordenadas(14.07313889, 64.37583333)
    _32XiDra = Coordenadas(17.89213889, 56.87277778)
    #_63EpsDra = Coordenadas(19.80288889, 70.26777778)
    _1LamDra = Coordenadas(11.52338889, 69.33111111)
    _5KapDra = Coordenadas(12.55805556, 69.78833333)
    _13TheDra = Coordenadas(16.03147222, 58.56527778)
    _43PhiDra = Coordenadas(18.34597222, 71.33777778)

    """
    _60TauDra = Coordenadas(19.25916667, 73.35555556)
    _67RhoDra = Coordenadas(20.04697222, 67.87361111)
    _31Psi1Dra = Coordenadas(17.69897222, 72.14888889)
    _58PiDra = Coordenadas(19.34447222, 65.71472222)
    _10Dra = Coordenadas(13.85719444, 64.72333333)
    _47OmiDra = Coordenadas(18.85336111, 59.38833333)
    _61SigDra = Coordenadas(19.53933333, 69.66111111)
    _45Dra = Coordenadas(18.54291667, 57.04555556)
    _28OmeDra = Coordenadas(17.61586111, 68.75805556)
    _42Dra = Coordenadas(18.43308333, 65.56361111)
    _52UpsDra = Coordenadas(18.90663889, 71.29722222)
    _18Dra = Coordenadas(16.68197222, 64.58916667)
    _25Nu2Dra = Coordenadas(17.53777778, 55.17305556)
    """
    _24Nu1Dra = Coordenadas(17.53627778, 55.18416667)

    Line(_1LamDra, _5KapDra)
    Line(_5KapDra, _11AlpDra)
    Line(_11AlpDra, _12IotDra)
    Line(_12IotDra, _13TheDra)
    Line(_13TheDra, _14EtaDra)
    Line(_14EtaDra, _22ZetDra)
    Line(_22ZetDra, _43PhiDra)
    Line(_43PhiDra, _57DelDra)
    Line(_57DelDra, _32XiDra)
    Line(_32XiDra, _24Nu1Dra)
    Line(_24Nu1Dra, _23BetDra)
    Line(_23BetDra, _33GamDra)
    Line(_33GamDra, _32XiDra)

    Const_Label('Dra', 17.66, 60)
    Star_Label(r'$\alpha$', 14, 63)
    Star_Label(r'$\beta$', 17.51, 51)
    Star_Label(r'$\gamma$', 18, 51.5)
    Star_Label(r'$\delta$', 19.33, 67.7)
    Star_Label(r'$\xi$', 18, 56.9)
    Star_Label(r'$\nu$', 17.53, 56)


def Equ():
    _8AlpEqu = Coordenadas(21.26372222, 5.247777778000001)
    _7DelEqu = Coordenadas(21.24136111, 10.00694444)
    _5GamEqu = Coordenadas(21.17236111, 10.13166667)

    Line(_8AlpEqu, _7DelEqu)
    Line(_7DelEqu, _5GamEqu)

    Const_Label('Equ', 21.25, 7.5)
    Star_Label(r'$\alpha$', 21.26, 4.85)


def Eri():
    _AlpEri = Coordenadas(1.6285833330000001, -57.23666667)
    _67BetEri = Coordenadas(5.130833333, -5.086388889)
    _34GamEri = Coordenadas(3.967166667, -13.50861111)
    _The1Eri = Coordenadas(2.9710277780000003, -40.30472222)
    _23DelEri = Coordenadas(3.720805556, -9.763333333)
    _PhiEri = Coordenadas(2.2751666669999997, -51.51222222)
    _41Ups4Eri = Coordenadas(4.29825, -33.79833333)
    _16Tau4Eri = Coordenadas(3.3252777780000002, -21.75777778)
    _ChiEri = Coordenadas(1.9326388890000001, -51.60888889)
    _18EpsEri = Coordenadas(3.548833333, -9.458333332999999)
    _52Ups2Eri = Coordenadas(4.5925, -30.56222222)
    #_53Eri = Coordenadas(4.6363333330000005, -14.30388889)
    _3EtaEri = Coordenadas(2.940472222, -8.898055556000001)
    _48NuEri = Coordenadas(4.605305556, -3.3525)
    _43Eri = Coordenadas(4.400611111, -34.01694444)
    _57MuEri = Coordenadas(4.758361111, -3.254722222)
    _38Omi1Eri = Coordenadas(4.19775, -6.8375)
    _11Tau3Eri = Coordenadas(3.0398611110000004, -23.62444444)
    _IotEri = Coordenadas(2.6777777780000003, -39.85555556)
    _27Tau6Eri = Coordenadas(3.7808055560000002, -23.24972222)
    _KapEri = Coordenadas(2.44975, -47.70388889)
    _19Tau5Eri = Coordenadas(3.5631388889999998, -21.63277778)
    #_69LamEri = Coordenadas(5.1524444439999995, -8.754166667)
    #_54Eri = Coordenadas(4.674027778, -19.67166667)
    #_The2Eri = Coordenadas(2.9711944439999995, -40.30444444)
    #_61OmeEri = Coordenadas(4.881583333, -5.452777778)
    _26PiEri = Coordenadas(3.7690277780000003, -12.10166667)
    #_40Omi2Eri = Coordenadas(4.254527778, -7.652777778)
    _1Tau1Eri = Coordenadas(2.7517222219999997, -18.5725)
    _50Ups1Eri = Coordenadas(4.5585, -29.76666667)
    _33Tau8Eri = Coordenadas(3.895166667, -24.6125)
    _36Tau9Eri = Coordenadas(3.99875, -24.01638889)
    #_17Eri = Coordenadas(3.510305556, -5.075277778)
    _2Tau2Eri = Coordenadas(2.850638889, -21.00416667)
    """
    _32Eri = Coordenadas(3.904861111, -2.954722222)
    _64Eri = Coordenadas(4.998833333, -12.5375)
    _13ZetEri = Coordenadas(3.263888889, -8.819722222000001)
    _65PsiEri = Coordenadas(5.023972222, -7.173888889)
    _39Eri = Coordenadas(4.239916667, -10.25638889)
    _15Eri = Coordenadas(3.3061388889999996, -22.51138889)
    _45Eri = Coordenadas(4.531305556, 0.04388888889)
    _60Eri = Coordenadas(4.836555556, -16.21722222)
    _47Eri = Coordenadas(4.569888889, -8.231388889)
    _66Eri = Coordenadas(5.112694444, -4.655)
    _68Eri = Coordenadas(5.145444444, -4.456111111)
    _42XiEri = Coordenadas(4.394666667, -3.7455555560000002)
    _20Eri = Coordenadas(3.604833333, -17.46694444)
    _51Eri = Coordenadas(4.626694444, -2.4733333330000002)
    _28Tau7Eri = Coordenadas(3.794333333, -23.87472222)
    _24Eri = Coordenadas(3.741805556, -1.163055556)
    _10Rho3Eri = Coordenadas(3.071222222, -7.600833333)
    _35Eri = Coordenadas(4.0255555560000005, -1.549722222)
    _9Rho2Eri = Coordenadas(3.045083333, -7.685277778)
    _63Eri = Coordenadas(4.997333333, -10.26333333)
    _37Eri = Coordenadas(4.172916667, -6.923888889)
    _4Eri = Coordenadas(2.956583333, -23.86194444)
    _30Eri = Coordenadas(3.8782222219999998, -5.361388889)
    _58Eri = Coordenadas(4.793416667, -16.93444444)
    _62Eri = Coordenadas(4.940055556, -5.171388889)
    _22Eri = Coordenadas(3.6773055560000003, -5.210555556)
    _25Eri = Coordenadas(3.7490277780000003, 0.2966666667)
    _5Eri = Coordenadas(2.994777778, -2.465)
    _46Eri = Coordenadas(4.565222222, -6.738888889)
    _8Rho1Eri = Coordenadas(3.019444444, -7.662777778)
    _59Eri = Coordenadas(4.809027778, -16.32944444)
    _6Eri = Coordenadas(2.96825, -23.60611111)
    _56Eri = Coordenadas(4.734805556, -8.503611111)
    _21Eri = Coordenadas(3.650305556, -5.626111111)
    _7Eri = Coordenadas(3.014166667, -2.878611111)
    _32Eri = Coordenadas(3.904833333, -2.952777778)
    _14Eri = Coordenadas(3.276583333, -9.154444444)
    _55Eri = Coordenadas(4.726416667, -8.796111111)
    """
    HR1189 = Coordenadas(3.809833333, -37.62222222)

    Line(_AlpEri, _ChiEri)
    Line(_ChiEri, _PhiEri)
    Line(_PhiEri, _KapEri)
    Line(_KapEri, _IotEri)
    Line(_IotEri, _The1Eri)
    Line(_The1Eri, HR1189)
    Line(HR1189, _41Ups4Eri)
    Line(_41Ups4Eri, _43Eri)
    Line(_43Eri, _52Ups2Eri)
    Line(_52Ups2Eri, _50Ups1Eri)
    Line(_50Ups1Eri, _36Tau9Eri)
    Line(_36Tau9Eri, _33Tau8Eri)
    Line(_33Tau8Eri, _27Tau6Eri)
    Line(_27Tau6Eri, _19Tau5Eri)
    Line(_19Tau5Eri, _16Tau4Eri)
    Line(_16Tau4Eri, _11Tau3Eri)
    Line(_11Tau3Eri, _2Tau2Eri)
    Line(_2Tau2Eri, _1Tau1Eri)
    Line(_1Tau1Eri, _3EtaEri)
    Line(_3EtaEri, _18EpsEri)
    Line(_18EpsEri, _23DelEri)
    Line(_23DelEri, _26PiEri)
    Line(_26PiEri, _34GamEri)
    Line(_34GamEri, _38Omi1Eri)
    Line(_38Omi1Eri, _48NuEri)
    Line(_48NuEri, _57MuEri)
    Line(_57MuEri, _67BetEri)

    Const_Label('Eri', 2.5, -50)
    Star_Label(r'$\alpha$', 1.5, -57.5)
    Star_Label(r'$\beta$', 5.130833333, -5.086388889)
    Star_Label(r'$\gamma$', 3.967166667, -13.50861111)
    Star_Label(r'$\delta$', 3.720805556, -9.763333333)
    Star_Label(r'$\epsilon$', 3.548833333, -9.458333332999999)
    Star_Label(r'$\zeta$', 3.263888889, -8.819722222000001)
    Star_Label(r'$\eta$', 2.940472222, -8.898055556000001)
    Star_Label(r'$\theta^1$', 2.9710277780000003, -40.30472222)
    Star_Label(r'$\iota$', 2.6777777780000003, -39.85555556)
    Star_Label(r'$\kappa$', 2.44975, -47.70388889)
    Star_Label(r'$\lambda$', 5.1524444439999995, -8.754166667)
    Star_Label(r'$\mu$', 4.758361111, -3.254722222)
    Star_Label(r'$\nu$', 4.605305556, -3.3525)
    Star_Label(r'$\xi$', 4.394666667, -3.7455555560000002)
    Star_Label(r'$o^1$', 4.19775, -6.8375)
    Star_Label(r'$\pi$', 3.7690277780000003, -12.10166667)
    Star_Label(r'$\rho^1$', 3.019444444, -7.662777778)
    Star_Label(r'$\tau^1$', 2.7517222219999997, -18.5725)
    Star_Label(r'$\upsilon^1$', 4.5585, -29.76666667)
    Star_Label(r'$\phi$', 2.2751666669999997, -51.51222222)
    Star_Label(r'$\chi$', 1.9326388890000001, -51.60888889)
    Star_Label(r'$\psi$', 5.023972222, -7.173888889)
    Star_Label(r'$\omega$', 4.881583333, -5.452777778)


def For():
    _AlpFor = Coordenadas(3.201194444, -28.98694444)
    _BetFor = Coordenadas(2.818166667, -32.40583333)
    _NuFor = Coordenadas(2.074833333, -29.29694444)

    Line(_AlpFor, _BetFor)
    Line(_BetFor, _NuFor)

    Const_Label('For', 2.5, -33)
    Star_Label(r'$\alpha$', 3.2, -27.5)
    Star_Label(r'$\beta$', 2.818166667, -32.40583333)
    Star_Label(r'$\nu$', 2.074833333, -29.29694444)


def Gem():
    _78BetGem = Coordenadas(7.75525, 28.02611111)
    _24GamGem = Coordenadas(6.628527778, 16.39916667)
    _66AlpGem = Coordenadas(7.5766666670000005, 31.88833333)
    _13MuGem = Coordenadas(6.3826666670000005, 22.51361111)
    _66AlpGem = Coordenadas(7.5766666670000005, 31.88861111)
    _27EpsGem = Coordenadas(6.732194444, 25.13111111)
    #_7EtaGem = Coordenadas(6.247944444, 22.50666667)
    _31XiGem = Coordenadas(6.754833333, 12.89555556)
    _55DelGem = Coordenadas(7.335388889, 21.98222222)
    _77KapGem = Coordenadas(7.740777777999999, 24.39805556)
    _54LamGem = Coordenadas(7.301555556, 16.54027778)
    _34TheGem = Coordenadas(6.879805556, 33.96111111)
    _43ZetGem = Coordenadas(7.0684722220000005, 20.57027778)
    _60IotGem = Coordenadas(7.428777778, 27.79805556)
    _69UpsGem = Coordenadas(7.5986944439999995, 26.89583333)
    _18NuGem = Coordenadas(6.4827222220000005, 20.21222222)
    #_1Gem = Coordenadas(6.0686666670000005, 23.26333333)
    #_62RhoGem = Coordenadas(7.485194443999999, 31.78444444)
    #_75SigGem = Coordenadas(7.721861111, 28.88361111)
    _46TauGem = Coordenadas(7.1856666670000005, 30.24527778)

    Line(_66AlpGem, _46TauGem)
    Line(_46TauGem, _34TheGem)
    Line(_46TauGem, _27EpsGem)
    Line(_27EpsGem, _18NuGem)
    Line(_27EpsGem, _13MuGem)
    Line(_46TauGem, _60IotGem)
    Line(_60IotGem, _69UpsGem)
    Line(_69UpsGem, _78BetGem)
    Line(_69UpsGem, _77KapGem)
    Line(_69UpsGem, _55DelGem)
    Line(_55DelGem, _43ZetGem)
    Line(_43ZetGem, _24GamGem)
    Line(_55DelGem, _54LamGem)
    Line(_54LamGem, _31XiGem)

    Const_Label('Gem', 7.16, 28)
    Star_Label(r'$\alpha$', 7.6, 33)
    Star_Label(r'$\beta$', 7.83, 27.5)
    Star_Label(r'$\gamma$', 6.628527778, 16.39916667)
    Star_Label(r'$\delta$', 7.335388889, 21.98222222)
    Star_Label(r'$\epsilon$', 6.732194444, 25.13111111)
    Star_Label(r'$\zeta$', 7.0684722220000005, 20.57027778)
    Star_Label(r'$\eta$', 6.247944444, 22.50666667)
    Star_Label(r'$\theta$', 6.879805556, 33.96111111)
    Star_Label(r'$\iota$', 7.428777778, 27.79805556)
    Star_Label(r'$\kappa$', 7.740777777999999, 24.39805556)
    Star_Label(r'$\lambda$', 7.301555556, 16.54027778)
    Star_Label(r'$\mu$', 6.3826666670000005, 22.51361111)
    Star_Label(r'$\nu$', 6.4827222220000005, 20.21222222)
    Star_Label(r'$\xi$', 6.754833333, 12.89555556)


def Gru():
    _AlpGru = Coordenadas(22.13722222, -46.96111111)
    _BetGru = Coordenadas(22.71113889, -46.88472222)
    _GamGru = Coordenadas(21.89880556, -37.365)
    _EpsGru = Coordenadas(22.80925, -51.31694444)
    _IotGru = Coordenadas(23.17266667, -45.24666667)
    _Del1Gru = Coordenadas(22.48783333, -43.49555556)
    #_Del2Gru = Coordenadas(22.49597222, -43.74944444)
    _ZetGru = Coordenadas(23.01466667, -52.75416667)
    #_TheGru = Coordenadas(23.11466667, -43.52055556)
    _LamGru = Coordenadas(22.10191667, -39.54333333)
    _Mu1Gru = Coordenadas(22.26025, -41.34666667)
    """
    _EtaGru = Coordenadas(22.76052778, -53.50027778)
    _RhoGru = Coordenadas(22.725, -41.41444444)
    _Mu2Gru = Coordenadas(22.27405556, -41.6275)
    _XiGru = Coordenadas(21.53497222, -41.17916667)
    _KapGru = Coordenadas(23.07766667, -53.965)
    _NuGru = Coordenadas(22.47755556, -39.13194444)
    _OmiGru = Coordenadas(23.4435, -52.72166667)
    _PhiGru = Coordenadas(23.30275, -40.82444444)
    _UpsGru = Coordenadas(23.11488889, -38.89222222)
    _Pi2Gru = Coordenadas(22.38555556, -45.92861111)
    _Tau3Gru = Coordenadas(22.94661111, -47.96916667)
    _Sig2Gru = Coordenadas(22.61633333, -40.59111111)
    _Tau1Gru = Coordenadas(22.89386111, -48.59805556)
    _Sig1Gru = Coordenadas(22.60813889, -40.58277778)
    _Pi1Gru = Coordenadas(22.37886111, -45.94777778)
    """

    Line(_ZetGru, _EpsGru)
    Line(_EpsGru, _BetGru)
    Line(_BetGru, _AlpGru)
    Line(_AlpGru, _Del1Gru)
    Line(_Del1Gru, _Mu1Gru)
    Line(_Mu1Gru, _LamGru)
    Line(_LamGru, _GamGru)
    Line(_BetGru, _IotGru)
    Line(_IotGru, _Del1Gru)

    Const_Label('Gru', 22.66, -42.5)
    Star_Label(r'$\alpha$', 22.1, -47.5)
    Star_Label(r'$\beta$', 22.66, -47.5)


def Hercules():
    AlphaHerculis = Coordenadas(17.244139, 14.390278)
    BetaHerculis = Coordenadas(16.503667, 21.489722)
    GammaHerculis = Coordenadas(16.365333, 19.153056)
    DeltaHerculis = Coordenadas(17.250528, 24.839167)
    EpsilonHerculis = Coordenadas(17.004833, 30.926389)
    ZetaHerculis = Coordenadas(16.688111, 31.603056)
    EtaHerculis = Coordenadas(16.714944, 38.922222)
    ThetaHerculis = Coordenadas(17.937556, 37.250556)
    IotaHerculis = Coordenadas(17.657750, 46.006389)
    #KappaHerculis = Coordenadas()
    LambdaHerculis = Coordenadas(17.512306, 26.110556)
    MuHerculis = Coordenadas(17.774306, 27.720556)
    #NuHerculis = Coordenadas(17.975056,  30.189444)
    XiHerculis = Coordenadas(17.962750, 29.247778)
    OmicronHerculis = Coordenadas(18.125722, 28.762500)
    PiHerculis = Coordenadas(17.250778, 36.809167)
    RhoHerculis = Coordenadas(17.394722, 37.145833)
    SigmaHerculis = Coordenadas(16.568389, 42.436944)
    TauHerculis = Coordenadas(16.329000, 46.313333)
    #UpsilonHerculis = Coordenadas(16.046639, 46.036667)
    PhiHerculis = Coordenadas(16.146167, 44.935000)
    ChiHerculis = Coordenadas(15.877917, 42.451667)
    #PsiHerculis = Coordenadas()
    OmegaHerculis = Coordenadas(16.423611, 14.033333)

    Line(IotaHerculis, ThetaHerculis)
    Line(ThetaHerculis, RhoHerculis)
    Line(RhoHerculis, PiHerculis)
    Line(PiHerculis, EtaHerculis)
    Line(EtaHerculis, ZetaHerculis)
    Line(ZetaHerculis, EpsilonHerculis)
    Line(EpsilonHerculis, PiHerculis)
    Line(EtaHerculis, SigmaHerculis)
    Line(SigmaHerculis, TauHerculis)
    Line(TauHerculis, PhiHerculis)
    Line(PhiHerculis, ChiHerculis)
    Line(ZetaHerculis, BetaHerculis)
    Line(BetaHerculis, GammaHerculis)
    Line(GammaHerculis, OmegaHerculis)
    Line(EpsilonHerculis, LambdaHerculis)
    Line(DeltaHerculis, LambdaHerculis)
    Line(LambdaHerculis, MuHerculis)
    Line(MuHerculis, XiHerculis)
    Line(XiHerculis, OmicronHerculis)
    Line(DeltaHerculis, AlphaHerculis)

    Const_Label('Her', 16.9, 33)
    Star_Label(r'$\alpha$', 17.24, 13.1)
    Star_Label(r'$\beta$', 16.58, 21.5)
    Star_Label(r'$\delta$', 17.2, 24.83)
    Star_Label(r'$\gamma$', 16.31, 19.15)
    Star_Label(r'$\zeta$', 16.58, 31)
    Star_Label(r'$\epsilon$', 17, 30)
    Star_Label(r'$\eta$', 16.75, 39)
    Star_Label(r'$\pi$', 17.25, 37)
    Star_Label(r'$\theta$', 17.93, 36)


def Hor():
    _AlpHor = Coordenadas(4.233361111000001, -42.29444444)
    #_DelHor = Coordenadas(4.180722222, -41.99361111)
    _BetHor = Coordenadas(2.9799444439999996, -64.07138889)
    _MuHor = Coordenadas(3.0602222219999997, -59.73777778)
    _ZetHor = Coordenadas(2.677666667, -54.55)
    #_NuHor = Coordenadas(2.8170833330000002, -62.80666667)
    _EtaHor = Coordenadas(2.623444444, -52.54305556)
    #_LamHor = Coordenadas(2.414972222, -60.31194444)
    _IotHor = Coordenadas(2.7093055560000003, -50.80027778)
    #_GamHor = Coordenadas(2.757638889, -63.70444444)

    Line(_AlpHor, _IotHor)
    Line(_IotHor, _EtaHor)
    Line(_EtaHor, _ZetHor)
    Line(_ZetHor, _MuHor)
    Line(_MuHor, _BetHor)

    Const_Label('Hor', 3.5, -50)
    Star_Label(r'$\alpha$', 4.33, -42)


def HyaSouth():

    _30AlpHya = Coordenadas(9.459777778, -8.658611111)
    _46GamHya = Coordenadas(13.31536111, -23.17166667)
    _NuHya = Coordenadas(10.82708333, -16.19361111)
    #_16ZetHya = Coordenadas(8.923222222, 5.945555556)
    _49PiHya = Coordenadas(14.10619444, -26.6825)
    #_11EpsHya = Coordenadas(8.779611111, 6.418888889)
    _XiHya = Coordenadas(11.55002778, -31.85777778)
    _41LamHya = Coordenadas(10.17647222, -12.35416667)
    _42MuHya = Coordenadas(10.43483333, -16.83638889)
    #_22TheHya = Coordenadas(9.239416667, 2.314166667)
    _35IotHya = Coordenadas(9.664277777999999, -1.142777778)
    _39Ups1Hya = Coordenadas(9.857972222, -14.84666667)
    #_4DelHya = Coordenadas(8.627611111, 5.703611111)
    _BetHya = Coordenadas(11.88183333, -33.90805556)
    #_7EtaHya = Coordenadas(8.720416667, 3.398611111)
    #_12Hya = Coordenadas(8.772916667, -13.54777778)
    #_13RhoHya = Coordenadas(8.807222222, 5.8377777779999995)
    #_58Hya = Coordenadas(14.83813889, -27.96027778)
    #_5SigHya = Coordenadas(8.645944444, 3.3413888889999996)
    #_32Tau2Hya = Coordenadas(9.533027778, -1.185)
    #_31Tau1Hya = Coordenadas(9.485805556, -2.768888889)
    _40Ups2Hya = Coordenadas(10.08541667, -13.06472222)
    #_OmiHya = Coordenadas(11.67022222, -34.74472222)
    _51Hya = Coordenadas(14.38494444, -27.75388889)

    Line(_51Hya, _49PiHya)
    Line(_49PiHya, _46GamHya)
    Line(_46GamHya, _BetHya)
    Line(_BetHya, _XiHya)
    Line(_XiHya, _NuHya)
    Line(_NuHya, _42MuHya)
    Line(_42MuHya, _41LamHya)
    Line(_41LamHya, _40Ups2Hya)
    Line(_40Ups2Hya, _39Ups1Hya)
    Line(_39Ups1Hya, _30AlpHya)
    Line(_30AlpHya, _35IotHya)

    Const_Label('Hya', 12, -33)
    Star_Label(r'$\alpha$', 9.46, -8.7)
    Star_Label(r'$\beta$', 11.88183333, -33.90805556)
    Star_Label(r'$\gamma$', 13.31536111, -23.17166667)
    Star_Label(r'$51$', 14.38494444, -27.75388889)
    Star_Label(r'$\iota$', 9.664277777999999, -1.142777778)
    Star_Label(r'$\lambda$', 10.17647222, -12.35416667)
    Star_Label(r'$\mu$', 10.43483333, -16.83638889)
    Star_Label(r'$\nu$', 10.82708333, -16.19361111)
    Star_Label(r'$\xi$', 11.55002778, -31.85777778)
    Star_Label(r'$\pi$', 14.10619444, -26.6825)


def HyaNorth():
    #_30AlpHya = Coordenadas(9.459777778, -8.658611111)
    #_46GamHya = Coordenadas(13.31536111, -23.17166667)
    #_NuHya = Coordenadas(10.82708333, -16.19361111)
    _16ZetHya = Coordenadas(8.923222222, 5.945555556)
    #_49PiHya = Coordenadas(14.10619444, -26.6825)
    _11EpsHya = Coordenadas(8.779611111, 6.418888889)
    #_XiHya = Coordenadas(11.55002778, -31.85777778)
    #_41LamHya = Coordenadas(10.17647222, -12.35416667)
    #_42MuHya = Coordenadas(10.43483333, -16.83638889)
    _22TheHya = Coordenadas(9.239416667, 2.314166667)
    _35IotHya = Coordenadas(9.664277777999999, 0)  # dec rebatida
    #_39Ups1Hya = Coordenadas(9.857972222, -14.84666667)
    _4DelHya = Coordenadas(8.627611111, 5.703611111)
    #_BetHya = Coordenadas(11.88183333, -33.90805556)
    _7EtaHya = Coordenadas(8.720416667, 3.398611111)
    #_12Hya = Coordenadas(8.772916667, -13.54777778)
    _13RhoHya = Coordenadas(8.807222222, 5.8377777779999995)
    #_58Hya = Coordenadas(14.83813889, -27.96027778)
    _5SigHya = Coordenadas(8.645944444, 3.3413888889999996)
    #_32Tau2Hya = Coordenadas(9.533027778, -1.185)
    #_31Tau1Hya = Coordenadas(9.485805556, -2.768888889)
    #_40Ups2Hya = Coordenadas(10.08541667, -13.06472222)
    #_OmiHya = Coordenadas(11.67022222, -34.74472222)
    #_51Hya = Coordenadas(14.38494444, -27.75388889)

    Line(_35IotHya, _22TheHya)
    Line(_22TheHya, _16ZetHya)
    Line(_16ZetHya, _11EpsHya)
    Line(_11EpsHya, _4DelHya)
    Line(_4DelHya, _5SigHya)
    Line(_5SigHya, _7EtaHya)
    Line(_7EtaHya, _13RhoHya)
    Line(_13RhoHya, _11EpsHya)

    Const_Label('Hya', 9, 5)


def Hyi():
    _BetHyi = Coordenadas(0.4291944444, -77.25416667)
    _AlpHyi = Coordenadas(1.9795, -61.56972222)
    _GamHyi = Coordenadas(3.787305556, -74.23888889)
    #_DelHyi = Coordenadas(2.362472222, -68.65944444)
    #_EpsHyi = Coordenadas(2.659833333, -68.26694444)
    _Eta2Hyi = Coordenadas(1.915583333, -67.64722222)
    _MuHyi = Coordenadas(2.527916667, -79.10944444)
    #_NuHyi = Coordenadas(2.84125, -75.06694444)

    Line(_BetHyi, _MuHyi)
    Line(_MuHyi, _GamHyi)
    Line(_GamHyi, _Eta2Hyi)
    Line(_Eta2Hyi, _AlpHyi)

    Const_Label('Hyi', 2.33, -72.5)
    Star_Label(r'$\alpha$', 1.83, -67.5)
    Star_Label(r'$\beta$', 0.96, -77.5)
    Star_Label(r'$\gamma$', 3.83, -73.2)


def Ind():
    _AlpInd = Coordenadas(20.62611111, -47.29138889)
    _BetInd = Coordenadas(20.9135, -58.45416667)
    _TheInd = Coordenadas(21.33111111, -53.44972222)
    _DelInd = Coordenadas(21.96530556, -54.9925)
    _EtaInd = Coordenadas(20.73397222, -51.92111111)

    Line(_AlpInd, _TheInd)
    Line(_TheInd, _DelInd)
    Line(_DelInd, _BetInd)
    Line(_BetInd, _EtaInd)
    Line(_EtaInd, _AlpInd)

    Const_Label('Ind', 21.33, -55)
    Star_Label(r'$\alpha$', 20.66, -47)


def Lac():
    _7AlpLac = Coordenadas(22.52152778, 50.2825)
    _1Lac = Coordenadas(22.26616667, 37.74888889)
    _5Lac = Coordenadas(22.49216667, 47.70694444)
    _3BetLac = Coordenadas(22.39266667, 52.22916667)
    _11Lac = Coordenadas(22.67525, 44.27638889)
    #_6Lac = Coordenadas(22.50813889, 43.12333333)
    _2Lac = Coordenadas(22.35044444, 46.53666667)
    _4Lac = Coordenadas(22.40861111, 49.47638889)

    Line(_3BetLac, _7AlpLac)
    Line(_7AlpLac, _4Lac)
    Line(_4Lac, _5Lac)
    Line(_5Lac, _2Lac)
    Line(_2Lac, _11Lac)
    Line(_11Lac, _1Lac)

    Const_Label('Lac', 22.5, 45)
    Star_Label(r'$1$', 22.26616667, 37.74888889)
    Star_Label(r'$11$', 22.67525, 44.27638889)
    Star_Label(r'$2$', 22.35044444, 46.53666667)
    Star_Label(r'$4$', 22.40861111, 49.47638889)
    Star_Label(r'$5$', 22.49216667, 47.70694444)
    Star_Label(r'$\alpha$', 22.52152778, 50.2825)
    Star_Label(r'$\beta$', 22.39266667, 52.22916667)


def Leo():
    _32AlpLeo = Coordenadas(10.13952778, 11.96722222)
    _94BetLeo = Coordenadas(11.81766667, 14.57194444)
    _68DelLeo = Coordenadas(11.23513889, 20.52361111)
    _41Gam1Leo = Coordenadas(10.33286111, 19.84166667)
    _17EpsLeo = Coordenadas(9.764194444, 23.77416667)
    _70TheLeo = Coordenadas(11.23733333, 15.42944444)
    _36ZetLeo = Coordenadas(10.27816667, 23.41722222)
    _30EtaLeo = Coordenadas(10.12222222, 16.76277778)
    _14OmiLeo = Coordenadas(9.685833333, 9.892222222000001)
    #_41Gam2Leo = Coordenadas(10.33294444, 19.84055556)
    #_47RhoLeo = Coordenadas(10.54686111, 9.306666667)
    _24MuLeo = Coordenadas(9.879388889, 26.00694444)

    """
    _78IotLeo = Coordenadas(11.39875, 10.52916667)
    _77SigLeo = Coordenadas(11.35227778, 6.029444444)
    _91UpsLeo = Coordenadas(11.61580556, 0.8238888889)
    _4LamLeo = Coordenadas(9.528666667000001, 22.96805556)
    _31Leo = Coordenadas(10.13175, 9.9975)
    _60Leo = Coordenadas(11.03883333, 20.17972222)
    _1KapLeo = Coordenadas(9.410916667, 26.18222222)
    _74PhiLeo = Coordenadas(11.27769444, -3.6516666669999998)
    _54Leo = Coordenadas(10.92688889, 24.74972222)
    _93Leo = Coordenadas(11.79975, 20.21888889)
    _72Leo = Coordenadas(11.25338889, 23.09555556)
    _63ChiLeo = Coordenadas(11.08361111, 7.336111111)
    _29PiLeo = Coordenadas(10.00355556, 8.044166667)
    _61Leo = Coordenadas(11.03047222, -2.484722222)
    _87Leo = Coordenadas(11.50525, -3.003611111)
    _40Leo = Coordenadas(10.32891667, 19.47083333)
    _58Leo = Coordenadas(11.00933333, 3.6175)
    _84TauLeo = Coordenadas(11.46561111, 2.856111111)
    _5XiLeo = Coordenadas(9.532416667, 11.29972222)
    """

    Line(_94BetLeo, _68DelLeo)
    Line(_68DelLeo, _70TheLeo)
    Line(_70TheLeo, _94BetLeo)
    Line(_68DelLeo, _30EtaLeo)
    Line(_41Gam1Leo, _30EtaLeo)
    Line(_30EtaLeo, _32AlpLeo)
    Line(_32AlpLeo, _70TheLeo)
    Line(_41Gam1Leo, _36ZetLeo)
    Line(_36ZetLeo, _24MuLeo)
    Line(_24MuLeo, _17EpsLeo)
    Line(_32AlpLeo, _14OmiLeo)
    #Line(,)

    Const_Label('Leo', 10.66, 18)
    Star_Label(r'$\alpha$', 10.12, 13)
    Star_Label(r'$\beta$', 11.81, 15)
    Star_Label(r'$\gamma$', 10.28, 20)
    Star_Label(r'$\delta$', 11.23513889, 20.52361111)
    Star_Label(r'$\epsilon$', 9.764194444, 23.77416667)
    Star_Label(r'$\zeta$', 10.27816667, 23.41722222)
    Star_Label(r'$\eta$', 10.12222222, 16.76277778)
    Star_Label(r'$\theta$', 11.23733333, 15.42944444)
    Star_Label(r'$\iota$', 11.39875, 10.52916667)
    Star_Label(r'$\kappa$', 9.410916667, 26.18222222)
    Star_Label(r'$\lambda$', 9.528666667000001, 22.96805556)
    Star_Label(r'$\mu$', 9.879388889, 26.00694444)
    Star_Label(r'$o$', 9.685833333, 9.892222222000001)
    Star_Label(r'$\rho$', 10.54686111, 9.306666667)


def Lep():
    _11AlpLep = Coordenadas(5.5455, -17.82222222)
    _9BetLep = Coordenadas(5.47075, -20.75944444)
    _2EpsLep = Coordenadas(5.091027778, -22.37111111)
    _5MuLep = Coordenadas(5.215527778, -16.20555556)
    _14ZetLep = Coordenadas(5.782583333, -14.82194444)
    _13GamLep = Coordenadas(5.741055556, -22.44833333)
    _16EtaLep = Coordenadas(5.940083333, -14.16777778)
    _15DelLep = Coordenadas(5.855361111000001, -20.87916667)
    _6LamLep = Coordenadas(5.32625, -13.17666667)
    _4KapLep = Coordenadas(5.220527778, -12.94138889)
    #_3IotLep = Coordenadas(5.204972222, -11.86916667)
    _18TheLep = Coordenadas(6.102583332999999, -14.93527778)
    """
    _17Lep = Coordenadas(6.083083332999999, -16.48444444)
    _8Lep = Coordenadas(5.391722222, -13.92722222)
    _7NuLep = Coordenadas(5.333083333, -12.31555556)
    _19Lep = Coordenadas(6.128222222000001, -19.16583333)
    _10Lep = Coordenadas(5.518777778, -20.86361111)
    _1Lep = Coordenadas(5.045805556, -22.795)
    _12Lep = Coordenadas(5.703861111, -22.37361111)
    """

    Line(_11AlpLep, _9BetLep)
    Line(_9BetLep, _13GamLep)
    Line(_13GamLep, _15DelLep)
    Line(_15DelLep, _18TheLep)
    Line(_18TheLep, _16EtaLep)
    Line(_16EtaLep, _14ZetLep)
    Line(_14ZetLep, _11AlpLep)
    Line(_11AlpLep, _5MuLep)
    Line(_5MuLep, _2EpsLep)
    Line(_2EpsLep, _9BetLep)
    Line(_5MuLep, _6LamLep)
    Line(_5MuLep, _4KapLep)

    Const_Label('Lep', 5.66, -18)
    Star_Label(r'$\alpha$', 5.5155, -17.82222222)
    Star_Label(r'$\beta$', 5.44075, -20.75944444)
    Star_Label(r'$\gamma$', 5.701055556, -22.44833333)
    Star_Label(r'$\delta$', 5.855361111000001, -20.87916667)
    Star_Label(r'$\epsilon$', 5.091027778, -22.37111111)
    Star_Label(r'$\zeta$', 5.782583333, -14.82194444)
    Star_Label(r'$\eta$', 5.940083333, -14.16777778)
    Star_Label(r'$\theta$', 6.102583332999999, -14.93527778)
    Star_Label(r'$\iota$', 5.204972222, -11.86916667)
    Star_Label(r'$\kappa$', 5.220527778, -12.94138889)
    Star_Label(r'$\lambda$', 5.32625, -13.17666667)
    Star_Label(r'$\mu$', 5.215527778, -16.20555556)


def Libra():
    AlphaLibrae = Coordenadas(14.84, -16.04)
    BetaLibrae = Coordenadas(15.28, -9.38)
    GammaLibrae = Coordenadas(15.59, -14.79)
    SigmaLibrae = Coordenadas(15.07, -25.28)

    Line(AlphaLibrae, SigmaLibrae)
    Line(AlphaLibrae, BetaLibrae)
    Line(GammaLibrae, BetaLibrae)

    Const_Label('Lib', 15.16, 17.5)
    Star_Label(r'$\alpha$', 14.84, -16.04)
    Star_Label(r'$\beta$', 15.28, -9.38)
    Star_Label(r'$\gamma$', 15.59, -14.79)
    Star_Label(r'$\delta$', 15.07, -25.28)


def LMi():
    _46LMi = Coordenadas(10.88852778, 34.215)
    _31BetLMi = Coordenadas(10.46472222, 36.70722222)
    _21LMi = Coordenadas(10.12383333, 35.24472222)
    #_10LMi = Coordenadas(9.570388889, 36.3975)
    #_37LMi = Coordenadas(10.64533333, 31.97611111)
    #_30LMi = Coordenadas(10.43191667, 33.79611111)

    Line(_21LMi, _31BetLMi)
    Line(_31BetLMi, _46LMi)

    Const_Label('LMi', 10.66, 34)
    Star_Label(r'$46$', 10.88852778, 34.215)
    Star_Label(r'$\beta$', 10.46472222, 36.70722222)
    Star_Label(r'$21$', 10.12383333, 35.24472222)


def Lup():
    _AlpLup = Coordenadas(14.69883333, -47.38833333)
    _BetLup = Coordenadas(14.97552778, -43.13388889)
    _GamLup = Coordenadas(15.58569444, -41.16694444)
    _DelLup = Coordenadas(15.35619444, -40.6475)
    _EpsLup = Coordenadas(15.37802778, -44.68944444)
    _EtaLup = Coordenadas(16.00202778, -38.39694444)
    _ZetLup = Coordenadas(15.20475, -52.09916667)
    _Phi1Lup = Coordenadas(15.36344444, -36.26138889)
    _5ChiLup = Coordenadas(15.84930556, -33.62722222)

    Line(_AlpLup, _ZetLup)
    Line(_ZetLup, _EpsLup)
    Line(_EpsLup, _GamLup)
    Line(_GamLup, _EtaLup)
    Line(_EtaLup, _ZetLup)
    Line(_GamLup, _DelLup)
    Line(_DelLup, _BetLup)
    Line(_EtaLup, _Phi1Lup)
    Line(_Phi1Lup, _5ChiLup)
    Line(_5ChiLup, _EtaLup)

    Const_Label('Lup', 15.83, 43)
    Star_Label(r'$\alpha$', 14.69883333, -47.38833333)
    Star_Label(r'$\beta$', 14.97552778, -43.13388889)
    Star_Label(r'$\gamma$', 15.58569444, -41.16694444)
    Star_Label(r'$\delta$', 15.35619444, -40.6475)
    Star_Label(r'$\epsilon$', 15.37802778, -44.68944444)
    Star_Label(r'$\zeta$', 15.20475, -52.09916667)
    Star_Label(r'$\eta$', 16.00202778, -38.39694444)
    Star_Label(r'$\theta$', 16.10986111, -36.80222222)
    Star_Label(r'$\iota$', 14.32338889, -46.05777778)
    Star_Label(r'$\kappa$', 15.19891667, -48.73777778)
    Star_Label(r'$\lambda$', 15.14738889, -45.27972222)
    Star_Label(r'$\mu$', 15.30888889, -47.875)
    Star_Label(r'$\phi^1$', 15.36344444, -36.26138889)
    Star_Label(r'$\phi^2$', 15.38594444, -36.85861111)
    Star_Label(r'$\chi$', 15.84930556, -33.62722222)


def Lyn():
    _40AlpLyn = Coordenadas(9.350916667, 34.3925)
    _38Lyn = Coordenadas(9.314083333, 36.8025)
    _31Lyn = Coordenadas(8.380583332999999, 43.18805556)
    _15Lyn = Coordenadas(6.9545833329999995, 58.4225)
    _2Lyn = Coordenadas(6.327055556, 59.01083333)
    _21Lyn = Coordenadas(7.445222222000001, 49.21138889)
    _27Lyn = Coordenadas(8.140944444, 51.50666667)

    Line(_40AlpLyn, _38Lyn)
    Line(_38Lyn, _31Lyn)
    Line(_31Lyn, _27Lyn)
    Line(_27Lyn, _21Lyn)
    Line(_21Lyn, _15Lyn)
    Line(_15Lyn, _2Lyn)

    Const_Label('Lyn', 8, 48)
    Star_Label(r'$\alpha$', 9.35, 34.5)


def Lyra():
    AlphaLyrae = Coordenadas(18.615639, 38.783611)
    BetaLyrae = Coordenadas(18.834667, 33.362778)
    GammaLyrae = Coordenadas(18.982389, 32.689444)
    DeltaLyrae = Coordenadas(18.908389, 36.898889)
    #EpsilonLyrae = Coordenadas(18.739694, 39.613056)
    ZetaLyrae = Coordenadas(18.746222, 37.605000)

    Line(AlphaLyrae, ZetaLyrae)
    Line(ZetaLyrae, BetaLyrae)
    Line(ZetaLyrae, DeltaLyrae)
    Line(GammaLyrae, BetaLyrae)
    Line(GammaLyrae, DeltaLyrae)

    Const_Label('Lyr', 18.66, 35)
    Star_Label(r'$\alpha$', 18.6, 39.5)
    Star_Label(r'$\beta$', 18.73, 32.5)
    Star_Label(r'$\gamma$', 19.02, 32.7)
    Star_Label(r'$\delta$', 18.9, 37.1)
    Star_Label(r'$\zeta$', 18.7, 37.95)
    Star_Label(r'$\epsilon$', 18.75, 40)


def Men():
    Const_Label('Men', 5.5, -75)


def Mic():
    Const_Label('Mic', 21, -40)


def Mon():
    _26AlpMon = Coordenadas(7.687444444, -9.551111111)
    _5GamMon = Coordenadas(6.247583333, -6.274722222)
    _22DelMon = Coordenadas(7.19775, -0.49277777780000004)
    _29ZetMon = Coordenadas(8.143222222, -2.9838888889999997)
    _11BetMon = Coordenadas(6.480277778, -7.032777778)

    Line(_26AlpMon, _29ZetMon)
    Line(_29ZetMon, _22DelMon)
    Line(_22DelMon, _11BetMon)
    Line(_11BetMon, _5GamMon)

    Const_Label('Mon', 7.5, -5)
    Star_Label(r'$\alpha$', 7.687444444, -9.551111111)
    Star_Label(r'$\beta$', 6.480277778, -7.032777778)
    Star_Label(r'$\gamma$', 6.247583333, -6.274722222)
    Star_Label(r'$\delta$', 7.19775, -0.49277777780000004)
    Star_Label(r'$\zeta$', 8.143222222, -2.9838888889999997)


def Musca():
    AlphaMuscae = Coordenadas(12.62, -69.13)
    BetaMuscae = Coordenadas(12.77, -68.10)
    GammaMuscae = Coordenadas(12.54, -72.13)
    DeltaMuscae = Coordenadas(13.03, -71.55)
    EpsilonMuscae = Coordenadas(12.29, -67.96)
    LambdaMuscae = Coordenadas(11.76, -66.73)
    #Alpha-Beta
    Line(AlphaMuscae, BetaMuscae)
    #Beta-Delta
    Line(BetaMuscae, DeltaMuscae)
    #Delta-Gamma
    Line(DeltaMuscae, GammaMuscae)
    #Gamma-Alpha
    Line(GammaMuscae, AlphaMuscae)
    #Alpha-Epsilon
    Line(AlphaMuscae, EpsilonMuscae)
    #Epsilon-Lambda
    Line(EpsilonMuscae, LambdaMuscae)

    Const_Label('Mus', 12.33, -70)


def Nor():
    _Gam2Nor = Coordenadas(16.33066667, -50.15555556)
    _EpsNor = Coordenadas(16.45308333, -47.555)
    #_Iot1Nor = Coordenadas(16.05886111, -57.77527778)
    _EtaNor = Coordenadas(16.05358333, -49.22972222)
    _DelNor = Coordenadas(16.10816667, -45.17333333)

    Line(_Gam2Nor, _EpsNor)
    Line(_EpsNor, _DelNor)
    Line(_DelNor, _EtaNor)
    Line(_EtaNor, _Gam2Nor)

    Const_Label('Nor', 16.25, 48)


def Oct():
    _NuOct = Coordenadas(21.69125, -77.39)
    _BetOct = Coordenadas(22.76758333, -81.38166667)
    _DelOct = Coordenadas(14.44858333, -83.66777778)
    #_TheOct = Coordenadas(0.02658333333, -77.06583333)
    #_EpsOct = Coordenadas(22.33375, -80.43972222)
    #_Gam1Oct = Coordenadas(23.86844444, -82.01888889)
    #_AlpOct = Coordenadas(21.07861111, -77.02388889)

    Line(_NuOct, _BetOct)
    Line(_BetOct, _DelOct)
    Line(_DelOct, _NuOct)

    Const_Label('Oct', 21.5, -85)
    Star_Label(r'$\alpha$', 21.07861111, -77.02388889)
    Star_Label(r'$\beta$', 22.76758333, -81.38166667)
    Star_Label(r'$\gamma$', 23.86844444, -82.01888889)
    Star_Label(r'$\delta$', 14.44858333, -83.66777778)
    Star_Label(r'$\epsilon$', 22.33375, -80.43972222)
    Star_Label(r'$\zeta$', 0.02658333333, -77.06583333)
    Star_Label(r'$\nu$', 21.69125, -77.39)


def Oph():
    _55AlpOph = Coordenadas(17.58225, 12.56)
    _60BetOph = Coordenadas(17.72455556, 4.567222222)
    _27KapOph = Coordenadas(16.96113889, 9.375)
    _62GamOph = Coordenadas(17.79822222, 2.707222222)
    _10LamOph = Coordenadas(16.51522222, 1.9838888890000002)

    Line(Coordenadas(16.396, 0), _10LamOph)
    Line(_10LamOph, _27KapOph)
    Line(_27KapOph, _55AlpOph)
    Line(_55AlpOph, _60BetOph)
    Line(_60BetOph, _62GamOph)
    Line(_62GamOph, Coordenadas(17.69, 0))

    Const_Label('Oph', 17.33, 5)


def OphSouth():
    _35EtaOph = Coordenadas(17.17297222, -15.72472222)
    _13ZetOph = Coordenadas(16.61930556, -10.56722222)
    _1DelOph = Coordenadas(16.23908333, -3.6944444439999997)
    _32MuSer = Coordenadas(15.827, -3.430277778)

    Line(_32MuSer, Coordenadas(15.827, 0))
    Line(_32MuSer, _1DelOph)
    Line(Coordenadas(16.396, 0), _1DelOph)
    Line(_1DelOph, _13ZetOph)
    Line(_13ZetOph, _35EtaOph)
    Line(_35EtaOph, Coordenadas(17.69, 0))

    Const_Label('Oph', 17, -10)
    Star_Label(r'$\eta$', 17.2, -16)
    Star_Label(r'$\zeta$', 16.66, -10.2)
    Star_Label(r'$\delta$', 16.25, -3)


def Ori():
    _19BetOri = Coordenadas(5.242305556, -8.201666667000001)
    #_46EpsOri = Coordenadas(5.603555556, -1.201944444)
    _50ZetOri = Coordenadas(5.679305556, -1.9427777780000002)
    _53KapOri = Coordenadas(5.795944444, -9.669722222)
    _34DelOri = Coordenadas(5.533444444, -0.29916666670000003)

    Line(_19BetOri, _34DelOri)
    Line(_34DelOri, _50ZetOri)
    Line(_50ZetOri, _53KapOri)
    Line(_50ZetOri, Coordenadas(5.7, 0))

    Const_Label('Ori', 5.5, -5)
    Star_Label(r'$\beta$', 5.24, -9)
    Star_Label(r'$\kappa$', 5.8, -9.8)
    Star_Label(r'$\epsilon$', 5.6, -1.35)
    Star_Label(r'$\zeta$', 5.7, -2.1)


def OriNorth():
    _58AlpOri = Coordenadas(5.919527778, 7.406944444)
    _24GamOri = Coordenadas(5.418861111, 6.3497222220000005)
    _1Pi3Ori = Coordenadas(4.830666667, 6.961388889)
    #_28EtaOri = Coordenadas(5.407944444, -2.396944444)
    _39LamOri = Coordenadas(5.585638889, 9.934166667000001)
    #_20TauOri = Coordenadas(5.2934444439999995, -6.844444444)
    _3Pi4Ori = Coordenadas(4.853444444, 5.605)
    _8Pi5Ori = Coordenadas(4.904194444, 2.440555556)
    #_48SigOri = Coordenadas(5.645777777999999, -2.6)
    _9Omi2Ori = Coordenadas(4.939527778, 13.51444444)
    #_40Phi2Ori = Coordenadas(5.615083332999999, 9.290555556000001)
    _61MuOri = Coordenadas(6.039722222000001, 9.6475)
    #_29Ori = Coordenadas(5.399111111, -7.808055556)
    #_32Ori = Coordenadas(5.513083332999999, 5.948055556)
    #_50ZetOri = Coordenadas(5.679333333, -1.9427777780000002)
    _2Pi2Ori = Coordenadas(4.843527778, 8.900277778)
    #_37Phi1Ori = Coordenadas(5.580333333, 9.489444444)
    _54Chi1Ori = Coordenadas(5.906361111, 20.27611111)
    _67NuOri = Coordenadas(6.126194443999999, 14.76833333)
    #_17RhoOri = Coordenadas(5.2215277780000005, 2.861111111)
    _10Pi6Ori = Coordenadas(4.975805556, 1.714166667)
    _70XiOri = Coordenadas(6.199, 14.20888889)
    _62Chi2Ori = Coordenadas(6.065333333, 20.13833333)
    _7Pi1Ori = Coordenadas(4.914944444, 10.15083333)

    Line(Coordenadas(5.7, 0), _58AlpOri)
    Line(_24GamOri, _39LamOri)
    Line(_24GamOri, _58AlpOri)
    Line(_39LamOri, _58AlpOri)
    Line(_24GamOri, _1Pi3Ori)
    Line(_10Pi6Ori, _8Pi5Ori)
    Line(_8Pi5Ori, _3Pi4Ori)
    Line(_3Pi4Ori, _1Pi3Ori)
    Line(_1Pi3Ori, _2Pi2Ori)
    Line(_2Pi2Ori, _7Pi1Ori)
    Line(_7Pi1Ori, _9Omi2Ori)
    Line(_24GamOri, Coordenadas(5.533, 0))
    Line(_58AlpOri, _61MuOri)
    Line(_61MuOri, _70XiOri)
    Line(_70XiOri, _62Chi2Ori)
    Line(_62Chi2Ori, _54Chi1Ori)
    Line(_54Chi1Ori, _67NuOri)
    Line(_67NuOri, _61MuOri)

    Const_Label('Ori', 5.75, 5)
    Star_Label(r'$\alpha$', 5.92, 9)
    Star_Label(r'$\gamma$', 5.42, 7.8)
    Star_Label(r'$\lambda$', 5.61, 11)
    Star_Label(r'$\delta$', 5.53, 1.5)
    Star_Label(r'$\mu$', 6.05, 9)
    Star_Label(r'$\pi^3$', 4.8, 7)
    Star_Label(r'$\pi^4$', 4.82, 5.1)
    Star_Label(r'$\pi^2$', 4.81, 8.9)
    Star_Label(r'$\pi^1$', 4.89, 10.8)


def Pav():
    _AlpPav = Coordenadas(20.42747222, -56.735)
    _BetPav = Coordenadas(20.74930556, -66.20305556)
    _DelPav = Coordenadas(20.14544444, -66.18194444)
    _EtaPav = Coordenadas(17.76222222, -64.72388889)
    _EpsPav = Coordenadas(20.00986111, -72.91055556)
    _ZetPav = Coordenadas(18.71725, -71.42805556)
    _LamPav = Coordenadas(18.87027778, -62.1875)
    _GamPav = Coordenadas(21.44072222, -65.36611111)
    _PiPav = Coordenadas(18.143, -63.66833333)
    _XiPav = Coordenadas(18.38711111, -61.49388889)
    _KapPav = Coordenadas(18.94916667, -67.23361111)

    Line(_AlpPav, _DelPav)
    Line(_DelPav, _BetPav)
    Line(_BetPav, _GamPav)
    Line(_GamPav, _AlpPav)
    Line(_DelPav, _LamPav)
    Line(_LamPav, _XiPav)
    Line(_XiPav, _PiPav)
    Line(_PiPav, _EtaPav)
    Line(_PiPav, _KapPav)
    Line(_KapPav, _DelPav)
    Line(_DelPav, _ZetPav)
    Line(_DelPav, _EpsPav)

    Const_Label('Pav', 19.66, -65)
    Star_Label(r'$\alpha$', 20.33, -56.5)
    Star_Label(r'$\beta$', 20.66, -66)


def Peg():
    AlphaAnd = Coordenadas(0.139806, 29.090556)
    AlphaPegasi = Coordenadas(23.079361, 15.205278)
    BetaPegasi = Coordenadas(23.062917, 28.082778)
    GammaPegasi = Coordenadas(0.220611, 15.183611)
    EpsilonPegasi = Coordenadas(21.736444, 9.875000)
    ZetaPegasi = Coordenadas(22.691028, 10.831389)
    EtaPegasi = Coordenadas(22.716694, 30.221389)
    ThetaPegasi = Coordenadas(22.170000, 6.197778)
    IotaPegasi = Coordenadas(22.116861, 25.345000)
    KappaPegasi = Coordenadas(21.744083, 25.645000)
    LambdaPegasi = Coordenadas(22.775528, 23.565556)
    MuPegasi = Coordenadas(22.833389, 24.601667)
    PiPegasi = Coordenadas(22.166444, 33.178333)

    Line(AlphaPegasi, GammaPegasi)
    Line(AlphaPegasi, BetaPegasi)
    Line(AlphaPegasi, ZetaPegasi)
    Line(GammaPegasi, AlphaAnd)
    Line(BetaPegasi, EtaPegasi)
    Line(BetaPegasi, MuPegasi)
    Line(BetaPegasi, AlphaAnd)
    Line(ZetaPegasi, ThetaPegasi)
    Line(ThetaPegasi, EpsilonPegasi)
    Line(MuPegasi, LambdaPegasi)
    Line(LambdaPegasi, IotaPegasi)
    Line(IotaPegasi, KappaPegasi)
    Line(EtaPegasi, PiPegasi)

    Const_Label('Peg', 23.5, 23)
    Star_Label(r'$\alpha$', 23.07, 14.5)
    Star_Label(r'$\beta$', 23.06, 29.3)
    Star_Label(r'$\gamma$', 0.22, 14.6)
    Star_Label(r'$\epsilon$', 21.66, 10)
    Star_Label(r'$1$', 21.36811111, 19.80444444)
    Star_Label(r'$\zeta$', 22.691028, 10.831389)
    Star_Label(r'$\eta$', 22.716694, 30.221389)
    Star_Label(r'$\theta$', 22.170000, 6.197778)
    Star_Label(r'$\iota$', 22.116861, 25.345000)
    Star_Label(r'$\kappa$', 21.744083, 25.645000)
    Star_Label(r'$\lambda$', 22.775528, 23.565556)
    Star_Label(r'$\mu$', 22.833389, 24.601667)
    Star_Label(r'$\nu$', 22.09466667, 5.058611111)
    Star_Label(r'$\xi$', 22.77822222, 12.17277778)
    Star_Label(r'$o$', 22.69594444, 29.3075)
    Star_Label(r'$\pi$', 22.166444, 33.178333)
    Star_Label(r'$\rho$', 22.92047222, 8.815833332999999)
    Star_Label(r'$\sigma$', 22.87336111, 9.835555556000001)
    Star_Label(r'$51$', 22.95775, 20.76888889)


def Per():
    _33AlpPer = Coordenadas(3.4053888889999997, 49.86111111)
    _26BetPer = Coordenadas(3.1361388889999997, 40.95555556)
    _44ZetPer = Coordenadas(3.9021944439999996, 31.88361111)
    _45EpsPer = Coordenadas(3.964222222, 40.01027778)
    _23GamPer = Coordenadas(3.0799444439999997, 53.50638889)
    _39DelPer = Coordenadas(3.715416667, 47.7875)
    _15EtaPer = Coordenadas(2.844944444, 55.89555556)
    _41NuPer = Coordenadas(3.7532222219999998, 42.57861111)
    _27KapPer = Coordenadas(3.158277778, 44.85722222)

    Line(_15EtaPer, _23GamPer)
    Line(_23GamPer, _33AlpPer)
    Line(_33AlpPer, _39DelPer)
    Line(_39DelPer, _41NuPer)
    Line(_41NuPer, _45EpsPer)
    Line(_45EpsPer, _44ZetPer)
    Line(_33AlpPer, _27KapPer)
    Line(_27KapPer, _26BetPer)

    Const_Label('Per', 3.5, 45)
    Star_Label(r'$\alpha$', 3.4, 51.5)
    Star_Label(r'$\beta$', 3.08, 40.95)
    Star_Label(r'$\gamma$', 3.0799444439999997, 53.50638889)
    Star_Label(r'$\delta$', 3.715416667, 47.7875)
    Star_Label(r'$\epsilon$', 3.964222222, 40.01027778)
    Star_Label(r'$\zeta$', 3.9021944439999996, 31.88361111)
    Star_Label(r'$\eta$', 2.844944444, 55.89555556)
    Star_Label(r'$\kappa$', 3.158277778, 44.85722222)
    Star_Label(r'$\nu$', 3.7532222219999998, 42.57861111)


def Phe():
    AlpPhe = Coordenadas(0.43805555560000004, -42.30611111)
    BetPhe = Coordenadas(1.101388889, -46.71861111)
    GamPhe = Coordenadas(1.47275, -43.31833333)
    EpsPhe = Coordenadas(0.1568611111, -45.7475)
    ZetPhe = Coordenadas(1.13975, -55.24583333)
    #KapPhe = Coordenadas(0.4367222222, -43.68)
    DelPhe = Coordenadas(1.5208611109999999, -49.07277778)

    Line(AlpPhe, BetPhe)
    Line(BetPhe, EpsPhe)
    Line(EpsPhe, AlpPhe)
    Line(BetPhe, GamPhe)
    Line(DelPhe, GamPhe)
    Line(DelPhe, ZetPhe)
    Line(ZetPhe, BetPhe)

    Const_Label('Phe', 1.33, -48)
    Star_Label(r'$\alpha$', 0.42, -42)


def Pic():

    _AlpPic = Coordenadas(6.803166667, -61.94138889)
    _BetPic = Coordenadas(5.788083332999999, -51.06638889)
    _GamPic = Coordenadas(5.830472222, -56.16666667)

    Line(_AlpPic, _GamPic)
    Line(_GamPic, _BetPic)

    Const_Label('Pic', 6, -55)
    Star_Label(r'$\alpha$', 6.66, -62)
    Star_Label(r'$\beta$', 5.73, -51)


def PsA():
    _24AlpPsA = Coordenadas(22.96086111, -29.62222222)
    _18EpsPsA = Coordenadas(22.67761111, -27.04361111)
    _23DelPsA = Coordenadas(22.93247222, -32.53972222)
    _17BetPsA = Coordenadas(22.52508333, -32.34611111)
    _9IotPsA = Coordenadas(21.74911111, -33.02583333)
    _22GamPsA = Coordenadas(22.87544444, -32.87555556)
    _14MuPsA = Coordenadas(22.13972222, -32.98861111)
    #_15TauPsA = Coordenadas(22.16911111, -32.54833333)
    #_UpsPsA = Coordenadas(22.14055556, -34.04388889)
    _10ThePsA = Coordenadas(21.79561111, -30.89833333)

    Line(_24AlpPsA, _18EpsPsA)
    Line(_18EpsPsA, _14MuPsA)
    Line(_14MuPsA, _17BetPsA)
    Line(_17BetPsA, _22GamPsA)
    Line(_22GamPsA, _23DelPsA)
    Line(_23DelPsA, _24AlpPsA)
    Line(_14MuPsA, _10ThePsA)
    Line(_10ThePsA, _9IotPsA)
    Line(_9IotPsA, _14MuPsA)

    Const_Label('PsA', 22.66, -30)
    Star_Label(r'$\alpha$', 23, -31)


def Psc():
    _99EtaPsc = Coordenadas(1.5247222219999998, 15.34583333)
    _6GamPsc = Coordenadas(23.28608333, 3.2822222219999997)
    _28OmePsc = Coordenadas(23.98852778, 6.863333333)
    _17IotPsc = Coordenadas(23.66583333, 5.626388888999999)
    _10OmiPsc = Coordenadas(1.756555556, 9.157777778)
    _10ThePsc = Coordenadas(23.46613889, 6.378888889)
    _71EpsPsc = Coordenadas(1.049055556, 7.89)
    _13AlpPsc = Coordenadas(2.034111111, 2.7636111110000003)
    _63DelPsc = Coordenadas(0.8113888889, 7.585)
    _06NuPsc = Coordenadas(1.690527778, 5.4875)
    _18LamPsc = Coordenadas(23.70077778, 1.78)
    _83TauPsc = Coordenadas(1.1943333329999999, 30.08972222)
    _85PhiPsc = Coordenadas(1.2291388890000001, 24.58361111)
    _90UpsPsc = Coordenadas(1.324444444, 27.26416667)
    _98MuPsc = Coordenadas(1.5030833330000002, 6.143888888999999)
    _8KapPsc = Coordenadas(23.44888889, 1.255555556)

    Line(_6GamPsc, _8KapPsc)
    Line(_8KapPsc, _18LamPsc)
    Line(_18LamPsc, _17IotPsc)
    Line(_17IotPsc, _10ThePsc)
    Line(_10ThePsc, _6GamPsc)
    Line(_17IotPsc, _28OmePsc)
    Line(_28OmePsc, _63DelPsc)
    Line(_63DelPsc, _71EpsPsc)
    Line(_71EpsPsc, _98MuPsc)
    Line(_98MuPsc, _06NuPsc)
    Line(_06NuPsc, _13AlpPsc)
    Line(_13AlpPsc, _10OmiPsc)
    Line(_10OmiPsc, _99EtaPsc)
    Line(_99EtaPsc, _85PhiPsc)
    Line(_85PhiPsc, _83TauPsc)
    Line(_83TauPsc, _90UpsPsc)
    Line(_90UpsPsc, _85PhiPsc)

    Const_Label('Psc', 0, 5)
    Star_Label(r'$\eta$', 1.5247222219999998, 15.34583333)
    Star_Label(r'$\gamma$', 23.28608333, 3.2822222219999997)
    Star_Label(r'$\omega$', 23.98852778, 6.863333333)
    Star_Label(r'$\iota$', 23.66583333, 5.626388888999999)
    Star_Label(r'$o$', 1.756555556, 9.157777778)
    Star_Label(r'$\theta$', 23.46613889, 6.378888889)
    Star_Label(r'$\epsilon$', 1.049055556, 7.89)
    Star_Label(r'$\alpha$', 2.034111111, 2.7636111110000003)


def Pup():
    _AlpCar = Coordenadas(6.399194444, -52.69583333)
    _ChiCar = Coordenadas(7.946305556, -52.98222222)
    _ZetPup = Coordenadas(8.05975, -40.00333333)
    _PiPup = Coordenadas(7.285722222, -37.0975)
    _15RhoPup = Coordenadas(8.125722222, -24.30416667)
    #_TauPup = Coordenadas(6.832277778, -50.61472222)
    _NuPup = Coordenadas(6.629361111000001, -43.19611111)
    #_SigPup = Coordenadas(7.487166667, -43.30138889)
    _7XiPup = Coordenadas(7.8215833329999995, -24.85972222)
    #_3Pup = Coordenadas(7.730138889, -28.95472222)
    #_11Pup = Coordenadas(7.947638888999999, -22.88)
    #_16Pup = Coordenadas(8.150444444, -19.245)
    #_OmiPup = Coordenadas(7.8014444439999995, -25.93722222)

    Line(_NuPup, _PiPup)
    Line(_PiPup, _7XiPup)
    Line(_7XiPup, _15RhoPup)
    Line(_15RhoPup, _ZetPup)
    Line(_ZetPup, _ChiCar)
    Line(_AlpCar, _NuPup)

    Const_Label('Pup', 7, -45)
    Star_Label(r'$\zeta$', 8.05975, -40.00333333)
    Star_Label(r'$\pi$', 7.285722222, -37.0975)
    Star_Label(r'$\rho$', 8.125722222, -24.30416667)
    Star_Label(r'$\nu$', 6.629361111000001, -43.19611111)
    Star_Label(r'$\xi$', 7.8215833329999995, -24.85972222)


def Pyx():
    _AlpPyx = Coordenadas(8.726527778, -33.18638889)
    _BetPyx = Coordenadas(8.668388889, -35.30833333)
    _GamPyx = Coordenadas(8.842194444, -27.71)

    Line(_GamPyx, _AlpPyx)
    Line(_AlpPyx, _BetPyx)

    Const_Label('Pyx', 8.83, -31)
    Star_Label(r'$\alpha$', 8.66, -32.6)


def Ret():
    _AlpRet = Coordenadas(4.240416667, -62.47388889)
    _BetRet = Coordenadas(3.7366666669999997, -64.80694444)
    _EpsRet = Coordenadas(4.274694444, -59.30194444)
    #_GamRet = Coordenadas(4.014944444, -62.15944444)
    _DelRet = Coordenadas(3.979083333, -61.40027778)
    #_KapRet = Coordenadas(3.4896388889999996, -62.9375)
    #_IotRet = Coordenadas(4.021722222, -61.07888889)

    Line(_AlpRet, _BetRet)
    Line(_BetRet, _DelRet)
    Line(_DelRet, _EpsRet)
    Line(_EpsRet, _AlpRet)

    Const_Label('Ret', 4, -60)
    Star_Label(r'$\alpha$', 4.18, -63)


def Scl():
    _AlpScl = Coordenadas(0.9767777778, -29.3575)
    _BetScl = Coordenadas(23.54952778, -37.81833333)
    _GamScl = Coordenadas(23.31372222, -32.53194444)
    _DelScl = Coordenadas(23.81544444, -28.13027778)
    #_EtaScl = Coordenadas(0.4654722222, -33.00722222)
    #_ZetScl = Coordenadas(0.03886111111, -29.72027778)
    _IotScl = Coordenadas(0.3586666667, -28.98166667)

    Line(_AlpScl, _IotScl)
    Line(_IotScl, _DelScl)
    Line(_DelScl, _GamScl)
    Line(_GamScl, _BetScl)

    Const_Label('Scl', 0, -31)
    Star_Label(r'$\alpha$', 1, -28.5)
    Star_Label(r'$\beta$', 23.5, -38)


def Sco():
    AlphaSco = Coordenadas(16.49, -26.43)
    BetaSco = Coordenadas(16.09, -19.80)
    DeltaSco = Coordenadas(16.00, -22.62)
    EpsilonSco = Coordenadas(16.84, -34.29)
    ZetaSco = Coordenadas(16.90, -42.36)
    EtaSco = Coordenadas(17.20, -43.23)
    ThetaSco = Coordenadas(17.62, -42.99)
    IotaSco = Coordenadas(17.79, -40.12)
    KappaSco = Coordenadas(17.71, -39.03)
    LambdaSco = Coordenadas(17.56, -37.10)
    MuSco = Coordenadas(16.864, -38.04)
    NuSco = Coordenadas(16.20, -19.46)
    RhoSco = Coordenadas(15.95, -29.21)
    PiSco = Coordenadas(15.98, -26.11)
    SigmaSco = Coordenadas(16.35, -25.59)
    TauSco = Coordenadas(16.60, -28.21)

    Line(AlphaSco, SigmaSco)
    Line(AlphaSco, TauSco)
    Line(DeltaSco, SigmaSco)
    Line(DeltaSco, BetaSco)
    Line(NuSco, BetaSco)
    Line(DeltaSco, PiSco)
    Line(PiSco, RhoSco)
    Line(EpsilonSco, TauSco)
    Line(EpsilonSco, MuSco)
    Line(ZetaSco, MuSco)
    Line(ZetaSco, EtaSco)
    Line(ThetaSco, EtaSco)
    Line(ThetaSco, IotaSco)
    Line(KappaSco, IotaSco)
    Line(KappaSco, LambdaSco)

    Const_Label('Sco', 16.5, -33)
    Star_Label(r'$\alpha$', 16.51, -26.8)
    Star_Label(r'$\beta$', 16.09, -19)
    Star_Label(r'$\delta$', 15.84, -22.5)
    Star_Label(r'$\epsilon$', 16.84, -33.2)
    Star_Label(r'$\zeta$', 16.90, -42.36)
    Star_Label(r'$\theta$', 17.62, -44)
    Star_Label(r'$\eta$', 17.20, -43.23)
    Star_Label(r'$\iota$', 17.79, -40.12)
    Star_Label(r'$\kappa$', 17.71, -39.03)
    Star_Label(r'$\lambda$', 17.56, -36.3)
    Star_Label(r'$\rho$', 15.95, -30.3)
    Star_Label(r'$\tau$', 16.64, -28)
    Star_Label(r'$\mu$', 16.864, -38.04)
    Star_Label(r'$\nu$', 16.20, -19.46)


def Sct():
    _AlpSct = Coordenadas(18.58677778, -8.244166667)
    _BetSct = Coordenadas(18.78625, -4.747777778000001)
    _GamSct = Coordenadas(18.48663889, -14.56583333)
    _DelSct = Coordenadas(18.70455556, -9.0525)

    Line(_AlpSct, _BetSct)
    Line(_BetSct, _DelSct)
    Line(_DelSct, _GamSct)
    Line(_GamSct, _AlpSct)

    Const_Label('Sct', 18.66, -12)


def SerCaput():
    _24AlpSer = Coordenadas(15.73780556, 6.425555556)
    _28BetSer = Coordenadas(15.76980556, 15.42194444)
    _37EpsSer = Coordenadas(15.84694444, 4.477777778)
    _13DelSer = Coordenadas(15.58002778, 10.53916667)
    _41GamSer = Coordenadas(15.94088889, 15.66166667)
    _35KapSer = Coordenadas(15.81233333, 18.14166667)
    _21IotSer = Coordenadas(15.69252778, 19.67027778)
    _34OmeSer = Coordenadas(15.83819444, 2.196388889)

    Line(Coordenadas(15.83819444, 0), _34OmeSer)
    Line(_34OmeSer, _37EpsSer)
    Line(_37EpsSer, _24AlpSer)
    Line(_24AlpSer, _13DelSer)
    Line(_13DelSer, _28BetSer)
    Line(_28BetSer, _21IotSer)
    Line(_21IotSer, _35KapSer)
    Line(_35KapSer, _41GamSer)
    Line(_41GamSer, _28BetSer)

    Const_Label('Ser Caput', 15.66, 10)


def SerCauda():
    _35EtaOph = Coordenadas(17.17297222, -15.72472222)
    _64NuOph = Coordenadas(17.98377778, -9.773611111000001)
    _58EtaSer = Coordenadas(18.35516667, -2.8988888889999997)
    #_32MuSer = Coordenadas(15.827, -3.430277778)
    _55XiSer = Coordenadas(17.62644444, -15.39861111)
    _56OmiSer = Coordenadas(17.69025, -12.87527778)
    _53NuSer = Coordenadas(17.34713889, -12.84694444)

    Line(_35EtaOph, _53NuSer)
    Line(_53NuSer, _55XiSer)
    Line(_55XiSer, _56OmiSer)
    Line(_56OmiSer, _64NuOph)
    Line(_64NuOph, _58EtaSer)
    Line(_58EtaSer, Coordenadas(18.57, 0))

    Const_Label('Ser Cauda', 18, -8)


def Sextans():
    AlphaSextantis = Coordenadas(10.13, -0.37)
    BetaSextantis = Coordenadas(10.50, -0.64)
    GammaSextantis = Coordenadas(9.87, -8.10)
    DeltaSextantis = Coordenadas(10.49, -2.73)

    Line(AlphaSextantis, BetaSextantis)
    Line(AlphaSextantis, GammaSextantis)
    Line(BetaSextantis, DeltaSextantis)
    Line(GammaSextantis, DeltaSextantis)

    Const_Label('Sex', 10.25, -5)
    Star_Label(r'$\alpha$', 10.13, -0.8)
    Star_Label(r'$\beta$', 10.50, -0.64)
    Star_Label(r'$\gamma$', 9.87, -8.10)
    Star_Label(r'$\delta$', 10.49, -2.73)


def Sge():
    _12GamSge = Coordenadas(19.97927778, 19.49222222)
    _7DelSge = Coordenadas(19.78980556, 18.53416667)
    _5AlpSge = Coordenadas(19.66827778, 18.01388889)
    _6BetSge = Coordenadas(19.68413889, 17.47611111)

    Line(_5AlpSge, _7DelSge)
    Line(_7DelSge, _6BetSge)
    Line(_7DelSge, _12GamSge)

    Const_Label('Sge', 19.85, 16)
    Star_Label(r'$\alpha$', 19.65, 18.2)
    Star_Label(r'$\beta$', 19.66, 16.8)
    Star_Label(r'$\gamma$', 20.05, 19)


def Sgr():
    GammaSgr = Coordenadas(18.10, -30.42)
    DeltaSgr = Coordenadas(18.35, -29.83)
    EpsilonSgr = Coordenadas(18.40, -34.38)
    LambdaSgr = Coordenadas(18.47, -25.42)
    PhiSgr = Coordenadas(18.76, -26.99)
    EtaSgr = Coordenadas(18.29, -36.76)
    ZetaSgr = Coordenadas(19.04, -29.88)
    TauSgr = Coordenadas(19.11, -27.67)
    SigmaSgr = Coordenadas(18.92, -26.30)
    XiSgr = Coordenadas(18.96, -21.11)
    OmicronSgr = Coordenadas(19.08, -21.74)
    PiSgr = Coordenadas(19.16, -21.02)

    Line(GammaSgr, DeltaSgr)
    Line(GammaSgr, EpsilonSgr)
    Line(DeltaSgr, LambdaSgr)
    Line(DeltaSgr, PhiSgr)
    Line(DeltaSgr, EpsilonSgr)
    Line(ZetaSgr, EpsilonSgr)
    Line(LambdaSgr, PhiSgr)
    Line(PhiSgr, SigmaSgr)
    Line(PhiSgr, ZetaSgr)
    Line(SigmaSgr, TauSgr)
    Line(TauSgr, ZetaSgr)
    Line(SigmaSgr, XiSgr)
    Line(XiSgr, OmicronSgr)
    Line(XiSgr, PiSgr)
    Line(EtaSgr, EpsilonSgr)

    Const_Label('Sgr', 19.16, -26)
    # Star_Label(r'$\alpha$', 19.4, -40)
    # Star_Label(r'$\lambda$', 18.5, -26)
    # Star_Label(r'$\delta$', 18.36, -30)
    # Star_Label(r'$\epsilon$', 18.4, -34)
    Star_Label(r'$\alpha$', 19.39811111, -40.61611111)
    Star_Label(r'$\beta^1$', 19.37730556, -44.45888889)
    Star_Label(r'$\gamma$', 18.09680556, -30.42416667)
    Star_Label(r'$\delta$', 18.34991667, -29.82805556)
    Star_Label(r'$\epsilon$', 18.40286111, -34.38472222)
    Star_Label(r'$\zeta$', 19.04352778, -29.88027778)
    Star_Label(r'$\eta$', 18.29377778, -36.76166667)
    Star_Label(r'$\theta$', 19.99561111, -35.27638889)
    Star_Label(r'$\iota$', 19.92102778, -41.86833333)
    Star_Label(r'$\kappa^1$', 20.37430556, -42.04972222)
    Star_Label(r'$\lambda$', 18.46616667, -25.42166667)
    Star_Label(r'$\mu$', 18.22938889, -21.05888889)
    Star_Label(r'$\nu^1$', 18.90283333, -22.745)
    Star_Label(r'$\xi$', 18.96216667, -21.10666667)
    Star_Label(r'$o$', 19.07805556, -21.74166667)
    Star_Label(r'$\pi$', 19.16272222, -21.02361111)
    Star_Label(r'$\rho$', 19.36122222, -17.84722222)
    Star_Label(r'$\sigma$', 18.92108333, -26.29666667)
    Star_Label(r'$\tau$', 19.11566667, -27.67055556)
    Star_Label(r'$\upsilon$', 19.36211111, -15.955)
    Star_Label(r'$\phi$', 18.76094444, -26.99083333)


def Taurus():
    AlphaTauri = Coordenadas(4.598667, 16.509167)
    BetaTauri = Coordenadas(5.438194, 28.607500)
    GammaTauri = Coordenadas(4.329889, 15.627500)
    DeltaTauri = Coordenadas(4.382250, 17.542500)
    EpsilonTauri = Coordenadas(4.476944, 19.180278)
    ZetaTauri = Coordenadas(5.627417, 21.142500)
    #EtaTauri = Coordenadas(3.791417, 24.105000)
    ThetaTauri = Coordenadas(4.476250, 15.962222)
    #IotaTauri = Coordenadas(5.051583, 21.590000)
    #KappaTauri = Coordenadas(4.422806, 22.293889)
    LambdaTauri = Coordenadas(4.011333, 12.490278)
    #MuTauri = Coordenadas(4.258917, 8.892222)
    #NuTauri = Coordenadas(4.052611, 5.989167)
    XiTauri = Coordenadas(3.452833, 9.732778)
    #OmicronTauri = Coordenadas(3.413556, 9.028889)
    #PiTauri = Coordenadas(4.443444, 14.713611)

    Line(BetaTauri, EpsilonTauri)
    Line(EpsilonTauri, DeltaTauri)
    Line(DeltaTauri, GammaTauri)
    Line(GammaTauri, ThetaTauri)
    Line(ThetaTauri, AlphaTauri)
    Line(AlphaTauri, ZetaTauri)
    Line(GammaTauri, LambdaTauri)
    Line(LambdaTauri, XiTauri)

    Const_Label('Tau', 4.5, 23)
    Star_Label(r'$\alpha$', 4.6, 16)
    Star_Label(r'$\beta$', 5.438194, 28.607500)
    Star_Label(r'$\gamma$', 4.329889, 15.627500)
    Star_Label(r'$\delta$', 4.382250, 17.542500)
    Star_Label(r'$\epsilon$', 4.476944, 19.180278)
    Star_Label(r'$\zeta$', 5.627417, 21.142500)
    Star_Label(r'$\theta$', 4.476250, 15.962222)
    Star_Label(r'$\lambda$', 4.011333, 12.490278)
    Star_Label(r'$\xi$', 3.452833, 9.732778)
    # Star_Label(r'$\eta$', 3.791417, 24.105000)


def Tel():
    _AlpTel = Coordenadas(18.44955556, -45.96833333)
    _ZetTel = Coordenadas(18.48052778, -49.07083333)
    _EpsTel = Coordenadas(18.18716667, -45.95444444)

    Line(_EpsTel, _AlpTel)
    Line(_AlpTel, _ZetTel)

    Const_Label('Tel', 18.6, -48)


def TrA():
    AlphaTrA = Coordenadas(16.81, -69.03)
    BetaTrA = Coordenadas(15.92, -63.43)
    GammaTrA = Coordenadas(15.31, -68.68)

    Line(AlphaTrA, BetaTrA)
    Line(AlphaTrA, GammaTrA)
    Line(GammaTrA, BetaTrA)

    Const_Label('TrA', 15.8, -68)


def Tri():
    AlphaTri = Coordenadas(1.884694, 29.578889)
    BetaTri = Coordenadas(2.159056, 34.987222)
    GammaTri = Coordenadas(2.288583, 33.847222)

    Line(AlphaTri, BetaTri)
    Line(AlphaTri, GammaTri)
    Line(GammaTri, BetaTri)

    Const_Label('Tri', 2.16, 32)
    Star_Label(r'$\alpha$', 1.88, 29.4)
    Star_Label(r'$\beta$', 2.15, 36.5)
    Star_Label(r'$\gamma$', 2.3, 33.85)


def Tuc():
    _AlpTuc = Coordenadas(22.30836111, -60.25972222)
    _GamTuc = Coordenadas(23.2905, -58.23583333)
    _ZetTuc = Coordenadas(0.33452777780000004, -64.87472222)
    _Bet1Tuc = Coordenadas(0.52575, -62.95805556)
    _DelTuc = Coordenadas(22.45555556, -64.96638889)
    _EpsTuc = Coordenadas(23.99861111, -65.57722222)

    Line(_AlpTuc, _DelTuc)
    Line(_DelTuc, _EpsTuc)
    Line(_EpsTuc, _ZetTuc)
    Line(_ZetTuc, _Bet1Tuc)
    Line(_Bet1Tuc, _GamTuc)
    Line(_GamTuc, _AlpTuc)

    Const_Label('Tuc', 23.5, -62.5)
    Star_Label(r'$\alpha$', 22.30, -60)
    Star_Label(r'$\beta$', 0.5, -63)


def UMa():

    AlphaUrsaeMajoris = Coordenadas(11.062139, 61.750833)
    BetaUrsaeMajoris = Coordenadas(11.030694, 56.382500)
    GammaUrsaeMajoris = Coordenadas(11.897167, 53.694722)
    DeltaUrsaeMajoris = Coordenadas(12.257111, 57.032500)
    EpsilonUrsaeMajoris = Coordenadas(12.900472, 55.959722)
    ZetaUrsaeMajoris = Coordenadas(13.399000, 54.921667)
    EtaUrsaeMajoris = Coordenadas(13.792333, 49.313333)
    ThetaUrsaeMajoris = Coordenadas(9.547611, 51.677222)
    IotaUrsaeMajoris = Coordenadas(8.986778, 48.041667)
    KappaUrsaeMajoris = Coordenadas(9.060417, 47.156667)
    LambdaUrsaeMajoris = Coordenadas(10.284944, 42.914444)
    MuUrsaeMajoris = Coordenadas(10.372139, 41.499444)
    NuUrsaeMajoris = Coordenadas(11.307972, 33.094167)
    XiUrsaeMajoris = Coordenadas(11.303056, 31.529167)
    OmicronUrsaeMajoris = Coordenadas(8.504417, 60.718056)
    #PiUrsaeMajoris = Coordenadas(8.670222, 64.327778)
    #RhoUrsaeMajoris = Coordenadas(9.042417, 67.629722)
    #SigmaUrsaeMajoris = Coordenadas(9.173111, 67.134722)
    #TauUrsaeMajoris = Coordenadas(9.181972, 63.513611)
    UpsilonUrsaeMajoris = Coordenadas(9.849833, 59.038611)
    #PhiUrsaeMajoris = Coordenadas(9.868444, 54.064444)
    ChiUrsaeMajoris = Coordenadas(11.767500, 47.779444)
    PsiUrsaeMajoris = Coordenadas(11.161056, 44.498611)
    #OmegaUrsaeMajoris = Coordenadas(10.899639, 43.190000)
    _23UrsaeMajoris = Coordenadas(9.525472, 63.061944)

    Line(EtaUrsaeMajoris, ZetaUrsaeMajoris)
    Line(ZetaUrsaeMajoris, EpsilonUrsaeMajoris)
    Line(EpsilonUrsaeMajoris, DeltaUrsaeMajoris)
    Line(DeltaUrsaeMajoris, AlphaUrsaeMajoris)
    Line(AlphaUrsaeMajoris, BetaUrsaeMajoris)
    Line(BetaUrsaeMajoris, GammaUrsaeMajoris)
    Line(GammaUrsaeMajoris, DeltaUrsaeMajoris)
    Line(GammaUrsaeMajoris, ChiUrsaeMajoris)
    Line(ChiUrsaeMajoris, NuUrsaeMajoris)
    Line(ChiUrsaeMajoris, PsiUrsaeMajoris)
    Line(NuUrsaeMajoris, XiUrsaeMajoris)
    Line(PsiUrsaeMajoris, MuUrsaeMajoris)
    Line(MuUrsaeMajoris, LambdaUrsaeMajoris)
    Line(BetaUrsaeMajoris, UpsilonUrsaeMajoris)
    Line(UpsilonUrsaeMajoris, OmicronUrsaeMajoris)
    Line(UpsilonUrsaeMajoris, ThetaUrsaeMajoris)
    Line(UpsilonUrsaeMajoris, _23UrsaeMajoris)
    Line(_23UrsaeMajoris, AlphaUrsaeMajoris)
    Line(_23UrsaeMajoris, OmicronUrsaeMajoris)
    Line(ThetaUrsaeMajoris, KappaUrsaeMajoris)
    Line(KappaUrsaeMajoris, IotaUrsaeMajoris)

    Const_Label('UMa', 11, 60)
    Star_Label(r'$\alpha$', 11.062139, 61.750833)
    Star_Label(r'$\beta$', 11.030694, 56.382500)
    Star_Label(r'$\gamma$', 11.897167, 54.8)
    Star_Label(r'$\delta$', 12.257111, 57.032500)
    Star_Label(r'$\epsilon$', 12.900472, 55.959722)
    Star_Label(r'$\zeta$', 13.399000, 54.921667)
    Star_Label(r'$\theta$', 9.547611, 51.677222)
    Star_Label(r'$\iota$', 8.986778, 48.041667)
    Star_Label(r'$\kappa$', 9.060417, 47.156667)
    Star_Label(r'$\lambda$', 10.284944, 42.914444)
    Star_Label(r'$\eta$', 13.792333, 49.313333)
    Star_Label(r'$\mu$', 10.372139, 41.499444)
    Star_Label(r'$\nu$', 11.307972, 33.094167)
    Star_Label(r'$\xi$', 11.303056, 31.529167)
    Star_Label(r'$o$', 8.504417, 60.718056)
    Star_Label(r'$\pi$', 8.670222, 64.327778)
    Star_Label(r'$\rho$', 9.042417, 67.929722)
    Star_Label(r'$\sigma$', 9.173111, 67.134722)
    Star_Label(r'$\tau$', 9.181972, 63.513611)
    Star_Label(r'$\upsilon$', 9.849833, 59.038611)
    Star_Label(r'$\phi$', 9.868444, 54.064444)
    Star_Label(r'$\chi$', 11.767500, 47.779444)
    Star_Label(r'$\psi$', 11.161056, 44.498611)
    Star_Label(r'$\omega$', 10.899639, 43.190000)


def UMi():

    AlphaUMi = Coordenadas(2.530194, 89.264167)
    BetaUMi = Coordenadas(14.845083, 74.155556)
    GammaUMi = Coordenadas(15.345472, 71.833889)
    DeltaUMi = Coordenadas(17.536917, 86.586389)
    EpsilonUMi = Coordenadas(16.766139, 82.037222)
    ZetaUMi = Coordenadas(15.734306, 77.794444)
    EtaUMi = Coordenadas(16.291750, 75.755278)
    #ThetaUMi = Coordenadas(15.523583  77.349444)

    Line(AlphaUMi, DeltaUMi)
    Line(DeltaUMi, EpsilonUMi)
    Line(EpsilonUMi, ZetaUMi)
    Line(ZetaUMi, EtaUMi)
    Line(EtaUMi, GammaUMi)
    Line(GammaUMi, BetaUMi)
    Line(BetaUMi, ZetaUMi)

    Const_Label('UMi', 15.66, 78)
    Star_Label(r'$\alpha$', 6, 89)
    Star_Label(r'$\beta$', 14.85, 75)
    Star_Label(r'$\gamma$', 15.5, 71)
    Star_Label(r'$\delta$', 17.536917, 86.586389)
    Star_Label(r'$\epsilon$', 16.766139, 82.037222)
    Star_Label(r'$\zeta$', 15.734306, 77.794444)
    Star_Label(r'$\eta$', 16.291750, 75.755278)
    Star_Label(r'$\theta$', 15.523583, 77.349444)


def Vel():
    _EpsCar = Coordenadas(8.375222222, -59.50972222)
    _Gam2Vel = Coordenadas(8.158888889, -47.33666667)
    _DelVel = Coordenadas(8.745055556, -54.70833333)
    _LamVel = Coordenadas(9.133277778, -43.4325)
    _KapVel = Coordenadas(9.368555556, -55.01083333)
    _MuVel = Coordenadas(10.7795, -49.42)
    _PhiVel = Coordenadas(9.947722222000001, -54.56777778)
    _PsiVel = Coordenadas(9.511666667, -40.46666667)
    #_Gam1Vel = Coordenadas(8.158138889, -47.34583333)

    Line(_DelVel, _Gam2Vel)
    Line(_Gam2Vel, _LamVel)
    Line(_LamVel, _PsiVel)
    Line(_PsiVel, _MuVel)
    Line(_MuVel, _PhiVel)
    Line(_PhiVel, _KapVel)
    Line(_KapVel, _DelVel)
    Line(_DelVel, _EpsCar)

    Const_Label('Vel', 9.33, -48)
    Star_Label(r'$\gamma$', 8.158138889, -47.34583333)
    Star_Label(r'$\delta$', 8.745055556, -54.70833333)
    Star_Label(r'$\epsilon$', 8.375222222, -59.50972222)
    Star_Label(r'$\kappa$', 9.368555556, -55.01083333)
    Star_Label(r'$\lambda$', 9.133277778, -43.4325)
    Star_Label(r'$\mu$', 10.7795, -49.42)


def Vir():
    _67AlpVir = Coordenadas(13.41988889, -11.16138889)
    _79ZetVir = Coordenadas(13.57822222, -0.5958333333)
    _29GamVir = Coordenadas(12.69433333, -1.449444444)
    _07MuVir = Coordenadas(14.71766667, -5.658333333)
    _15EtaVir = Coordenadas(12.33177778, -0.6669444444)
    _99IotVir = Coordenadas(14.26691667, -6.000555556)
    _51TheVir = Coordenadas(13.16583333, -5.538888889)

    Line(_07MuVir, _99IotVir)
    Line(_99IotVir, _79ZetVir)
    Line(_79ZetVir, _29GamVir)
    Line(_29GamVir, Coordenadas(12.73, 0))
    Line(_29GamVir, _15EtaVir)
    Line(_29GamVir, _51TheVir)
    Line(_51TheVir, _67AlpVir)

    Const_Label('Vir', 13.5, -5)
    Star_Label(r'$\alpha$', 13.5, -11)
    Star_Label(r'$\gamma$', 12.69433333, -1.449444444)
    Star_Label(r'$\zeta$', 13.57822222, -0.5958333333)
    Star_Label(r'$\eta$', 12.33177778, -0.6669444444)
    Star_Label(r'$\theta$', 13.16583333, -5.538888889)
    Star_Label(r'$\iota$', 14.26691667, -6.000555556)
    Star_Label(r'$\mu$', 14.71766667, -5.658333333)


def VirNorth():
    _47EpsVir = Coordenadas(13.03627778, 10.95916667)
    _43DelVir = Coordenadas(12.92672222, 3.3975)
    _5BetVir = Coordenadas(11.84491667, 1.7647222219999998)
    _109Vir = Coordenadas(14.77080556, 1.8927777780000001)
    _3NuVir = Coordenadas(11.76433333, 6.529444444)
    _9OmiVir = Coordenadas(12.08680556, 8.733055556)
    _93TauVir = Coordenadas(14.02744444, 1.544444444)

    Line(_109Vir, _93TauVir)
    Line(_93TauVir, Coordenadas(13.57822222, 0))
    Line(_47EpsVir, _43DelVir)
    Line(_43DelVir, Coordenadas(12.73, 0))
    Line(_5BetVir, _3NuVir)
    Line(_3NuVir, _9OmiVir)
    Line(_9OmiVir, Coordenadas(12.305, 0))
    Line(_5BetVir, Coordenadas(12.203, 0))

    Const_Label('Vir', 12.5, 3)
    Star_Label(r'$\beta$', 11.84491667, 1.7647222219999998)
    Star_Label(r'$\delta$', 12.92672222, 3.3975)
    Star_Label(r'$\epsilon$', 13.03627778, 10.95916667)
    Star_Label(r'$\nu$', 11.76433333, 6.529444444)
    Star_Label(r'$o$', 12.08680556, 8.733055556)
    Star_Label(r'$\tau$', 14.02744444, 1.544444444)


def Vol():
    _BetVol = Coordenadas(8.428944443999999, -66.13694444)
    _Gam2Vol = Coordenadas(7.145805556, -70.49888889)
    _ZetVol = Coordenadas(7.697, -72.60611111)
    _DelVol = Coordenadas(7.2805, -67.95722222)
    _AlpVol = Coordenadas(9.040777777999999, -66.39611111)
    _EpsVol = Coordenadas(8.132166667, -68.61722222)
    """
    _TheVol = Coordenadas(8.651444444, -70.38694444)
    _EtaVol = Coordenadas(8.367888889, -73.4)
    _Kap1Vol = Coordenadas(8.330277778, -71.515)
    _IotVol = Coordenadas(6.8575, -70.96333333)
    _Kap2Vol = Coordenadas(8.333527777999999, -71.50527778)
    _Gam1Vol = Coordenadas(7.145055556, -70.49722222)
    """

    Line(_AlpVol, _BetVol)
    Line(_BetVol, _DelVol)
    Line(_DelVol, _Gam2Vol)
    Line(_Gam2Vol, _ZetVol)
    Line(_ZetVol, _EpsVol)
    Line(_EpsVol, _BetVol)

    Const_Label('Vol', 7.5, -69)


def Vul():
    _6AlpVul = Coordenadas(19.47841667, 24.665)
    _13Vul = Coordenadas(19.89102778, 24.07972222)
    _1Vul = Coordenadas(19.27027778, 21.39027778)

    Line(_1Vul, _6AlpVul)
    Line(_6AlpVul, _13Vul)

    Const_Label('Vul', 19.66, 23.5)
    Star_Label(r'$\alpha$', 19.47841667, 24.665)
    Star_Label(r'$13$', 19.89102778, 24.07972222)
    Star_Label(r'$1$', 19.27027778, 21.39027778)

###############################################################################


#PLOTA AS LINHAS DAS CONSTELACOES NO HEMISFERIO SUL
def LinesSouth():
    Ant()
    Apus()
    AqlSouth()  # Complemento da Constelacao no Hemisferio Sul.
    Aqr()
    Ara()
    Cae()
    CMa()
    Cap()
    Car()
    Cen()
    Cet()
    Cha()
    Cir()
    Col()
    Crv()
    CrA()
    Crt()
    Cru()
    Dor()
    Eri()
    For()
    Gru()
    Hor()
    HyaSouth()
    Hyi()
    Ind()
    Lep()
    Libra()
    Lup()
    Men()
    Mic()
    Musca()
    Mon()
    Nor()
    Oct()
    OphSouth()
    Ori()
    Pav()
    Phe()
    Pic()
    PsA()
    Pup()
    Pyx()
    Ret()
    Sgr()
    Scl()
    Sco()
    Sct()
    SerCauda()
    Sextans()
    Tel()
    TrA()
    Tuc()
    Vel()
    Vir()
    Vol()


#PLOTA AS LINHAS DAS CONSTELACOES NO HEMISFERIO NORTE
def LinesNorth():
    And()
    Aql()
    Aries()
    Aur()
    Bootes()
    Cancer()
    Cam()
    CMi()
    Cas()
    Cep()
    CetNorth()
    Com()
    CrB()
    CVn()
    Cygnus()
    Del()
    Dra()
    Equ()
    Gem()
    Hercules()
    HyaNorth()
    Lac()
    Leo()
    LMi()
    Lyn()
    Lyra()
    Oph()
    OriNorth()
    Peg()
    Per()
    Psc()
    SerCaput()
    Sge()
    Taurus()
    Tri()
    UMa()
    UMi()
    VirNorth()
    Vul()


#%%
###############################################################################
##SIMBOLOS E ROTULOS DOS OBJETOS DE CEU PROFUNDO
###############################################################################
def DSO_south(dso_marker, dso_type):
    DSO = messier_south[messier_south['Type'] == dso_type]
    if retangular:
        plt.scatter(DSO.RAHour + DSO.RAMinute / 60,
                    -1 * (DSO.DecDeg + DSO.DecMinute / 60),
                    alpha=0.5, c='gray', marker=dso_marker, zorder=3
                    )
    else:
        plt.scatter((DSO.RAHour + DSO.RAMinute / 60) * 2 * np.pi / 24,
                    90 - (DSO.DecDeg + DSO.DecMinute / 60),
                    alpha=0.3, c='gray', marker=dso_marker, zorder=3
                    )


def MessierSul():
    #NEBULAE ##################################################################
    DSO_south('s', 'Diffuse Nebula')
    DSO_south('s', 'Supernova Remnant')
    DSO_south(r"$\emptyset$", 'Planetary Nebula')
    #GALAXIES #################################################################
    DSO_south('d', 'Spiral Galaxy')
    DSO_south('d', 'Elliptical Galaxy')
    DSO_south('d', 'Irregular Galaxy')
    DSO_south('d', 'Lenticular (S0) Galaxy')
    #GLOBULAR CLUSTERS ########################################################
    DSO_south((r'$\bigotimes$'), 'Globular Cluster',)
    #OPEN CLUSTERS/ASTERISMS ##################################################
    DSO_south('^', 'Open Cluster',)
    DSO_south('^', 'Star Cloud')
    DSO_south('^', 'Group/Asterism')
    DSO_south('^', 'Double Star')

###############################################################################
#Rotulo dos Objetos Messier no Hemisferio Sul


def RotuloMessierSul():
    for numero_m, ra_m, ra_min_m, dec_m, dec_min_m, alpha_label in zip(
            messier_south.Label,
            messier_south.RAHour,
            messier_south.RAMinute,
            messier_south.DecDeg,
            messier_south.DecMinute,
            messier_south.AlphaLabel):
        if polar_sul or polar_duplo:
            plt.annotate(str(numero_m),
                         xy=((ra_m + ra_min_m / 60) * 2 * np.pi / 24,
                             90 - (dec_m + dec_min_m / 60)),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')
        if retangular:
            plt.annotate(str(numero_m),
                         xy=(ra_m + ra_min_m / 60,
                             -1 * (dec_m + dec_min_m / 60)),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')


###############################################################################
def DSO_north(dso_marker, dso_type):
    DSO = messier_north[messier_north['Type'] == dso_type]
    symbol = dso_marker
    if retangular:
        plt.scatter(DSO.RAHour + DSO.RAMinute / 60,
                    DSO.DecDeg + DSO.DecMinute / 60,
                    alpha=0.5, c='gray', marker=symbol, zorder=3
                    )
    else:
        plt.scatter((DSO.RAHour + DSO.RAMinute / 60) * 2 * np.pi / 24,
                    90 - (DSO.DecDeg + DSO.DecMinute / 60),
                    alpha=0.3, c='gray', marker=symbol, zorder=3
                    )


def MessierNorte():
    #NEBULAE ##################################################################
    DSO_north('s', 'Diffuse Nebula')
    DSO_north('s', 'Supernova Remnant')
    DSO_north(r"$\emptyset$", 'Planetary Nebula')
    #GALAXIES #################################################################
    DSO_north('d', 'Spiral Galaxy')
    DSO_north('d', 'Elliptical Galaxy')
    DSO_north('d', 'Irregular Galaxy')
    DSO_north('d', 'Lenticular (S0) Galaxy')
    #GLOBULAR CLUSTERS ########################################################
    DSO_north((r'$\bigotimes$'), 'Globular Cluster',)
    #OPEN CLUSTERS/ASTERISMS ##################################################
    DSO_north('^', 'Open Cluster',)
    DSO_north('^', 'Star Cloud')
    DSO_north('^', 'Group/Asterism')
    DSO_north('^', 'Double Star')

###############################################################################
#Rotulo dos Objetos Messier no Hemisferio Norte


def RotuloMessierNorte():
    for numero_m, ra_m, ra_min_m, dec_m, dec_min_m, alpha_label in zip(
            messier_north.Label,
            messier_north.RAHour,
            messier_north.RAMinute,
            messier_north.DecDeg,
            messier_north.DecMinute,
            messier_north.AlphaLabel):
        if polar_norte or polar_duplo:
            plt.annotate(str(numero_m),
                         xy=((ra_m + ra_min_m / 60) * 2 * np.pi / 24,
                             90 - (dec_m + dec_min_m / 60)),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')
        if retangular:
            plt.annotate(str(numero_m),
                         xy=(ra_m + ra_min_m / 60,
                             dec_m + dec_min_m / 60),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')


###############################################################################
def CALD_north(dso_marker, dso_type):
    DSO = caldwell_north[caldwell_north['Type'] == dso_type]
    symbol = dso_marker
    if retangular:
        plt.scatter(DSO.RAHour + DSO.RAMinute / 60,
                    DSO.DecDeg + DSO.DecMinute / 60,
                    alpha=0.5, c='gray', marker=symbol, zorder=3
                    )
    else:
        plt.scatter((DSO.RAHour + DSO.RAMinute / 60) * 2 * np.pi / 24,
                    90 - (DSO.DecDeg + DSO.DecMinute / 60),
                    alpha=0.3, c='gray', marker=symbol, zorder=3
                    )


def CaldwellNorte():
    #NEBULAE ##################################################################
    CALD_north('s', 'Diffuse Nebula')
    CALD_north('s', 'Supernova Remnant')
    CALD_north('s', 'Dark Nebula')
    CALD_north(r"$\emptyset$", 'Planetary Nebula')
    #GALAXIES #################################################################
    CALD_north('d', 'Spiral Galaxy')
    CALD_north('d', 'Elliptical Galaxy')
    CALD_north('d', 'Irregular Galaxy')
    CALD_north('d', 'Lenticular (S0) Galaxy')
    #GLOBULAR CLUSTERS ########################################################
    CALD_north((r'$\bigotimes$'), 'Globular Cluster',)
    #OPEN CLUSTERS/ASTERISMS ##################################################
    CALD_north('^', 'Open Cluster',)
    CALD_north('^', 'Star Cloud')
    CALD_north('^', 'Group/Asterism')
    CALD_north('^', 'Double Star')
###############################################################################
#Rotulo dos Objetos Caldwell no Hemisferio Norte


def RotuloCaldwellNorte():
    for numero_m, ra_m, ra_min_m, dec_m, dec_min_m, alpha_label in zip(
            caldwell_north.Label,
            caldwell_north.RAHour,
            caldwell_north.RAMinute,
            caldwell_north.DecDeg,
            caldwell_north.DecMinute,
            caldwell_north.AlphaLabel):
        if polar_norte or polar_duplo:
            plt.annotate(str(numero_m),
                         xy=((ra_m + ra_min_m / 60) * 2 * np.pi / 24,
                             90 - (dec_m + dec_min_m / 60)),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')
        if retangular:
            plt.annotate(str(numero_m),
                         xy=(ra_m + ra_min_m / 60,
                             dec_m + dec_min_m / 60),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')


###############################################################################
def CALD_south(dso_marker, dso_type):
    DSO = caldwell_south[caldwell_south['Type'] == dso_type]
    if retangular:
        plt.scatter(DSO.RAHour + DSO.RAMinute / 60,
                    -1 * (DSO.DecDeg + DSO.DecMinute / 60),
                    alpha=0.5, c='gray', marker=dso_marker, zorder=3
                    )
    else:
        plt.scatter((DSO.RAHour + DSO.RAMinute / 60) * 2 * np.pi / 24,
                    90 - (DSO.DecDeg + DSO.DecMinute / 60),
                    alpha=0.3, c='gray', marker=dso_marker, zorder=3
                    )


def CaldwellSul():
    #NEBULAE ##################################################################
    CALD_south('s', 'Diffuse Nebula')
    CALD_south('s', 'Supernova Remnant')
    CALD_south('s', 'Dark Nebula')
    CALD_south(r"$\emptyset$", 'Planetary Nebula')
    #GALAXIES #################################################################
    CALD_south('d', 'Spiral Galaxy')
    CALD_south('d', 'Elliptical Galaxy')
    CALD_south('d', 'Irregular Galaxy')
    CALD_south('d', 'Lenticular (S0) Galaxy')
    #GLOBULAR CLUSTERS ########################################################
    CALD_south((r'$\bigotimes$'), 'Globular Cluster',)
    #OPEN CLUSTERS/ASTERISMS ##################################################
    CALD_south('^', 'Open Cluster',)
    CALD_south('^', 'Star Cloud')
    CALD_south('^', 'Group/Asterism')
    CALD_south('^', 'Double Star')
###############################################################################


# Rotulo dos Objetos Caldwell no Hemisferio Sul
def RotuloCaldwellSul():
    for numero_m, ra_m, ra_min_m, dec_m, dec_min_m, alpha_label in zip(
            caldwell_south.Label,
            caldwell_south.RAHour,
            caldwell_south.RAMinute,
            caldwell_south.DecDeg,
            caldwell_south.DecMinute,
            caldwell_south.AlphaLabel):
        if polar_sul or polar_duplo:
            plt.annotate(str(numero_m),
                         xy=((ra_m + ra_min_m / 60) * 2 * np.pi / 24,
                             90 - (dec_m + dec_min_m / 60)),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')
        if retangular:
            plt.annotate(str(numero_m),
                         xy=(ra_m + ra_min_m / 60,
                             -1 * (dec_m + dec_min_m / 60)),
                         color='gray', alpha=0.5 * alpha_label,
                         fontsize='small')


###############################################################################
#%%
# ECLIPTICA
def EclipticaRetangular():
    if retangular:
        RAecliptica = np.arange(0, 24, .1)  # EIXO X (ASCENCAO RETA)
        ecliptica = 23.5 * np.sin(RAecliptica * 2 * np.pi / 24)  # ECLIPTICA
        plt.plot(RAecliptica, ecliptica, 'b--', alpha=0.4, zorder=2)
    # FAIXA COM POSSIBILIDADE DE OCULTACAO PELA LUA
    if faixa_de_ocultacao:
        plt.plot(RAecliptica, ecliptica + 5.3, 'b--', alpha=0.3, zorder=2)
        plt.plot(RAecliptica, ecliptica - 5.3, 'b--', alpha=0.3, zorder=2)

###############################################################################


def EclipticaPolarNorte():
    ra = np.arange(0, 2 * np.pi, 0.1)
    dec = np.sin(ra)
    ax.plot(ra, 90 - 23.5 * dec, 'w--', alpha=0.5)
    ax.plot(ra, 90 - 23.5 * dec, 'b--', alpha=0.2)


def EclipticaPolarSul():
    ra = np.arange(0, 2 * np.pi, 0.1)
    dec = np.sin(ra)
    ax.plot(ra, 90 + 23.5 * dec, 'w--', alpha=0.5)
    ax.plot(ra, 90 + 23.5 * dec, 'b--', alpha=0.2)

###############################################################################
#CRIA O GRID POLAR COM ESCALA DE ASCENCAO RETA NO FORMATO XXhXX


def GridPolar():
    lines, labels = plt.thetagrids(range(0, 360, 5),
                                   ('0h00', '', '', '1h00', '', '', '2h00', '',
                                    '', '3h00', '', '', '4h00', '', '', '5h00',
                                    '', '', '6h00', '', '', '7h00', '', '', '8h00',
                                    '', '', '9h00', '', '', '10h00', '', '',
                                    '11h00', '', '', '12h00', '', '', '13h00',
                                    '', '', '14h00', '', '', '15h00', '', '',
                                    '16h00', '', '', '17h00', '', '', '18h00',
                                    '', '', '19h00', '', '', '20h00', '', '',
                                    '21h00', '', '', '22h00', '', '', '23h00',
                                    '', '',),
                                   alpha=0.8)

###############################################################################
#Rotulo Declinacao a cada 10 graus, Ticks a cada 5 graus


def GridDeclinacaoSul():
    ax.set_rmax(90)
    ax.set_rgrids([5, 10, 15, 20, 25, 30, 35, 40, 45, 50,
                   55, 60, 65, 70, 75, 80, 85],
                  ('', '-80°', '', '-70°', '', '-60°', '', '-50°', '',
                   '-40°', '', '-30°', '', '-20°', '', '-10°', ''),
                  alpha=0.2)
    ax.set_rlabel_position(0)
    ax.grid(True, alpha=0.4)


def GridDeclinacaoNorte():
    ax.set_rmax(90)
    ax.set_rgrids([5, 10, 15, 20, 25, 30, 35, 40, 45, 50,
                   55, 60, 65, 70, 75, 80, 85],
                  ('', '80°', '', '70°', '', '60°', '', '50°', '',
                   '40°', '', '30°', '', '20°', '', '10°', ''),
                  alpha=0.2)
    ax.set_rlabel_position(0)
    ax.grid(True, alpha=0.4, zorder=3)


#%% CABECALHO

# Imprime na tela o texto do arquivo CEUPROFUNDO
CEUPROFUNDO = open("CEUPROFUNDO", 'r')
CEUPROFUNDO_txt = CEUPROFUNDO.read()
print(CEUPROFUNDO_txt)
CEUPROFUNDO.close()

#Exibe data/hora do inicio da execucao
timestring = time.strftime("%y-%m-%d %H:%M:%S %Z UTC", time.localtime())
print(timestring + '\n\n')

# String YYMMDDhhmmss para gerar nomes unicos de arquivos
filename = time.strftime("%y%m%d%H%M%S", time.localtime())

#Muda o formato de saída se preciso
if png:
    file_format = '.png'

#Registra tempo inicial da execucao
t1 = time.time()


###############################################################################
#%%                             DATA FRAME
"""
###############################################################################
#
#                           IMPORTA CATALOGOS
#
###############################################################################
"""
#catalogo de estrelas BSC (mag < 6.5)
if stars:
    cat_stars = pd.DataFrame(pd.read_csv('BrightStarCatalogDecimal.csv',
                                         usecols=[0, 9, 10, 11, 12, 13]
                                         )
                             )
    stars_south = cat_stars[cat_stars.Hemisphere < 0]
    stars_north = cat_stars[cat_stars.Hemisphere > 0]
# catalogo messier
# importa catalogo e separa hemisferios
if messier:
    cat_messier = pd.DataFrame(pd.read_csv('MessierObjects.csv', sep=',',
                                           usecols=[0, 2, 4, 5, 6, 7,
                                                    8, 9, 11, 13]
                                           )
                               )
    messier_south = cat_messier[cat_messier.DecSign == '-']
    messier_north = cat_messier[cat_messier.DecSign == '+']
# catalogo caldwell
# importa catalogo e separa hemisferios
if caldwell:
    cat_caldwell = pd.DataFrame(pd.read_csv('CaldwellObjects.csv', sep=',',
                                            usecols=[0, 2, 4, 5, 6, 7,
                                                     8, 9, 11, 13]
                                            )
                                )
    caldwell_south = cat_caldwell[cat_caldwell.DecSign == '-']
    caldwell_north = cat_caldwell[cat_caldwell.DecSign == '+']

###############################################################################
#
#
#
###############################################################################

#%%  CARTA RETANGULAR / RECTANGULAR CHART
if retangular:

    fig = plt.figure(figsize=(2.0 * plot_size, plot_size), dpi=plot_dpi)
    ax = plt.subplot(111)
    ###########################################################################
    # Ecliptica

    EclipticaRetangular()

    ###########################################################################
    # ESTRELAS / STARS
    if stars:
        magnitude = (plot_dpi / fator) * (base ** -cat_stars.V) - limite
        if darkmode:
            #Pinta o retangulo de preto
            rect = ax.patch
            rect.set_facecolor('black')
            #Plota estrelas brancas abaixo das estrelas coloridas
            plt.scatter(cat_stars.RA, cat_stars.DEC, c='white',
                        s=magnitude, alpha=star_background, zorder=2)
        plt.scatter(cat_stars.RA,
                    cat_stars.DEC,
                    c=ColorIndex(cat_stars.BminusV),
                    cmap=plt.cm.RdYlBu,
                    s=magnitude, alpha=star_alpha, zorder=3)
    ###########################################################################
    # MESSIER
    if messier:
        #HEMISFERIO NORTE
        MessierNorte()
        #CRIA ROTULOS Mxx
        RotuloMessierNorte()
        #HEMISFERIO SUL
        MessierSul()
        #CRIA ROTULOS Mxx
        RotuloMessierSul()

    if caldwell:
        #HEMISFERIO SUL
        CaldwellSul()
        #CRIA ROTULOS NGC/ICxxxx
        RotuloCaldwellSul()
        #HEMISFERIO NORTE
        CaldwellNorte()
        #CRIA ROTULOS Mxx
        RotuloCaldwellNorte()

    ###########################################################################

    # A funcao 'Cru()' plota o cruzeiro do sul em destaque.
    Cru()
    LinesNorth()
    LinesSouth()
    ###########################################################################

    ax.set_title("Carta Retangular | -" + str(declinacao_limite)
                 + "$^\circ$ a " + str(declinacao_limite)
                 + "$^\circ$\nwww.ceuprofundo.com", va='bottom')
    ax.axis([24, 0, -declinacao_limite, declinacao_limite])
    ax.xaxis.set_major_locator(tck.MultipleLocator(3))  # RA Tick a cada 3h
    plt.grid(True, alpha=0.6, linewidth=0.4)
    plt.xlabel('Ascenção Reta')
    plt.ylabel('Declinação')
    plt.savefig('Retangular_' + filename + file_format, dpi=plot_dpi)
    #plt.show()
###############################################################################


#%%  CARTA POLAR SUL
"""
######################### HEMISFÉRIO SUL CELESTE ##############################
#
# Ascenção Reta (R.A.) crescente no sentido horário.
#
###############################################################################
"""

if polar_sul:
    r = np.arange(90, 0, 1)
    theta = 2 * np.pi * r

    fig = plt.figure(figsize=(plot_size, plot_size), dpi=plot_dpi)

    ax = plt.subplot(111, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(1)
    ax.plot()
    ###########################################################################
    # STARS
    if stars:
        StarsSul()
        LinesSouth()
    ###########################################################################
    # MESSIER
    if messier:
        #HEMISFERIO SUL
        MessierSul()
        #CRIA ROTULOS Mxx
        RotuloMessierSul()
    ###########################################################################
    # CALDWELL
    if caldwell:
        #HEMISFERIO SUL
        CaldwellSul()
        #CRIA ROTULOS NGC/ICxxxx
        RotuloCaldwellSul()
    ###########################################################################

    EclipticaPolarSul()
    GridPolar()
    GridDeclinacaoSul()

    ax.set_title("Hemisfério SUL celeste\nwww.ceuprofundo.com", va='bottom')
    plt.savefig('HemisferioSul_' + filename + file_format, dpi=plot_dpi / 2)
    #plt.show()

#%% CARTA POLAR NORTE
"""
######################### HEMISFÉRIO NORTE CELESTE ############################
#
# Ascenção Reta (R.A.) crescente no sentido anti-horário.
#
###############################################################################
"""
if polar_norte:
    r = np.arange(0, 90, 1)
    theta = 2 * np.pi * r

    fig = plt.figure(figsize=(plot_size, plot_size), dpi=plot_dpi)

    ax = plt.subplot(111, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.plot()
    ###########################################################################
    #STARS
    if stars:
        StarsNorte()
        LinesNorth()
    ###########################################################################
    #MESSIER
    if messier:
        #HEMISFERIO NORTE
        MessierNorte()
        #CRIA ROTULOS Mxx
        RotuloMessierNorte()
    ###########################################################################
    #CALDWELL
    if caldwell:
        #HEMISFERIO NORTE
        CaldwellNorte()
        #CRIA ROTULOS Mxx
        RotuloCaldwellNorte()
    ###########################################################################

    EclipticaPolarNorte()
    GridPolar()
    GridDeclinacaoNorte()

    ax.set_title("Hemisfério NORTE celeste\nwww.ceuprofundo.com", va='bottom')
    plt.savefig('HemisferioNorte_' + filename + file_format, dpi=plot_dpi / 2)
    #plt.show()


#%% POLAR DUPLO
"""
###############################################################################
#                              CARTA POLAR DUPLA                              #
###############################################################################
"""

if polar_duplo:

    r = np.arange(0, 90, 1)
    theta = 2 * np.pi * r
    fig = plt.figure(figsize=(1.4 * plot_size, plot_size),
                     dpi=plot_dpi,
                     constrained_layout=True)
    gs = GridSpec(6, 8, figure=fig)


#################NORTE
    ax = fig.add_subplot(gs[1:5, 0:4], projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    #ax.plot()

    if stars:
        StarsNorte()
        LinesNorth()

    ###########################################################################
    # MESSIER
    if messier:
        #HEMISFERIO NORTE
        MessierNorte()
        #CRIA ROTULOS Mxx
        RotuloMessierNorte()

    ###########################################################################
    # CALDWELL
    if caldwell:
        #HEMISFERIO NORTE
        CaldwellNorte()
        #CRIA ROTULOS Mxx
        RotuloCaldwellNorte()
    ###########################################################################
    EclipticaPolarNorte()
    GridPolar()
    GridDeclinacaoNorte()

    ax.set_title("Hemisfério NORTE celeste", va='bottom')
    # plt.plot(RA*2*np.pi/24, 23.5*np.sin(RA*2*np.pi/24))
#################SUL

    ax = fig.add_subplot(gs[1:5, 4:], projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(1)
    ax.plot()

    if stars:
        StarsSul()
        LinesSouth()
    ###########################################################################
    # MESSIER
    if messier:
        #HEMISFERIO SUL
        MessierSul()
        #CRIA ROTULOS Mxx
        RotuloMessierSul()
    ###########################################################################
    # CALDWELL
    if caldwell:
        #HEMISFERIO SUL
        CaldwellSul()
        #CRIA ROTULOS Mxx
        RotuloCaldwellSul()
    ###########################################################################
    EclipticaPolarSul()
    GridPolar()
    GridDeclinacaoSul()

    ax.set_title("Hemisfério SUL celeste", va='bottom')

    #plt.subplots_adjust(wspace=None)

###############################################################################
#PERFUMARIA - RODAPE
    rodape()

###############################################################################

    #fig.suptitle('CARTA CELESTE\nwww.ceuprofundo.com', fontsize=plot_dpi / 10)
    plt.savefig('CartaDupla_' + filename + file_format, dpi=plot_dpi / 2)
    # plt.show()

###############################################################################

###############################################################################

# Calcula e exibe tempo total da execucao
t2 = time.time()
delta_t = t2 - t1
print('\n''@ceuprofundo'
      '\n')
goodbye = ' Tarefas Concluídas '
print(goodbye.center(80, '#'))
('')
print('tempo de execução: ' + str(round(delta_t, 4)) + ' s')
