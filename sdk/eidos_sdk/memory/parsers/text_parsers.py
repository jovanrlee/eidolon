from typing import Iterable, Dict, Union, Sequence

from bs4 import BeautifulSoup

from eidos_sdk.system.reference_model import Specable
from eidos_sdk.memory.parsers.base_parser import BaseParser, DataBlob, BaseParserSpec
from eidos_sdk.memory.document import Document


class TextParser(BaseParser):
    def parse(self, blob: DataBlob) -> Sequence[Document]:
        yield [Document(page_content=blob.as_string(), metadata={"source": blob.path})]


class PyPDFParserSpec(BaseParserSpec):
    features: str = "lxml"
    text_separator: str = ""


class BS4HTMLParser(BaseParser, Specable[PyPDFParserSpec]):
    """Pparse HTML files using `Beautiful Soup`."""

    def __init__(self, spec: PyPDFParserSpec):
        super().__init__(spec)
        self.bs_kwargs = {"features": spec.features}
        self.text_separator = spec.text_separator

    def parse(self, blob: DataBlob) -> Iterable[Document]:
        with blob.as_bytes() as f:
            soup = BeautifulSoup(f, **self.bs_kwargs)

        text = soup.get_text(self.text_separator)

        if soup.title:
            title = str(soup.title.string)
        else:
            title = ""

        metadata: Dict[str, Union[str, None]] = {
            "source": blob.path,
            "title": title,
        }
        yield Document(page_content=text, metadata=metadata)
