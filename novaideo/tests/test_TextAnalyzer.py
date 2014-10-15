from novaideo.testing import FunctionalTests
from novaideo.utilities.text_analyzer import ITextAnalyzer
from novaideo.content.processes.amendment_management.behaviors import SubmitAmendment
from pyramid.threadlocal import get_current_request, get_current_registry
from bs4 import BeautifulSoup


class TestUtilityTextAnalyzer(FunctionalTests):

    def setUp(self):
        super(TestUtilityTextAnalyzer, self).setUp()

    def _include_spanids(self, spanids, todel, toins, soup):
        spanids_data = []
        for spanid in spanids:
            explanation_data = {'tag': spanid,
                                'todel': todel,
                                'toins': toins,
                                'blocstodel': None
                                }
            spanids_data.append(explanation_data)
        return spanids_data

    def list_all_spans(self, identifier, soup):
        all_id_spans = soup.find_all('span',{'id': identifier})
        spans_list = [tag for tag in all_id_spans]
        return spans_list

    def html_diff(self):
        #deletion
        self.text_analyzer = get_current_registry().getUtility(ITextAnalyzer,'text_analyzer')
        self.text1 = "<p>Organisation !</p>"
        self.text2 = "<p>Organisation</p>"
        self.souptextdiff, self.textdiff1 = self.text_analyzer.render_html_diff(text1=self.text1, text2=self.text2)
        #insertion
        self.text3 = "<p>Organisation</p>"
        self.text4 = "<p>Organisation !</p>"
        self.souptextdiff2, self.textdiff2 = self.text_analyzer.render_html_diff(text1=self.text3, text2=self.text4)
        #replacement
        self.text5 = "<p>Organisation&nbsp!</p>"
        self.text6 = "<p>Organisation de conferences\xa0?</p>"
        self.souptextdiff, self.textdiff3 = self.text_analyzer.render_html_diff(text1=self.text5, text2=self.text6)

    def test_render_html_diff(self):
        self.html_diff()
        self.assertNotIn("&nbsp", self.textdiff1)
        self.assertNotIn("\xa0", self.textdiff1)
        self.assertIn("Organisation", self.textdiff1)
        self.assertNotIn("Organisation  ", self.textdiff1)
        self.assertEqual(self.textdiff1,'<div class="diff"><p>Organisation <span id="diffid"><del>!</del></span></p></div>')
#        Selon moi il aurait du prendre l'espace a l'interieur des balises <del></del>.

        self.assertNotIn("&nbsp", self.textdiff2)
        self.assertNotIn("\xa0", self.textdiff2)
        self.assertIn("Organisation ", self.textdiff2)
        self.assertNotIn("Organisation  ", self.textdiff2)
        self.assertEqual(self.textdiff2,'<div class="diff"><p>Organisation <span id="diffid"><ins>!</ins></span></p></div>')

        self.assertNotIn("&nbsp", self.textdiff3)
        self.assertNotIn("\xa0", self.textdiff3)
        self.assertIn("Organisation", self.textdiff3)
        self.assertNotIn("Organisation  ", self.textdiff3)
        self.assertEqual(self.textdiff3,'<div class="diff"><p>Organisation <span id="diffid"><del>!</del></span> <span id="diffid"><ins>de conferences ?</ins></span></p></div>')
#        Textdiff3 contient un espace entre les deux spans.

    def test_wrap_diff(self):
        self.html_diff()
        soup_wrapped1 = self.text_analyzer.wrap_diff(self.textdiff1, '1')
        soup_wrapped2 = self.text_analyzer.wrap_diff(self.textdiff2, '2')
        soup_wrapped3 = self.text_analyzer.wrap_diff(self.textdiff3, '3')
        self.assertEqual(str(soup_wrapped1), '<html><body><div class="diff"><p>Organisation <span id="diffid"><span id="1"><del>!</del></span></span></p></div></body></html>')
        self.assertEqual(str(soup_wrapped2), '<html><body><div class="diff"><p>Organisation <span id="diffid"><span id="2"><ins>!</ins></span></span></p></div></body></html>')
        self.assertEqual(str(soup_wrapped3), '<html><body><div class="diff"><p>Organisation <span id="diffid"><span id="3"><del>!</del></span></span> <span id="diffid"><span id="3"><ins>de conferences ?</ins></span></span></p></div></body></html>')
        #Dans str(soup_wrapped3) il y a encore l'espace entre les spans.

    def test_unwrapped_diff_and_soup_to_text(self):
        self.html_diff()
        soup_wrapped1 = self.text_analyzer.wrap_diff(self.textdiff1, '1')
        soup_wrapped2 = self.text_analyzer.wrap_diff(self.textdiff2, '2')
        soup_wrapped3 = self.text_analyzer.wrap_diff(self.textdiff3, '3')

        #All corrections are accepted for text1 and 2 (deletion)
        spans_list_1 = self.list_all_spans('1', soup_wrapped1)
        spanids_data1 = self._include_spanids(spans_list_1, "del", "ins", soup_wrapped1)
        self.text_analyzer.unwrap_diff(spanids_data1, soup_wrapped1)
        self.assertEqual(soup_wrapped1.find_all("span", id ="1"),[])
        self.assertEqual(str(soup_wrapped1),'<html><body><div class="diff"><p>Organisation <span id="diffid"></span></p></div></body></html>')
#       Toujours meme souci de l'espace (apres organisation car pas pris dans le del).

        diffids_list_1 = self.list_all_spans('diffid', soup_wrapped1)
        diffids_data1 = self._include_spanids(diffids_list_1, "ins", "del", soup_wrapped1)
        self.text_analyzer.unwrap_diff(diffids_data1, soup_wrapped1)
        self.assertEqual(soup_wrapped1.find_all("span", id ="diffid"),[])
        self.assertEqual(str(soup_wrapped1),'<html><body><div class="diff"><p>Organisation </p></div></body></html>')

        #All corrections are refused for text 3 and 4 (insertion)
        spans_list_2 = self.list_all_spans('2', soup_wrapped2)
        spanids_data2 = self._include_spanids(spans_list_2, "ins", "del", soup_wrapped2)
        self.text_analyzer.unwrap_diff(spanids_data2, soup_wrapped2)
        self.assertEqual(soup_wrapped2.find_all("span", id ="2"),[])
        self.assertEqual(str(soup_wrapped2),'<html><body><div class="diff"><p>Organisation <span id="diffid"></span></p></div></body></html>')
        #Le point d'explamation a ete supprime mais pas l'espace, voir apres Organisation

        diffids_list_2 = self.list_all_spans('diffid', soup_wrapped2)
        diffids_data2 = self._include_spanids(diffids_list_2, "ins", "del", soup_wrapped2)
        self.text_analyzer.unwrap_diff(diffids_data2, soup_wrapped2)
        self.assertEqual(soup_wrapped2.find_all("span", id ="diffid"),[])
        self.assertEqual(str(soup_wrapped2),'<html><body><div class="diff"><p>Organisation </p></div></body></html>')

        #All corrections are accepted for text5 and 6 (replacement)
        spans_list_3 = self.list_all_spans('3', soup_wrapped3)
        spanids_data3 = self._include_spanids(spans_list_3, "del", "ins", soup_wrapped3)
        self.text_analyzer.unwrap_diff(spanids_data3, soup_wrapped3)
        self.assertEqual(soup_wrapped3.find_all("span", id ="3"),[])
        self.assertEqual(str(soup_wrapped3),'<html><body><div class="diff"><p>Organisation <span id="diffid"></span> <span id="diffid">de conferences ?</span></p></div></body></html>')

        diffids_list_3 = self.list_all_spans('diffid', soup_wrapped3)
        diffids_data3 = self._include_spanids(diffids_list_3, "del", "ins", soup_wrapped3)
        self.text_analyzer.unwrap_diff(diffids_data3, soup_wrapped3)
        self.assertEqual(soup_wrapped3.find_all("span", id ="diffid"),[])
        self.assertEqual(str(soup_wrapped3),'<html><body><div class="diff"><p>Organisation  de conferences ?</p></div></body></html>')
        #Selon moi il ne devrait pas y a voir deux espaces entre Organisation et de.

        soup1_to_text = self.text_analyzer.soup_to_text(soup_wrapped1)
        #Note pour moi meme: str pas de test possible self.assertEqual(soup1_to_text.find_all(attrs={"class": "diff"}),[])
        self.assertEqual(soup1_to_text,'<p>Organisation </p>')
        # Selon moi il ne devrait pas y avoir d'espace apres organisation.

        soup2_to_text = self.text_analyzer.soup_to_text(soup_wrapped2)
        self.assertEqual(soup2_to_text,'<p>Organisation </p>')
        # Selon moi il ne devrait pas y avoir d'espace apres organisation.

        soup3_to_text = self.text_analyzer.soup_to_text(soup_wrapped3)
        self.assertEqual(soup3_to_text,'<p>Organisation  de conferences ?</p>')
        #Selon moi il ne devrait pas y a voir deux espaces entre Organisation et de.
