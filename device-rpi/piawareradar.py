"""
Angelina Tsuboi
angelinatsuboi.com

ADS-B Spoof Detector Radar

"""

from argparse import ArgumentParser
import pygame
from radar import Radar
from gpsutils import GPSUtils
from flightdata import FlightData
from copy import deepcopy
from threading import Timer
import os

def lat_lon_to_x_y(lat, lon):
    x, y = GPSUtils.lat_lon_to_x_y(lat, lon)
    x = int(x)
    y = int(y)
    #negate the y so the numbers are 'going the right way' as the screen goes down!
    y = y * -1
    return x, y

def calc_scale_km(scale, line_length):
    return str(round((line_length / scale) / 1000)) + " km"

#read command line options
parser = ArgumentParser(description="PiAware Flight Radar")
parser.add_argument("lat", type=float, help="The latitude of the receiver")
parser.add_argument("lon", type=float, help="The longitude of the receiver")
parser.add_argument("--piawareip", help="The ip address of the piaware server")
args = parser.parse_args()

#import the relevant constants
from const_normal import *

#create the piaware url
piawareip = args.piawareip
if piawareip == None: piawareip = "localhost"
piaware_url = "http://{}:8080/data/aircraft.json".format(piawareip)

#set default scale
scale = 0.001

#init pygame
pygame.init()

#load font
myfont = pygame.font.SysFont(FONT, FONTSIZE)

#create the screen
screenflags = 0
screen = pygame.display.set_mode([SIZE[0], SIZE[1]])

#setup the screen
#set the screen background
screen.fill(BLACK)
#set the screen caption
pygame.display.set_caption("Fly Catcher Radar")
#draw close button
close_rect = pygame.draw.rect(screen, GREEN, CLOSERECT, 2)
pygame.draw.line(screen, GREEN,
                 (CLOSERECT[0], CLOSERECT[1]), (CLOSERECT[0] + CLOSERECT[2], CLOSERECT[1] + CLOSERECT[3]),
                 1)
pygame.draw.line(screen, GREEN,
                 (CLOSERECT[0], CLOSERECT[1] + CLOSERECT[3]), (CLOSERECT[0] + CLOSERECT[2], CLOSERECT[1]),
                 1)
#draw scale plus button
scale_plus_rect = pygame.draw.rect(screen, GREEN, SCALEPLUSRECT, 2)
pygame.draw.line(screen, GREEN,
                 (SCALEPLUSRECT[0] + (SCALEPLUSRECT[2] / 2), SCALEPLUSRECT[1] + 5),
                 (SCALEPLUSRECT[0] + (SCALEPLUSRECT[2] / 2), SCALEPLUSRECT[1] + SCALEPLUSRECT[3] - 5),
                 1)
pygame.draw.line(screen, GREEN,
                 (SCALEPLUSRECT[0] + 5, SCALEPLUSRECT[1] + (SCALEPLUSRECT[3] / 2)),
                 (SCALEPLUSRECT[0] + SCALEPLUSRECT[2] - 5, SCALEPLUSRECT[1] + (SCALEPLUSRECT[3] / 2)),
                 1)
#draw scale negative button
scale_neg_rect = pygame.draw.rect(screen, GREEN, SCALENEGRECT, 2)
pygame.draw.line(screen, GREEN,
                 (SCALENEGRECT[0] + 5, SCALENEGRECT[1] + (SCALENEGRECT[3] / 2)),
                 (SCALENEGRECT[0] + SCALENEGRECT[2] - 5, SCALENEGRECT[1] + (SCALENEGRECT[3] / 2)),
                 1)
#draw scale line
pygame.draw.line(screen, GREEN,
                 (SCALELINERECT[0], SCALELINERECT[1] + (SCALELINERECT[3] / 2)),
                 (SCALELINERECT[0] + SCALELINERECT[2], SCALELINERECT[1] + (SCALELINERECT[3] / 2)),
                 1)
pygame.draw.line(screen, GREEN,
                 (SCALELINERECT[0], SCALELINERECT[1]),
                 (SCALELINERECT[0], SCALELINERECT[1] + SCALELINERECT[3]),
                 1)
pygame.draw.line(screen, GREEN,
                 (SCALELINERECT[0] + SCALELINERECT[2], SCALELINERECT[1]),
                 (SCALELINERECT[0] + SCALELINERECT[2], SCALELINERECT[1] + SCALELINERECT[3]),
                 1)
scale_text = myfont.render(calc_scale_km(scale, SCALELINERECT[2]), 1, GREEN)
screen.blit(scale_text, (SCALETEXTRECT[0], SCALETEXTRECT[1]))

#flight data timer
flight_data_timer = None

#get the home position
home_x, home_y = lat_lon_to_x_y(args.lat, args.lon)

#startup the radar
radar = Radar(screen, RADARRECT, radar_pos = (home_x, home_y), scale = scale, back_col = BLACK, radar_col = GREEN)
radar.start()

#get the flight data
print(piaware_url)
myflights = FlightData(data_url = "http://localhost:8080/data/aircraft.json", flight_log_number = flight_log_number, flight_folder = FLIGHTLOGS)

done = False
next_refresh = pygame.time.get_ticks()
while not done:
    
    #should the flights be refreshed
    if pygame.time.get_ticks() > next_refresh:

        #keep a track of the last aircraft we saw
        lastaircraftseen = deepcopy(myflights.aircraft)
        
        #loop through all the flights and update them
        for aircraft in myflights.aircraft:
            if aircraft.lat != None:
                x, y = lat_lon_to_x_y(aircraft.lat, aircraft.lon)
                radar.dot_add(aircraft.hex, x, y, data = aircraft)
        
        next_refresh += FLIGHTDATAREFRESH
        myflights.refresh()

        #remove the dots that are no longer there
        for lostaircraft in set(lastaircraftseen) - set(myflights.aircraft):
            radar.dot_remove(lostaircraft.hex)

    #check for pygame events
    for event in pygame.event.get():

        #quit
        if event.type == pygame.QUIT:
            done = True
            
        #mouse press
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            #close button
            if close_rect.collidepoint(mousepos):
                done = True
            
            #scale buttons
            if scale_plus_rect.collidepoint(mousepos):
                scale = scale * 2
                pygame.draw.rect(screen, BLACK, SCALETEXTRECT, 0)
                scale_text = myfont.render(calc_scale_km(scale, SCALELINERECT[2]), 1, GREEN)
                screen.blit(scale_text, (SCALETEXTRECT[0], SCALETEXTRECT[1]))
                radar.set_scale(scale)
                
            if scale_neg_rect.collidepoint(mousepos):
                scale = scale * 0.5
                pygame.draw.rect(screen, BLACK, SCALETEXTRECT, 0)
                scale_text = myfont.render(calc_scale_km(scale, SCALELINERECT[2]), 1, GREEN)
                screen.blit(scale_text, (SCALETEXTRECT[0], SCALETEXTRECT[1]))
                radar.set_scale(scale)
                
            #dot clicked
            dot_found = radar.dot_at_point(mousepos)
            if dot_found != None:
                #output the flight data to the screen
                pygame.draw.rect(screen, BLACK, FLIGHTDATARECT, 0)
                text = myfont.render(radar.dots[dot_found].data.hex, 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1]))
                text = myfont.render(radar.dots[dot_found].data.squawk, 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1] + LINESPACE))
                text = myfont.render(radar.dots[dot_found].data.flight, 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1] + (LINESPACE * 2)))
                text = myfont.render("lat: " + str(radar.dots[dot_found].data.lat), 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1] + (LINESPACE * 3)))
                text = myfont.render("lon: " + str(radar.dots[dot_found].data.lon), 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1] + (LINESPACE * 4)))
                text = myfont.render("alt: " + str(radar.dots[dot_found].data.altitude), 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1] + (LINESPACE * 5)))
                text = myfont.render("spd: " + str(radar.dots[dot_found].data.speed), 1, GREEN)
                screen.blit(text, (FLIGHTDATAPOS[0], FLIGHTDATAPOS[1] + (LINESPACE * 6)))
                #start the flight data timer
                if flight_data_timer != None: flight_data_timer.cancel()
                flight_data_timer = Timer(FLIGHTDATATIMEOUT, pygame.draw.rect, (screen, BLACK, FLIGHTDATARECT, 0))
                flight_data_timer.start()

    #wait for a while
    pygame.time.wait(10)

#stop
if flight_data_timer != None: flight_data_timer.cancel()
radar.stop()
pygame.quit()
