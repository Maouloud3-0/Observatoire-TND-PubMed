from pathlib import Path

from observatoire_tnd_pubmed.collecte_pubmed import analyser_xml_pubmed


def test_analyser_notice_complete() -> None:
    xml = Path("tests/donnees/pubmed_exemple.xml").read_text(encoding="utf-8")
    article = analyser_xml_pubmed(xml)[0]

    assert article["pmid"] == "12345678"
    assert article["annee"] == 2024
    assert article["doi"] == "10.0000/example"
    assert article["resume"] == "A first paragraph. A second paragraph."
    assert article["auteurs"][0]["orcid"] == "0000-0001-2345-6789"
    assert article["articles_lies"][0]["pmid_lie"] == "87654321"
