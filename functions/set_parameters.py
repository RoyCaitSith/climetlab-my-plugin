import colormaps as cmaps

def set_variables(var):
    information = {}
    information.update({'ua':     {'unit': 'ms-1', 'lb_title': 'ua (m/s)', 'factor': 1.0}})
    information.update({'va':     {'unit': 'ms-1', 'lb_title': 'va (m/s)', 'factor': 1.0}})
    information.update({'temp':   {'unit': 'K', 'lb_title': 'T (K)', 'factor': 1.0}})
    information.update({'QVAPOR': {'unit': 'null', 'lb_title': "QVAPOR " + "($\mathregular{gkg^{-1}}$)", 'factor': 1000.0}})

    levels = {}
    if 'ua' in var:
        levels.update({925: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({850: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({700: [['-20', '-15', '-10', '-5', '0', '5', '10', '15', '20'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({500: [['-20', '-15', '-10', '-5', '0', '5', '10', '15', '20'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({300: [['-32', '-24', '-16', '-8', '0', '8', '16', '24', '32'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({200: [['-32', '-24', '-16', '-8', '0', '8', '16', '24', '32'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
    if 'va' in var:
        levels.update({925: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({850: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({700: [['-12',  '-9',  '-6', '-3', '0', '3',  '6',  '9', '12'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({500: [['-12',  '-9',  '-6', '-3', '0', '3',  '6',  '9', '12'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({300: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({200: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
    if 'temp' in var:
        levels.update({925: [[  '284',   '287',   '290',   '293',   '296',   '299',   '302',   '305',   '308'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({850: [[  '284',   '287',   '290',   '293',   '296',   '299',   '302',   '305',   '308'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({700: [[  '274',   '276',   '278',   '280',   '282',   '284',   '286',   '288',   '290'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({500: [[  '262',   '263',   '264',   '265',   '266',   '267',   '268',   '269',   '270'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({300: [['232.0', '233.5', '235.0', '236.5', '238.0', '239.5', '241.0', '242.5', '244.0'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({200: [['212.0', '213.5', '215.0', '216.5', '218.0', '219.5', '221.0', '222.5', '224.0'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
    if 'QVAPOR' in var:
        levels.update({925: [['0',    '2',    '4',    '6',    '8',   '10',   '12',   '14',   '16'], cmaps.imola, ['-3.2', '-2.4', '-1.6', '-0.8', '0', '0.8', '1.6', '2.4', '3.2'], cmaps.cork]})
        levels.update({850: [['0',    '2',    '4',    '6',    '8',   '10',   '12',   '14',   '16'], cmaps.imola, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.cork]})
        levels.update({700: [['0',  '1.5',    '3',  '4.5',    '6',  '7.5',    '9', '10.5',   '12'], cmaps.imola, ['-1.2', '-0.9', '-0.6', '-0.3', '0', '0.3', '0.6', '0.9', '1.2'], cmaps.cork]})
        levels.update({500: [['0',    '1',    '2',    '3',    '4',    '5',    '6',    '7',    '8'], cmaps.imola, ['-0.8', '-0.6', '-0.4', '-0.2', '0', '0.2', '0.4', '0.6', '0.8'], cmaps.cork]})
        levels.update({300: [['0',  '0.1',  '0.2',  '0.3',  '0.4',  '0.5',  '0.6',  '0.7',  '0.8'], cmaps.imola, ['-0.4', '-0.3', '-0.2', '-0.1', '0', '0.1', '0.2', '0.3', '0.4'], cmaps.cork]})
        levels.update({200: [['0',  '0.1',  '0.2',  '0.3',  '0.4',  '0.5',  '0.6',  '0.7',  '0.8'], cmaps.imola, ['-0.4', '-0.3', '-0.2', '-0.1', '0', '0.1', '0.2', '0.3', '0.4'], cmaps.cork]})

    return (information[var], levels)