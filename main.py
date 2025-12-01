from collections import Counter

def getGrade(score, best):
    if score >= best - 10:
        return 'A'
    elif score >= best - 20:
        return 'B'
    elif score >= best - 30:
        return 'C'
    elif score >= best - 40:
        return 'D'
    else:
        return 'F'


def calculateGrades(scores):
    if not scores:
        raise ValueError("Scores list cannot be empty")
    
    best = max(scores)
    results = []
    
    for i, score in enumerate(scores, 1):
        grade = getGrade(score, best)
        results.append((i, score, grade))
    
    gradeCounts = {}
    gradeCounts = Counter(grade for student_num, score, grade in results)
    
    return best, results, gradeCounts


def runCli():
    count = int(input("Total number of students: "))
    while True:
        scores = input(f"Enter {count} score(s): ").split()
        if len(scores) == count:
            scores = [int(s) for s in scores]
            break
    
    bestScore, studentResults, gradeDistribution = calculateGrades(scores)
    
    for studentNum, score, grade in studentResults:
        print(f"Student {studentNum} score is {score} and grade is {grade}")
def main():
    from gui import main as guiMain
    guiMain()


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()