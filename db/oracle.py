# encoding: utf-8
import cx_Oracle
import os

# 这样可以保证select出来的中文显示没有问题。
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

__author__ = 'jeffye'

db = cx_Oracle.connect('test', 'test', '192.168.1.165:1521/orcl')
dsn_tns = cx_Oracle.makedsn('192.168.1.165', 1521, 'orcl')

curs = db.cursor()


def insert_update_cn():
    """
    正常的insert和update中文，还需要指定python源文件的字符集密码和oracle一致
    """
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    rs = curs.execute('select * from cfg_haoduan_gh where rownum<9')
    li = rs.fetchall()
    print li[0][3].decode('utf-8')

    curs.execute('insert into test_ccc values(1,sysdate,\'北\')')
    db.commit()
    db.close()


def show_all_tables(cur):
    sql = "select * from tab"
    curs.execute(sql)
    # print all tables?
    for row_data in cur:
        print row_data


def show_item():
    sql = "select * from NEWS_MAIN"
    curs2 = db.cursor()
    curs2.execute(sql)
    item = next(curs2)
    print 'NEWS_MAIN', item

    sql1 = "select * from NEWS_CONTENT"
    curs_sql1 = db.cursor()
    curs_sql1.execute(sql1)

    item = next(curs_sql1)
    print "NEWS_CONTENT", item
    lob_term = item[-1]
    # read lob column
    print lob_term.read().decode('gb2312')


def show_description(cur):
    # 获取数据表的列名，并输出
    title = [i[0] for i in cur.description]
    # 格式化字符串
    g = lambda k: "%-8s" % k
    title = map(g, title)
    for i in title:
        print i,
    print


def join_test():
    sql = "select t1.news_id, t1.title_main, t1.nega_posi_par, t2.html_txt " + \
          "from news_main t1, news_content t2 where t1.news_id = t2.news_id and t1.nega_posi_par in (0, 1,2) " + \
          "and t1.isvalid = 1 and t2.isvalid = 1"
    sql = "select t1.news_id, t1.title_main, t1.nega_posi_par, t2.html_txt " + \
          "from news_main t1, news_content t2 where t1.news_id = t2.news_id " + \
          "and t1.isvalid = 1 and t2.isvalid = 1"
    cur = db.cursor()
    cur.execute(sql)

    # all_data = cur.fetchall()
    # print "all data count", type(all_data)
    # print 'row_count', cur.rowcount, len(cur.fetchall())
    # return

    all_data_coverted = []
    for i, row in enumerate(cur):
        all_data_coverted.append((row[0], row[1], row[3].read() if row[3] else row[3], row[2]))

    # all_data_coverted = [(x[0], x[1], x[3].read(), x[2]) for x in all_data]
    import pandas as pd
    col = ['news_id', 'title', 'content', 'tag']
    df = pd.DataFrame(all_data_coverted, columns=col)
    df1 = df.set_index('news_id')
    df1.to_csv("/home/jeffye/Desktop/data/youpin/converted.csv", sep='\t', encoding='utf-8')
    print 'finished %s rows' % len(all_data_coverted)


if __name__ == '__main__':
    # sql = "select * from NEWS_MAIN"d
    # cur = db.cursor()
    # cur.execute(sql)
    # show_description(cur)
    # sql1 = "select * from NEWS_CONTENT"
    # cur1 = db.cursor()
    # cur1.execute(sql1)
    # show_description(cur1)
    #
    # show_item()

    join_test()
