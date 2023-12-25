import matplotlib.pyplot as plt

# consts for the moment
Mb          = 4.0e30                    # black hole
Ms          = 2.0e30                    # sun
Me          = 5.972e24                  # earth
Mm          = 6.39e23                   # mars
AU          = 1.5e11                    # sun earth distance

e_ap_v      = 29290                     # earth velocity at aphelion
m_ap_v      = 21970                     # mars velocity at aphelion

daysec      = 24.0*60*60
t           = 0.0
dt          = 1*daysec

class Planet:
    def __init__(self, name, posX, posY, mass, velX, velY):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.mass = mass
        self.velX = velX
        self.velY = velY

class CentralStar:
    def __init__(self, name, mass):
        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.name = name
        self.mass = mass

class Gravity:
    def __init__(self,Planet,CentralStar):
        self.Planet = Planet
        self.CentralStar = CentralStar
        self.px = Planet.posX
        self.py = Planet.posY
        self.sx = CentralStar.posX
        self.sy = CentralStar.posY
        self.pvx = Planet.velX
        self.pvy = Planet.velY
        self.svx = CentralStar.velX
        self.svy = CentralStar.velY
        self.grav = 6.67e-11 * Planet.mass * CentralStar.mass

    #force on planets directiory
    def calculateForce(self):
        grav = self.grav

        rx = self.px - self.sx
        ry = self.py - self.sy
        modr3 = (rx**2 + ry**2)**1.5

        fx = -grav*rx/modr3
        fy = -grav*ry/modr3

        return fx,fy

    def calculateVelocity(self):
        fx = self.calculateForce()[0]
        fy = self.calculateForce()[1]
        pm = self.Planet.mass

        self.pvx += fx*dt/pm
        self.pvy += fy*dt/pm

    def planetDisplacement(self):
        self.calculateVelocity()
        self.px += self.pvx * dt
        self.py += self.pvy * dt

        posx = self.px
        posy = self.py

        return posx, posy


xelist,yelist = [],[]
xmlist,ymlist = [],[]
xslist,yslist = [],[]

earth = Planet('earth',1.0167*AU,0,Me,0,e_ap_v)
mars = Planet('mars',1.666*AU,0,Me,0,m_ap_v)
sun = CentralStar('sun',Ms)
gravity_sun_earth = Gravity(earth, sun)
gravity_sun_mars = Gravity(mars, sun)

while t < 1 * 365 * daysec:

    # save the position in list
    xelist.append(gravity_sun_earth.planetDisplacement()[0])
    yelist.append(gravity_sun_earth.planetDisplacement()[1])

    xmlist.append(gravity_sun_mars.planetDisplacement()[0])
    ymlist.append(gravity_sun_mars.planetDisplacement()[1])

    xslist.append(0)
    yslist.append(0)

    # update dt
    t += dt


plt.plot(xelist,yelist,'--g',lw=1.5,label='earth')
plt.plot(xmlist,ymlist, '--r',lw=1.2,label='mars')
plt.plot(0,0,'yo',label='sun')
plt.axis('equal')
plt.legend()
plt.show()
