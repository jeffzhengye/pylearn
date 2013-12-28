__author__ = 'zheng'


import os, re, sys, lucene

from java.io import File

from org.apache.lucene.analysis.core import LowerCaseFilter, StopFilter, StopAnalyzer
from org.apache.lucene.analysis.en import PorterStemFilter
from org.apache.lucene.analysis.standard import StandardTokenizer, StandardFilter, StandardAnalyzer
from org.apache.pylucene.analysis import PythonAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.index import IndexWriter, IndexWriterConfig

from org.apache.lucene.util import Version
from java.io import StringReader
from org.apache.lucene.analysis.tokenattributes import OffsetAttribute
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
#from org.apache.lucene.analysis.ja.tokenattributes import PartOfSpeechAttribute

from string import Template
from subprocess import *


class PorterStemmerAnalyzer(PythonAnalyzer):
    def createComponents(self, fieldName, reader):
        source = StandardTokenizer(Version.LUCENE_CURRENT, reader)
        filter = StandardFilter(Version.LUCENE_CURRENT, source)
        filter = LowerCaseFilter(Version.LUCENE_CURRENT, filter)
        filter = PorterStemFilter(filter)
        filter = StopFilter(Version.LUCENE_CURRENT, filter,
        StopAnalyzer.ENGLISH_STOP_WORDS_SET)
        return self.TokenStreamComponents(source, filter)



lucene.initVM(vmargs=['-Djava.awt.headless=true'])
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
input = 'this is a test string for Analyzer'
ts = analyzer.tokenStream("dummy", StringReader(input))

#matchVersion = Version.LUCENE_XY; ##Substitute desired Lucene version for XY

offsetAtt = ts.addAttribute(OffsetAttribute.class_)
termAtt = ts.addAttribute(CharTermAttribute.class_)
#posAtt = ts.addAttribute(PartOfSpeechAttribute.class_)

def testStandard():
    ts.reset(); ##Resets this stream to the beginning. (Required
    while ts.incrementToken():
        #print ts.r
        #print ts.reflectAsString(True)
        print offsetAtt.startOffset()
        print offsetAtt.endOffset()
        print termAtt.toString() #, posAtt.getPartOfSpeech()
    ts.end()
    ts.close()


def testPorter():
    print 'lucene', lucene.VERSION, lucene.CLASSPATH
    input = 'this is a test string for Analyzer'
    input = "krasnoselskii organ  distingish zalog injection injector gps information"
    analyzer = PorterStemmerAnalyzer()
    ts = analyzer.tokenStream("dummy", StringReader(input))
    offsetAtt = ts.addAttribute(OffsetAttribute.class_)
    termAtt = ts.addAttribute(CharTermAttribute.class_)
    ts.reset(); ##Resets this stream to the beginning. (Required
    while ts.incrementToken():
        #print ts.r
        #print ts.reflectAsString(True)
        print termAtt.toString(), offsetAtt.startOffset(), offsetAtt.endOffset()
    ts.end()
    ts.close()

testPorter()


def indexFile(dir, filename):

    path = os.path.join(dir, filename)
    print "  File: ", filename

    if filename.endswith('.gz'):
        child = Popen('gunzip -c ' + path + ' | groff -t -e -E -mandoc -Tascii | col -bx', shell=True, stdout=PIPE, cwd=os.path.dirname(dir)).stdout
        command, section = re.search('^(.*)\.(.*)\.gz$', filename).groups()
    else:
        child = Popen('groff -t -e -E -mandoc -Tascii ' + path + ' | col -bx',
                      shell=True, stdout=PIPE, cwd=os.path.dirname(dir)).stdout
        command, section = re.search('^(.*)\.(.*)$', filename).groups()

    data = child.read()
    err = child.close()
    if err:
        raise RuntimeError, '%s failed with exit code %d' %(command, err)

    matches = re.search('^NAME$(.*?)^\S', data,
                        re.MULTILINE | re.DOTALL)
    name = matches and matches.group(1) or ''

    matches = re.search('^(?:SYNOPSIS|SYNOPSYS)$(.*?)^\S', data,
                        re.MULTILINE | re.DOTALL)
    synopsis = matches and matches.group(1) or ''

    matches = re.search('^(?:DESCRIPTION|OVERVIEW)$(.*?)', data,
                        re.MULTILINE | re.DOTALL)
    description = matches and matches.group(1) or ''

    doc = Document()
    doc.add(Field("command", command, StringField.TYPE_STORED))
    doc.add(Field("section", section, StringField.TYPE_STORED))
    doc.add(Field("name", name.strip(), TextField.TYPE_STORED))
    doc.add(Field("synopsis", synopsis.strip(), TextField.TYPE_STORED))
    doc.add(Field("keywords", ' '.join((command, name, synopsis, description)),
                  TextField.TYPE_NOT_STORED))
    doc.add(Field("filename", os.path.abspath(path), StringField.TYPE_STORED))

    writer.addDocument(doc)


def indexDirectory(dir):

    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            indexFile(dir, name)

def TestIndex(index_path='./index'): ##from manindex.py
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    directory = SimpleFSDirectory(index_path)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
    config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    manpath = os.environ.get('MANPATH', '/usr/share/man').split(os.pathsep)
    for dir in manpath:
        print 'Crawling', dir
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isdir(path):
                indexDirectory(path)

def search_with_Similarity():
    import datetime
    from org.apache.lucene.search.similarities import BM25Similarity

    class CustomTemplate(Template):
        delimiter = '#'

    template = CustomTemplate(format)

    fsDir = SimpleFSDirectory(File(indexDir))
    searcher = IndexSearcher(DirectoryReader.open(fsDir))
    searcher.setSimilarity(BM25Similarity(1.2, 0.75)) ##BM25Similarity(float k1, float b)
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    parser = QueryParser(Version.LUCENE_CURRENT, "keywords", analyzer)
    parser.setDefaultOperator(QueryParser.Operator.AND)
    query = parser.parse(' '.join(args))
    start = datetime.now()
    hits = searcher.search(query, 50)
    scoreDocs = searcher.search(query, 50).scoreDocs
    duration = datetime.now() - start
    stats = True
    if stats:
        print >>sys.stderr, "Found %d document(s) (in %s) that matched query '%s':" %(len(scoreDocs), duration, query)

    for h in hits:
      hit = lucene.Hit.cast_(h)
      id, doc = hit.getId(), hit.getDocument()
      print (id, doc)

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        table = dict((field.name(), field.stringValue())
                     for field in doc.getFields())
        print template.substitute(table)
