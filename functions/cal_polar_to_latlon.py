import math

def Cal_LatLon(lat_c, lon_c, radius, angle):

    a = 6378137.0
    b = 6356752.3142
    f = 1/298.2572236
    Alpha1 = math.radians(angle)
    sinAlpha1 = math.sin(Alpha1)
    cosAlpha1 = math.cos(Alpha1)
    tanU1 = (1-f)*math.tan(math.radians(lat_c))
    cosU1 = 1/math.sqrt((1+tanU1*tanU1))
    sinU1 = tanU1*cosU1
    sigma1 = math.atan2(tanU1,cosAlpha1)
    sinAlpha = cosU1*sinAlpha1
    cosSqAlpha = 1-sinAlpha*sinAlpha
    uSq = cosSqAlpha*(a*a-b*b)/(b*b)
    A = 1+uSq/16384.0*(4096.0+uSq*(-768.0+uSq*(320.0-175.0*uSq)))
    B = uSq/1024.0*(256.0+uSq*(-128.0+uSq*(74.0-47.0*uSq)))
    cos2SigmaM=0.0
    sinSigma=0.0
    cosSigma=0.0
    sigma = radius*1000.0/(b*A)
    sigmaP = 2.0*math.pi
    while math.fabs(sigma-sigmaP)>1e-12:
        cos2SigmaM = math.cos(2*sigma1+sigma)
        sinSigma = math.sin(sigma)
        cosSigma = math.cos(sigma)
        deltaSigma = B*sinSigma*(cos2SigmaM+B/4.0*(cosSigma*(-1.0+2.0*cos2SigmaM*cos2SigmaM)-B/6.0*cos2SigmaM*(-3.0+4.0*sinSigma*sinSigma)*(-3.0+4.0*cos2SigmaM*cos2SigmaM)))
        sigmaP = sigma
        sigma = radius*1000.0/(b*A)+deltaSigma

    tmp = sinU1*sinSigma-cosU1*cosSigma*cosAlpha1
    lat = math.atan2(sinU1*cosSigma+cosU1*sinSigma*cosAlpha1, (1.0-f)*math.sqrt(sinAlpha*sinAlpha+tmp*tmp))
    lamb = math.atan2(sinSigma*sinAlpha1, cosU1*cosSigma-sinU1*sinSigma*cosAlpha1)
    C = f/16.0*cosSqAlpha*(4.0+f*(4.0-3.0*cosSqAlpha))
    L = lamb-(1.0-C)*f*sinAlpha*(sigma+C*sinSigma*(cos2SigmaM+C*cosSigma*(-1.0+2.0*cos2SigmaM*cos2SigmaM)))
    revAz = math.atan2(sinAlpha, -tmp)
    lat = math.degrees(lat)
    lon = lon_c+math.degrees(L)
    return [lat, lon]
