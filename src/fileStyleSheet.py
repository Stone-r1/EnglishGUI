styleSheet = """
    * {
        background-color: #F6B420;
        color: #4840A3;
        font-size: 25px;
    }

    QPushButton {
        border-radius: 20px;
        padding: 10px 30px;
        font-weight: 700;
        color: white;
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                    stop:0 #F7B008, stop:1 #FFC02F);
    }

    #StartButton:hover {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 #F9B007, stop:1 #9564F9);
    }

    #AddButton:hover { 
        background: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, 
                                    stop:0 #F9B007, stop:1 #9564F9);
    }

    QPushButton:pressed {
        background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, 
                                    stop:0 #F7B008, stop:1 #FFC02F);
    }
"""

