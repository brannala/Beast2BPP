import xml.sax

noloci = 0
maxNoSeqs = 0

class BeastHandler ( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.data = ""
        self.format = ""
        self.sequence = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""
        self.title = ""
        self.firstcall = 0


    # Call when an element starts
    def startElement(self, tag, attributes):
        global noloci
        global maxNoSeqs
        self.CurrentData = tag
        if tag == "data":
            noseqs = attributes["id"]
            noloci+=1
            f.write('\n')
            f.write("  ")
            f.write(noseqs)
            if int(noseqs) > maxNoSeqs:
                maxNoSeqs=int(noseqs)
            self.firstcall=0
        elif tag == "sequence":
            self.title = attributes["taxon"]
    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "type":
            print ("Type:", self.type)
        elif self.CurrentData == "format":
            print ("Format:", self.format)
        elif self.CurrentData == "sequence":
            astring=self.sequence
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
        elif self.CurrentData == "year":
            print ("Year:", self.year)
        elif self.CurrentData == "rating":
            print ("Rating:", self.rating)
        elif self.CurrentData == "stars":
            print ("Stars:", self.stars)
        elif self.CurrentData == "description":
            print ("Description:", self.description)
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):

        if self.CurrentData == "type":
            self.type = content
        elif self.CurrentData == "format":
            self.format = content
        elif self.CurrentData == "sequence":
            self.sequence = content
        elif self.CurrentData == "year": 
            self.year = content
        elif self.CurrentData == "rating":
            self.rating = content
        elif self.CurrentData == "stars":
            self.stars = content
        elif self.CurrentData == "description":
            self.description = content

if ( __name__ == "__main__"):

    beast_xml_file = input("Enter Beast xml file name: ")
    f = open("bpp.txt",'w')

    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # override the default ContextHandler
    Handler = BeastHandler()
    parser.setContentHandler( Handler )
    
    parser.parse(beast_xml_file)
    print("File",beast_xml_file, "with", noloci, "loci and a maximum of",maxNoSeqs,"sequences per locus was successfully converting to BPP format.")
    print("BPP files are named bpp.ctl, bpp.txt and bpp.map.")

    f.close()


 
