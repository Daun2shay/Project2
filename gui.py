import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from main import calculateGrades, exportToCsv

class GradingSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Grading System")
        self.setGeometry(100, 100, 500, 350)
        
        # Create central widget and main layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)
        
        # Title
        titleLabel = QLabel("Student Grading System")
        titleFont = QFont("Arial", 16, QFont.Weight.Bold)
        titleLabel.setFont(titleFont)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(titleLabel)
        mainLayout.addSpacing(20)
        
        # Input section
        inputLayout = QVBoxLayout()
        
        # Student name input
        studentNameLayout = QHBoxLayout()
        studentNameLabel = QLabel("Student Name:")
        studentNameLabel.setFont(QFont("Arial", 10))
        self.studentNameEntry = QLineEdit()
        studentNameLayout.addWidget(studentNameLabel)
        studentNameLayout.addWidget(self.studentNameEntry)
        inputLayout.addLayout(studentNameLayout)
        
        # Number of attempts input
        attemptsLayout = QHBoxLayout()
        attemptsLabel = QLabel("Number of Attempts:")
        attemptsLabel.setFont(QFont("Arial", 10))
        self.attemptsEntry = QLineEdit()
        self.attemptsEntry.setMaximumWidth(200)
        self.attemptsEntry.textChanged.connect(self.onAttemptsChanged)
        attemptsLayout.addWidget(attemptsLabel)
        attemptsLayout.addWidget(self.attemptsEntry)
        
        # Warning label for exceeding limit
        self.warningLabel = QLabel("")
        self.warningLabel.setFont(QFont("Arial", 9))
        self.warningLabel.setStyleSheet("color: red; font-weight: bold;")
        attemptsLayout.addWidget(self.warningLabel)
        
        attemptsLayout.addStretch()
        inputLayout.addLayout(attemptsLayout)
        
        # Number of students input (removed - now automatic)
        
        # Dynamic score input fields container
        self.scoreInputsLayout = QVBoxLayout()
        inputLayout.addLayout(self.scoreInputsLayout)
        
        # Store score entry widgets
        self.scoreEntries = []
        
        mainLayout.addLayout(inputLayout)
        mainLayout.addSpacing(20)
        
        # Buttons layout
        buttonLayout = QHBoxLayout()
        
        # Calculate and Export button
        self.calculateBtn = QPushButton("Calculate & Export to CSV")
        self.calculateBtn.clicked.connect(self.calculateGrades)
        self.calculateBtn.setMinimumHeight(40)
        buttonLayout.addWidget(self.calculateBtn)
        
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch()
    
    def onAttemptsChanged(self):
        """Create score input boxes based on number of attempts."""
        # Clear existing score input fields
        while self.scoreInputsLayout.count():
            item = self.scoreInputsLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.scoreEntries = []
        
        try:
            attempts = int(self.attemptsEntry.text())
            
            # Check if attempts exceeds 4
            if attempts > 4:
                self.warningLabel.setText("⚠ Maximum 4 attempts allowed!")
                # Cap at 4
                attempts = 4
            else:
                self.warningLabel.setText("")
            
            if attempts > 0:
                for i in range(1, attempts + 1):
                    scoreLayout = QHBoxLayout()
                    scoreLabel = QLabel(f"Score {i}:")
                    scoreLabel.setFont(QFont("Arial", 10))
                    scoreLabel.setMinimumWidth(100)
                    
                    scoreEntry = QLineEdit()
                    scoreEntry.setPlaceholderText(f"Enter score {i}")
                    
                    scoreLayout.addWidget(scoreLabel)
                    scoreLayout.addWidget(scoreEntry)
                    
                    self.scoreInputsLayout.addLayout(scoreLayout)
                    self.scoreEntries.append(scoreEntry)
                
                # Adjust window height based on number of attempts
                newHeight = 250 + (attempts * 40)
                self.setGeometry(100, 100, 500, min(newHeight, 700))
        except ValueError:
            # Invalid input, clear fields and warning
            self.warningLabel.setText("")
            pass
        
    def calculateGrades(self):
        try:
            # Get student name
            studentName = self.studentNameEntry.text().strip()
            if not studentName:
                QMessageBox.critical(self, "Error", "Please enter a student name!")
                return
            
            # Get number of attempts
            try:
                attempts = int(self.attemptsEntry.text())
                if attempts <= 0:
                    QMessageBox.critical(self, "Error", "Number of attempts must be positive!")
                    return
            except ValueError:
                QMessageBox.critical(self, "Error", "Please enter a valid number for attempts!")
                return
            
            # Check if we have the correct number of score entry fields
            if len(self.scoreEntries) != attempts:
                QMessageBox.critical(self, "Error", "Please wait for score fields to update!")
                return
            
            # Collect scores from individual input fields
            scores = []
            for i, scoreEntry in enumerate(self.scoreEntries, 1):
                scoreText = scoreEntry.text().strip()
                if not scoreText:
                    QMessageBox.critical(self, "Error", f"Please enter score {i}!")
                    return
                try:
                    score = int(scoreText)
                    scores.append(score)
                except ValueError:
                    QMessageBox.critical(self, "Error", f"Score {i} must be a valid number!")
                    return
            
            # Validate scores
            for score in scores:
                if score < 0:
                    QMessageBox.critical(self, "Error", "Scores cannot be negative!")
                    return
            
            # Calculate best score using main.py logic
            best = calculateGrades(scores)
            
            # Export to CSV using main.py logic (always uses data.csv)
            savedFile = exportToCsv(studentName, scores, best)
            QMessageBox.information(
                self,
                "Success",
                f"Results exported successfully to:\n{savedFile}"
            )
            # Clear fields after successful export
            self.clearFields()
                    
        except ValueError:
            QMessageBox.critical(self, "Error", 
                "Please enter valid numbers for student count and scores!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def clearFields(self):
        self.studentNameEntry.clear()
        self.attemptsEntry.clear()
        
        # Clear all score entry fields
        for scoreEntry in self.scoreEntries:
            scoreEntry.clear()


def main():
    app = QApplication(sys.argv)
    window = GradingSystemGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
