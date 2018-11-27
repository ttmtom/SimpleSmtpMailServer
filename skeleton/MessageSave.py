#!/usr/bin/python3

import datetime
import calendar
import re
import base64
from pathlib import Path
from io import StringIO


# Class to save the message and attachment
class MessageSave:
    CRLF = '\r\n'

    # constructor
    def __init__(self, From, To, wholeBody):
        # sender of the message
        self.From = From
        # recever of the message
        self.To = To
        # the body of message
        self.rawData = wholeBody

    def save(self):
        Body = "From: "+self.From+self.CRLF+"To: "+self.To+self.CRLF
        # Use StringIO to read string as a file
        Data = StringIO(self.rawData)

        # Boolean flags for header information
        base64Encoded = False
        _7bitEncoded = False
        mime = False
        multipart = False
        plainText = False
        contentType = False

        # Boolean flags for header processing
        isHeader = True
        isMultiLine = False

        # boundary identificaion string
        boundary = ''
        # Sting for encoded message body
        encodedBody = ''
        # directory for saving files
        directory = self.FindVacancy('')

        # String for attachment appendix
        attachment = ''
        # String for filename to be saved
        fileName = ''
        # Create the directory
        Path(directory).mkdir()

        # Read the message header for the parameters used in this Email
        while True:
            dataLine = Data.readline()
            if dataLine == '':
                break
            dataLine = dataLine.rstrip()
            encodedBody += dataLine + self.CRLF

            # Save the Message Header Field (listed in project specification) to the message.txt
            # Different mail client may have different mail struct, you can modify the code here to satify different mail client.
            if re.fullmatch('^From:.*', dataLine) or re.fullmatch('^To:.*', dataLine) or re.fullmatch('Date:.*', dataLine) or re.fullmatch('Subject:.*', dataLine):
                Body += dataLine + self.CRLF
            # Break the while loop if all the header lines have been processed
            elif not isHeader or isMultiLine:
                break
            # Check all the tags in Content-Type (may be multiple line)
            elif re.fullmatch('''Fill in''', dataLine) or isMultiLine:
                Body += dataLine + self.CRLF
                if not contentType:
                    # Set up the flag to indicate Content-Type is processing
                    contentType = '''Fill in'''
                    # Crop the "Content-Type:" head
                    dataLine = '''Fill in'''
                # If all the Content-Type tags is read, put down the flag
                elif not re.fullmatch('''Fill in''', dataLine):
                    contentType = False

                # Parse the tags as tokens
                attribute = dataLine.split(';')
                for parameter in attribute:
                    parameter = parameter.strip()
                    # Check if this tag talks about boundary
                    if re.fullmatch('''Fill in''', parameter):
                        boundary = parameter[parameter.find("\"")+1:parameter.rfind("\"")]
                    # Check if this tag talks about multipart
                    if re.fullmatch('''Fill in''', parameter):
                        multipart = True
                    # Check if this tag talks about text/plain
                    if re.fullmatch('''Fill in''', parameter):
                        plainText = True
            # check the encoding of the transferred content
            elif re.fullmatch('Content-Transfer-Encoding:.*', dataLine):
                Body += dataLine + self.CRLF
                if re.fullmatch('Content-Transfer-Encoding:\\s*base64\\s*', dataLine):
                    base64Encoded = True
                elif re.fullmatch('Content-Transfer-Encoding:\\s*7bit\\s*', dataLine):
                    _7bitEncoded = True
            # Check if MIME is enabled in this Email
            elif re.fullmatch('''Fill in''', dataLine):
                mime = True
                Body += dataLine + self.CRLF
            # Check if invalid header field exist, if yes, it means that this is not header
            elif not (re.fullmatch('From:.*', dataLine) or re.fullmatch('To:.*', dataLine) or re.fullmatch('Message-Id:.*', dataLine) or re.fullmatch('Importance:.*', dataLine) or re.fullmatch('User-Agent:.*', dataLine) or re.fullmatch('X.+', dataLine) or re.fullmatch('Thread-Index:.*', dataLine) or re.fullmatch('Content-Language:.*', dataLine) or isMultiLine):
                isHeader = False

            # Check if this header consists of multiple line
            if re.fullmatch('.*;$', dataLine):
                isMultiLine = True
            else:
                isMultiLine = False

        # Separate the message header with actual message content
        Body += "-------------------------------------------------" + self.CRLF

        # If the above while loop do processing header, discard them
        if isHeader:
            encodedBody = ''

        # This while loop crops the non-MIME parts in MIME email
        while True:
            dataLine = Data.readline()
            if dataLine == '':
                break
            dataLine = dataLine.rstrip()
            # Check if we meet the boundary in MIME message
            # Here we use equals instead of matchs because the matches opration may be confused due to the Escape character in the boudnary string
            if mime and (dataLine == '''Fill in''' or dataLine == '''Fill in'''):
                break
            # if the Email is non-MIME, Single Part or without header, save the body
            encodedBody += '''Fill in'''

        # Do it only if the Email is non-MIME, Single Part or without header
        if '''Fill in''' or (not mime) or '''Fill in''':
            # If it is base64 encoded, decode it and place it at message.txt
            if '''Fill in''' and len(encodedBody) > 0:
                Body += base64.b64decode(encodedBody).decode()
            else:
                Body += '''Fill in'''
        # This block is only for Multipart Message
        else:
            # isHeader is reused to indicate MIME header is processing
            isHeader = True
            # A flag to indicate MIME-style message.txt is filled or not
            bodyFilled = False
            # Reset the encodedBody
            encodedBody = ''
            # This while loop loops for each part
            while True:
                dataLine = Data.readline()
                if dataLine == '':
                    break
                dataLine = dataLine.rstrip()
                # We are processing MIME header
                if isHeader:
                    # Turn down the flag if all header is processed
                    if dataLine == '':
                        isHeader = False
                    # Check the supported encoding method (base64/7bit) and set the corresponding flags
                    elif re.fullmatch('''Fill in''', dataLine):
                        '''Fill in'''
                        Body += dataLine + self.CRLF + self.CRLF
                    elif re.fullmatch('''Fill in''', dataLine):
                        '''Fill in'''
                        Body += dataLine + self.CRLF + self.CRLF
                    # Check the Content-Type tags, Same as above
                    elif re.fullmatch('Content-Type:.*', dataLine) or contentType:
                        Body += dataLine + self.CRLF
                        if not contentType:
                            contentType = True
                            dataLine = dataLine[13:]
                        elif not re.fullmatch('.*;$', dataLine):
                            contentType = False

                        attribute = dataLine.split(';')
                        for parameter in attribute:
                            # We get the filename of this attachment
                            if re.fullmatch('\\s*name=.*', parameter):
                                fileName = parameter[parameter.find("\"")+1:parameter.rfind("\"")]
                                # Check if the filename is encoded. If so, we decode the filename
                                if re.fullmatch('^=\\?.+\\?B\\?.*', fileName):
                                    encoding = fileName[2:fileName.find('?B?')]
                                    fileName = fileName[fileName.find('?B?')+3:]
                                    fileName = base64.b64decode(fileName).decode(encoding)
                                print("filename=" + fileName)
                            # If this part is text/plain or not
                            if re.fullmatch('\\s*text/plain.*', parameter):
                                plainText = True
                # We hit the boundary, it is the time to save the attachment
                elif dataLine == ("--"+boundary) or dataLine == ("--"+boundary+"--"):
                    # If this part is using un-supported encoding method
                    if (not _7bitEncoded) and (not base64Encoded):
                        # If this part doesn't give the filename, use "Attachment" as default
                        if fileName == '':
                            fileName = 'Attachment'
                        # Check if the filename already exists. If so, we choose a new one
                        fileName = str(self.FindVacancy(str(directory)+'\\'+fileName))
                        # Display a line in message.txt to indicate this attachment encounters problem
                        attachment += fileName[fileName.rfind('\\') + 1:] + ' (discarded due to unknown encoding method)' + self.CRLF
                    # If this part is the first MIME-style text message, serve it as message body
                    # (This part should be no attachment filename and Content-type is text/plain)
                    elif (not bodyFilled) and plainText and fileName == '':
                        bodyFilled = True
                        if base64Encoded:
                            Body += base64.b64decode(encodedBody).decode()
                        else:
                            Body += encodedBody
                    # For other supported attachment, process it here
                    else:
                        if fileName == '':
                            fileName = 'Attachment'
                        fileName = str(self.FindVacancy(str(directory)+'\\'+fileName))
                        # Open the file for writing
                        with Path(fileName).open('wb') as f:
                            if base64Encoded:
                                f.write(base64.b64decode(encodedBody))
                            else:
                                f.write(encodedBody.encode())
                        # Display a line in message.txt to indicate this attachment
                        attachment += fileName[fileName.rfind('\\') + 1:] + self.CRLF

                    # Reset the necessary flags and variable for next MIME part.
                    base64Encoded = '''Fill in'''
                    _7bitEncoded = '''Fill in'''
                    plainText = False
                    isHeader = True
                    encodedBody = ''
                    fileName = ''
                # In normal case, just accumulate the string read
                else:
                    encodedBody += dataLine + self.CRLF

        # Finally we save the message body to message.txt
        # Append the attachment information at the end of the message.txt
        if multipart and mime:
            Body += "-------------------------------------------------" + self.CRLF + "File(s) of Attachment :" + self.CRLF + attachment
            print("multipart and mime=" + str(multipart) + " " + str(mime))
            print("attachment=" + attachment)

        # Open the message.txt file and write it
        with Path(self.FindVacancy(str(directory)+'\\'+'message.txt')).open('wb') as f:
            f.write(Body.encode())

        return True

    # This method find out the next available directory/file name
    def FindVacancy(self, prefix):
        counter = 0
        extension = ''

        if prefix == '':
            entry = Path(self.Today()+'_'+str(counter))
        else:
            entry = Path(prefix)

        if prefix.rfind('.') >= 0:
            extension = prefix[prefix.rfind('.'):]
            prefix = prefix[:prefix.rfind('.')]

        while entry.exists():
            counter = counter + 1
            if prefix == '':
                entry = Path(self.Today()+'_'+str(counter))
            else:
                entry = Path(prefix+'_'+str(counter)+extension)
        return entry.resolve()


    # This method return the date in simple DDMMM format
    def Today(self):
        now = datetime.datetime.now()
        monthAbbr = calendar.month_abbr[now.month]
        return str(now.day) + monthAbbr
