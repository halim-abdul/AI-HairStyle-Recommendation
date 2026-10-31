from io import BytesIO
import pytest
from PIL import Image
from hairstyle.vision import decode_image, analyze_image, MAX_BYTES
from hairstyle.preview import make_preview
from hairstyle.recommender import load_catalog

def encoded(format="PNG", size=(20,30), mode="RGBA"):
    buf = BytesIO()
    Image.new(mode, size).save(buf, format=format)
    return buf.getvalue()

def test_decode_normalizes():
    image = decode_image(encoded())
    assert image.mode == "RGB"
    assert image.size == (20,30)

def test_resize():
    assert decode_image(encoded(size=(2000,1000))).size == (1600,800)

@pytest.mark.parametrize("data", [b"", b"not an image", b"x"*(MAX_BYTES+1)])
def test_bad_upload(data):
    with pytest.raises(ValueError):
        decode_image(data)

def test_other_format():
    with pytest.raises(ValueError, match="JPEG and PNG"):
        decode_image(encoded(format="GIF", mode="RGB"))

def test_pixel_limit():
    with pytest.raises(ValueError, match="12 megapixels"):
        decode_image(encoded(size=(4000,3001), mode="RGB"))

def test_missing_model(tmp_path):
    with pytest.raises(ValueError, match="model missing"):
        analyze_image(Image.new("RGB",(20,20)), str(tmp_path/"absent.task"))

def test_all_previews():
    for style in load_catalog():
        figure = make_preview(style)
        assert len(figure.data) == 3
        assert figure.data[0].type == "surface"
        assert figure.data[1].type == "surface"
        assert len(figure.to_json()) > 100
