from  pymongo import MongoClient

class db_connect:

    def __init__(self):
        # self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.client = MongoClient('mongodb + srv: // xxxx: xxxx @ myfirstdb.x7c5s.mongodb.net / test') # connecting with mongoDB Atlas
        self.mydb = self.client['Attendance_System']  # db name given if this db name not there then it will create
        self.employees_collection = self.mydb.employees

    def data_fetchingDB(self, dbname_list):
        for record in self.employees_collection.find({}, {'_id': 0, 'Day': 0, 'Time': 0}):  # or find() will also give same output, here fetching employee name only
            for key, value in record.items():
                dbname_list.append(value.lower())  # fetching the employee's name from DB
        # print(dbname_list)
        return dbname_list

    def data_storingDB(self, emp_name, Timing, day):
        self.employees_collection.insert_one({'Employee Name': emp_name, 'Day': day, 'Time': Timing})
        print("Thanks your Attendance has been recorded!")
