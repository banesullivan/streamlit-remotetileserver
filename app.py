import json
from json.decoder import JSONDecodeError

import folium
import streamlit as st
from folium.plugins import Fullscreen
from localtileserver import RemoteTileClient, get_folium_tile_layer
from localtileserver.validate import (ValidateCloudOptimizedGeoTIFFException,
                                      validate_cog)
from streamlit_folium import folium_static

st.set_page_config(page_title="streamlit-remotetileserver")

"# streamlit-remotetileserver"

url = st.text_input(
    "Input a URL, try: https://data.kitware.com/api/v1/file/626854a14acac99f42126a74/download",
    placeholder="https://data.kitware.com/api/v1/file/626854a14acac99f42126a74/download",
)

with st.expander("Styling"):
    style_text = st.text_area(
        "Style dictionary",
        help="https://girder.github.io/large_image/tilesource_options.html#style",
    )
style = None
if style_text:
    try:
        style = json.loads(style_text)
    except JSONDecodeError:
        st.warning("Style is not valid JSON")


if url:
    client = RemoteTileClient(url)
    layer = get_folium_tile_layer(client, style=style)

    try:
        is_valid = validate_cog(client)
    except ValidateCloudOptimizedGeoTIFFException:
        is_valid = False
    st.write(f"Is valid Cloud Optimized GeoTiff?: {is_valid}")

    m = folium.Map(location=client.center(), zoom_start=client.default_zoom)
    m.add_child(layer)

    with st.sidebar:
        st.image(str(client.thumbnail()))
        st.write("Metadata")
        st.json(client.metadata())
else:
    with st.sidebar:
        pass
    m = folium.Map()

Fullscreen().add_to(m)

# call to render Folium map in Streamlit
folium_static(m)
