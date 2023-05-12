import numpy as np
import cv2 as cv


class town:
    def __init__(self, size:int = 4):
        self.size = size
        self.map = np.arange(1, size*size+1).reshape(size, size)
        self.img = None
        self.img_base = None

    def connect_crossroads(self, debug =False):
        result = []
        for x in range(self.size):
            for y in range(self.size):
                point_connections = []
                try:
                    point_connections.append(np.array([self.map[x-1,y], True, np.array([])]))
                except:
                    pass                
                try:
                    point_connections.append(np.array([self.map[x+1,y], True, np.array([])]))
                except:
                    pass                
                try:
                    point_connections.append(np.array([self.map[x,y-1], True, np.array([])]))
                except:
                    pass                
                try:
                    point_connections.append(np.array([self.map[x,y+1], True, np.array([])]))
                except:
                    pass
                result.append(np.array([self.map[x, y], point_connections]))
        self.map = np.array(result).reshape(self.size, self.size, 2) 

        if debug:
            print(self.map)
        


    def render_map(self, zoom: int = 10, road_lenght: int = 10, debug: bool = False):
        self.img_size = self.size*4+road_lenght*(self.size-1)
        self.img_base = np.full((self.img_size, self.img_size, 3), (255,255,255), dtype = np.uint8)
        self.road_lenght = road_lenght
        for x in range(self.size):
            for y in range(self.size):
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4),y*(road_lenght+4)), (x*(road_lenght+4)+3, y*(road_lenght+4)+3), (0,0,127), -1)      #skrzyzowanie
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4)+4,y*(road_lenght+4)), (x*(road_lenght+4)+4, y*(road_lenght+4)), (0,0,0), -1)        #swiatlo praw
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4),y*(road_lenght+4)-1), (x*(road_lenght+4), y*(road_lenght+4)-1), (0,0,0), -1)    #swiatlo dolne
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4)+3,y*(road_lenght+4)+4), (x*(road_lenght+4)+3, y*(road_lenght+4)+4), (0,0,0), -1)    #swiatlo dolne
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4)-1,y*(road_lenght+4)+3), (x*(road_lenght+4)-1, y*(road_lenght+4)+3), (0,0,0), -1)    #swiatlo lewe  
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4)+4,y*(road_lenght+4)+1), (x*(road_lenght+4)+(road_lenght+4), y*(road_lenght+4)+2), (100,100,100), -1) #droga pozioma 
                self.img_base = cv.rectangle(self.img_base,(x*(road_lenght+4)+1,y*(road_lenght+4)+4), (x*(road_lenght+4)+2, y*(road_lenght+4)+(road_lenght+4)), (100,100,100), -1) #droga pozioma 
        if debug:
            cv.imshow("mapa", cv.resize(self.img_base,[zoom*self.img_size, zoom*self.img_size], interpolation=cv.INTER_AREA))
            cv.waitKey(2000)
        
    def show_map(self,zoom: int = 10, debug: bool = False):
        self.img = self.img_base.copy()
        for x, line in enumerate(self.map):
            for y, crossroad in enumerate(line):
                crossroad_name = crossroad[0]
                for connected_crossroad in crossroad[1]:
                    connected_crossroad_name = connected_crossroad[0]
                    connected_crossroad_state = connected_crossroad[1]
                    conected_crossroad_cars_list = connected_crossroad[2]

                    x_pos = x*(self.road_lenght+4)
                    y_pos = y*(self.road_lenght+4)

                    if crossroad_name == connected_crossroad_name - 1: #skrzyzowanie w prawo

                        x_pos = x_pos + 3 + self.road_lenght
                        y_pos = y_pos + 3
                    else:    
                        if crossroad_name == connected_crossroad_name - self.size:     #skrzyzowanie w dol
                            x_pos = x*(self.road_lenght+4)
                            y_pos = y*(self.road_lenght+4)
                            y_pos = y_pos +3 +self.road_lenght
                        else:
                            if crossroad_name == connected_crossroad_name + 1:  #skrzyzowanie w lewo
                                x_pos = x*(self.road_lenght+4)
                                y_pos = y*(self.road_lenght+4)
                                x_pos -= self.road_lenght
                            else:
                                if crossroad_name == connected_crossroad_name + self.size:     # skrzyzowanie w gore
                                    x_pos = x*(self.road_lenght+4)
                                    y_pos = y*(self.road_lenght+4)
                                    x_pos = x_pos +3
                                    y_pos = y_pos -self.road_lenght

                    if connected_crossroad_state:
                        light_color = [0, 255, 0]
                    else:
                        light_color = [0, 0, 255]

                    self.img = cv.rectangle(self.img,(x_pos, y_pos), (x_pos, y_pos), light_color, -1)    #swiatlo dolne
        cv.imshow("mapa", cv.resize(self.img,[zoom*self.img_size, zoom*self.img_size], interpolation=cv.INTER_AREA))
        cv.waitKey(20000)



                        

                    

    
    




lodz = town(4)
lodz.connect_crossroads(debug=True)
lodz.render_map(debug=False)
lodz.show_map()
