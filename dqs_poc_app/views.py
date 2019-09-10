from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, request, response, HttpResponseRedirect, JsonResponse
import pyodbc
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import authenticate
import json

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def db_select(request):
    print("selected db",request.GET.get('dropdown'))
    selected_database = request.GET.get('dropdown')
    db_names = connect_to_selected_db(selected_database)
    # return HttpResponse(status=200)
    print("returned from method",db_names)
    # return render(request, template_name='db_name.html')
    return render(request, 'db_name.html',{'db_names': db_names})

def connect_to_selected_db(selected_database):
   if selected_database == 'mssql':
       return connect_mssql()
   elif selected_database == 'postgres':
       return connect_postgresql()

def connect_mssql():
    # conn = pyodbc.connect('Driver={SQL Server};'
    #                       'Server=DESKTOP-UC1L6FT\SQLEXPRESS;'
    #                       'Database=ExtractionData;'
    #                       'Trusted_Connection=yes;')
    # conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};'+'Server=dqspilot.database.windows.net;'+'Database=dq_solution;'+'UID=dqs_admin;'+'PWD=Akira@123;'+'Trusted_Connection=yes;')

    server = 'dqspilot.database.windows.net'
    database = 'dq_solution'
    username = 'dqs_admin'
    password = 'Akira@123'
    driver = '{ODBC Driver 13 for SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM dbo.sysdatabases")
    database_names = []
    for row in cursor:
        # print("db names",row[0])
        database_names.append(row[0])
    print(database_names)
    conn.commit()
    return database_names
    # print("connected to mssql",cursor)

def connect_postgresql():
    print("connected to postgresql")

def get_tables(request):
    jsonResponseObject = {}
    db_name = request.GET.get('db_name')
    # conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};'+'Server=dqspilot.database.windows.net;'+'Database=dq_solution;'+'UID=dqs_admin;'+'PWD=Akira@123;'+'Trusted_Connection=yes;')

    server = 'dqspilot.database.windows.net'
    database = 'dq_solution'
    username = 'dqs_admin'
    password = 'Akira@123'
    driver = '{ODBC Driver 13 for SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


    cursor = conn.cursor()
    cursor.execute("select table_name from "+db_name+".INFORMATION_SCHEMA.TABLES where TABLE_TYPE = 'BASE TABLE'")
    table_names = []
    for row in cursor:
        table_names.append(row[0])
    jsonResponseObject['status'] = 200
    jsonResponseObject['data'] = table_names
    return JsonResponse(jsonResponseObject, safe=False)

def login_validation(request):
    user_name = request.GET.get("username")
    print("username",user_name)
    password = request.GET.get("password")
    print("password",password)
    user = authenticate(username = user_name, password = password)
    if user is not None:
        print("Your username and password is correct.")
        return render(request, 'home.html')
    else:
        print("Your username and password were incorrect.")
        return render(request, 'login.html')


def runProcedure(request):
    jsonResponseObject = {}
    table_name = request.GET.get('table_name')
    # db_name = request.GET.get('db_name')
    print("db name run procedure",table_name)
    # conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};'+'Server=dqspilot.database.windows.net;'+'Database=dq_solution;'+'UID=dqs_admin;'+'PWD=Akira@123;'+'Trusted_Connection=yes;')

    server = 'dqspilot.database.windows.net'
    database = 'dq_solution'
    username = 'dqs_admin'
    password = 'Akira@123'
    driver = '{ODBC Driver 13 for SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    # table_names_data = json.loads(table_name)
    # print("procedure table name",type(table_names_data))
    cursor.execute("truncate table dbo.DATA_ACC_PROFILER")
    cursor.execute("EXEC GET_TABLE_INFO '"+table_name+"'")
    # for row in table_names_data:
    #     print('table names',row)
    #     cursor.execute("EXEC GET_TABLE_INFO '"+row+"'")
    cursor.commit()
    conn.close()

    table_name = []

    return getResults()

def getResults():
    jsonResponseObject = {}
    # db_name_connect = db_name
    # print("JSON db_name",db_name_connect)
    # conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};'+'Server=dqspilot.database.windows.net;'+'Database=dq_solution;'+'UID=dqs_admin;'+'PWD=Akira@123;'+'Trusted_Connection=yes;')


    server = 'dqspilot.database.windows.net'
    database = 'dq_solution'
    username = 'dqs_admin'
    password = 'Akira@123'
    driver = '{ODBC Driver 13 for SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    cursor.execute("SELECT TBL_NAME,COL_NAME,COL_DATA_LENGTH,COL_DATE_TYPE,COL_MIN_DATA_LENGTH,COL_MAX_DATA_LENGTH\
                    ,COL_AVG_DATA_LENGTH,COL_MIN_DATE,COL_MAX_DATE,COL_DISTINCT_CNT,COL_NULLS_CNT,COL_EMPTY_CNT,"
                   "COL_NULLS_PERCENTAGE,"
                   "COL_EMPTY_PERCENTAGE,COL_FK,COL_DATA_TYPE_RECOMMEND"
                   "\
                 FROM DATA_ACC_PROFILER")
    cols_dict = {
        1: 'TBL_NAME',
        2: 'COL_NAME',
        3: 'COL_DATA_LENGTH',
        4: 'COL_DATE_TYPE',
        5: 'COL_MIN_DATA_LENGTH',
        6: 'COL_MAX_DATA_LENGTH',
        7: 'COL_AVG_DATA_LENGTH',
        8: 'COL_MIN_DATE',
        9: 'COL_MAX_DATE',
        10: 'COL_DISTINCT_CNT',
        11: 'COL_NULLS_CNT',
        12: 'COL_EMPTY_CNT',
        13: 'COL_NULLS_PERCENTAGE',
        14: 'COL_EMPTY_PERCENTAGE',
        15: 'COL_FK',
        16: 'COL_DATA_TYPE_RECOMMEND',
    }
    myresult = cursor.fetchall()
    table_names = []
    i = 0
    for x in myresult:
        print("x",x)
        table_names.append(list(x))
        i = i+1
        # for i in range(len(x)):
        #     print("test",x[i])
            # table_names[cols_dict[i]] = x[i]
    # print("table_names",type(table_names))
    jsonResponseObject['status'] = 200
    jsonResponseObject['data'] = table_names
    print("JSON response")
    # print(jsonResponseObject)
    return JsonResponse(jsonResponseObject, safe=False)

def getTablesHealth(request):
    jsonResponseObject = {}
    db_name = request.GET.get('db_name');
    # conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};'+'Server=dqspilot.database.windows.net;'+'Database='+db_name+';'+'UID=dqs_admin;'+'PWD=Akira@123;'+'Trusted_Connection=yes;'+'Authentication=ActiveDirectoryPassword')


    server = 'dqspilot.database.windows.net'
    database = 'dq_solution'
    username = 'dqs_admin'
    password = 'Akira@123'
    driver = '{ODBC Driver 13 for SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + db_name + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    cursor.execute("Select [TABLE_NAME],upper([TABLE_HEALTH]) from "+db_name+".[dbo].[DATA_ACC_TBL_HEALTH]")
    table_names = []
    results = cursor.fetchall()
    # table_names = []
    i = 0
    for x in results:
        print("x", x)
        table_names.append(list(x))
        i = i + 1
    print("table names",table_names)
    jsonResponseObject['status'] = 200
    jsonResponseObject['data'] = table_names
    return JsonResponse(jsonResponseObject, safe=False)

def getProfileResults(request):
    jsonResponseObject = {}
    query = request.GET.get('table_name')
    # sku = request.GET.get('sku')
    print("query",query)
    jsonResponseObject['status'] = 200
    jsonResponseObject['data'] = query
    return render(request, 'proc_results.html',{'table_name': query})
    # return JsonResponse(jsonResponseObject, safe=False)