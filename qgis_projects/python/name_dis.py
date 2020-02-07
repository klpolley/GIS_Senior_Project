from qgis.utils import iface

join_layer = iface.activeLayer()

def set_name():

    with edit(join_layer):
        layer_provider=join_layer.dataProvider()
        layer_provider.addAttributes([QgsField("name",QVariant.String)])
        join_layer.updateFields()
        for feature in join_layer.getFeatures():
            state = feature['statename']
            district = feature['district']
            name = state + " " + str(district)
            feature.setAttribute(feature.fieldNameIndex('name'), name)
            join_layer.updateFeature(feature)
    print("Done!")

set_name()
    