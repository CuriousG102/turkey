import re
from django.utils import six
from django.utils.encoding import smart_text
from django.utils.six import StringIO
from django.utils.xmlutils import SimplerXMLGenerator
from rest_framework.renderers import BaseRenderer


# credit to: http://jpadilla.github.io/django-rest-framework-xml/
# for much of this code
class XMLBodyRenderer(BaseRenderer):
    media_type = 'application/xml'
    format = 'xml'
    charset = 'utf-8'

    def __init__(self, item_tag_name='list_item', root_tag_name=None, body=True):
        """
        item_tag_name controls name of list elements, root_tag_name controls
        whether or not there is a root tag and what its name is. if body
        is false then this creates a header, otherwise no
        """
        self.root_tag_name = root_tag_name
        self.item_tag_name = item_tag_name
        self.body = body
        super().__init__()

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        if not self.body:
            xml.startDocument()
        if self.root_tag_name:
            xml.startElement(self.root_tag_name, {})

        self._to_xml(xml, data)

        if self.root_tag_name:
            xml.endElement(self.root_tag_name)
        if not self.body:
            xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement(self.item_tag_name, {})
                self._to_xml(xml, item)
                xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in six.iteritems(data):
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', smart_text(data)))
