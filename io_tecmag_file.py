"""
Created on Wed Mar 25 02:06:00 2020

@author: saisivakumar
"""

import numpy as np

def read_tecmag_file(filename):
    """Opens the .tnt file in read and binary mode as fobj"""
    with open(filename, "rb") as fobj:
        """read() everything from fobj"""
        filebytes = fobj.read()
        fobj.close()
    #    print(filebytes)
        """Bytearray stores filebytes as an fbytes array"""
        fbytes = bytearray(filebytes)
    #    print(fbytes)
    #    del filebytes
        
        """Defining global variables"""
        endian = '<'
        bidx = 0
        
        """Retrieves versionID of the input file from 0 to 8 bytes"""
        versionID = fbytes[bidx:bidx+8]
#        print("versionID: ", versionID)
        bidx += 8
            
        """Retrieves tecmag tag from 8 to 12 bytes"""
        Tmagtag_0 = fbytes[bidx:bidx+4]
        assert(Tmagtag_0 == b'TMAG')
#        print("Tecmag tag:", Tmagtag_0)
        bidx += 4
        
        """Retrieves boolean value from 12 to 16 bytes"""
        Boolval_0 = bool(fbytes[bidx:bidx+4])
#        print("Boolean Values:", Boolval_0)
        bidx += 4
        
        """Retrieves tecmag length from 16 to 20 bytes"""
        #1st element of returned array
        TECLength = np.array(fbytes[bidx:bidx+4]).view(endian + 'i4')[0]  
#        print("Tecmag length:", TECLength)
        bidx += 4
     
        """Retrieves tecmag bytes from 20 to 1044 bytes"""
        Tbytes = fbytes[bidx:bidx+TECLength]
    #    print("Tecmag bytes:", Tbytes)
        bidx += TECLength
       
        """Retrieves nmr datatag from 1044 to 1048 bytes"""
        data_tag = fbytes[bidx:bidx+4]
        assert(data_tag == b'DATA')
#        print("Data tag:", data_tag)
        bidx += 4
    
        """Retrieves boolean value from 1048 to 1052 bytes"""
        Boolval_1 = bool(fbytes[bidx:bidx+4])
#        print("Boolean value:", Boolval_1)
        bidx += 4
        
        """Retrieves data length from fbytes array from 1052 to 1056 bytes"""
        #1st element of returned array
        data_length = np.array(fbytes[bidx:bidx+4]).view(endian+'i4')[0]
#        print("Data length:", data_length, "\n")
        bidx += 4
        
        """Retrieves data bytes from fbytes array"""
        databytes =  fbytes[bidx:bidx+data_length]
    #    print("Data types:", databytes, "\n")
        bidx += data_length
        
        """Retrives tecmag tag from fbytes array"""
        Tmagtag_1 = fbytes[bidx:bidx+4]
        assert(Tmagtag_1 == b'TMG2')
#        print("Tecmag tag:", Tmagtag_1)
        bidx += 4
        
        """Retrieves boolean value from fbytes array"""
        Boolval_2 = bool(fbytes[bidx:bidx+4])
#        print("Boolean value:", Boolval_2)
        bidx += 4
        
        """Retrieves tecmag length 2 from fbytes array"""
        TEC2Length = np.array(fbytes[bidx:bidx+4]).view(endian+'i4')[0]
#        print("Tecmag length_2:", TEC2Length)
        bidx += 4
        
        """Retrieves tecmag 2 bytes from fbytes array"""
        T2bytes = fbytes[bidx:bidx+TEC2Length]
        bidx += TEC2Length
        
        """Retrieves tecmag tag 2 from fbytes array"""
        Tmagtag_2 = fbytes[bidx:bidx+4]
        assert(Tmagtag_2 == b'PSEQ')
#        print("Tecmag tag:", Tmagtag_2)
        bidx += 4
        
    
        """Retrieves boolean value from fbytes array"""
        Boolval_3 = bool(fbytes[bidx:bidx+4])
#        print("Boolean value:", Boolval_3)
        bidx += 4
        
        """Retrives entire RF sequence bytes"""
        RFsequencebytes = fbytes[bidx:len(fbytes)]
    #    print("RF sequence bytes:", RFsequencebytes)
#        print("Length of bytes in fbyres array:", len(fbytes))
        
        # read header specifics
        """Reads number of points in four dimensions"""
        npts4d = np.array(Tbytes[0:16]).view(endian+'i4')
#        print("Num of points in 4-dimension:", npts4d)
        
        """Reads observed frequency in four dimennsions"""
        obsfreq4d = np.array(Tbytes[84:84+32]).view(endian+'f8')
#        print("Observed frequency in 4-dimension:", obsfreq4d)
        
        """Reads referece frequency"""
        #1st element of returned array
        referencefreq = np.array(Tbytes[180:180+8]).view(endian+'f8')[0]
#        print("Reference frequency:", referencefreq)
        
        """Reads observed channel"""
        obschannel = np.array(Tbytes[196:196+2]).view(endian+'h')[0]
#        print("Observed frequency channel:", obschannel)
        
        """Reads spectral width data in four dimensions"""
        spectralwidth4d = np.array(Tbytes[240:240+32]).view(endian+'f8')
#        print("Spectral width in 4-dimension:", spectralwidth4d)
        
        """Reads dwell time in four dimensions"""
        dwell4d = np.array(Tbytes[272:272+32]).view(endian+'f8')
#        print("Dwell time:", dwell4d)
    
        """Checks datalength is equal to num of points"""
    #    if (datalength != np.prod(npts4d)):    
    #        print('error in reading the tecmag file, dimensions do not agree')
       
        #read data specifics    
        data_int_float_format = 1       # 1=float16 and 0 = int16
        data_number_type = 1            # 1=complex, 0 = real values only
        complex_interleaved =  1        # 0=re,re,re...im,im,im,   %1=re,im,re,im...
        
        if data_int_float_format:
            datapts = np.array(databytes).view(endian+'f4')
        else:
            datapts = np.array(databytes).view(endian+'i4')
        numdatapts = len(datapts)
        
        if data_number_type:    # complex numbers
            if complex_interleaved:
                datapts = datapts[0:numdatapts:2]+1j*datapts[1:numdatapts:2]       # %1=re,im,re,im...
            else:
                datapts = datapts[0:numdatapts/2]+1j*datapts[numdatapts/2+1:numdatapts]      #0=re,re,re...im,im,im,
        else:  #real values only
            #datapts = datapts
            pass
        numdatapts = len(datapts)
    
        ndim = sum(npts4d>1)
        
        #assuming that the first dimension(s) are the populated ones
        data = np.reshape(datapts,npts4d[0:ndim])
        dwell = dwell4d[0:ndim]
        obsFreq = obsfreq4d[obschannel-1]
    return data, dwell, obsFreq 

