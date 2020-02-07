boundaries = QgsProject.instance().mapLayersByName('bound')[0]
boundaries.startEditing()


num = 2
for f in boundaries.getFeatures():
    f['FID'] = num
    boundaries.updateFeature(f)
    num += 1
    
boundaries.commitChanges()
print("Done")

boundaries.stopEditing()