import sqlite3
from sqlite3 import Error
from datetime import date, timedelta, datetime
import sys

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def query_base_table(conn, start_date, end_date):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    query = "select DATE(created_at) as date1, strftime('%W', created_at) as week, strftime('%Y', created_at) as year, workflow_state as ws, count(*) as count from applicants where date1>=? and date1<=? group by date1,ws;"
    cur = conn.cursor()
    cur.execute(query, (start_date,end_date,))
    rows = cur.fetchall()
    return rows


def query_aux_table(conn, start_date, end_date):
    query = "select * from application_aux where date1>=? and date1<=? order by date1"
    cur = conn.cursor()
    cur.execute(query,(start_date,end_date,))
    rows = cur.fetchall()
    return rows


def fill_missing_gaps(rows):
	date_strs = [r[0] for r in rows]
	missing_dates = get_missing_gaps(date_strs)
	for m in missing_dates:
		tup = (m.strftime('%Y-%m-%d'), m.strftime('%W'), m.strftime('%Y'),'blah', 0)
		rows.append(tup)
	for row in rows:
		insert_to_aux_table(row)
	return rows

def get_missing_gaps(date_strs):
	d = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in date_strs]
	date_set = set(d[0] + timedelta(x) for x in range((d[-1] - d[0]).days))
	missing = sorted(date_set - set(d))
	return missing

def get_missing_date_ranges(rows):
    if len(rows)==0:
        return []
    date_strs = [row[0] for row in rows]
    d = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in date_strs]
    date_set = set(d[0] + timedelta(x) for x in range((d[-1] - d[0]).days))
    missing = sorted(date_set - set(d))
    start = False
    date_ranges = []
    for date in missing:
        if start==False:
            start = True
            curr = date
            start_date = date
        else:
            if date == (curr + timedelta(1)):
                curr = date
                continue
            else:
                date_ranges.append((start_date,curr))
                start_date = date
    if start==True:
        date_ranges.append((start_date,date))
    
    return date_ranges

def create_aux_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    create_query = "create table application_aux (date1 date, week1 varchar, year1 varchar, ws1 varchar, count1 integer);"
    c = conn.cursor()
    c.execute(create_query)


def insert_to_aux_table(conn, rows):
    for row in rows:
        date_str = datetime.strptime(row[0], '%Y-%m-%d').date()
        new_row = (date_str, row[1], row[2], row[3], row[4])
        insert_query = "insert into application_aux values (?,?,?,?,?)"
        c = conn.cursor()
        c.execute(insert_query, new_row)


def query_base_table_for_missing_date_ranges(conn, date_ranges):
    super_list = []
    for date_range in date_ranges:
        start_date = date_range[0]
        end_date = date_range[1]
        rows = select_from_base_table(conn, start_date, end_date)
        rows = fill_missing_gaps(rows)
        for row in rows:
            super_list.append(row)
    return super_list

def compute_answer(rows):
    ans_dict = {}
    for row in rows:
        date, week, year, ws, count = row
        if (week, year) in ans_dict:
            old_data = ans_dict[(week, year)]
            if date<old_data[0]:
                old_data[0] = date
            if ws in old_data[1]:
                old_data[1][ws] += count
            else:
                old_data[1][ws] = count
            ans_dict[(week,year)] = old_data

        else:
            ws_dict = {}
            ws_dict[ws] = count
            ans_dict[(week, year)] = [date, ws_dict]

    print "count,week,workflow_state"
    for key in ans_dict:
        val = ans_dict[key]
        date_str = val[0]
        #date_str = val[0].strftime('%Y-%m-%d')
        for key1 in val[1]:
            ws = key1
            count = val[1][key1]
            output = str(count) + ',' + date_str + ',' + str(ws)
            if ws!='blah':
                print output


def main() :
    database = "/Users/amitpanda/Downloads/applicants.sqlite3"
    conn =  create_connection(database)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    try:
        # Creating an auxillary table which can store data for future reuse
        create_aux_table(conn)
    except Exception as e: 
        #table already created
        pass
    
    #Getting data from auxillary table which has derived data from previous runs 
    auxTableRows = query_aux_table(conn, start_date, end_date)

    # Identifying if we need to query the base (applicants) table
    missingDateRangesForAuxData = get_missing_date_ranges(auxTableRows)

    if len(auxTableRows)==0:
        # Get data from old table because the auxillary table didn't have any rows for this date range.
        baseTableRows = query_base_table(conn, start_date, end_date)
    else :
        # If there was some data in the auxillary table BUT still need to get some data from the old table
        if len(missingDateRangesForAuxData) != 0:
            baseTableRows = query_base_table_for_missing_date_ranges(conn, missingDateRangesForAuxData)

    # Add the data fetched from the base into the auxillary table for future reuse
    insert_to_aux_table(conn, baseTableRows)

    # Merging the data from the base table and the auxillary table for in-memory computation
    for baseTableRow in baseTableRows:
        auxTableRows.append(baseTableRow)

    # Compute the week wise grouping and print the result
    compute_answer(auxTableRows)

if __name__ == '__main__':
    main()
