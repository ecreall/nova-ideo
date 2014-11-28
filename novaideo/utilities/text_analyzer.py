# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""Text analyzer utility
"""
import re

from dace.util import utility
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from zope.interface import Interface, implementer

from novaideo.ips.htmldiff import htmldiff


class ITextAnalyzer(Interface):
    """Interface for TextAnalyzer
    """

    def has_conflict(origin_text, texts):
        pass

    def merge(origin_text, texts):
        pass

    def render_html_diff(text1, text2):
        pass

    def wrap_diff(diff, diff_id):
        pass


@utility(name='text_analyzer')
@implementer(ITextAnalyzer)
class TextAnalyzer(object):
    """TextAnalyzer utility
    """

    def has_conflict(self, origin_text, texts):
        """True if origin_text has conflicts with one of texts"""
        d = diff_match_patch()
        d.Match_Threshold = 0.1
        result = origin_text
        has_conflict = False
        for alternative in texts:
            patch = d.patch_make(origin_text, alternative)
            result, results = d.patch_apply(patch, result)
            if False in results:
                has_conflict = True
                break

        return has_conflict

    def merge(self, origin_text, texts):
        """Merge origin_text with texts"""
        d = diff_match_patch()
        d.Match_Threshold = 0.1
        text_result = origin_text
        # conflict = False
        for alternative in texts:
            patch = d.patch_make(origin_text, alternative)
            text_result, results = d.patch_apply(patch, text_result)
            if False in results:
                # conflict = True
                break

        return text_result

    def render_html_diff(self, text1, text2, diff_id="diff_id"):
        """Render html diff between text1 and text2"""
        text1 = text1.replace('&nbsp;', '')
        text2 = text2.replace('&nbsp;', '')
        result = htmldiff.render_html_diff(text1, text2)
        soup = self.wrap_diff(result.replace('\xa0', ' '), diff_id)
        return soup, u''.join([str(t) for t in soup.body.contents])

    def _del_added_space(self, soup, tag):
        """Remove added space from tag"""
        next_sibling = tag.next_sibling
        if next_sibling is not None and \
           isinstance(next_sibling, NavigableString):
            if next_sibling.startswith(' '):
                new_string = soup.new_string(next_sibling[1:])
                tag.next_sibling.replace_with(new_string)

        elif next_sibling is None:
            previous_sibling = tag.previous_sibling
            if previous_sibling is not None and \
               isinstance(previous_sibling, NavigableString):
                if previous_sibling.endswith(' '):
                    new_string = soup.new_string(previous_sibling[:-1])
                    tag.previous_sibling.replace_with(new_string)

    def wrap_diff(self, diff, diff_id):
        """Wrap diff with span tags"""
        soup = BeautifulSoup(diff)
        ins_tags = soup.find_all('ins')
        del_tags = soup.find_all('del')
        del_included = []
        for ins_tag in ins_tags:
            new_tag = soup.new_tag("span", id=diff_id)
            previous_del_tag = ins_tag.find_previous_sibling('del')
            ins_string = ins_tag.string
            if previous_del_tag is not None:
                previous_del_tag_string = previous_del_tag.string
                to_find = "{} *{}".format(previous_del_tag, ins_tag)
                modified = len(re.findall(to_find, diff)) > 0
                if previous_del_tag_string != ins_string and modified:
                    self._del_added_space(soup, previous_del_tag)
                    previous_del_tag.wrap(new_tag)
                    new_tag.append(ins_tag)
                    del_included.append(previous_del_tag)
                    continue
                elif modified:
                    del_included.append(previous_del_tag)
                    self._del_added_space(soup, previous_del_tag)
                    ins_tag.unwrap()
                    previous_del_tag.extract()

            if ins_tag.parent is not None:
                ins_tag.wrap(new_tag)

        for del_tag in del_tags:
            if del_tag not in del_included:
                if del_tag.string is not None:
                    new_tag = soup.new_tag("span", id=diff_id)
                    del_tag.wrap(new_tag)
                else:
                    self._del_added_space(soup, del_tag)
                    del_tag.extract()

        return soup

    def unwrap_diff(self, tags_data, soup, unwrap_ins=True):
        """Unwrap diff"""
        for tag_data in tags_data:
            tag = tag_data['tag']
            to_del = tag_data['todel']
            to_ins = tag_data['toins']
            blocks_to_del = tag_data['blocstodel']
            del_tags = tag.find_all(to_del)
            ins_tags = tag.find_all(to_ins)
            if del_tags:
                for del_tag in del_tags:
                    del_tag.extract()

            if ins_tags and unwrap_ins:
                for ins_tag in ins_tags:
                    ins_tag.unwrap()

            if blocks_to_del is not None:
                blocs = tag.find_all(blocks_to_del[0], blocks_to_del[1])
                for bloc in blocs:
                    bloc.extract()

            if tag.contents and tag.contents[-1] == '\n':
                tag.contents.pop()

            if del_tags and not ins_tags:
                self._del_added_space(soup, tag)

            tag.unwrap()

    def include_diffs(self, soup, diffs, todel, toins, blocstodel=None):
        """Include diffs to text"""
        diffs_data = []
        for diff in diffs:
            diff_data = {'tag': diff,
                         'todel': todel,
                         'toins': toins,
                         'blocstodel': blocstodel
                        }
            diffs_data.append(diff_data)

        self.unwrap_diff(diffs_data, soup)
        return soup

    def soup_to_text(self, soup):
        """Convert soup data to string"""
        divs_diff = soup.find_all('div', {'class': 'diff'})
        for div_diff in divs_diff:
            div_diff.unwrap()

        return ''.join([str(t) for t in soup.body.contents])

    #experimental, don't test it.
    def render_html_diff_del(self, text1, text2):
        soup, diff = self.render_html_diff(text1, text2, "modif")
        modifs_data = []
        modifs = soup.find_all('span', {'id':'modif'})
        for modif in modifs:
            modif_data = {'tag': modif,
                          'todel': "ins",
                          'toins': "del",
                          'blocstodel': None
                         }
            modifs_data.append(modif_data)

        self.unwrap_diff(modifs_data, soup, False)
        diff_divs = soup.find_all('div', {'class':'diff'})
        for div in diff_divs:
            div.unwrap()

        return u''.join([str(t) for t in soup.body.contents])

    #experimental, don't test it.
    def update_text(self, new_text, old_text, text):
        soup, deleted_text = self.render_html_diff_del(old_text, text, "modif")
        soupdiff, diff = self.render_html_diff(new_text, deleted_text, "modif")
        ins_tags = soupdiff.find_all('ins')
        del_tags = soupdiff.find_all('del')
        valid_del_tags = []
        valid_ins_tags = []
        for del_tag in del_tags:
            del_parents = del_tag.find_parents('del')
            if del_parents:
                continue

            valid_del_tags.append(del_tag)

        for ins_tag in ins_tags:
            ins_parents = ins_tag.find_parents('del')
            if ins_parents:
                continue

            valid_ins_tags.append(ins_tag)

        for tag in valid_del_tags:
            new_tag = soupdiff.new_tag('span', type='del')
            tag.wrap(new_tag)
            tag.unwrap()

        for tag in valid_ins_tags:
            new_tag = soupdiff.new_tag('span', type='ins')
            tag.wrap(new_tag)
            tag.unwrap()

        diff = u''.join([str(t) for t in soupdiff.body.contents])
        modifs_data = []
        modifs = soupdiff.find_all('span', {'id':'modif'})
        for modif in modifs:
            modif_data = {'tag': modif,
                          'todel': "ins",
                          'toins': "del",
                          'blocstodel': None
                         }
            modifs_data.append(modif_data)

        self.unwrap_diff(modifs_data, soupdiff)
        del_tags = soupdiff.find_all('span', {'type':'del'})
        ins_tags = soupdiff.find_all('span', {'type':'ins'})
        for tag in ins_tags:
            new_tag = soupdiff.new_tag('ins')
            tag.wrap(new_tag)
            tag.unwrap()

        for tag in del_tags:
            new_tag = soupdiff.new_tag('del')
            tag.wrap(new_tag)
            tag.unwrap()

        soupdiff = self.wrap_diff(diff, "modif")
        modifs_data = []
        modifs = soupdiff.find_all('span', {'id':'modif'})
        for modif in modifs:
            modif_data = {'tag': modif,
                          'todel': "del",
                          'toins': "ins",
                          'blocstodel': None
                         }
            modifs_data.append(modif_data)

        self.unwrap_diff(modifs_data, soupdiff)
        new_diff = u''.join([str(t) for t in soupdiff.body.contents])
        return self.merge(new_text, [text, new_diff])
