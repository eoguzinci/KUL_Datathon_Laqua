# Lecture on Geospatial Informaiton in R by Romaike Middendorp

XploData - data scientist
Utrecht

## Spatial data

* 80% of data is spatial data.
* Coordinate reference system (CRS)
    - latitude/long. (unprojected, e.g. WGS84)
    - X/Y coordinates (projected, e.g. UTM)

Time, spatial and data

### Spatial data objects

Vector data:

* Point/Node, -> weather stations
* Line, -> Roads,etc.
* Polygon. -> countries

Raster data: is the gridded data

* Single band
* Multi band (topography bands)

__Note:__ Don't use dataframe when dealing with spatial data.

`sp` package in R is specialized for that.
`sf` package in R is improve version of `sp`.

### Visualizing spatial data

`tmap`:

* similar with `ggplot`; a plot is built up in layers.

```r
tmap_mode('view')
tm_shape(active_leuven) + tmlines(col= "car", scale = 3) + 
```

`leaflet`:

```r
air_stations <- fromJSON()
```

### Spatialoperations on vector data

### Spatio-temporal data

`spacetime` package
`zoo` package for time series