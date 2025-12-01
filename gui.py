import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from main import calculateGrades

# used AI with the gui
class GradingSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Grading System")
        self.setGeometry(100, 100, 600, 500)
        
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
        
        # Number of students input
        studentCountLayout = QHBoxLayout()
        studentCountLabel = QLabel("Number of Students:")
        studentCountLabel.setFont(QFont("Arial", 10))
        self.studentCountEntry = QLineEdit()
        self.studentCountEntry.setMaximumWidth(200)
        studentCountLayout.addWidget(studentCountLabel)
        studentCountLayout.addWidget(self.studentCountEntry)
        studentCountLayout.addStretch()
        inputLayout.addLayout(studentCountLayout)
        
        # Scores input
        scoresLayout = QHBoxLayout()
        scoresLabel = QLabel("Enter Scores (space-separated):")
        scoresLabel.setFont(QFont("Arial", 10))
        self.scoresEntry = QLineEdit()
        scoresLayout.addWidget(scoresLabel)
        scoresLayout.addWidget(self.scoresEntry)
        inputLayout.addLayout(scoresLayout)
        
        mainLayout.addLayout(inputLayout)
        mainLayout.addSpacing(10)
        
        # Buttons layout
        buttonLayout = QHBoxLayout()
        
        # Calculate button
        self.calculateBtn = QPushButton("Calculate Grades")
        self.calculateBtn.clicked.connect(self.calculateGrades)
        self.calculateBtn.setMinimumHeight(35)
        buttonLayout.addWidget(self.calculateBtn)
        
        # Clear button
        self.clearBtn = QPushButton("Clear")
        self.clearBtn.clicked.connect(self.clearFields)
        self.clearBtn.setMinimumHeight(35)
        buttonLayout.addWidget(self.clearBtn)
        
        mainLayout.addLayout(buttonLayout)
        mainLayout.addSpacing(10)
        
        # Results section
        resultsGroup = QGroupBox("Results")
        resultsLayout = QVBoxLayout()
        
        self.resultsText = QTextEdit()
        self.resultsText.setReadOnly(True)
        self.resultsText.setFont(QFont("Courier", 10))
        resultsLayout.addWidget(self.resultsText)
        
        resultsGroup.setLayout(resultsLayout)
        mainLayout.addWidget(resultsGroup)
        
    def calculateGrades(self):
        try:
            # Get student count
            count = int(self.studentCountEntry.text())
            
            if count <= 0:
                QMessageBox.critical(self, "Error", "Number of students must be positive!")
                return
            
            # Get scores
            scoresInput = self.scoresEntry.text().split()
            
            if len(scoresInput) != count:
                QMessageBox.critical(self, "Error", 
                    f"Please enter exactly {count} score(s). You entered {len(scoresInput)}.")
                return
            
            # Convert to integers
            scores = [int(s) for s in scoresInput]
            
            # Validate scores
            for score in scores:
                if score < 0:
                    QMessageBox.critical(self, "Error", "Scores cannot be negative!")
                    return
            
            # Calculate grades using main.py logic
            best, results, gradeCounts = calculateGrades(scores)
            
            # Clear previous results
            self.resultsText.clear()
            
            # Build results text
            resultText = f"Best Score: {best}\n"
            resultText += "=" * 50 + "\n\n"
            
            # Display grades
            for studentNum, score, grade in results:
                resultText += f"Student {studentNum}: Score = {score}, Grade = {grade}\n"
            
            # Summary
            resultText += "\n" + "=" * 50 + "\n"
            resultText += "Grade Distribution:\n"
            for grade in ['A', 'B', 'C', 'D', 'F']:
                if grade in gradeCounts:
                    resultText += f"  {grade}: {gradeCounts[grade]} student(s)\n"
            
            self.resultsText.setPlainText(resultText)
                    
        except ValueError:
            QMessageBox.critical(self, "Error", 
                "Please enter valid numbers for student count and scores!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def clearFields(self):
        self.studentCountEntry.clear()
        self.scoresEntry.clear()
        self.resultsText.clear()


def main():
    app = QApplication(sys.argv)
    window = GradingSystemGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
