# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi

"""Text analyzer utility
"""
import re
from html.parser import HTMLParser
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from zope.interface import Interface, implementer

from dace.util import utility

from novaideo.ips.htmldiff import htmldiff


HTML_INLINE_ELEMENTS = [
           'b', 'big', 'i', 'small', 'tt',
           'abbr', 'acronym', 'cite', 'code',
           'dfn', 'em', 'kbd', 'strong', 'samp', 
           'var', 'a', 'bdo', 'br', 'img', 'map',
           'object', 'q', 'script', 'span', 'sub', 
           'sup', 'button', 'input', 'label', 'select',
           'textarea']


HTML_BLOCK_ELEMENTS = [
           'p', 'h1', 'h2', 'h3', 'h4', 
           'h5', 'h6', 'ol', 'ul', 'pre', 
           'address', 'blockquote', 'dl', 
           'div', 'fieldset', 'form', 'hr', 
           'noscript', 'table']


class EndKind:
    START = 0
    END = 1
    BOTH = 2


DEL_TAG_ENDS = {
            EndKind.START: '<del>',
            EndKind.END: '</del>',
            EndKind.BOTH: '<del></del>' 
}


INS_TAG_ENDS = {
            EndKind.START: '<ins>',
            EndKind.END: '</ins>',
            EndKind.BOTH: '<ins></ins>' 
}


SPACE_TAG = '[#]'


def prepare_text_spaces(text):
    return text.replace('\xa0', ' ').replace(' ', ' '+SPACE_TAG+' ')


def format_spaces(text):
    soup = BeautifulSoup(text)
    for tagstring in list(soup.strings):
        value = tagstring.replace(' ', '').replace(SPACE_TAG, ' ')
        new_tag = soup.new_string(value)
        tagstring.replace_with(new_tag)
        if new_tag == '':
            new_tag.extract()

    return soup, u''.join([str(t) for t in soup.body.contents])


def tag_to_text(tag):
    return ''.join([str(t) for t in tag.contents])


def normalize_text(text):
    parser = HTMLParser()
    text = parser.unescape(text)
    soup = BeautifulSoup(text)
    return ''.join([str(t) for t in soup.body.contents])


def index(list_values, index, default=None):
    try:
        return list_values[index]
    except IndexError:
        return default


def get_del_tags_positions(text):
    start_tag = DEL_TAG_ENDS[EndKind.START]
    end_tag = DEL_TAG_ENDS[EndKind.END]
    starts = [a.start() for a in re.finditer(start_tag, text)]
    ends = [a.start() for a in re.finditer(end_tag, text)]
    positions = list(zip(starts, ends))
    for i, position in enumerate(positions):
        reduce_to = i * (len(start_tag) + len(end_tag))
        positions[i] = (position[0]-reduce_to, 
                      position[1]-reduce_to-len(start_tag))

    return positions


def get_firsts_positions(all_positions):
    firsts = [index(positions, 0) for positions in all_positions \
              if index(positions, 0)]
    firsts = sorted(firsts, key=lambda e: e[0])
    return firsts


def get_global_interval(start_position, all_positions):
    end_interval = start_position[1]
    all_diffs = [item for sublist in all_positions for item in sublist]
    ends = [a for a in all_diffs \
            if a[1] >= end_interval and a[0] <= end_interval]
    ends = sorted(ends, key=lambda e: e[1], reverse=True)
    return (start_position[0], ends[0][1])


def remove_positions_in_interval(interval, positions):
    def is_in_interval(position):
        if position[0] >= interval[0] and \
           position[1] <= interval[1]:
            return True

        return False
    return [position for position in positions if not is_in_interval(position)]


def get_ins_tags_positions(diff):
    ins_tag = INS_TAG_ENDS[EndKind.BOTH]
    positions = [a.start() for a in re.finditer(ins_tag, diff)]
    for i, position in enumerate(positions):
        reduce_to = i * len(ins_tag)
        positions[i] = position-reduce_to

    return positions


def _convert_position(position, intervals):
    start_tag = DEL_TAG_ENDS[EndKind.START]
    end_tag = DEL_TAG_ENDS[EndKind.END]
    result = 0
    for interval in intervals:
        if position > interval[0]:
            result += len(start_tag)

        if position >= interval[1]:
            result += len(end_tag)

    return result


def add_ins_tags(origin_text, texts, intervals):
    ins_tag = INS_TAG_ENDS[EndKind.BOTH]
    positions = [get_ins_tags_positions(text) for text in texts]
    positions = sorted(list(set([item for sublist in positions \
                                 for item in sublist])))
    for i, position in enumerate(positions):
        convert_to = i * len(ins_tag) + _convert_position(position, intervals)
        origin_text = origin_text[:position+convert_to] + ins_tag + \
                      origin_text[position+convert_to:]

    return origin_text


def get_inline_root(tag):
    parent = tag.parent
    if parent and \
       len(parent.contents) == 1 and \
       parent.name in HTML_INLINE_ELEMENTS:
        return get_inline_root(parent)

    return tag


def get_next_tag(tag, name):
    valid = re.compile(r"^\s*$")
    next_tags = tag.next_siblings
    for next_tag in list(next_tags):
        if isinstance(next_tag, NavigableString) and \
           valid.match(next_tag):
            continue

        if not next_tag or \
           (next_tag and \
           next_tag.name != name):
            return None

        return next_tag

    return None


def get_previous_tag(tag, name):
    valid = re.compile(r"^\s*$")
    previous_tags = tag.previous_siblings
    for previous_tag in list(previous_tags):
        if isinstance(previous_tag, NavigableString) and \
           valid.match(previous_tag):
            continue

        if not previous_tag or \
           (previous_tag and \
           previous_tag.name != name):
            return None

        return previous_tag

    return None


def merge_with_next_tags(tag, name):
    valid = re.compile(r"^\s*$")
    next_tags = tag.next_siblings
    to_wrap = []
    for next_tag in list(next_tags):
        if isinstance(next_tag, NavigableString) and \
           valid.match(next_tag):
            to_wrap.append(next_tag)
            continue

        if not next_tag or \
           (next_tag and \
           next_tag.name != name):
            return tag

        to_wrap.append(next_tag)
        for tag_to_wrap in to_wrap:
            tag.append(tag_to_wrap)  

        next_tag.unwrap()
        to_wrap = []

    return tag


def _find_optimum_text(source, tofind):
    notvalid = re.compile(r"^\s*$")
    if notvalid.match(tofind) or len(tofind) < 2:
        return None

    soup = BeautifulSoup(source)
    strings = list(soup.body.strings)
    for source_string in strings:
        if source_string.find(tofind) >= 0:
            return soup, source_string, tofind

    return None

def correct_insertion(soup, tag):
    start_tag = DEL_TAG_ENDS[EndKind.START]
    end_tag = DEL_TAG_ENDS[EndKind.END]
    tagname = 'del'
    if tag.name == 'del':
        start_tag = INS_TAG_ENDS[EndKind.START]
        end_tag = INS_TAG_ENDS[EndKind.END]
        tagname = 'ins'

    text_ins = tag_to_text(tag)
    next_tag = get_next_tag(tag, tagname)
    if next_tag:
        text_del = start_tag+tag_to_text(next_tag)+end_tag
        result = _find_optimum_text(text_del, text_ins)
        if result:
            text_del_soup = result[0]
            string_to_replace = result[1]
            text_of_replacement = result[2]
            newstr = str(string_to_replace.replace(text_of_replacement,
                         end_tag+text_of_replacement+start_tag, 1))
            newstr = text_del_soup.new_string(newstr)
            string_to_replace.replace_with(newstr)
            new_tag = u''.join([str(t) for t in text_del_soup.body.contents])
            new_tag = new_tag.replace('&gt;', '>').replace('&lt;', '<')
            new_tag = prepare_text_spaces(new_tag)
            text_del_soup, new_tag = format_spaces(new_tag)
            new_sub_tags = list(text_del_soup.body.contents)
            new_sub_tags.reverse()
            for sub_tag in new_sub_tags:
                next_tag.insert_after(sub_tag)

            next_tag.extract()
            tag.extract()


def normalize_diff(diff):
    soup = None
    if isinstance(diff, BeautifulSoup):
        soup = diff
    else:
        soup = BeautifulSoup(diff)

    #wrap inline parent
    tags = soup.find_all(['del', 'ins'])
    for tag in list(tags):
        inline_parent = get_inline_root(tag)
        if inline_parent is not tag:
            tag.unwrap()
            inline_parent.wrap(tag)

    #merge tags with same name
    tags = soup.find_all(['del', 'ins'])
    for tag in list(tags):
        if tag.parent:
            merge_with_next_tags(tag, tag.name)

    #remove empty tags
    tags = soup.find_all(['del', 'ins'])
    for tag in list(tags):
        if not tag.contents:
            tag.extract()

    #correct insertions 
    tags = soup.find_all(['del', 'ins'])
    for tag in list(tags):
        if tag.parent:
            correct_insertion(soup, tag)

    #remove empty tags
    tags = soup.find_all(['del', 'ins'])
    for tag in list(tags):
        if not tag.contents:
            tag.extract()

    return soup, u''.join([str(t) for t in soup.body.contents])

def merge_tags(tag1, tag2, separators, soup):
    if tag1 and tag2:
        tag1 = tag1[0]
        tag2 = tag2[0]
        newcontents = []
        if separators:
            newcontents = [soup.new_string(' ') for s in separators]
        newcontents.extend(tag2.contents)
        for content in newcontents:
            tag1.append(content)

        return True

    return False


def merge_with_next_modif(tag, diff_id, soup):
    valid = re.compile(r"^\s*$")
    next_tags = tag.next_siblings
    strings = []
    for next_tag in list(next_tags):
        if isinstance(next_tag, NavigableString) and \
           valid.match(next_tag):
            strings.append(next_tag)
            continue

        if not next_tag or \
           (next_tag and \
            (next_tag.name != "span" or \
             next_tag['id'] != diff_id)):
            return tag

        next_ins = next_tag.find_all('ins')
        next_del = next_tag.find_all('del')
        tag_ins = tag.find_all('ins')
        tag_del = tag.find_all('del')
        ins_merged = merge_tags(tag_ins, next_ins, strings, soup)
        del_merged = merge_tags(tag_del, next_del, strings, soup)
        if del_merged or ins_merged:
            for str_tag in strings:
                str_tag.extract()

        strings = []
        next_tag.extract()

    return tag


def merge_modifs(soup, diff_id):
    tags = soup.find_all("span", id=diff_id)
    for tag in list(tags):
        if tag.parent:
            merge_with_next_modif(tag, diff_id, soup)

    return soup

def list_eq(list1, list2):
    if len(list1) != len(list2):
        return False
    
    ziped_list = list(zip(list1, list2))
    for value1, value2 in ziped_list:
        if value1 != value2:
            return False

    return True


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
        """Render html diff between text1 and text2
           text1 and text2 will be normalized"""
        parser = HTMLParser()
        normalized_space_t1 = prepare_text_spaces(text1)
        normalized_space_t2 = prepare_text_spaces(text2)
        result = htmldiff.render_html_diff(normalized_space_t1, 
                                           normalized_space_t2)
        soup, result = format_spaces(result)
        soup, result = normalize_diff(soup)
        soup = self.wrap_diff(soup, diff_id)
        result = u''.join([str(t) for t in soup.body.contents])
        result = parser.unescape(result)
        return soup, result

    def wrap_diff(self, diff, diff_id):
        """Wrap diff with span tags"""
        soup = None
        if isinstance(diff, BeautifulSoup):
            soup = diff
        else:
            soup = BeautifulSoup(diff)

        ins_tags = soup.find_all('ins')
        del_tags = soup.find_all('del')
        del_included = []
        for ins_tag in ins_tags:
            new_tag = soup.new_tag("span", id=diff_id)
            previous_del_tag = get_previous_tag(ins_tag, 'del')
            ins_strings = list(ins_tag.strings)
            if previous_del_tag:
                previous_del_tag_strings = list(previous_del_tag.strings)
                if not list_eq(previous_del_tag_strings, ins_strings):
                    previous_del_tag.wrap(new_tag)
                    new_tag.append(ins_tag)
                    del_included.append(previous_del_tag)
                    continue
                else:
                    del_included.append(previous_del_tag)
                    ins_tag.unwrap()
                    previous_del_tag.extract()

            if ins_tag.parent is not None:
                ins_tag.wrap(new_tag)

        for del_tag in del_tags:
            if del_tag not in del_included:
                if del_tag.contents:
                    new_tag = soup.new_tag("span", id=diff_id)
                    del_tag.wrap(new_tag)
                else:
                    del_tag.extract()

        soup = merge_modifs(soup, diff_id)
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

            if blocks_to_del:
                blocs = tag.find_all(blocks_to_del[0], blocks_to_del[1])
                for bloc in blocs:
                    bloc.extract()

            if tag.contents and tag.contents[-1] == '\n':
                tag.contents.pop()

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

    def _get_removed_diffs(self, text1, text2):
        soup, diff = self.render_html_diff(text1, text2, 'amendment-modif')
        modifs = soup.find_all('span', {'id':'amendment-modif'})
        ins_tags = soup.find_all('ins')
        #ignore the inserted text
        for ins_tag in ins_tags:
            ins_tag.extract()

        for modif in modifs:
            modif.unwrap()

        return self.soup_to_text(soup)

    def _get_add_diffs(self, text1, text2):
        soup, diff = self.render_html_diff(text1, text2, 'amendment-modif')
        modifs = soup.find_all('span', {'id':'amendment-modif'})
        del_tags = soup.find_all('del')
        for del_tag in del_tags:
            del_tag.unwrap()

        ins_tags = soup.find_all('ins')
        #ignore the inserted text
        for ins_tag in ins_tags:
            ins_tag.clear()

        for modif in modifs:
            modif.unwrap()

        return self.soup_to_text(soup)

    def get_merged_diffs(self, 
                         text, 
                         texts, 
                         tag_removed_attrs, 
                         tag_added_attrs):
        start_tag = DEL_TAG_ENDS[EndKind.START]
        end_tag = DEL_TAG_ENDS[EndKind.END]
        intervals = []
        all_del_positions = [get_del_tags_positions(
                                  self._get_removed_diffs(text, t)) \
                             for t in texts]
        firsts = get_firsts_positions(all_del_positions)
        if firsts:
            interval = get_global_interval(firsts[0], all_del_positions)
            intervals.append(interval)
            all_del_positions = [remove_positions_in_interval(interval, 
                                                              del_positions) \
                                 for del_positions in all_del_positions]
            all_del_positions = [l for l in all_del_positions if l]
            while all_del_positions:
                firsts = get_firsts_positions(all_del_positions)
                interval = get_global_interval(firsts[0], all_del_positions)
                intervals.append(interval)
                all_del_positions = [remove_positions_in_interval(interval, 
                                                                del_positions) \
                                     for del_positions in all_del_positions]
                all_del_positions = [l for l in all_del_positions if l]

        merged_diff = text
        for i, interval in enumerate(intervals):
            convert_to = i * (len(start_tag) + len(end_tag))
            merged_diff = merged_diff[:interval[0]+convert_to] + \
                start_tag + \
                merged_diff[interval[0]+convert_to:interval[1]+convert_to] + \
                end_tag + \
                merged_diff[interval[1]+convert_to:]

        added_diffs = [self._get_add_diffs(text, t) for t in texts]
        merged_diff = add_ins_tags(merged_diff, added_diffs, intervals)
        merged_diff = prepare_text_spaces(merged_diff)
        soup, merged_diff = format_spaces(merged_diff)
        ins_tags = soup.find_all('ins')
        for ins_tag in ins_tags:
            ins_span = soup.new_tag("span", **tag_added_attrs)
            ins_tag.replace_with(ins_span)

        del_tags = soup.find_all('del')
        for del_tag in del_tags:
            del_span = soup.new_tag("span", **tag_removed_attrs)
            del_tag.wrap(del_span)
            del_tag.unwrap()

        merged_diff = self.soup_to_text(soup)
        return merged_diff   

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
        diff_divs = soup.find_all('span', {'class':'modif'})
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
