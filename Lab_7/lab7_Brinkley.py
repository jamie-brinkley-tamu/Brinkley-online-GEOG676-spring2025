import arcpy

# Assign Bands
source = r"C:\Users\SuperNova\Nextcloud\GISProgramming\Lab7\Data"
band1 = arcpy.sa.Raster(source + r"\band1.tif") # Blue
band2 = arcpy.sa.Raster(source + r"\band2.tif") # Green
band3 = arcpy.sa.Raster(source + r"\band3.tif") # Red
band4 = arcpy.sa.Raster(source + r"\band4.tif") # NIR
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\output_combined.tif")

# Hillside
azimuth = 315
altitude = 45
shadows = 'NO_SHADOWS'
z_factor = 1
arcpy.ddd.HillShade(source + r"\DEM.tif",source + r"\output_Hillshade.tif", azimuth, altitude, shadows, z_factor)

# Slope
output_measurement = "DEGREE"
z_factor = 1
arcpy.ddd.Slope(source + r"\DEM.tif",source + r"\output_Slope.tif",output_measurement, z_factor)
print("success!")