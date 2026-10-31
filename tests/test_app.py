from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_manual_flow():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=15).run()
    assert not app.exception
    assert "10 ideas" in app.subheader[0].value
    app.sidebar.selectbox[0].set_value("coily")
    app.sidebar.selectbox[1].set_value("long")
    app.sidebar.selectbox[2].set_value("low")
    app.run()
    assert not app.exception
    assert "0 ideas" in app.subheader[0].value
    assert any("No catalog" in warning.value for warning in app.warning)

def test_measurements_and_photo_modes():
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=15).run()
    app.radio[0].set_value("Enter measurements").run()
    assert not app.exception
    assert len(app.number_input) == 4
    app.radio[0].set_value("Analyze photo").run()
    assert not app.exception
    assert len(app.subheader) == 0
