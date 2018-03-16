#!/usr/bin/python3.4

'''
SOFT-361 -- Course Planner -- Spring 2018
Description: Retrieves course and major data from UNL API
             Processes and prepares an sql script for database insertion
Start Date: ~February 26, 2018
'''

import requests

def main():

    initialize()

    subjectDct = generateSubjectDct()
    courseDct = generateCourseDct(subjectDct)
    majorDct = generateMajorDct(subjectDct)

    generateSqlScript(subjectDct, courseDct, majorDct)

    return

def initialize():
    clearErrFile()
    return

def logErr(msg):
    #TODO: Needs to be integrated to account for unseen errors
    #print(msg)
    f = open("loader.err", "a")
    f.write(msg)
    f.close()
    return

def clearErrFile():
    open("loader.err", "w").close()
    return

'''
Data retrieval methods:
'''
def getDataFromLink(url):
    rep = requests.get(url)
    dat = rep.json()
    return dat

def getMajorData():
    return getDataFromLink("https://bulletin.unl.edu/undergraduate/majors.json")

def getCourseData(courseId):
    return getDataFromLink("https://bulletin.unl.edu/undergraduate/courses/" \
                         + "{}.json".format(courseId))

def getSubjectData():
    return getDataFromLink("https://bulletin.unl.edu/undergraduate/courses.json")

def getMajorSubjectData(majorUri):
    return getDataFromLink(majorUri + "/courses.json")

#========================#
#Data Processing methods:#
#========================#
'''
Process Subject Data:
'''
def generateSubjectDct():
    subjectDat = getSubjectData()
    return processSubjectDat(subjectDat)

def processSubjectDat(subjectDat):
    '''
    Output: dict of subjects key = id, value = Subject Object
    '''
    subjectDct = {}
    for subjectId, subject in subjectDat.items():
        subjectDct[subjectId] = Subject(subjectId, subject.get('title'))
    return subjectDct

'''
Process Course Data:
'''
def generateCourseDct(subjectDct):
    courseDct = {}
    for prefix, subject in subjectDct.items():
        courseList = getCourseListBySubject(subject)
        if courseList is not None:
            courseDct[prefix] = courseList
        else:
            print("Error: url query did not return results for: " \
                + subject.getSubjectId())
    return courseDct


def getCourseListBySubject(subject):
    courseData = getCourseData(subject.getSubjectId())
    if courseData is not None:
        return processCourseData(courseData, subject)
    return None

def processCourseData(courseDat, subject):
    '''
    Returns a list of all course for given subject
    '''
    courseList = []
    courseDataList = courseDat.get('courses')
    if courseDataList is not None:
        for course in courseDataList:
            courseObj = getCourseObjFromData(course)
            courseObj.setSubject(subject)
            courseList.append(courseObj)
    return courseList

def getCourseObjFromData(course):
    try:
        tempCourse = Course(course.get('title'), \
            course.get('description'), \
            course.get('prerequisite'), \
            getCourseNumFromData(course), \
            getCreditHours(course))
        tempCourse.setAceList(getAceList(course))
        return tempCourse
    except Exception as err:
        print("Error: " + type(err) + " Omitting course: " + course.get('title'))

def getCourseNumFromData(course):
    courseCodeList = course.get('courseCodes')
    if len(courseCodeList) > 0:
        return courseCodeList[0].get('courseNumber')
    else:
        raise Exception("Error: no course codes for " + course.get('title'))

def getCreditHours(course):
    creditsRaw = course.get('credits')
    if len(creditsRaw) > 0:
        return creditsRaw[0].get('')
    return None

def getAceList(course):
    aceListRaw = course.get('aceOutcomes')
    aceCont = AceContainer()
    aceList = []
    if aceListRaw is not None:
        for ace in aceListRaw:
            aceList.append(aceCont.getAce(ace))
    return aceList

'''
Process Major Data:
'''
def generateMajorDct(subjectDct):
    majorData = getMajorData()
    return processMajorData(majorData, subjectDct)

def processMajorData(majorDataRaw, subjectDct):
    majorDct = {}
    for maj in majorDataRaw:
        subjList = generateMajorSubjectList(maj.get('uri'), subjectDct)
        tempMajor = Major(maj.get('title'), \
                          maj.get('uri'), \
                          maj.get('minorAvailable'), \
                          maj.get('minorOnly'), \
                          subjList)
        majorDct[maj.get('title')] = tempMajor
    return majorDct

def generateMajorSubjectList(uri, subjectDct):
    MajorSubjectDat = getMajorSubjectData(uri)
    return processMajorSubjectData(MajorSubjectDat, subjectDct)

def processMajorSubjectData(MajorSubjectDat, subjectDct):
    majSubjList = []
    for subjectId in MajorSubjectDat.values():
        if subjectId in subjectDct.keys():
            majSubjList.append(subjectId)
        else:
            msg = "Error: subject " + subjectId + " does not exist in subjectDct\n"
            logErr(msg)
    return majSubjList

'''
Create SQL script for output to database:
'''
def generateSqlScript(subjectDct, courseDct, majorDct):
    sqlOutputFile = open("dbLoader.sql", "w")
    sqlOutputFile.write("USE apages;\n\n")
    writeAceInserts(sqlOutputFile)
    writeSubjectCourseInserts(subjectDct, courseDct, sqlOutputFile)
    writeMajorInserts(majorDct, sqlOutputFile)
    sqlOutputFile.close()

def writeSubjectCourseInserts(subjectDct, courseDct, sqlOutputFile):
    for subject in subjectDct.values():
        writeSubjectInsert(subject, sqlOutputFile)
        sqlOutputFile.write(getSqlVarSetterSubject())
        courseList = courseDct[subject.getSubjectId()]
        writeCourseListInserts(courseList, sqlOutputFile)
    return None

def writeCourseListInserts(courseList, sqlOutputFile):
    for course in courseList:
        sqlOutputFile.write(course.getSqlInsert())
    return None

def getSqlVarSetterSubject():
    return "SET @tempSubj_key=LAST_INSERT_ID();\n"

def writeSubjectInsert(subject, sqlOutputFile):
    sqlOutputFile.write('# SUBJECT AND COURSE TABLE POPULATION: (' + subject.getSubjectId() + ')\n')
    query = subject.getSqlInsert()
    sqlOutputFile.write(query)
    return None

def writeAceInserts(sqlOutputFile):
    sqlOutputFile.write("# ACE TABLE POPULATION:\n")
    aceCont = AceContainer()
    aceCont.writeAceInserts(sqlOutputFile)
    return None

def writeMajorInserts(majorDct, sqlOutputFile):
    sqlOutputFile.write("# MAJOR TABLE POPULATION:\n")
    for major in majorDct.values():
        sqlOutputFile.write(major.getSqlInsert())
    return None

def prepareNN(var):
    '''
    use to prepare NOT NULL fields
    '''
    if var is None:
        raise ValueError
    return prepare(var)

def prepare(var):
    if var is None:
        return 'NULL'
    elif type(var) is bool:
        return str(var).upper()
    elif type(var) is str:
        return var.replace('\'', "\'\'") # sql apostrophes escaped ( '' )
    elif type(var) is int or float:
        return str(var)
    else:
        # This should never happen
        return None

'''
Class Definitions:
'''
class Subject:
    def __init__(self, subjectId, title):
        self.subjectId = subjectId
        self.title = title

    def getSubjectId(self):
        return self.subjectId

    def getSqlInsert(self):
        try:
            query = "INSERT INTO Subject (subjectId, title) VALUES" \
                 + "(\'" + prepareNN(self.subjectId) + "\', " \
                 + "\'" + prepareNN(self.title) + "\');\n"
            return query
        except ValueError:
            print("Error: " + self.getSubjectId() + " has 'None' attribute for NOT NULL field")
            return

class Major:
    def __init__(self, title, uri, minorOffered, minorOnly, subjectList):
        self.title = title
        self.uri = uri
        self.minorOffered = minorOffered
        self.minorOnly = minorOnly
        self.subjectList = subjectList
        self.subjectId = None

    def getTitle(self):
        return self.title

    def addId(self, subjectId):
        self.subjectId = subjectId
        return

    def getUri(self):
        return self.uri

    def getSubjectList(self):
        return self.subjectList

    def getSqlInsert(self):
        try:
            query = self.getMajorInsert()
            if len(self.getSubjectList()) > 0:
                query += self.getMajorSubjectInsert()
            return query
        except ValueError:
            print("Error: " + self.title() + " has 'None' attribute for NOT NULL field")

    def getMajorInsert(self):
        try:
            query = "INSERT INTO Major (title, uri, minorOffered, minorOnly) VALUES " \
                    + "(\'" + prepareNN(self.title) + "\', " \
                    + "\'" + prepareNN(self.uri) + "\', " \
                    + prepare(self.minorOffered) + ", " \
                    + prepare(self.minorOnly) + ");\n"
            return query
        except ValueError:
            raise ValueError("'None' attribute in major insert")

    def getMajorSubjectInsert(self):
        try:
            query = self.getSqlVarSetterMajor()
            for subjectId in self.getSubjectList():
                query += "INSERT INTO MajorSubject (major_fk, subject_fk) VALUES (" \
                    + "@tempMajor_key, " \
                    + "(SELECT subject_key FROM Subject WHERE subjectId =" \
                    + "\'" + prepareNN(subjectId) + "\'));\n"
            return query
        except ValueError:
            raise ValueError("'None attribute in majorSubject insert'")

    def getSqlVarSetterMajor(self):
        return "SET @tempMajor_key=LAST_INSERT_ID();\n"


class Course:
    def __init__(self, title, description, prerequisite, \
                 courseNum, creditHours):
        self.title = title
        self.description = description
        self.prerequisite = prerequisite
        self.courseNum = courseNum
        self.creditHours = creditHours
        self.aceList = []
        self.subject = None

    def setAceList(self, aceList):
        self.aceList = aceList

    def setSubject(self, subject):
        self.subject = subject

    def getSqlInsert(self):
        try:
            query = "INSERT INTO Course (title, description, creditHours, "\
                  + "prerequisite, subject_fk, courseNum, ace_1_fk, ace_2_fk) "\
                  + "VALUES (" \
                  + "\'" + prepareNN(self.title) + "\', " \
                  + "\'" + prepareNN(self.description) + "\', " \
                  + prepare(self.creditHours) + ", " \
                  + "\'" + prepare(self.prerequisite) + "\', " \
                  + " @tempSubj_key , " \
                  + "\'" + prepareNN(self.courseNum) + "\'"

            #TODO: rewrite the following ifs
            if len(self.aceList) > 0:
                query += ", " + self.aceList[0].getKeyVar()
            else:
                query += ", NULL"
            if len(self.aceList) > 1:
                query += ",  " + self.aceList[1].getKeyVar()
            else:
                query += ", NULL"
            query += ");\n"
            return query
        except ValueError:
            print("Error: " + self.title + " has 'None' attribute for NOT NULL field")
            return None


'''
Singleton ace container making aces accessible in different areas throughout
without need to pass an ace dictionary as argument or create global variable
'''
class AceContainer:

    __instance = None # stores instance of inner class

    class inner:
        def __init__(self):
            aceDct = self.__dict__
            with  open('aceData.txt', 'r') as aceFile:
                for line in aceFile:
                    field = line.split('; ')
                    aceCourse = self.AceCourseObj(str(field[0]), field[1].rstrip('\n'))
                    aceDct[str(field[0])] = aceCourse

        def get(self, aceNum):
            return self.__dict__[aceNum]

        def writeAceInserts(self, sqlOutputFile):
            for ace in self.__dict__.values():
                aceQuery = ace.writeSqlInsert()
                setKeyVarQuery = "SET " + ace.getKeyVar() + "=LAST_INSERT_ID();\n"
                sqlOutputFile.write(aceQuery)
                sqlOutputFile.write(setKeyVarQuery)
            return

        class AceCourseObj:

            def __init__(self, aceNum, description):
                self.aceNum = aceNum
                self.description = description
                self.keyVar = "@ace" + aceNum

            def getAceNum(self):
                return self.aceNum

            def getKeyVar(self):
                return self.keyVar

            def writeSqlInsert(self):
                try:
                    query = "INSERT INTO Ace (aceNum, aceDescription) VALUES (" \
                            + "\'" + prepareNN(self.aceNum) + "\', " \
                            + "\'" + prepareNN(self.description) + "\');\n"
                    return query
                except ValueError:
                    print("Error: Ace" + self.aceNum() + " has None attribute for NOT NULL field")
                return None

    def __init__(self):
        if AceContainer.__instance is None:
            AceContainer.__instance = AceContainer.inner()

    def getAce(self, aceNum):
        if 0 <= int(aceNum) <= 10:
            return AceContainer.__instance.get(aceNum)
        print("Error: Invalid ace number " + aceNum)
        return None

    def writeAceInserts(self, sqlOutputFile):
        AceContainer.__instance.writeAceInserts(sqlOutputFile)
        return

if __name__ == '__main__':
    main()
