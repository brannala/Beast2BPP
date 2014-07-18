from xml.sax.handler import ContentHandler
from xml.sax import parse

noloci = 0
maxNoSeqs = 0

class dataHandler(ContentHandler):
    in_sequence = False

    def __init__(self,sequence):
        ContentHandler.__init__(self)
        self.sequence = sequence
        self.data = []
        self.firstcall = 0
        self.title=""
       
    def startElement(self,name,attrs):
        global noloci
        global maxNoSeqs
        self.data = name
        if name == "data":
            noseqs = attrs["id"]
            noloci+=1
            f.write('\n')
            f.write("  ")
            f.write(noseqs)
            if int(noseqs) > maxNoSeqs:
                maxNoSeqs=int(noseqs)
            self.firstcall=0
        elif name == "sequence":
            self.title = attrs["taxon"]
            self.in_sequence = True

    def endElement(self, name):
        if name == "sequence":
            astring=self.data
            a2=astring.strip()
            if self.firstcall==0:
                a3=len(a2)
                f.write("  ")
                f.write(str(a3))
                f.write('\n\n')
                self.firstcall=1
            f.write(self.title)
            f.write('\n')
            f.write(a2)
            f.write('\n')
            self.data = []

    def characters(self,string):
        if self.in_sequence:
            self.data=string
            
class BeastHandler(ContentHandler):
    in_taxonsuperset = False
    currSpecies=''
        
    def startElement(self,name,attrs):
        if name == 'taxonset':
            if attrs["id"] == 'taxonsuperset':
                self.in_taxonsuperset = True
        if name == 'taxon':
            if self.in_taxonsuperset:
                if attrs["spec"] == 'TaxonSet':
                    self.currSpecies=attrs["id"]
                elif attrs["spec"] == 'Taxon':
                    m.write(self.currSpecies)
                    m.write("\t")
                    m.write(attrs["id"])
                    m.write("\n")
    
    def endElement(self, name):
        if name == 'taxonset':
            self.in_taxonsuperset = False

            
sequence = []
species = []

beast_xml_file = input("Enter Beast xml file name: ")
f = open("bpp.txt",'w')
m = open("bpp.map",'w')

parse(beast_xml_file,dataHandler(sequence))
print('The following sequences were found:')
for h in sequence:
    print(h)

parse('examples/testStarBeast.xml',BeastHandler())
print("File",beast_xml_file, "with", noloci, "loci and a maximum of",maxNoSeqs,"sequences per locus was successfully converting to BPP format.")
print("BPP files are named bpp.ctl, bpp.txt and bpp.map.")
f.close()
m.close()
    
