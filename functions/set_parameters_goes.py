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
        information.update({'ERA5': 'u'})
        information.update({'HRES': ('U', '131_u.regn1280uv')})
        
        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})

    if var == 'u_inc':
        information = {}
        information.update({'lb_title': 'Inc. of U ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'U component of wind'})
        information.update({'ERA5': 'u'})
        information.update({'HRES': ('U', '131_u.regn1280uv')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
    
    if var == 'u10' or var == 'u10_anl':
        information = {}
        information.update({'name': 'uvmet10'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 0})
        information.update({'lb_title': '10m U ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': '10 metre U wind component'})
        information.update({'ERA5': 'u10'})
        
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
        information.update({'ERA5': 'v'})
        information.update({'HRES': ('V', '132_v.regn1280uv')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})

    if var == 'v_inc':
        information = {}
        information.update({'lb_title': 'Inc. of V ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'V component of wind'})
        information.update({'ERA5': 'v'})
        information.update({'HRES': ('V', '132_v.regn1280uv')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-4, 5, 1)], cmaps.vik]})

    if var == 'v10' or var == 'v10_anl':
        information = {}
        information.update({'name': 'uvmet10'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 1})
        information.update({'lb_title': '10m V ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': '10 metre V wind component'})
        information.update({'ERA5': 'v10'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})

    if var == 'wspd10' or var == 'wspd10_anl':
        information = {}
        information.update({'name': 'uvmet10_wspd_wdir'})
        information.update({'unit': 'ms-1'})
        information.update({'index': 0})
        information.update({'lb_title': '10m WSpd ($\mathregular{ms^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        information.update({'GFS': ['10 metre U wind component', '10 metre V wind component']})
        information.update({'ERA5': ['u10', 'v10']})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(0, 49, 3)], cmaps.wind_17lev]})

    if var == 't' or var == 't_anl':
        information = {}
        information.update({'name': 'temp'})
        information.update({'unit': 'K'})
        information.update({'lb_title': 'T (K)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Temperature'})
        information.update({'ERA5': 't'})
        information.update({'HRES': ('T', '130_t.regn1280sc')})
        
        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(284, 309, 3)], cmaps.lajolla]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(274, 291, 2)], cmaps.lajolla]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(274, 291, 2)], cmaps.lajolla]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(274, 291, 2)], cmaps.lajolla]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(262, 270, 1)], cmaps.lajolla]})
        levels.update({ 400: [[f'{float(i/2):.1f}' for i in range(464, 489, 3)], cmaps.lajolla]})
        levels.update({ 300: [[f'{float(i/2):.1f}' for i in range(464, 489, 3)], cmaps.lajolla]})
        levels.update({ 200: [[f'{float(i/2):.1f}' for i in range(424, 449, 3)], cmaps.lajolla]})
        levels.update({ 100: [[f'{float(i/2):.1f}' for i in range(424, 449, 3)], cmaps.lajolla]})

    if var == 't_inc':
        information = {}
        information.update({'name': 'temp'})
        information.update({'unit': 'K'})
        information.update({'lb_title': 'Inc. of T (K)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Temperature'})
        information.update({'ERA5': 't'})
        information.update({'HRES': ('T', '130_t.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/100):.2f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/100):.2f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/100):.2f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/ 10):.1f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/ 10):.1f}' for i in range( -4,  5, 1)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/ 10):.1f}' for i in range( -8,  9, 2)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/ 10):.1f}' for i in range(-20, 21, 5)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/ 10):.1f}' for i in range( -4,  5, 1)], cmaps.vik]})

    if var == 'q' or var == 'q_anl':
        information = {}
        information.update({'name': 'QVAPOR'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'WV MR ($\mathregular{gkg^{-1}}$)'})
        information.update({'factor': 1000.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Relative humidity'})
        information.update({'ERA5': 'q'})
        information.update({'HRES': ('Q', '133_q.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'q_inc':
        information = {}
        information.update({'name': 'QVAPOR'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of WV MR ($\mathregular{gkg^{-1}}$)'})
        information.update({'factor': 1000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Relative humidity'})
        information.update({'ERA5': 'q'})
        information.update({'HRES': ('Q', '133_q.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/100):.2f}' for i in range( -8,  9, 2)], cmaps.cork]})
        levels.update({ 975: [[f'{float(i/100):.2f}' for i in range( -8,  9, 2)], cmaps.cork]})
        levels.update({ 950: [[f'{float(i/100):.2f}' for i in range( -8,  9, 2)], cmaps.cork]})
        levels.update({ 925: [[f'{float(i/100):.2f}' for i in range( -8,  9, 2)], cmaps.cork]})
        levels.update({ 900: [[f'{float(i/100):.2f}' for i in range( -8,  9, 2)], cmaps.cork]})
        levels.update({ 850: [[f'{float(i/100):.2f}' for i in range(-12, 13, 3)], cmaps.cork]})
        levels.update({ 800: [[f'{float(i/ 10):.1f}' for i in range( -4,  5, 1)], cmaps.cork]})
        levels.update({ 700: [[f'{float(i/ 10):.1f}' for i in range( -4,  5, 1)], cmaps.cork]})
        levels.update({ 600: [[f'{float(i/ 10):.1f}' for i in range(-12, 13, 3)], cmaps.cork]})
        levels.update({ 500: [[f'{float(i/ 10):.1f}' for i in range( -8,  9, 2)], cmaps.cork]})
        levels.update({ 400: [[f'{float(i/ 10):.1f}' for i in range( -4,  5, 1)], cmaps.cork]})
        levels.update({ 300: [[f'{float(i/100):.2f}' for i in range(-12, 13, 3)], cmaps.cork]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.cork]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range( -4,  5, 1)], cmaps.cork]})

    if var == 'qc' or var == 'qc_anl':
        information = {}
        information.update({'name': 'QCLOUD'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'MR of cloud ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Cloud mixing ratio'})
        information.update({'ERA5': 'clwc'})

        levels = {}
        levels.update({1000: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/  1):.0f}' for i in range(0, 33, 4)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'qc_inc':
        information = {}
        information.update({'name': 'QCLOUD'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of cloud MR ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Cloud mixing ratio'})
        information.update({'ERA5': 'clwc'})

        levels = {}
        levels.update({1000: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 975: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 950: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 925: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 900: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 850: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 800: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 700: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 600: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 500: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 400: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 300: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 200: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 100: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})

    if var == 'qr' or var == 'qr_anl':
        information = {}
        information.update({'name': 'QRAIN'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'MR of rain ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Rain mixing ratio'})
        information.update({'ERA5': 'crwc'})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})

    if var == 'qr_inc':
        information = {}
        information.update({'name': 'QRAIN'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of rain MR ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Rain mixing ratio'})
        information.update({'ERA5': 'crwc'})

        levels = {}
        levels.update({1000: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 975: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 950: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 925: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 900: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 850: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 800: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 700: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 600: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 500: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 400: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 300: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})

    if var == 'qg' or var == 'qg_anl':
        information = {}
        information.update({'name': 'QGRAUP'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'MR of graupel ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Graupel'})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})

    if var == 'qg_inc':
        information = {}
        information.update({'name': 'QGRAUP'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of graupel MR ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Graupel'})

        levels = {}
        levels.update({1000: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 975: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 950: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 925: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 900: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 850: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 800: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 700: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 600: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 500: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 400: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 300: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})

    if var == 'qs' or var == 'qs_anl':
        information = {}
        information.update({'name': 'QSNOW'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'MR of snow ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Snow mixing ratio'})
        information.update({'ERA5': 'cswc'})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})

    if var == 'qs_inc':
        information = {}
        information.update({'name': 'QSNOW'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of snow MR ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Snow mixing ratio'})
        information.update({'ERA5': 'cswc'})

        levels = {}
        levels.update({1000: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 975: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 950: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 925: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 900: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 850: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 800: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 700: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 600: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 500: [[f'{float(i/100):.2f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 400: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 300: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(-4, 5, 1)], cmaps.cork]})

    if var == 'qi' or var == 'qi_anl':
        information = {}
        information.update({'name': 'QICE'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'MR of ice ($\mathregular{10^{-3} gkg^{-1}}$)'})
        information.update({'factor': 1000000.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Ice water mixing ratio'})
        information.update({'ERA5': 'ciwc'})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(0, 9, 1)], cmaps.imola]})

    if var == 'qi_inc':
        information = {}
        information.update({'name': 'QICE'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of ice MR ($\mathregular{10^{-2} gkg^{-1}}$)'})
        information.update({'factor': 100000.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Ice water mixing ratio'})
        information.update({'ERA5': 'ciwc'})

        levels = {}
        levels.update({1000: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 975: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 950: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 925: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 900: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 850: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 800: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 700: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 600: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 500: [[f'{float(i/10):.1f}' for i in range(-8, 9, 2)], cmaps.cork]})
        levels.update({ 400: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 300: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 200: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})
        levels.update({ 100: [[f'{float(i/10):.1f}' for i in range(-4, 5, 1)], cmaps.cork]})

    if var == 'avo' or var == 'avo_anl':
        information = {}
        information.update({'name': 'avo'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Abs. vor. ($\mathregular{10^{-5}s^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Absolute vorticity'})
        information.update({'ERA5': 'vo'})
        information.update({'HRES': ('VO', '138_vo.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})

    if var == 'avo_inc':
        information = {}
        information.update({'name': 'avo'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of Abs. vor. ($\mathregular{10^{-5}s^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Absolute vorticity'})
        information.update({'ERA5': 'vo'})
        information.update({'HRES': ('VO', '138_vo.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})

    if var == 'rvo' or var == 'rvo_anl':
        information = {}
        information.update({'name': 'vo'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Rel. vor. ($\mathregular{10^{-5}s^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Absolute vorticity'})
        information.update({'ERA5': 'vo'})
        information.update({'HRES': ('VO', '138_vo.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-16, 17, 4)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-20, 21, 4)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-32, 33, 8)], cmaps.vik]})

    if var == 'rvo_inc':
        information = {}
        information.update({'name': 'vo'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of Rel. vor. ($\mathregular{10^{-5}s^{-1}}$)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Absolute vorticity'})
        information.update({'ERA5': 'vo'})
        information.update({'HRES': ('VO', '138_vo.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(-8, 9, 2)], cmaps.vik]})

    if var == 'rh' or var == 'rh_anl':
        information = {}
        information.update({'name': 'rh'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'RH (%)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Relative humidity'})
        information.update({'ERA5': 'r'})
        information.update({'HRES': ('R', '157_r.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 400: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 300: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 200: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})
        levels.update({ 100: [[f'{float(i/1):.0f}' for i in range(0, 101, 10)], cmaps.div3_green_brown_r]})

    if var == 'rh_inc':
        information = {}
        information.update({'name': 'rh'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of RH (%)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Relative humidity'})
        information.update({'ERA5': 'r'})
        information.update({'HRES': ('R', '157_r.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 975: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 950: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 925: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 900: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 850: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 800: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 700: [[f'{float(i/1):.0f}' for i in range( -4,  5, 1)], cmaps.div3_green_brown_r]})
        levels.update({ 600: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.div3_green_brown_r]})
        levels.update({ 500: [[f'{float(i/1):.0f}' for i in range(-12, 13, 3)], cmaps.div3_green_brown_r]})
        levels.update({ 400: [[f'{float(i/1):.1f}' for i in range(-12, 13, 3)], cmaps.div3_green_brown_r]})
        levels.update({ 300: [[f'{float(i/1):.1f}' for i in range(-12, 13, 3)], cmaps.div3_green_brown_r]})
        levels.update({ 200: [[f'{float(i/1):.2f}' for i in range(-12, 13, 3)], cmaps.div3_green_brown_r]})
        levels.update({ 100: [[f'{float(i/1):.2f}' for i in range(-12, 13, 3)], cmaps.div3_green_brown_r]})

    if var == 'geopt' or var == 'geopt_anl':
        information = {}
        information.update({'name': 'geopt'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'H (gpm)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Geopotential Height'})
        information.update({'ERA5': 'z'})
        information.update({'HRES': ('Z', '129_z.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'geopt_inc':
        information = {}
        information.update({'name': 'geopt'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'Inc. of Z (gpm)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'both'})
        information.update({'GFS': 'Geopotential Height'})
        information.update({'ERA5': 'z'})
        information.update({'HRES': ('Z', '129_z.regn1280sc')})

        levels = {}
        levels.update({1000: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 975: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 950: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 925: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 900: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 850: [[f'{float(i/  1):.0f}' for i in range(0, 17, 2)], cmaps.imola]})
        levels.update({ 800: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 700: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 600: [[f'{float(i/  2):.0f}' for i in range(0, 25, 3)], cmaps.imola]})
        levels.update({ 500: [[f'{float(i/  1):.0f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 400: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 300: [[f'{float(i/ 10):.1f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 200: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})
        levels.update({ 100: [[f'{float(i/100):.2f}' for i in range(0,  9, 1)], cmaps.imola]})

    if var == 'rain_6h':
        information = {}
        information.update({'name': ['RAINNC', 'RAINC']})
        information.update({'unit': 'null'})
        information.update({'lb_title': '6h accumulated rainfall (mm)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Precipitation rate'})
        information.update({'ERA5': 'tp'})

        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(0, 109, 6)], cmaps.prcp_2]})

    if var == 'sp' or var == 'sp_anl':
        information = {}
        information.update({'name': 'PSFC'})
        information.update({'unit': 'null'})
        information.update({'lb_title': 'SP (hPa)'})
        information.update({'factor': 0.01})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Surface pressure'})
        information.update({'ERA5': 'sp'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(1000, 1041, 5)], cmaps.vik]})

    if var == 'slp' or var == 'slp_anl':
        information = {}
        information.update({'name': 'slp'})
        information.update({'unit': 'hPa'})
        information.update({'lb_title': 'SLP (hPa)'})
        information.update({'factor': 1.0})
        information.update({'extend': 'max'})
        information.update({'GFS': 'Pressure reduced to MSL'})
        information.update({'ERA5': 'msl'})
        
        levels = {}
        levels.update({9999: [[f'{float(i/1):.0f}' for i in range(1000, 1041, 5)], cmaps.vik]})
    
    return (information, levels)