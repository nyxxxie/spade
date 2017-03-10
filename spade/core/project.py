import datetime
import hashlib
from sqlalchemy import create_engine
from .file import sfile, filemode
from .models.project import Base, ProjectInfo, ProjectFile

SCHEMA_VERSION = "0.1"

class SpadeProjectException(Exception): pass

class Project:
    """Represents an open session for spade."""

    def __init__(self, dbfile):
        self._db_init(path)
        self._db_update()

    def save(self, path: str=None):
        if path is None:
            path = self._dbfile

        if path == ":memory:":
            raise SpaceProjectException("Can't save to memory-mapped database...")

        self._db_update()

    def open_file(self, path: str, mode: filemode=filemode.rw):
        return sfile(self, path, mode)

    def db_engine(self):
        return self._engine

    def files(self):
        """
        Returns a list of files in the project.  Tuple format is (id, path,
        contents hash, base change, head change).
        """
        paths = []
        return paths

    def add_template(self, template):
        """
        Adds a template to the project.  Fails on adding duplicate templates.
        Can take both the path to a valid file and a currently open file object.
        """
        pass

    def remove_template(self, template):
        """
        Remove template from project.
        """
        pass

    def templates(self):
        """
        Returns a list of templates in the project.
        """
        pass

    def set_template_for_file(self, f, template):
        """
        Associates a template with a file.
        """
        pass

    def get_template_for_file(self, f, template):
        """
        Gets the associated template for a file.
        """
        pass

    def get_info(self, key: str=None):
        """
        Retrieves information about the project (schema version, database path,
        etc).  If no key is specified, this function will return a list of all
        project info available.
        """
        pass

    def _add_info(self, key, value):
        # Create db session
        Session = sessionmaker(bind=self._db_engine)
        session = Session()

        # Add info to table
        info = ProjectInfo(key=key, value=value)
        session.merge(entry)
        session.commit()

        return None

    def _db_init(self, path):
        self._dbfile = path
        self._db_engine = create_engine(
            "sqlite:///" + path,         # Create sqlite db and engine for sqlalchemy
            echo=True)                   # TODO: This should probably be commented out at some point
        Base.metadata.create_all(engine) # Adds all of our tables into the sqlite db

    def _db_update(self):
        date = datetime.datetime.now()
        if self.get_info("schema_version") is None:
            self._add_info("schema_version", SCHEMA_VERSION)
            self._add_info("creation_datetime", date)
            self._add_info("update_datetime", date)
        else
            self._add_info("update_datetime", date)
