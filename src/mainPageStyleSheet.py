styleSheet = """
    * {
        background-color: #F6B420;
        color: #4840A3;
        font-size: 25px;
    }

    QLabel {
        background: transparent;
        font-weight: 600;
    } 
    
    QLineEdit {
        border: 2px solid #F9CD6A;
        border-radius: 10px;
        padding: 5px 15px;
        background-color: rgba(249, 205, 106, 0.5);
        color: #4840A3;
        selection-background-color: #F9CD6A; 
        selection-color: #D8EFF7;
        font-weight: 600;
    }

    QLineEdit:focus { 
        border: 2px solid #F6B420;
        background-color: rgba(246, 180, 32, 0.5);
    }

    QTextEdit {
        border: 2px solid #F9CD6A;
        border-radius: 10px;
        padding: 5px 15px;
        background-color: rgba(249, 205, 106, 0.5);
        color: #4840A3; 
        selection-background-color: #F9CD6A; 
        selection-color: #D8EFF7;
        font-weight: 600;
    }

    QTextEdit:focus { 
        border: 2px solid #F6B420;
        background-color: rgba(246, 180, 32, 0.5);
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

