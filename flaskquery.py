import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QDateEdit, QGroupBox, QFormLayout, QSizePolicy
from PyQt5.QtCore import QDate, Qt

class FlaskQueryApp(QWidget):
    def __init__(self):
        super().__init__()
        #sys.path.append('/Volumes/ccg/src/db/')
        sys.path.append('W:\\src\\db')
        import db_utils.db_conn as db_conn
        self.db = db_conn.HATS_ng()

        self.initUI()

    def initUI(self):
        # Set the fixed width of the window
        self.setFixedWidth(400)  # Adjust the width as needed

        # Layouts
        vbox = QVBoxLayout()

        # Analysis Date Input
        hbox_analysis_date = QHBoxLayout()
        self.analysis_date_label = QLabel('Analysis Date:')
        self.analysis_date_input = QDateEdit()
        self.analysis_date_input.setCalendarPopup(True)
        self.analysis_date_input.setDate(QDate.currentDate())  # Set default to today
        hbox_analysis_date.addWidget(self.analysis_date_label)
        hbox_analysis_date.addWidget(self.analysis_date_input)
        vbox.addLayout(hbox_analysis_date)

        # Flask Number Input
        hbox_flask = QHBoxLayout()
        self.flask_label = QLabel('Flask Number:')
        self.flask_input = QLineEdit()
        hbox_flask.addWidget(self.flask_label)
        hbox_flask.addWidget(self.flask_input)
        vbox.addLayout(hbox_flask)

        # Connect pressing Enter to the query function
        self.flask_input.returnPressed.connect(self.query_flask)

        # Query Button
        self.query_button = QPushButton('Query')
        self.query_button.clicked.connect(self.query_flask)
        vbox.addWidget(self.query_button)

        # Create a group box with a black border for the results
        results_group = QGroupBox()
        results_group.setTitle("Query Results")
        results_group.setStyleSheet("QGroupBox { border: 2px solid black; padding: 10px; }")

        form_layout = QFormLayout()

        # Site Code Output
        self.site_label = QLabel('Site Code:')
        self.site_output = QLineEdit()
        self.site_output.setReadOnly(True)
        #self.site_output.setMinimumWidth(400)  # Set a minimum width
        form_layout.addRow(self.site_label, self.site_output)

        # Fill Date Output
        self.date_label = QLabel('Fill Date:')
        self.date_output = QLineEdit()
        self.date_output.setReadOnly(True)
        #self.date_output.setMinimumWidth(400)  # Set a minimum width
        form_layout.addRow(self.date_label, self.date_output)

        # Pair ID Output
        self.pair_label = QLabel('Pair ID:')
        self.pair_output = QLineEdit()
        self.pair_output.setReadOnly(True)
        #self.pair_output.setMinimumWidth(400)  # Set a minimum width
        form_layout.addRow(self.pair_label, self.pair_output)

        # Combined Output
        self.combined_label = QLabel('Combined:')
        self.combined_output = QLineEdit()
        self.combined_output.setReadOnly(True)
        #self.combined_output.setMinimumWidth(400)  # Set a minimum width
        form_layout.addRow(self.combined_label, self.combined_output)

        # Ensure the QLineEdit widgets stretch to fill the available space
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        results_group.setLayout(form_layout)
        vbox.addWidget(results_group)

        self.setLayout(vbox)

        self.setWindowTitle('Flask Query')
        self.show()

    def query_flask(self):
        flask_number = self.flask_input.text()
        analysis_date = self.analysis_date_input.date().toString('yyyy-MM-dd')
        
        sql = """
            SELECT site, pair_id, ev_datetime FROM hats.hatsflask_event_view
            WHERE ev_datetime < %s AND flask_id = %s
            ORDER BY ev_datetime DESC LIMIT 1;
        """
        try:
            ret = self.db.doquery(sql, (analysis_date, flask_number))[0]
            site_code = ret['site']
            fill_date = ret['ev_datetime'].strftime('%d %b %y')
            pair_id = ret['pair_id']
        except Exception:
            print(f'ERROR: Perhaps the flask number is not in the database?')
            self.site_output.setText('')
            self.date_output.setText('')
            self.pair_output.setText('')
            self.combined_output.setText('')
            return
       
        # Update output fields
        self.site_output.setText(site_code)
        self.date_output.setText(fill_date)
        self.pair_output.setText(str(pair_id))

        # Update combined field
        combined_text = f"{site_code.lower()} {fill_date.lower()} #{flask_number}-{pair_id}"
        self.combined_output.setText(combined_text)

        # Highlight the combined output field text for easy copying
        self.combined_output.selectAll()
        self.combined_output.setFocus()  # Ensure the focus is on the field so the selection is visible

def main():
    app = QApplication(sys.argv)
    ex = FlaskQueryApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
