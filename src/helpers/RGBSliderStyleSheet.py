RgbSliderStyleSheet = """

    QSlider::groove:horizontal {
        border: 1px solid #000000;
        background: white;
        height: 15px;
        border-radius: 5px;
    }

    QSlider::add-page:horizontal {
        background: #FFFFFF;
        border: 1px solid #4C4B4B;
        height: 10px;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop: 0 #EEEEEE, stop: 1 #CCCCCC);
        border: 1px solid #4C4B4B;
        width: 13px;
        margin-top: -3px;
        margin-bottom: -3px;
        border-radius: 4px;
    }

    QSlider::handle:horizontal:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop: 0 #FFFFFF, stop: 1 #DDDDDD);
        border: 1px solid #393838;
        border-radius: 4px;
    }

    QSlider#Red::sub-page:horizontal {
        background: qlineargradient(x1:0, y1:1, x2:1, y2:1, stop: 0 #1C1C1C, stop: 1 #FF0000);
        border: 1px solid #4C4B4B;
        height: 10px;
        border-radius: 4px;
    }
    
    QSlider#Green::sub-page:horizontal {
        background: qlineargradient(x1:0, y1:1, x2:1, y2:1, stop: 0 #1C1C1C, stop: 1 #00FF00);
        border: 1px solid #4C4B4B;
        height: 10px;
        border-radius: 4px;
    }
    
    QSlider#Blue::sub-page:horizontal {
        background: qlineargradient(x1:0, y1:1, x2:1, y2:1, stop: 0 #1C1C1C, stop: 1 #0000FF);
        border: 1px solid #4C4B4B;
        height: 10px;
        border-radius: 4px;
    }

    QSlider#Alpha::sub-page:horizontal {
        background: qlineargradient(x1:0, y1:1, x2:1, y2:1, stop: 0 #FFFFFF, stop: 1 #C0C0C0);
        border: 1px solid #4C4B4B;
        height: 10px;
        border-radius: 4px;
    }

    QLineEdit {
        font-size: 16px;
    }
"""
