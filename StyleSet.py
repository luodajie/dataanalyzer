def stylish(widget=None):
    widget.setStyleSheet('''
                   QWidget{
                       color: #b1b1b1;
                       background-color: #323232;
                   }

                   QPushButton:pressed
                   {
                       background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1
                        #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
                   }

                   QPushButton
                   {
                       color: #b1b1b1;
                       background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1
                        #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
                       border-width: 1px;
                       border-color: #1e1e1e;
                       border-style: solid;
                       border-radius: 6;
                       padding: 3px;
                       font-size: 12px;
                       padding-left: 5px;
                       padding-right: 5px;
                       }

                       QListView {
                           show-decoration-selected: 1; /* make the selection span the entire width of the view */
                       }

                       QListView::item:alternate {
                           background: #EEEEEE;
                       }

                       QListView::item:selected {
                           border: 1px solid #6a6ea9;
                       }

                       QListView::item:selected:!active {
                           background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                       stop: 0 #ABAFE5, stop: 1 #8588B2);
                       }

                       QListView::item:selected:active {
                           background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                       stop: 0 #6a6ea9, stop: 1 #888dd9);
                       }

                       QListView::item:hover {
                           background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                       stop: 0 , stop: 1 );
                       }


                   ''')

def form(Form=None):
    Form.setStyleSheet('''
                   QWidget{
                       color: #b1b1b1;
                       background-color: #323232;
                   }

                   QPushButton:pressed
                   {
                       background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1
                        #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
                   }

                   QPushButton
                   {
                       color: #b1b1b1;
                       background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1
                        #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
                       border-width: 1px;
                       border-color: #b3b3b3;
                       border-style: solid;
                       border-radius: 6;
                       padding: 3px;
                       font-size: 12px;
                       padding-left: 5px;
                       padding-right: 5px;
                       }


                   ''')

