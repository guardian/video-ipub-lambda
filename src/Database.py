import mysql.connector as mysql
import re
import logging


class InvalidData(StandardError):
    pass


class NotFound(StandardError):
    pass


class Database(object):
    FILENAME_FIELDS = ['filename','originalFilename']
    CHOPPER = re.compile(r'\.[^\.]+$')
    
    SCHEMA_COLUMNS = [
        "encodingid",
        "contentid",
        "url",
        "format",
        "mobile",
        "multirate",
        "vcodec",
        "acodec",
        "vbitrate",
        "abitrate",
        "lastupdate",
        "frame_width",
        "frame_height",
        "duration",
        "file_size",
        "fcs_id",
        "octopus_id",
        "aspect"
    ]
    
    def __init__(self,config=None,make_connection=True):
        self._conn = None
        if(make_connection): self.do_connect(config)
        
    def do_connect(self,configdict=None):
        import config
        
        if isinstance(configdict,dict):
            self._conn = mysql.connect(**configdict)
            return
        
        if hasattr(config,'DATABASE'):
            self._conn = mysql.connect(**config.DATABASE)
            return
            
        raise RuntimeError("DATABASE dictionary is missing from config.py, or environment variables are not set")
        
    @staticmethod
    def _remove_extension(string):
        return re.sub('\.[^\.]+$','',string)
        
    def _get_filename(self,meta):
        """
        Scans FILENAME_FIELDS looking for a value that is set
        :param meta: metadata dictionary
        :return: a valid filename, or None if none was found
        """
        for f in self.FILENAME_FIELDS:
            if f in meta:
                return self._remove_extension(meta[f])
        return None
    
    def _make_filebase(self,filename):
        """
        Chops any file extension off the end of filename
        :param filename:
        :return:
        """
        return self.CHOPPER.sub("",filename)
    
    def _find_in_database(self,filename):
        """
        Looks up the database record for the given filebase
        :param filename: filebase to query
        :return: a dictionary of data or None
        """
        cur = self._conn.cursor()
        cur.execute("SELECT contentid from idmapping WHERE filebase=%s order by contentid desc", (filename,))

        item_ids = map(lambda x: x[0],cur.fetchall())
        cur.close()
        
        if len(item_ids)>1: logging.warning("Multiple rows returned for filebase {}".format(filename))
        if len(item_ids)>0: return item_ids[0]

        raise NotFound(filename)
    
    def _make_new_record(self,filebase,octid,project):
        """
        Creates a new record in the idmapping table for the given filebase
        :param filebase:
        :param octid:
        :param project:
        :return:
        """
        
        cur = self._conn.cursor()
        cur.execute("INSERT INTO idmapping (filebase,octopus_id,project) values (%s,%s,%s)", (filebase,octid,project))
        self._conn.commit()
        return cur.lastrowid
    
    def get_contentid(self,meta):
        filename = self._get_filename(meta)
        if filename is None:
            raise InvalidData("No recognised filename in metadata. Tried {0}".format(self.FILENAME_FIELDS))
        
        try:
            return self._find_in_database(filename)
        except NotFound:
            return self._make_new_record(filename,meta['octopus_id'],meta.get('project', "(no project)"))
    
    def _get_sqlargs(self,meta):
        fields = []
        placeholders = []
        values = []
        for k,v in meta.items():
            if k in self.SCHEMA_COLUMNS:
                fields.append(k)
                placeholders.append("%s")
                values.append(v)
            else:
                logging.warning("Database::_get_sqlargs - column {0} does not exist in the database.".format(k))
        return (fields, placeholders, values)
    
    def add_encoding(self,contentid,meta):
        meta.update({'contentid': contentid})
        (fields, placeholders, values) = self._get_sqlargs(meta)

        print meta
        
        cur = self._conn.cursor()
        cur.execute("INSERT INTO encodings ({f}) values ({p})"
                      .format(f=",".join(fields),p=",".join(placeholders)),
                    tuple(values))
        
        self._conn.commit()
        cur.close()
        return cur.lastrowid
    
    def get_encoding(self,contentid,limit=None):
        cur = self._conn.cursor()
        sqlcmd = "SELECT * from encodings where contentid=%s order by encodingid"
        if isinstance(limit,int):
            sqlcmd += " limit {0}".format(limit)
            
        cur.execute(sqlcmd, (contentid,))
        
        fields = map(lambda x:x[0],cur.description)
        rtn = map(lambda row: dict(zip(fields,row)), cur.fetchall())
        cur.close()
        return rtn