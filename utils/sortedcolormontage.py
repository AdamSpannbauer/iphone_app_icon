import cv2
from .resultsmontage import results_montage
from .colorutils import get_dominant_color


def create_sorted_color_montage(image_paths, tile_size=(100, 100),
                                images_per_main_axis=10, by_row=True,
                                color_processing_size=(25, 25),
                                verbose=False):
    # sort image paths
    image_paths = sorted(image_paths)

    # init dominant color store
    colors = []
    # iterate over ims
    for i, path in enumerate(image_paths):
        if verbose:
            print('processing image {} of {}'.format(i, len(image_paths)))
        # read in im i
        image = cv2.imread(path)
        # get dominant color
        color = get_dominant_color(cv2.cvtColor(image, cv2.COLOR_BGR2HSV), k=3,
                                   image_processing_size=color_processing_size)
        # store color
        colors.append(color)

    # sort colors (return list of image inds sorted)
    sorted_inds = sorted(range(len(colors)), key=lambda i: colors[i], reverse=True)

    # init montage
    montage = results_montage(
        image_size=tile_size,
        images_per_main_axis=images_per_main_axis,
        num_results=len(image_paths),
        by_row=by_row
    )

    # iter over sorted image inds
    for ind in sorted_inds:
        tile = cv2.resize(cv2.imread(image_paths[ind]), tile_size, interpolation=cv2.INTER_AREA)
        # add image i to montage
        montage.add_result(tile)

    return montage.montage
