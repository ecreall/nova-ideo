import React from 'react';
import { EditorState, Modifier } from 'draft-js';
import {
  StringToTypeMap, Block, Entity as EntityConstants, beforeInput, getCurrentBlock, HANDLED
} from 'medium-draft';
import { blockToHTML, entityToHTML } from 'medium-draft/lib/exporter';
import { htmlToBlock, htmlToEntity } from 'medium-draft/lib/importer';
import { Inline } from 'medium-draft/lib/util/constants';
import Icon from '@material-ui/core/Icon';
import { I18n } from 'react-redux-i18n';

import {
  DQUOTE_START, DQUOTE_END, SQUOTE_START, SQUOTE_END
} from './constants';

import { getEmbedDataFromNode, extractEmbedData } from './BlockDataManager';

const newTypeMap = StringToTypeMap;
newTypeMap['2.'] = Block.OL;

export const newHTMLtoBlock = (nodeName, node) => {
  if (nodeName === 'figure') {
    if (node.className.match(/^md-block-image/)) {
      const imageNode = node.querySelector('img');
      return {
        type: Block.IMAGE,
        data: {
          src: imageNode && imageNode.src,
          ...getEmbedDataFromNode(imageNode)
        }
      };
    }
    if (node.className.match(/md-block-atomic/)) {
      const aNode = node.querySelector('a');
      return {
        type: Block.ATOMIC,
        data: {
          url: aNode && aNode.href,
          type: aNode && 'embed',
          ...getEmbedDataFromNode(aNode)
        }
      };
    }
    return undefined;
  }
  if (node.className.match(/md-block-atomic-break/)) {
    return {
      type: Block.ATOMIC,
      data: {
        type: 'separator'
      }
    };
  }
  return htmlToBlock(nodeName, node);
};

export const newHtmlToEntity = (nodeName, node, createEntity) => {
  const embedData = getEmbedDataFromNode(node, {});
  if (nodeName === 'a' && embedData.position) {
    return createEntity(EntityConstants.LINK, 'MUTABLE', { url: node.href, ...embedData });
  }
  return htmlToEntity(nodeName, node, createEntity);
};

export const newBlockToHTML = (block) => {
  if (block.type === Block.ATOMIC) {
    const data = block.data || {};
    const type = data.type;
    if (type === 'embed' || block.text === 'E') {
      if (data.url) {
        return (
          <figure className="md-block-atomic md-block-atomic-embed">
            <a
              href={data.url}
              className="md-inline-link"
              target="_blank"
              rel="noopener noreferrer"
              {...extractEmbedData(data, 'data-')}
            >
              {data.url}
            </a>
          </figure>
        );
      }
      return {
        start: '<figure class="md-block-atomic md-block-atomic-embed">',
        end: '</figure>'
      };
    }
    if (type === 'separator' || block.text === '-') {
      return (
        <div className="md-block-atomic md-block-atomic-break">
          <hr className="text-node-separator" />
        </div>
      );
    }
  } else if (block.type === Block.IMAGE) {
    const imgData = block.data;
    const text = block.text;
    const extraClass = text.length > 0 ? ' md-block-image-has-caption' : '';
    return (
      <figure className={`md-block-image${extraClass}`}>
        <img src={imgData.src} alt={text} {...extractEmbedData(imgData, 'data-')} />
        <figcaption className="md-block-image-caption">{text}</figcaption>
      </figure>
    );
  }
  return blockToHTML(block);
};

export const newEntityToHTML = (entity, originalText) => {
  const { data, type } = entity;
  if (type === 'embed' || data.position) {
    return (
      <a
        href={data.url}
        className="md-inline-link"
        target="_blank"
        rel="noopener noreferrer"
        {...extractEmbedData(data, 'data-')}
      >
        {data.url}
      </a>
    );
  }
  return entityToHTML(entity, originalText);
};

export const handleBeforeInput = (editorState, str, onChange) => {
  if (str === '"' || str === '\'') {
    const currentBlock = getCurrentBlock(editorState);
    const selectionState = editorState.getSelection();
    const contentState = editorState.getCurrentContent();
    const text = currentBlock.getText();
    const len = text.length;
    if (selectionState.getAnchorOffset() === 0) {
      onChange(
        EditorState.push(
          editorState,
          Modifier.insertText(contentState, selectionState, str === '"' ? DQUOTE_START : SQUOTE_START),
          'transpose-characters'
        )
      );
      return HANDLED;
    }
    if (len > 0) {
      const lastChar = text[len - 1];
      if (lastChar !== ' ') {
        onChange(
          EditorState.push(
            editorState,
            Modifier.insertText(contentState, selectionState, str === '"' ? DQUOTE_END : SQUOTE_END),
            'transpose-characters'
          )
        );
      } else {
        onChange(
          EditorState.push(
            editorState,
            Modifier.insertText(contentState, selectionState, str === '"' ? DQUOTE_START : SQUOTE_START),
            'transpose-characters'
          )
        );
      }
      return HANDLED;
    }
  }
  return beforeInput(editorState, str, onChange, newTypeMap);
};

export const BLOCK_BUTTONS = () => {
  return [
    {
      label: 'H1',
      style: 'header-one',
      icon: 'header',
      description: I18n.t('editor.heading1')
    },
    {
      label: 'H2',
      style: 'header-two',
      icon: 'header',
      description: I18n.t('editor.heading2')
    },
    {
      label: 'H3',
      style: 'header-three',
      icon: 'header',
      description: I18n.t('editor.heading3')
    },
    {
      label: <Icon className="icon mdi-set mdi-code-braces" />,
      style: 'code-block',
      icon: 'header',
      description: I18n.t('editor.heading3')
    },
    {
      label: <Icon className="icon mdi-set mdi-format-quote-open" />,
      style: 'blockquote',
      icon: 'quote-right',
      description: I18n.t('editor.blockquote')
    },
    {
      label: <Icon className="icon mdi-set mdi-format-list-bulleted" />,
      style: 'unordered-list-item',
      icon: 'list-ul',
      description: I18n.t('editor.unorderedL')
    },
    {
      label: <Icon className="icon mdi-set mdi-format-list-numbers" />,
      style: 'ordered-list-item',
      icon: 'list-ol',
      description: I18n.t('editor.orderedL')
    }
    // {
    //   label: <Icon className="icon mdi-set mdi-format-list-checks" />,
    //   style: 'todo',
    //   description: I18n.t('editor.todoL')
    // }
  ];
};

export const INLINE_BUTTONS = () => {
  return [
    {
      label: 'B',
      style: 'BOLD',
      icon: 'bold',
      description: I18n.t('editor.bold')
    },
    {
      label: 'I',
      style: 'ITALIC',
      icon: 'italic',
      description: I18n.t('editor.italic')
    },
    {
      label: 'U',
      style: 'UNDERLINE',
      icon: 'underline',
      description: I18n.t('editor.underline')
    },
    {
      label: <Icon className="icon mdi-set mdi-marker" />,
      style: 'HIGHLIGHT',
      description: I18n.t('editor.highlight')
    },
    {
      label: <Icon className="icon mdi-set mdi-link-variant" />,
      style: 'hyperlink',
      icon: 'link',
      description: I18n.t('editor.addLink')
    },
    {
      label: <Icon className="icon mdi-set mdi-code-tags" />,
      style: 'CODE',
      icon: 'code',
      description: I18n.t('editor.bold')
    }
  ];
};

export const customStyleMap = {
  [Inline.HIGHLIGHT]: {
    backgroundColor: 'rgba(3, 169, 244, 0.5)',
    padding: 3,
    borderRadius: 3
  },
  [Inline.CODE]: {
    fontFamily: 'Monaco,Menlo,Consolas,"Courier New",monospace !important',
    fontSize: '.75rem',
    lineHeight: '.75rem',
    whiteSpace: 'normal',
    color: '#d72b3f',
    padding: '2px 3px 1px',
    fontVariantLigatures: 'none',
    tabSize: 4,
    backgroundColor: '#f7f7f9',
    border: '1px solid #e1e1e8',
    borderRadius: 3
  }
};