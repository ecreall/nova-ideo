# -*- coding: utf-8 -*-
"""Tests for text_analyzer utility
"""
from pyramid.threadlocal import get_current_registry #pylint: disable=F0401

from novaideo.testing import FunctionalTests
from novaideo.utilities.text_analyzer import ITextAnalyzer


class TestTextAnalyzerIntegration(FunctionalTests): #pylint: disable=R0904
    """Test TextAnalyzer integration"""

    def setUp(self):
        super(TestTextAnalyzerIntegration, self).setUp()
        self.text_analyzer = get_current_registry().getUtility(ITextAnalyzer,
                                                               'text_analyzer')

    def _include_spanids(self, spanids, todel, toins):
        spanids_data = []
        for spanid in spanids:
            spanid_data = {'tag': spanid,
                           'todel': todel,
                           'toins': toins,
                           'blocstodel': None
                            }
            spanids_data.append(spanid_data)

        return spanids_data

    def _list_all_spans(self, identifier, soup):
        all_id_spans = soup.find_all('span',{'id': identifier})
        spans_list = [tag for tag in all_id_spans]
        return spans_list

    def _unwrap_spans(self, span_id, decision, soup_wrapped):
        spans_list = self._list_all_spans(span_id, soup_wrapped)
        if span_id == 'diffid' or decision == 'accept_modif':
            spanids_data = self._include_spanids(spans_list, "del", "ins")

        elif decision == 'refuse_modif':
            spanids_data = self._include_spanids(spans_list, "ins", "del")

        self.text_analyzer.unwrap_diff(spanids_data, soup_wrapped)

    def _entry_to_result(self, text1, text2, decision):
        soup_wrapped, textdiff = self.text_analyzer.render_html_diff(text1, text2, 'modif')
        self._unwrap_spans('modif', decision, soup_wrapped)
        soup_to_text = self.text_analyzer.soup_to_text(soup_wrapped)
        return soup_to_text

# - - - - - - - - - - - - - - - - - - - - - Beginning deletion

    def test_beginning_deletion_word(self):
        text1 = "Organisation de conferences lors de la Fete de la science"
        text2 = "Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        self.assertEqual(result1, 'Fete de la science')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result2, 'Organisation de conferences lors de la Fete de la science')

    def test_beginning_deletion_spaces(self):
        text1 = " Organisation de conferences lors de la Fete de la science"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1, 'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2, ' Organisation de conferences lors de la Fete de la science')

        text3 = "    Organisation de conferences lors de la Fete de la science"
        text4 = "Organisation de conferences lors de la Fete de la science"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3, 'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result4, '    Organisation de conferences lors de la Fete de la science')

    def test_beginning_deletion_special_character(self):
        text1 = "! Organisation de conferences lors de la Fete de la science"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1, 'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2, '! Organisation de conferences lors de la Fete de la science')

        text3 = "-Organisation de conferences lors de la Fete de la science"
        text4 = "Organisation de conferences lors de la Fete de la science"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3, 'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result4, '-Organisation de conferences lors de la Fete de la science')

        text5 = "$Organisation de conferences lors de la Fete de la science"
        text6 = "Organisation de conferences lors de la Fete de la science"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5, 'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result6, '$Organisation de conferences lors de la Fete de la science')

    def test_beginning_deletion_word_part(self):
        text1 = "Reorganisation de conferences lors de la Fete de la science"
        text2 = "organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1, 'organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2, 'Reorganisation de conferences lors de la Fete de la science')

    def test_beginning_deletion_word_followed_by_exclamation_point(self):
        text1 = "Fête! Organisation de conferences lors de la Fete de la science"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1, 'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2, 'Fête! Organisation de conferences lors de la Fete de la science')

        text3 = "Fête ! Organisation de conferences lors de la Fete de la science"
        text4 = "Organisation de conferences lors de la Fete de la science"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result4,'Fête ! Organisation de conferences lors de la Fete de la science')

# -------------------------------------- Beginning insertion

    def test_beginning_insertion_word(self):
        text1 = "Organisation de conferences lors de la Fete de la science"
        text2 = "1/ Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'1/ Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science')

    def test_beginning_insertion_spaces(self):
        text1 = "Organisation de conferences lors de la Fete de la science"
        text2 = " Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,' Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science')

        text3 = "Organisation de conferences lors de la Fete de la science"
        text4 = "    Organisation de conferences lors de la Fete de la science"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'    Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result4,'Organisation de conferences lors de la Fete de la science')

    def test_beginning_insertion_special_character(self):
        text1 = 'Organisation de conferences lors de la Fete de la science'
        text2 = '"Organisation de conferences !" lors de la Fete de la science'
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'"Organisation de conferences !" lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science')

        text3 = "Organisation de conferences lors de la Fete de la science"
        text4 = "- Organisation de conferences lors de la Fete de la science"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'- Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result4,'Organisation de conferences lors de la Fete de la science')

        text5 = "$Organisation de conferences lors de la Fete de la science"
        text6 = "Organisation de conferences lors de la Fete de la science"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result6,'$Organisation de conferences lors de la Fete de la science')

    def test_beginning_insertion_word_part(self):
        text1 = "organisation de conferences lors de la Fete de la science"
        text2 = "Reorganisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Reorganisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'organisation de conferences lors de la Fete de la science')

# - - - - - - - - - - - - - - - - - - - - - Beginning replacement

    def test_beginning_replacement_word(self):
        text1 = "Organisation de conferences lors de la Fete de la science"
        text2 = "Programmation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Programmation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science')

    def test_beginning_replacement_special_character(self):
        text1 = '- Organisation de conferences lors de la Fete de la science'
        text2 = '" Organisation de conferences ! " lors de la Fete de la science'
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'" Organisation de conferences ! " lors de la Fete de la science')
        self.assertEqual(result2,'- Organisation de conferences lors de la Fete de la science')

# - - - - - - - - - - - - - - - - - - - - - End deletion

    def test_end_deletion_word(self):
        text1 = "Organisation de conferences lors de la Fete de la science etc."
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science etc.')

    def test_end_deletion_special_character(self):
        text1 = "Organisation de conferences lors de la Fete de la science !"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science !')

        text3 = "Organisation de conferences lors de la Fete de la science."
        text4 = "Organisation de conferences lors de la Fete de la science"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result4,'Organisation de conferences lors de la Fete de la science.')

        text5 = "Organisation de conferences lors de la Fete de la science$"
        text6 = "Organisation de conferences lors de la Fete de la science"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result6,'Organisation de conferences lors de la Fete de la science$')

    def test_end_deletion_word_part(self):
        text1 = "Organisation de conferences lors de la Fete de la sciences"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la sciences')

# - - - - - - - - - - - - - - - - - - - - - End insertion

    def test_end_insertion_word(self):
        text1 = "Organisation de conferences lors de la Fete de la"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la')

    def test_end_insertion_special_character(self):
        text1 = "Organisation de conferences lors de la Fete de la science"
        text2 = "Organisation de conferences lors de la Fete de la science !"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Organisation de conferences lors de la Fete de la science !')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science')

        text3 = "Organisation de conferences lors de la Fete de la science pour un budget de 5000"
        text4 = "Organisation de conferences lors de la Fete de la science pour un budget de 5000€"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'Organisation de conferences lors de la Fete de la science pour un budget de 5000€')
        self.assertEqual(result4,'Organisation de conferences lors de la Fete de la science pour un budget de 5000')

        text5 = "Organisation de conferences lors de la Fete de la science pour un budget de 5000"
        text6 = "Organisation de conferences lors de la Fete de la science pour un budget de 5000$"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'Organisation de conferences lors de la Fete de la science pour un budget de 5000$')
        self.assertEqual(result6,'Organisation de conferences lors de la Fete de la science pour un budget de 5000')

    def test_end_insertion_word_part(self):
        text1 = "organisation de conferences lors de la Fete de la scien"
        text2 = "Reorganisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Reorganisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'organisation de conferences lors de la Fete de la scien')

# - - - - - - - - - - - - - - - - - - - - - End replacement

    def test_end_replacement_word(self):
        text1 = "Organisation de conferences lors de la Fete de l'innovation"
        text2 = "Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"Organisation de conferences lors de la Fete de la science")
        self.assertEqual(result2,"Organisation de conferences lors de la Fete de l'innovation")

    def test_end_replacement_special_character(self):
        text1 = 'Organisation de conferences lors de la Fete de la science!'
        text2 = 'Organisation de conferences lors de la Fete de la science ?'
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Organisation de conferences lors de la Fete de la science ?')
        self.assertEqual(result2,'Organisation de conferences lors de la Fete de la science!')

# - - - - - - - - - - - - - - - - - - - - - Middle deletion

    def test_middle_deletion_spaces(self):
        text1= "Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme:    - conferences - expositions - autres"
        text2= "Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres")
        self.assertEqual(result2,"Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme:    - conferences - expositions - autres")

    def test_middle_deletion_special_characters(self):
        text1= "Fete de la science !! Organiser des $animations lors de la Fete de la science qui se deroule au mois d'octobre... Programme: - conferences - expositions - autres"
        text2= "Fete de la science! Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"Fete de la science! Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres")
        self.assertEqual(result2,"Fete de la science !! Organiser des $animations lors de la Fete de la science qui se deroule au mois d'octobre... Programme: - conferences - expositions - autres")

        text3= "Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre)... ! Programme: - conferences - expositions - autres"
        text4= "Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre). Programme: - conferences - expositions - autres"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,"Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre). Programme: - conferences - expositions - autres")
        self.assertEqual(result4,"Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre)... ! Programme: - conferences - expositions - autres")

        text5= "Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]... ! Programme: - conferences - expositions - autres"
        text6= "Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]. Programme: - conferences - expositions - autres"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,"Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]. Programme: - conferences - expositions - autres")
        self.assertEqual(result6,"Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]... ! Programme: - conferences - expositions - autres")

# - - - - - - - - - - - - - - - - - - - - - Middle insertion

    def test_middle_insertion_special_characters(self):
        text1= "Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        text2= "Fete de la science. Organiser des animations lors de la Fete de la science, elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"Fete de la science. Organiser des animations lors de la Fete de la science, elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres")
        self.assertEqual(result2,"Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres")

        text1= "Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        text2= "Fete de la science. Organiser des animations lors de la Fete de la science ! Elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"Fete de la science. Organiser des animations lors de la Fete de la science ! Elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres")
        self.assertEqual(result2,"Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres")

    def test_middle_insertion_spaces(self):
        text1 = "-Organisation de conferences lors de la Fete de la science"
        text2 = "- Organisation de conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'- Organisation de conferences lors de la Fete de la science')
        self.assertEqual(result2,'-Organisation de conferences lors de la Fete de la science')

# - - - - - - - - - - - - - - - - - - - - - Middle replacement

    def test_middle_replacement_word(self):
        text1= "Fete de la science. Organiser des conferences lors de la Fete de la science"
        text2= "Fete de la science. Organiser des animations lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Fete de la science. Organiser des animations lors de la Fete de la science')
        self.assertEqual(result2,'Fete de la science. Organiser des conferences lors de la Fete de la science')

    def test_middle_replacement_word_part(self):
        text1= "Fete de la science. Organiser des animations lors de la Fete de la science"
        text2= "Fete de la science. Organiser des conferences lors de la Fete de la science"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'Fete de la science. Organiser des conferences lors de la Fete de la science')
        self.assertEqual(result2,'Fete de la science. Organiser des animations lors de la Fete de la science')

    def test_middle_replacement_special_characters(self):
        text1= "Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        text2= "Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois du 24/09/2014 au 19/10/2014. Programme: - conferences - expositions - autres"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois du 24/09/2014 au 19/10/2014. Programme: - conferences - expositions - autres")
        self.assertEqual(result2,"Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres")

# - - - - - - - - - - - - - - - - - - - - - merge texts

    def test_merge_add_sentences(self):
        text_origin = "Organiser des animations lors de la Fete de la science."
        text1 = "Programme d'octobre prochain. Organiser des animations lors de la Fete de la science."
        text2 = "Organiser des animations lors de la Fete de la science. Avec un budget de 5000€."
        result = self.text_analyzer.merge(text_origin, [text1, text2])
        self.assertEqual(result,
                         "Programme d'octobre prochain. Organiser des "\
                         "animations lors de la Fete de la science. Avec "\
                         "un budget de 5000€.")

    def test_merge_delete_sentences(self):
        text_origin="Programme d'octobre prochain. Organiser des animations lors de la Fete de la science."
        text1="Organiser des animations lors de la Fete de la science."
        text2="Organiser des animations lors de la Fete de la Science."
        result = self.text_analyzer.merge(text_origin, [text1, text2])
        self.assertEqual(result, "Organiser des animations lors de la Fete de la Science.")

    def test_merge_modify_words(self):
        text_origin = "Organiser des animations lors de la Fete de la science."
        text1 = "Programmer une animation lors de la Fete de la science en octobre prochain."
        text2 = "Organiser une animation lors de la Fete de la Science."
        result = self.text_analyzer.merge(text_origin, [text1, text2])
        self.assertEqual(result, "Programmer une animation lors de la Fete de la Science en octobre prochain.")

    def test_merge_modify_characters(self):
        text_origin = "#1 Organiser des animation lors de la Fete de la science !"
        text1 = "#1 Organiser des animation lors de la Fete de la science."
        text2 = "Organiser des animations lors de la Fete de la science & de l'innovation."
        result = self.text_analyzer.merge(text_origin, [text1, text2])
        self.assertEqual(result, "Organiser des animations lors de la Fete de la science & de l'innovation.")

        text_origin2 = "Organiser des animations lors de la Fete de la science."
        text3 = "Organiser des animations lors de la Fete de la science ?"
        text4 = "Organiser des animations; eventuellement, lors de la Fete de la science."
        result2 = self.text_analyzer.merge(text_origin2, [text3, text4])
        self.assertEqual(result2, "Organiser des animations; eventuellement, lors de la Fete de la science ?")

        text_origin3 = "Organiser des animations lors de la Fete de la science. Leur nombre dependra du budget alloue."
        text5 = "Organiser des animations le 24/09/2014."
        text6 = "Organiser des animations le 24/09/2014. Eventuellement, lors de la Fete de la Science."
        result3 = self.text_analyzer.merge(text_origin3, [text5, text6])
        self.assertEqual(result3, "Organiser des animations le 24/09/2014. Eventuellement, lors de la Fete de la Science.")


# - - - - - - - - - - accept and refuse modifications within a single sentence

    def test_different_treatments_in_one_sentence(self):
        text1 = "fete de la science.Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres"
        text2 = "Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois du 24/09/2014 au 19/10/2014. Programme: - conferences - expositions - autres"
        soup, textdiff = self.text_analyzer.render_html_diff(text1, text2, 'modif')

        spanids_data = []
        spans = soup.find_all('span', {'id': "modif"})
        descriminator = 1
        for span in spans:
            span['data-item'] = str(descriminator)
            descriminator += 1

        fselection = self._include_spanids(spans[0:2], "del", "ins")
        for span in fselection:
             spanids_data.append(span)

        lselection = self._include_spanids(spans[2:], "ins", "del")
        for span in lselection:
             spanids_data.append(span)

        self.text_analyzer.unwrap_diff(spanids_data, soup)
        soup_to_text = self.text_analyzer.soup_to_text(soup)
        self.assertEqual(soup_to_text, "Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres")
