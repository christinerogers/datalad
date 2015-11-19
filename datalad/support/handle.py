# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Implements datalad handle metadata representation.
"""

import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from .metadatahandler import DLNS, RDF, Graph, Literal
from.exceptions import ReadOnlyBackendError


lgr = logging.getLogger('datalad.handle')


class Handle(object):
    """Representation of a Handle's metadata.

    This is a top-level representation of a handle. In that sense a handle is
    a set of metadata, represented as a named rdflib.Graph. Parts of the
    metadata may be accessible directly by an attribute without the need to
    explicitly query the graph. The latter by now counts especially for the
    attributes `url` and `name`. Additionally, this kind of a handle is linked
    to an underlying backend, that may also provide access to the actual
    content of the handle.
    Note, that this graph is a runtime object residing in memory. The
    `update_metadata` and `commit_metadata` methods are meant to be used to
    synchronize the graph and the underlying storage.

    This is an abstract class, that basically defines a general interface to
    handles. Any backend to be supported should be implemented by deriving from
    this class.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self._graph = None

    def __repr__(self):
        return "<Handle name=%s (%s)>" % (self.name, type(self))

    @abstractproperty
    def url(self):
        """URL of the physical representation of a handle.

        This is a read-only property, since an url can only be provided by a
        physically existing handle. It doesn't make sense to tell a backend to
        change it.

        Returns
        -------
        str
        """
        pass

    @abstractmethod
    def update_metadata(self):
        """Update the graph containing the handle's metadata.

        Called to update 'self._graph' from the handle's backend.
        Creates a named graph, whose identifier is the name of the handle.
        """
        pass

    @abstractmethod
    def commit_metadata(self, msg="Metadata updated."):
        """Commit the metadata graph of a handle to its storage backend.

        A backend can deny to write handle data. In that case is should raise
        a ReadOnlyBackendError.

        Parameters
        ----------
        msg: str
            optional commit message.

        Raises
        ------
        ReadOnlyBackendError
        """
        pass

    def get_metadata(self):
        if self._graph is None:
            lgr.debug("Updating handle graph from backend.")
            self.update_metadata()
        return self._graph

    # TODO: Not sure yet, whether setting the graph directly should
    # be allowed. This involves change of the identifier, which may
    # mess up things. Therefore may be don't let the user set it.
    # Triples can be modified anyway.
    # This also leads to the thought of renaming routine, which would need
    # to copy the entire graph to a new one with a new identifier.
    def set_metadata(self, data):
        self._graph = data

    meta = property(get_metadata, set_metadata, doc="""
    Named rdflib.Graph representing the metadata of the handle.
    This is a lazy loading property, that is created only when accessed. Note,
    that this is not necessarily always in sync with the underlying backend.
    Therefore `update_metadata` and `commit_metadata` are provided,
    to explicitly make sure it's synchronized. """)

    @property
    def name(self):
        """Name of the handle.

        Returns
        -------
        str
        """
        return str(self.meta.identifier)


class RuntimeHandle(Handle):
    """Pure runtime Handle without a persistent backend.

    This kind of a handle can only be used as a "virtual" handle, that has no
    physical storage.

    Note: For now, there is no usecase.
    It serves as an example and a test case.
    """

    def __init__(self, name):
        super(RuntimeHandle, self).__init__()
        self._graph = Graph(identifier=Literal(name))
        self._graph.add((DLNS.this, RDF.type, DLNS.Handle))

    @property
    def url(self):
        return None

    def update_metadata(self):
        pass

    def commit_metadata(self, msg="Metadata updated."):
        raise ReadOnlyBackendError("Can't commit RuntimeHandle.")
