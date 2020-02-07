import math

#uri = '/Users/katie/Senior_Project/gerrymandering/help/congress113.gpkg'
#join_layer = iface.addVectorLayer(uri, 'Compactness', 'ogr')	#adds layer to map

join_layer = iface.activeLayer()

def calculate_compactness():

    with edit(join_layer):
        #layer_provider=join_layer.dataProvider()
        #layer_provider.addAttributes([QgsField("compactness",QVariant.Double)])
        #join_layer.updateFields()
        for feature in join_layer.getFeatures():
            perimeter = feature['perimeter']
            area = feature['area']
            if perimeter == NULL: continue
            circle = perimeter**2 / 4 * math.pi
            feature.setAttribute(feature.fieldNameIndex('compactness'), area/circle)
            join_layer.updateFeature(feature)
    print("Calculated Compactness")
    
    
def calculate_index():

    with edit(join_layer):
        #layer_provider=join_layer.dataProvider()
        #layer_provider.addAttributes([QgsField("index",QVariant.Double)])
        #join_layer.updateFields()
        for feature in join_layer.getFeatures():
            comp = feature['compactness']
            if comp == NULL: continue
            index = 100 - (100*comp)
            feature.setAttribute(feature.fieldNameIndex('index'), index)
            join_layer.updateFeature(feature)
    print("Calculated Index")

#calculate_compactness()
calculate_index()