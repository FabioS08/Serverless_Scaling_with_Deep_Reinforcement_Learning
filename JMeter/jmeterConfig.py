import pandas as pd
import xml.etree.ElementTree as ET


# This function adjusts the indentation of the generated XML file, just to make it more readable
def indent(elem, level = 0):

    i = "\n" + level * "  "
    
    if len(elem):
        
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        
        for child in elem:
            indent(child, level + 1)
        
        if not child.tail or not child.tail.strip():
            child.tail = i
    
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i


# We update the values of the Concurrency Thread Group (look at the ReadME for a complete explaination of the parameters) 

def writeConcurrencyThread(root, concurrencyValues):

    targetSampler = None

    for elem in root.iter("com.blazemeter.jmeter.threads.concurrency.ConcurrencyThreadGroup"):

        if elem.attrib.get("testname") == "Concurrency Thread Group":
            
            targetSampler = elem
            break


    for child in targetSampler:

        if child.tag == "stringProp":
            
            name = child.attrib.get("name")
        
            if name in concurrencyValues:

                child.text = concurrencyValues[name]

    return root


# We update the values of the HTTP Request format (look at the ReadME for a complete explaination of the parameters) 
def writeHTTPRequest(root, httpValues, jsonBody):

    targetSampler = None

    for elem in root.iter("HTTPSamplerProxy"):

        if elem.attrib.get("testname") == "Matrix Multiply - HTTP Request":
            
            targetSampler = elem
            break

    # Update the domain, port, path and method request
    for child in targetSampler:

        if child.tag == "stringProp":
            
            name = child.attrib.get("name")
        
            if name in httpValues:

                child.text = httpValues[name]

    # Update the request's body
    httpArgumentsProp = None
    for elem in targetSampler.iter("elementProp"):

        if elem.attrib.get("name") == "HTTPsampler.Arguments":
        
            httpArgumentsProp = elem
            break

    if httpArgumentsProp:

        for subelem in httpArgumentsProp.iter("stringProp"):
            
            if subelem.attrib.get("name") == "Argument.value":
            
                subelem.text = jsonBody
                break

    return root


# We update the values for the upload of the CSV file (look at the ReadME for a complete explaination of the parameters) 
def writeCSVFile(root, csvValues, csvBools):

    csvDataset = None

    for elem in root.iter("CSVDataSet"):

        if elem.attrib.get("testname") == "CSV File - Matrices":
        
            csvDataset = elem
            break

    for child in csvDataset:

        name = child.attrib.get("name")
        
        if child.tag == "stringProp" and name in csvValues:
            child.text = csvValues[name]
        
        elif child.tag == "boolProp" and name in csvBools:
            child.text = csvBools[name]

    return root


# Starting from the WorkLoad Profile, since the plug-in does not allow us to import it, we generate the actual elements to writes within the jmeter.jmx

def writeWorkload(root, workload, configFile):

    '''
    Format for each entry in the dataframe:

    <collectionProp name="84472748">                 # The name is not important, you can reuse it
        <stringProp name="48">0</stringProp>         # This represents the Initial RPS
        <stringProp name="49">1</stringProp>         # This represents the Final RPS
        <stringProp name="49">1</stringProp>         # This represents the Duration (expressed in seconds)
    </collectionProp>
    '''

    df = pd.read_csv(workload, delimiter = ';')

    duration = 1
    previousRPS = 1

    # Find the target <collectionProp name="load_profile"> (i.e. where we want to insert the workload)
    for elem in root.iter('collectionProp'):
        
        if elem.attrib.get('name') == 'load_profile':
            
            loadProfileElem = elem
            
            break

    # Just to be sure, we remove all the children of that node
    loadProfileElem.clear()
    loadProfileElem.set('name', 'load_profile')

    counter = 1
    for index, row in df.iterrows():

        #print(f"Row {index}: Time = {row['Time']}, RPS = {row['RPS']}")
        collection = ET.Element('collectionProp', {'name': str(counter)})
        
        ET.SubElement(collection, 'stringProp', {'name': str(previousRPS)}).text = str(previousRPS)
        ET.SubElement(collection, 'stringProp', {'name': str(row['RPS'])}).text = str(row['RPS'])
        ET.SubElement(collection, 'stringProp', {'name': str(duration)}).text = str(duration)

        loadProfileElem.append(collection)
        previousRPS = row['RPS']

        counter += 1

    indent(root)
    
    return root