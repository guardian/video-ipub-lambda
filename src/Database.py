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
    
    def __init__(self,make_connection=True):
        self._conn = None
        if(make_connection): self.do_connect()
        
    def do_connect(self):
        import config
        
        if not hasattr(config,'DATABASE'):
            raise RuntimeError("DATABASE dictionary is missing from config.py")
        self._conn = mysql.connect(**config.DATABASE)
    
    def _get_filename(self,meta):
        """
        Scans FILENAME_FIELDS looking for a value that is set
        :param meta: metadata dictionary
        :return: a valid filename, or None if none was found
        """
        for f in self.FILENAME_FIELDS:
            if f in meta:
                return meta[f]
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
            return self._make_new_record(filename,meta['octopus ID'],meta['project_name'])
        