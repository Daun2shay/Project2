import csv
import os

def calculateGrades(scores):
    """Calculate best score from list of scores."""
    if not scores:
        raise ValueError("Scores list cannot be empty")
    
    best = max(scores)
    return best

def exportToCsv(studentName, scores, best, filename="data.csv"):
    """Export student data to CSV file."""
    # Check if file exists to determine if we need to write header
    fileExists = os.path.exists(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header only if file doesn't exist
        if not fileExists:
            writer.writerow(['Name', 'Score 1', 'Score 2', 'Score 3', 'Score 4', 'Final'])
        
        # Prepare row data
        rowData = [studentName]
        
        # Add scores (pad with empty strings if less than 4 scores)
        for i in range(4):
            if i < len(scores):
                rowData.append(scores[i])
            else:
                rowData.append('')
        
        # Add the largest score (best score)
        rowData.append(best)
        
        # Write student data
        writer.writerow(rowData)
    
    return filename

def main():
    """Launch the GUI application."""
    from gui import main as guiMain
    guiMain()


if __name__ == "__main__":
    main()