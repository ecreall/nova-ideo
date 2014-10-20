from novaideo.testing import FunctionalTests
from novaideo.utilities.text_analyzer import ITextAnalyzer
from pyramid.threadlocal import get_current_registry


class TestTextAnalyzerIntegration(FunctionalTests):

    def setUp(self):
        super(TestTextAnalyzerIntegration, self).setUp()

    def _include_spanids(self, spanids, todel, toins, soup):
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
        if span_id == 'diffid' or decision == 'accept_modif':
            spans_list = self._list_all_spans(span_id, soup_wrapped)
            spanids_data = self._include_spanids(spans_list, "del", "ins", soup_wrapped)
            self.text_analyzer.unwrap_diff(spanids_data, soup_wrapped)

        elif decision == 'refuse_modif':
            spans_list = self._list_all_spans(span_id, soup_wrapped)
            spanids_data = self._include_spanids(spans_list, "ins", "del", soup_wrapped)
            self.text_analyzer.unwrap_diff(spanids_data, soup_wrapped)

    def _entry_to_result(self, text1, text2, decision):
        self.text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        soup_wrapped, textdiff = self.text_analyzer.render_html_diff(text1, text2, 'modif')
        self._unwrap_spans('modif', decision, soup_wrapped)
        soup_to_text = self.text_analyzer.soup_to_text(soup_wrapped)
        return soup_to_text

    def assert_text(self, results):
        for result in results:
            self.assertNotIn("&nbsp", result)
            self.assertNotIn("\xa0", result)
            self.assertNotIn("  ", result)

# - - - - - - - - - - - - - - - - - - - - - Beginning deletion

    def test_beginning_deletion_word(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science</p>')
    def test_beginning_deletion_paragraph(self):
        text1 = "<p>Premierement : </p><p>- conferences</p><p>- animations</p><p>- expositions</p>"
        text2 = "<p>- conferences</p><p>- animations</p><p>- expositions</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>- conferences</p><p>- animations</p><p>- expositions</p>')
        self.assertEqual(result2,'<p>Premierement : </p><p>- conferences</p><p>- animations</p><p>- expositions</p>')

    def test_beginning_deletion_spaces(self):
        text1 = "<p> Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p> Organisation de conferences lors de la Fete de la science</p>')

        text3 = "<p>    Organisation de conferences lors de la Fete de la science</p>"
        text4 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result4,'<p>    Organisation de conferences lors de la Fete de la science</p>')

    def test_beginning_deletion_special_character(self):
        text1 = "<p>! Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>! Organisation de conferences lors de la Fete de la science</p>')

        text3 = "<p>-Organisation de conferences lors de la Fete de la science</p>"
        text4 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result4,'<p>-Organisation de conferences lors de la Fete de la science</p>')

        text5 = "<p>$Organisation de conferences lors de la Fete de la science</p>"
        text6 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result6,'<p>$Organisation de conferences lors de la Fete de la science</p>')

    def test_beginning_deletion_word_part(self):
        text1 = "<p>Reorganisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Reorganisation de conferences lors de la Fete de la science</p>')

    def test_beginning_deletion_word_followed_by_exclamation_point(self):
        text1 = "<p>Fête! Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Fête! Organisation de conferences lors de la Fete de la science</p>')

        text3 = "<p>Fête ! Organisation de conferences lors de la Fete de la science</p>"
        text4 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result4,'<p>Fête ! Organisation de conferences lors de la Fete de la science</p>')

# -------------------------------------- Beginning insertion

    def test_beginning_insertion_word(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>1/ Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>1/ Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science</p>')

    def test_beginning_insertion_paragraph(self):
        text1 = "<p>- conferences</p><p>- animations</p><p>- expositions</p>"
        text2 = "<p>Premierement : </p><p>- conferences</p><p>- animations</p><p>- expositions</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Premierement : </p><p>- conferences</p><p>- animations</p><p>- expositions</p>')
        self.assertEqual(result2,'<p>- conferences</p><p>- animations</p><p>- expositions</p>')

    def test_beginning_insertion_spaces(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p> Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p> Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science</p>')

        text3 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text4 = "<p>    Organisation de conferences lors de la Fete de la science</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>    Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result4,'<p>Organisation de conferences lors de la Fete de la science</p>')

    def test_beginning_insertion_special_character(self):
        text1 = '<p>Organisation de conferences lors de la Fete de la science</p>'
        text2 = '<p>"Organisation de conferences !" lors de la Fete de la science</p>'
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>"Organisation de conferences !" lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science</p>')

        text3 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text4 = "<p>- Organisation de conferences lors de la Fete de la science</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>- Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result4,'<p>Organisation de conferences lors de la Fete de la science</p>')

        text5 = "<p>$Organisation de conferences lors de la Fete de la science</p>"
        text6 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result6,'<p>$Organisation de conferences lors de la Fete de la science</p>')

    def test_beginning_insertion_word_part(self):
        text1 = "<p>organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Reorganisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Reorganisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>organisation de conferences lors de la Fete de la science</p>')

# - - - - - - - - - - - - - - - - - - - - - Beginning replacement

    def test_beginning_replacement_word(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Programmation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Programmation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science</p>')

    def test_beginning_replacement_special_character(self):
        text1 = '<p>- Organisation de conferences lors de la Fete de la science</p>'
        text2 = '<p>" Organisation de conferences ! " lors de la Fete de la science</p>'
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>" Organisation de conferences ! " lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>- Organisation de conferences lors de la Fete de la science</p>')

# - - - - - - - - - - - - - - - - - - - - - End deletion

    def test_end_deletion_word(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science etc.</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science etc.</p>')

    def test_end_deletion_paragraph(self):
        text1 = "<p>Programme : </p><p>- conferences</p><p>- expositions</p><p>- animations</p>"
        text2 = "<p>Programme : </p><p>- conferences</p><p>- expositions</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Programme : </p><p>- conferences</p><p>- expositions</p>')
        self.assertEqual(result2,'<p>Programme : </p><p>- conferences</p><p>- expositions</p><p>- animations</p>')

    def test_end_deletion_special_character(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science !</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science !</p>')

        text3 = "<p>Organisation de conferences lors de la Fete de la science.</p>"
        text4 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result4,'<p>Organisation de conferences lors de la Fete de la science.</p>')

        text5 = "<p>Organisation de conferences lors de la Fete de la science$</p>"
        text6 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result6,'<p>Organisation de conferences lors de la Fete de la science$</p>')

    def test_end_deletion_word_part(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la sciences</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la sciences</p>')

# - - - - - - - - - - - - - - - - - - - - - End insertion

    def test_end_insertion_word(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la</p>')

    def test_end_insertion_paragraph(self):
        text1 = "<p>Programme : </p><p>- conferences</p><p>- animations</p>"
        text2 = "<p>Programme : </p><p>- conferences</p><p>- animations</p><p>- expositions</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Programme : </p><p>- conferences</p><p>- animations</p><p>- expositions</p>')
        self.assertEqual(result2,'<p>Programme : </p><p>- conferences</p><p>- animations</p>')

    def test_end_insertion_special_character(self):
        text1 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science !</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science !</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science</p>')

        text3 = "<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000</p>"
        text4 = "<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000€</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,'<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000€</p>')
        self.assertEqual(result4,'<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000</p>')

        text5 = "<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000</p>"
        text6 = "<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000$</p>"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,'<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000$</p>')
        self.assertEqual(result6,'<p>Organisation de conferences lors de la Fete de la science pour un budget de 5000</p>')

    def test_end_insertion_word_part(self):
        text1 = "<p>organisation de conferences lors de la Fete de la scien</p>"
        text2 = "<p>Reorganisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Reorganisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>organisation de conferences lors de la Fete de la scien</p>')

# - - - - - - - - - - - - - - - - - - - - - End replacement

    def test_end_replacement_word(self):
        text1 = "<p>Organisation de conferences lors de la Fete de l'innovation</p>"
        text2 = "<p>Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"<p>Organisation de conferences lors de la Fete de la science</p>")
        self.assertEqual(result2,"<p>Organisation de conferences lors de la Fete de l'innovation</p>")

    def test_end_replacement_special_character(self):
        text1 = '<p>Organisation de conferences lors de la Fete de la science!</p>'
        text2 = '<p>Organisation de conferences lors de la Fete de la science ?</p>'
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Organisation de conferences lors de la Fete de la science ?</p>')
        self.assertEqual(result2,'<p>Organisation de conferences lors de la Fete de la science!</p>')

# - - - - - - - - - - - - - - - - - - - - - Middle deletion

    def test_middle_deletion_spaces(self):
        text1= "<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme:    - conferences - expositions - autres</p>"
        text2= "<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result2,"<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme:    - conferences - expositions - autres</p>")

    def test_middle_deletion_special_characters(self):
        text1= "<p>Fete de la science !! Organiser des $animations lors de la Fete de la science qui se deroule au mois d'octobre... Programme: - conferences - expositions - autres</p>"
        text2= "<p>Fete de la science! Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"<p>Fete de la science! Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result2,"<p>Fete de la science !! Organiser des $animations lors de la Fete de la science qui se deroule au mois d'octobre... Programme: - conferences - expositions - autres</p>")

        text3= "<p>Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre)... ! Programme: - conferences - expositions - autres</p>"
        text4= "<p>Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre). Programme: - conferences - expositions - autres</p>"
        result3 = self._entry_to_result(text3, text4, 'accept_modif')
        result4 = self._entry_to_result(text3, text4, 'refuse_modif')
        self.assertEqual(result3,"<p>Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre). Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result4,"<p>Fete de la science. Organiser des animations lors de la Fete de la science (qui se deroule au mois d'octobre)... ! Programme: - conferences - expositions - autres</p>")

        text5= "<p>Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]... ! Programme: - conferences - expositions - autres</p>"
        text6= "<p>Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]. Programme: - conferences - expositions - autres</p>"
        result5 = self._entry_to_result(text5, text6, 'accept_modif')
        result6 = self._entry_to_result(text5, text6, 'refuse_modif')
        self.assertEqual(result5,"<p>Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]. Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result6,"<p>Fete de la science. Organiser des animations lors de la Fete de la science [qui se deroule au mois d'octobre]... ! Programme: - conferences - expositions - autres</p>")

# - - - - - - - - - - - - - - - - - - - - - Middle insertion

    def test_middle_insertion_special_characters(self):
        text1= "<p>Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        text2= "<p>Fete de la science. Organiser des animations lors de la Fete de la science, elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"<p>Fete de la science. Organiser des animations lors de la Fete de la science, elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result2,"<p>Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")

        text1= "<p>Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        text2= "<p>Fete de la science. Organiser des animations lors de la Fete de la science ! Elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"<p>Fete de la science. Organiser des animations lors de la Fete de la science ! Elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result2,"<p>Fete de la science. Organiser des animations lors de la Fete de la science elle se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")

    def test_middle_insertion_spaces(self):
        text1 = "<p>-Organisation de conferences lors de la Fete de la science</p>"
        text2 = "<p>- Organisation de conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>- Organisation de conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>-Organisation de conferences lors de la Fete de la science</p>')

# - - - - - - - - - - - - - - - - - - - - - Middle replacement

    def test_middle_replacement_word(self):
        text1= "<p>Fete de la science. Organiser des conferences lors de la Fete de la science</p>"
        text2= "<p>Fete de la science. Organiser des animations lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Fete de la science. Organiser des animations lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Fete de la science. Organiser des conferences lors de la Fete de la science</p>')

    def test_middle_replacement_word_part(self):
        text1= "<p>Fete de la science. Organiser des animations lors de la Fete de la science</p>"
        text2= "<p>Fete de la science. Organiser des conferences lors de la Fete de la science</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,'<p>Fete de la science. Organiser des conferences lors de la Fete de la science</p>')
        self.assertEqual(result2,'<p>Fete de la science. Organiser des animations lors de la Fete de la science</p>')

    def test_middle_replacement_special_characters(self):
        text1= "<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>"
        text2= "<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois du 24/09/2014 au 19/10/2014. Programme: - conferences - expositions - autres</p>"
        result1 = self._entry_to_result(text1, text2, 'accept_modif')
        result2 = self._entry_to_result(text1, text2, 'refuse_modif')
        self.assertEqual(result1,"<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois du 24/09/2014 au 19/10/2014. Programme: - conferences - expositions - autres</p>")
        self.assertEqual(result2,"<p>Fete de la science. Organiser des animations lors de la Fete de la science qui se deroule au mois d'octobre. Programme: - conferences - expositions - autres</p>")