import colormaps as cmaps

def set_variables(var):

    if var == 'u' or var == 'u_anl':
        information = {}
        information.update({'name': 'uvmet'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 0})
        information.update({'lb_title': 'U ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'U component of wind'})
        
        levels = {}
        levels.update({925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({700: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({500: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({300: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({200: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})

    if var == 'u_inc':
        information = {}
        information.update({'lb_title': 'Increment of U ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})

        levels = {}
        levels.update({925: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({850: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({700: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({500: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({300: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({200: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
    
    if var == 'u10':
        information = {}
        information.update({'name': 'uvmet10'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 0})
        information.update({'lb_title': '10m U ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})

    if var == 'v' or var == 'v_anl':
        information = {}
        information.update({'name': 'uvmet'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 1})
        information.update({'lb_title': 'V ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'V component of wind'})

        levels = {}
        levels.update({925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({700: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.vik]})
        levels.update({500: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.vik]})
        levels.update({300: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({200: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})

    if var == 'v_inc':
        information = {}
        information.update({'lb_title': 'Increment of V ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})

        levels = {}
        levels.update({925: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({850: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({700: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({500: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({300: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({200: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})

    if var == 'v10':
        information = {}
        information.update({'name': 'uvmet10'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 1})
        information.update({'lb_title': '10m V ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})

    if var == 'wspd10':
        information = {}
        information.update({'name': 'uvmet10_wspd_wdir'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 0})
        information.update({'lb_title': '10m WSpd ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(0, 33, 4)], cmaps.vik]})

    if var == 't' or var == 't_anl':
        information = {}
        information.update({'name': 'temp'})
        information.update({'unit': 'K'})
        information.update({'lb_title': 'T (K)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})

        levels = {}
        levels.update({925: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({850: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({700: [[f'{float(i/1):.0f}' for i in range(274, 291, 2)], cmaps.lajolla]})
        levels.update({500: [[f'{float(i/1):.0f}' for i in range(262, 270, 1)], cmaps.lajolla]})
        levels.update({300: [[f'{float(i/2):.1f}' for i in range(464, 489, 3)], cmaps.lajolla]})
        levels.update({200: [[f'{float(i/2):.1f}' for i in range(424, 449, 3)], cmaps.lajolla]})

    if var == 't_inc':
        information = {}
        information.update({'name': 'temp'})
        information.update({'unit': 'K'})
        information.update({'lb_title': 'Increment of T (K)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})

        levels = {}
        levels.update({925: [[f'{float(i/10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})
        levels.update({850: [[f'{float(i/10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})
        levels.update({700: [[f'{float(i/10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})
        levels.update({500: [[f'{float(i/10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})
        levels.update({300: [[f'{float(i/10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})
        levels.update({200: [[f'{float(i/10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})

    if var == 'q' or var == 'q_anl':
        information = {}
        information.update({'name': 'QVAPOR'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'WV MR ($\mathregular{gkg^{-1}}$)'})
        information.update({'factor': 1000.0})
        information.update({'extend': 'max'})

        levels = {}
        levels.update({925: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({850: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({700: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'q_inc':
        information = {}
        information.update({'name': 'QVAPOR'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Increment of WV MR ($\mathregular{gkg^{-1}}$)'})
        information.update({'factor': 1000.0})
        information.update({'extend': 'both'})

        levels = {}
        levels.update({925: [[f'{float(i/ 10):.1f}' for i in range(-32, 33, 8)], cmaps.cork]})
        levels.update({850: [[f'{float(i/ 10):.1f}' for i in range(-20, 21, 5)], cmaps.cork]})
        levels.update({700: [[f'{float(i/ 10):.1f}' for i in range(-12, 13, 3)], cmaps.cork]})
        levels.update({500: [[f'{float(i/ 10):.1f}' for i in range(-8,   9, 2)], cmaps.cork]})
        levels.update({300: [[f'{float(i/ 10):.1f}' for i in range(-4,   5, 1)], cmaps.cork]})
        levels.update({200: [[f'{float(i/100):.2f}' for i in range(-4,   5, 1)], cmaps.cork]})

    if var == 'avo':
        information = {}
        information.update({'name': 'avo'})
        information.update({'unit': 's-1'})
        information.update({'lb_title': 'Absolute vorticity ($\mathregular{10^{-4}s^{-1}}$)'})
        information.update({'factor': 10000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Absolute vorticity'})

        levels = {}
        levels.update({925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({700: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({500: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({300: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({200: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})

    if var == 'rh':
        information = {}
        information.update({'name': 'rh'})
        information.update({'unit': '%'})
        information.update({'lb_title': 'Relative humidity (%)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Relative humidity'})

        levels = {}
        levels.update({925: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({850: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({700: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'geopt':
        information = {}
        information.update({'name': 'geopt'})
        information.update({'unit': 'gpm'})
        information.update({'lb_title': 'Geopotential height (m)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Geopotential height'})

        levels = {}
        levels.update({925: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({850: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({700: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'rain_6h':
        information = {}
        information.update({'name': ['RAINNC', 'RAINC']})
        information.update({'unit': 'null'})
        information.update({'lb_title': '6h accumulated rainfall (mm)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})

        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(0, 49, 6)], cmaps.prcp_2]})

    if var == 'slp':
        information = {}
        information.update({'name': 'slp'})
        information.update({'unit': 'ms-1'})
        information.update({'lb_title': 'Slp (hPa)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(1000, 1041, 5)], cmaps.vik]})