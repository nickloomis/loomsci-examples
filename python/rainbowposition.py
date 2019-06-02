def solar_position():
  # https://en.wikipedia.org/wiki/Position_of_the_Sun
  # JD: julian date
  # n: number of days since Greenwich noon on 1 Jan 2000
  n = JD - 241545.0
  # L: mean longitude of the sun, in degrees
  L = 280.460 + 0.9856474 * n
  # g: mean anomaly of the sun's relative position (due to Earth's orbit), in deg
  g = 357.528 + 0.9856003 * n
  # note: may need to adjust L, g to [0, 360) deg by wrapping
  # lambda: ecliptic longitude, in degrees
  lambda = L + 1.915 * sind(g) + 0.020 * sind(2 * g)
  # beta, ecliptic latitude
  beta = 0
  # sun-earth distance in au
  R = 1.00014 - 0.01671 * cosd(g) - 0.00014 * cos(2*g)
  # lambda, beta, R form the complete position of the sun in ecliptic coords.
  # convert to equatorial coords..
  # epsilon: obliquity of orbit, in degrees (approx; can be calc'd with more precision)
  epsilon = 23.439 - 0.0000004 * n
  # alpha, right ascention
  alpha = atand(cosd(epsilon)*tand(lambda))  # alpha: same quadrant as lambda
  alpha = atan2(cosd(epsilon * sind(lambda), cosd(lambda)))  #...to get the right quadrant
  #declination:
  delta = asind(sind(epsilon) * sind(lambad))

  # from here, convert (alpha, delta) [right ascention, declination] in equatorial
  # coords to (alt, az) horizontal coords
  # https://en.wikipedia.org/wiki/Celestial_coordinate_system