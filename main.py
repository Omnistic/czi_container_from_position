import numpy as np
from czifile import CziFile
from xml.dom.minidom import parse, parseString

def get_container_centers_from_experiment(filepath):
    xml_data = parse(filepath)

    all_singletileregionarray = xml_data.getElementsByTagName("SingleTileRegionArray")

    container_names = []
    container_centers = []

    for singletileregionarray in all_singletileregionarray:
        container_name = singletileregionarray.getAttribute("Name")

        center_x = singletileregionarray.getElementsByTagName("CenterX")[0].firstChild.nodeValue
        center_y = singletileregionarray.getElementsByTagName("CenterY")[0].firstChild.nodeValue
        
        container_names.append(container_name)
        container_centers.append((float(center_x), float(center_y)))

    container_names = np.array(container_names)
    container_centers = np.array(container_centers)

    return container_names, container_centers

def get_singletileregions_from_czi(filepath):
    with CziFile(filepath) as czi:
        metadata = czi.metadata()

    xml_data = parseString(metadata)

    all_singletileregion = xml_data.getElementsByTagName("SingleTileRegion")

    tileregion_names = []
    tileregion_centers = []

    for singletileregion in all_singletileregion:
        tileregion_name = singletileregion.getAttribute("Name")

        center_x = singletileregion.getElementsByTagName("X")[0].firstChild.nodeValue
        center_y = singletileregion.getElementsByTagName("Y")[0].firstChild.nodeValue
        
        tileregion_names.append(tileregion_name)
        tileregion_centers.append((float(center_x), float(center_y)))

    tileregion_names = np.array(tileregion_names)
    tileregion_centers = np.array(tileregion_centers)

    return tileregion_names, tileregion_centers

def find_closest_container(position_x, position_y, container_names, container_centers):
    position = np.array([position_x, position_y])

    distances = np.linalg.norm(container_centers - position, axis=1)

    closest_index = np.argmin(distances)

    return container_names[closest_index], container_centers[closest_index]

if __name__ == "__main__":
    filepath_to_experiment_containing_well_positions = "F:\\well_positions.czexp"
    filepath_to_czi_image = "F:\\image.czi"

    container_names, container_centers = get_container_centers_from_experiment(filepath_to_experiment_containing_well_positions)
    position_names, positions = get_singletileregions_from_czi(filepath_to_czi_image)

    closest_names = []
    closest_centers = []

    for position_index, position in enumerate(positions):
        position_x, position_y = position
        closest_container_name, closest_container_center = find_closest_container(position_x, position_y, container_names, container_centers)

        closest_names.append(closest_container_name)
        closest_centers.append(closest_container_center)

    closest_names = np.array(closest_names)
    closest_centers = np.array(closest_centers)

    print(f"Number of well positions found in experiment: {len(container_names)}")
    print(f"Number of tile regions found in CZI: {len(position_names)}")

    for i in range(len(positions)):
        print(f"Position {position_names[i]} ({positions[i]}) is closest to container {closest_names[i]} ({closest_centers[i]})")

    print('hello')