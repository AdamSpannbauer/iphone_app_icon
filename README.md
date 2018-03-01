# iPhone App Icons

<p align='center'>
  <kbd>
    <img src='readme/sorted_app_icons.jpg', width=600>
  </kbd>
</p>

Repo for playing around with App Store app icons. Current scripts in repo:
* [`download_top_chart_icons.py`](/download_top_chart_icons.py): script to download top chart app icons (**output in [icons dir](/icons)**)
* [`sort_icons_by_color.py`](/sort_icons_by_color.py): sort app icons by hsv color space (**output shown above**)
* [`icon_cluster_color_bovw_kmeans.py`](/icon_cluster_color_bovw_kmeans.py): use k means to cluster app icons by colors and/or keypoint features in the form of a bag of visual words  (**output shown below**)

## Cluster output highlights

### Using only keypoint features

Below are 2 results from clustering using only the keypoint features (while ignoring color features).  You can see the focus on similar shapes/patterns that appear in the icons.  On the left we can see the Tidal & Dropbox logo designs focus on repeating diamond patterns.  On the left we can see similiarities in the sharp corners below a human-ish body and the 'stars' in the top of the icons.

<p align='center'>
  <kbd>
    <img src='readme/dropbox_tidal_bovw_cluster.jpg'>
  </kbd>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <kbd>
    <img src='readme/monumentvalley_parkourflight_bovw_cluster.jpg'>
  </kbd>
</p>


### Using only color features

Below are 2 results from clustering using only the color features (while ignoring keypoint features).  Interestingly, the icons in the cluster on the left show a very similar art style (for the most part) in addition to their similar colors that caused them to be grouped together.

<p align='center'>
  <kbd>
    <img src='readme/realistic_face_color_cluster.jpg' height=200>
  </kbd>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <kbd>
    <img src='readme/yellow_color_cluster.jpg'>
  </kbd>
</p>


### Using keypoint and color features

Below are 2 results from clustering using both the keypoint and color features.

<p align='center'>
  <kbd>
    <img src='readme/scribblenauts_bovw_color_cluster.jpg'>
  </kbd>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <kbd>
    <img src='readme/homescapes_myshelf_bovw_color_cluster.jpg' height=200>
  </kbd>
</p>
