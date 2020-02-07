from qgis.utils import iface
from PyQt5.QtCore import QVariant

_NAME_FIELD = 'name'

# Names of the new fields to be added to the layer
_NEW_NEIGHBORS_FIELD = 'borders'

districts = QgsProject.instance().mapLayersByName('Compactness congress113')[0]
boundaries = QgsProject.instance().mapLayersByName('bound')[0]

# Create 2 new fields in the layer that will hold the list of neighbors and sum
# of the chosen field.
districts.startEditing()
#districts.dataProvider().addAttributes(
#        [QgsField(_NEW_NEIGHBORS_FIELD, QVariant.String)])
#districts.updateFields()
# Create a dictionary of all features

dist_feats = {f.id(): f for f in districts.getFeatures()}
bound_feats = {f.id(): f for f in boundaries.getFeatures()}

# Build a spatial index
index = QgsSpatialIndex()
for f in bound_feats.values():
    index.insertFeature(f)

# Loop through all features and find features that touch each feature
for f in dist_feats.values():
    print ('Working on %s' % f[_NAME_FIELD])
    geom = f.geometry()
    # Find all features that intersect the bounding box of the current feature.
    # We use spatial index to find the features intersecting the bounding box
    # of the current feature. This will narrow down the features that we need
    # to check neighboring features.
    intersecting_ids = index.intersects(geom.boundingBox())
    # Initalize neighbors list and sum
    neighbors = []
    
    for intersecting_id in intersecting_ids:
        # Look up the feature from the dictionary
        intersecting_f = bound_feats[intersecting_id]

        # For our purpose we consider a feature as 'neighbor' if it touches or
        # intersects a feature. We use the 'disjoint' predicate to satisfy
        # these conditions. So if a feature is not disjoint, it is a neighbor.
        if (f != intersecting_f and not intersecting_f.geometry().disjoint(geom)):
            neighbors.append(str(intersecting_f['FID']))
    f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
    # Update the layer with new attribute values.
    districts.updateFeature(f)

districts.commitChanges()
print ('Processing complete.')
