#WASA-control file for snow routines;
a0	8.0092773439365e-07	Empirical coefficient (m/s); linear dependence of turbulent transfer coefficient (D) in sensible heat flux: D = a0 + a1*WindSpeed
a1	2.20251708149483e-05	Empirical coefficient (-)  ; linear dependence of turbulent transfer coefficient (D) in sensible heat flux: D = a0 + a1*WindSpeed
kSatSnow	0.00004	Saturated hydraulic conductivity of snow (m/s)
densDrySnow	450	Density of dry snow (kg/m³)
specCapRet	0.189949846858173	Capill. retention volume as fraction of solid SWE (-)
emissivitySnowMin	0.73965152664464	Minimum snow emissivity used for old snow (-)
emissivitySnowMax	0.99	Maximum snow emissivity used for new snow (-)
tempAir_crit	-2.10891411682448	Threshold temperature for rain-/snowfall (°C)
albedoMin	0.55	Minimum albedo used for old snow (-)
albedoMax	0.88	Maximum albedo used for new snow (-)
agingRate_tAirPos	0.00000111	Aging rate for air temperatures > 0 (1/s)
agingRate_tAirNeg	0.000000462	Aging rate for air temperatures < 0 (1/s)
soilDepth	0.1	Depth of interacting soil layer (m)
soilDens	1300	Density of soil (kg/m3)
soilSpecHeat	2.18	Spec. heat capacity of soil (kJ/kg/K)
weightAirTemp	0.92682685632386	Weighting param. for air temp. (-) in 0...1
lat	10	Latitude of centre of study area
lon	10	Longitude of centre of study area
do_rad_corr	.TRUE.	Modification of radiation with aspect and slope
do_alt_corr	.TRUE.	Modification of temperature with altitude of LU
tempLaps	-0.006	Temperature lapse rate for modification depending on elevation of TC (°C/m)
tempAmplitude	8	Temperature amplitude to simulate daily cycle (°C])
tempMaxOffset	2	Offset of daily temperature maximum from 12:00 (h)
snowFracThresh	0.02	Threshold to determine when TC snow covered (m)
