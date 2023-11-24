"""
Martin O'Hanlon
www.stuffaboutcode.com

Pygame radar

Attribution:

Some radar code - http://simpson.edu/computer-science/
Circle on line equation - http://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm

"""

import pygame
import math
import threading

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class Radar(threading.Thread):
    
    def __init__(self, screen, radar_rect, radar_pos = (0, 0), scale = 1,
                 back_col = BLACK, radar_col = GREEN):

        #setup threading
        threading.Thread.__init__(self)

        self.screen = screen
        self.radar_rect = radar_rect
        self.centre = (radar_rect[0] + (radar_rect[2] / 2),
                       radar_rect[1] + (radar_rect[3] / 2))
        self.sweeplen = (radar_rect[2] / 2)
        self.radar_pos = radar_pos
        self.scale = scale

        self.back_col = back_col
        self.radar_col = radar_col
        
        self.running = False
        self.stopped = True

        self.dots = {}

    def run(self):
        self.running = True
        self.stopped = False

        angle = 0

        #TODO - set the back of the radar to the back colour

        while not self.stopped:
        
            # Calculate the x,y for the end point of our 'sweep' based on the current angle
            x = self.centre[0] + math.sin(angle) * self.sweeplen
            y = self.centre[1] + math.cos(angle) * self.sweeplen

            # Draw the line from the center at 145, 145 to the calculated end spot
            pygame.draw.line(self.screen, self.radar_col, [self.centre[0], self.centre[1]], [x, y], 2)

            self._display_dots_on_line(self.centre[0], self.centre[1], x, y)
            
            # Draw the outline of a circle to 'sweep' the line around
            pygame.draw.ellipse(self.screen, self.radar_col, self.radar_rect, 2)

            #update the display, wait for the next frame
            pygame.display.update()
            pygame.time.Clock().tick(60)

            #redraw the line in black to clear it
            pygame.draw.line(self.screen, self.back_col, [self.centre[0], self.centre[1]], [x, y], 2)

            # Increase the angle by 0.03 radians
            angle = angle + .03

            # If we have done a full sweep, reset the angle to 0
            if angle > 2 * math.pi:
                angle = angle - 2 * math.pi

        self.running = False

    def stop(self):
        self.stopped = True

        #stop the dots
        for key, dot in self.dots.items():
            dot.stop()

        #wait till its stopped
        while(self.running):
            pygame.time.wait(10)

    def dot_add(self, dot_id, x, y, data = None, back_col = None, dot_col = None):
        if back_col == None: back_col = self.back_col
        if dot_col == None: dot_col = self.radar_col
        #work out x, y on screen
        screen_x, screen_y = self._calc_screen_x_y(x, y)
        
        #does the dot already exist?
        if dot_id in self.dots:
            dot = self.dots[dot_id]
            dot.move(screen_x, screen_y)
        else:                
            dot = RadarDot(self.screen, screen_x, screen_y, 10, data = data, back_col = back_col, dot_col = dot_col)
            self.dots[dot_id] = dot

    def dot_remove(self, dot_id):
        if dot_id in self.dots:
            del self.dots[dot_id]

    def dot_move(self, dot_id, x, y):
        screen_x, screen_y = self._calc_screen_x_y(x, y)
        self.dots[dot_id].move(screen_x, screen_y)

    def dot_move_by(self, dot_id, x, y):
        self.dots[dot_id].move_by(x, y)

    def _calc_screen_x_y(self, x, y):
        diff_x = (x - self.radar_pos[0]) * self.scale
        diff_y = (y - self.radar_pos[1]) * self.scale
        screen_x = int(round(self.centre[0] + diff_x, 0))
        screen_y = int(round(self.centre[1] + diff_y, 0))
        return screen_x, screen_y

    def _display_dots_on_line(self, x1, y1, x2, y2):
        for key, dot in self.dots.copy().items():
            if dot.fade_step == 0 or dot.fade_step > 50:
                intersect, pos = dot.on_line(x1, y1, x2, y2)
                if intersect == True:
                    dot.show()

    def dot_at_point(self, point):
        dot_found = None
        for key, dot in self.dots.copy().items():
            if dot.rect.collidepoint(point):
                dot_found = key
        return dot_found

    def set_scale(self, new_scale):
        self.scale = new_scale
        for key, dot in self.dots.copy().items():
            self.dot_move(key, dot.x, dot.y)
            

class RadarDot():
 
    def __init__(self, screen, x, y, radius,
                 back_col = BLACK, dot_col = GREEN,
                 fade_time = 4000, no_of_fade_steps = 100, data = None):
        
        self.screen = screen
        
        self.radius = radius
        self.move(x, y)
        
        self.back_col = back_col
        self.dot_col = dot_col
        
        self.fade_time = fade_time
        self.no_of_fade_steps = no_of_fade_steps
        self.fade_step = 0
        self.fade_running = False

        self.data = data
        
    def show(self):
        #if the fade is running
        if self.fade_running:
            #reset the fade
            self.fade_step = 0
        else:
            #start the fade again
            self.fade_thread = threading.Thread(target = self._fade)
            self.fade_thread.start()
        
    def _fade(self):
        #calc fade steps
        fade_steps = self._calc_fade(self.dot_col, self.back_col, self.no_of_fade_steps)
        fade_delay = int(self.fade_time / self.no_of_fade_steps)

        #keep fading out the dot until it disappears or its stopped
        now = pygame.time.get_ticks()
        self.fade_step = 0
        self.fade_running = True

        #keep fading the dot until its the back col or its stopped
        while self.fade_step < (len(fade_steps) - 1) and self.fade_running == True:
            
            #where am i drawing the dot this time?
            lastx, lasty = self.x, self.y
            pygame.draw.ellipse(self.screen,
                                fade_steps[self.fade_step],
                                (lastx - self.radius, lasty - self.radius, self.radius, self.radius), 0)
            
            #pygame.display.update()

            #wait until the next time or the fade is stopped
            till = now + fade_delay
            while till > pygame.time.get_ticks() and self.fade_running == True:
                pygame.time.wait(10)
            now = till
            
            #draw over the last ellipse in black
            pygame.draw.ellipse(self.screen,
                                self.back_col,
                                (lastx - self.radius, lasty - self.radius, self.radius, self.radius), 0)

            self.fade_step += 1

        self.fade_running = False
        #pygame.display.update()
        

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius, self.radius)

    def move_by(self, x, y):
        self.move(self.x + x, self.y + y)
        
    def _calc_fade(self, start_rgb, end_rgb, steps):
        #work out the number of colours and steps
        r_step = (end_rgb[0] - start_rgb[0]) / steps
        g_step = (end_rgb[1] - start_rgb[1]) / steps
        b_step = (end_rgb[2] - start_rgb[2]) / steps
        rgb_steps = []
        rgb_steps.append(start_rgb)
        for step in range(1, steps):
            last_rgb = rgb_steps[step - 1]
            this_rgb = (last_rgb[0] + r_step,
                        last_rgb[1] + g_step,
                        last_rgb[2] + b_step)
            rgb_steps.append(this_rgb)
        rgb_steps.append(end_rgb)
        return rgb_steps

    def stop(self):
        #if the fade is running, stop it
        if self.fade_running:
            self.fade_running = False
            self.fade_thread.join()

    def on_line(self, x1, y1, x2, y2):
        Q = pygame.math.Vector2(self.x, self.y)
        r = self.radius
        P1 = pygame.math.Vector2(x1, y1)
        V = pygame.math.Vector2(x2, y2) - P1

        a = V.dot(V)
        b = 2 * V.dot(P1 - Q)
        c = P1.dot(P1) + Q.dot(Q) - 2 * P1.dot(Q) - r**2

        disc = b**2 - 4 * a * c
        if disc < 0:
            return False, None

        sqrt_disc = math.sqrt(disc)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)

        if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
            return False, None

        t = max(0, min(1, - b / (2 * a)))
        return True, P1 + t * V

if __name__ == "__main__":

    pygame.init()

    # Set the height and width of the screen
    SIZE = [480, 320]
    BORDER = 10

    #create the screen
    screen = pygame.display.set_mode(SIZE)

    # Set the screen background
    screen.fill(BLACK)

    # Dimensions and location of radar sweep
    radar_rect = [BORDER, BORDER, SIZE[0] - (BORDER * 2), SIZE[1] - (BORDER * 2)]

    radar = Radar(screen, radar_rect)
    radar.start()
    radar.dot_add(1, -200, -200)
    radar.dot_add(2, 200, 200)
    radar.dot_add(3, -200, 250)
    
    # Loop until the user clicks the close button.
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.time.wait(75)
        radar.dot_move_by(1, 1, 1.5)
        radar.dot_move_by(2, -1.4, -1)
        radar.dot_move_by(3, 0, -1.5)

    radar.stop()

    pygame.quit()
