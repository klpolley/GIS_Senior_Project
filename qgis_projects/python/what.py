from qgis.utils import iface

def main():
    layer = iface.activeLayer()
    for feature in layer.getFeatures():
        attrs = feature.attributes()
        print(attrs[14])