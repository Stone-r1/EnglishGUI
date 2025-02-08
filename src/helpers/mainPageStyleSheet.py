styleSheet = """
    
    * {
        background-color: #388087;  
        font-family: "Comic Sans MS", "Baloo", "Fredoka One", sans-serif;
        color: #36557B;
        font-size: 25px;
    }

    QLabel {
        background: transparent;
        font-weight: 600;
    } 
    
    QLineEdit {
        border: 2px solid #B9F8FF;  /* light blue border */
        border-radius: 10px;
        padding: 5px 15px;
        background-color: rgba(194, 237, 206, 0.5); /* semi-transparent light green */
        color: #36557B;
        selection-background-color: #B9F8FF; 
        selection-color: #D8EFF7;
        font-weight: 600;
    }

    QLineEdit:focus { 
        border: 2px solid #6FB3B8;
        background-color: rgba(194, 237, 206, 0.7);
    }

    QTextEdit {
        border: 2px solid #B9F8FF;
        border-radius: 10px;
        padding: 5px 15px;
        background-color: rgba(194, 237, 206, 0.5);
        color: #36557B; 
        selection-background-color: #B9F8FF; 
        selection-color: #D8EFF7;
        font-weight: 600;
    }

    QTextEdit:focus { 
        border: 2px solid #6FB3B8;
        background-color: rgba(194, 237, 206, 0.7);
    }

    QPushButton {
        border-radius: 20px;
        font-family: "Comic Sans MS", "Baloo", "Fredoka One", sans-serif; 
        padding: 10px 30px;
        font-weight: 700;
        color: white;
        background: #295e63; 
        border: 2px solid rgba(41, 94, 99, 0.2);
    }

    #StartButton:hover {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 #4BA3A3, stop:1 #5FAEAE);
    }

    #AddButton:hover { 
        background: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:1, 
                                    stop:0 #4BA3A3, stop:1 #5FAEAE);
    }

    QPushButton:pressed {
        background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, 
                                    stop:0 #3D8C8D, stop:1 #6FB3B8);
    }

    QComboBox {
        border: 2px solid #B9F8FF;
        border-radius: 10px;
        padding: 5px 15px;
        background-color: rgba(194, 237, 206, 0.5);
        color: #36557B;
        font-weight: 600;
    }

    QComboBox::item {
        border: none;
        height: 45px;
        padding: 5px;
    }

    QComboBox:focus {
        border: 2px solid #6FB3B8;
        background-color: rgba(194, 237, 206, 0.7);
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left: 1px solid #B9F8FF;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
        background-color: rgba(194, 237, 206, 0.5);
    }

"""

