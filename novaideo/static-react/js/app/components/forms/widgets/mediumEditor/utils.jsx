import React from 'react';
import { EditorState, Modifier } from 'draft-js';
import { StringToTypeMap, Block, beforeInput, getCurrentBlock, HANDLED } from 'medium-draft';
import { blockToHTML, entityToHTML } from 'medium-draft/lib/exporter';
import { htmlToBlock } from 'medium-draft/lib/importer';

const newTypeMap = StringToTypeMap;
newTypeMap['2.'] = Block.OL;

const DQUOTE_START = '“';
const DQUOTE_END = '”';
const SQUOTE_START = '‘';
const SQUOTE_END = '’';

export const newHTMLtoBlock = (nodeName, node) => {
  if (nodeName === 'figure') {
    if (node.className.match(/^md-block-image/)) {
      const imageNode = node.querySelector('img');
      return {
        type: Block.IMAGE,
        data: {
          src: imageNode && imageNode.src
        }
      };
    } else if (node.className.match(/md-block-atomic/)) {
      const aNode = node.querySelector('a');
      return {
        type: Block.ATOMIC,
        data: {
          url: aNode && aNode.href,
          type: aNode && 'embed'
        }
      };
    }
    return undefined;
  } else if (node.className.match(/md-block-atomic-break/)) {
    return {
      type: Block.ATOMIC,
      data: {
        type: 'separator'
      }
    };
  }
  return htmlToBlock(nodeName, node);
};

export const newBlockToHTML = (block) => {
  if (block.type === Block.ATOMIC) {
    if (block.text === 'E') {
      return {
        start: '<figure class="md-block-atomic md-block-atomic-embed">',
        end: '</figure>'
      };
    } else if (block.text === '-') {
      return (
        <div className="md-block-atomic md-block-atomic-break">
          <hr className="text-node-separator" />
        </div>
      );
    }
  }
  return blockToHTML(block);
};

export const newEntityToHTML = (entity, originalText) => {
  if (entity.type === 'embed') {
    return (
      <div className="embedly-card-url-container">
        <a className="embedly-card-url embedly-card" href={entity.data.url} data-card-controls="0">
          {entity.data.url}
        </a>
      </div>
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
    } else if (len > 0) {
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

export class AtomicEmbedComponent extends React.Component {
  state = {
    showIframe: false
  };

  componentDidMount() {
    this.renderEmbedly();
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevState.showIframe !== this.state.showIframe && this.state.showIframe === true) {
      this.renderEmbedly();
    }
  }

  getScript = () => {
    const script = document.createElement('script');
    script.async = 1;
    script.src = '//cdn.embedly.com/widgets/platform.js';
    script.onload = () => {
      window.embedly();
    };
    document.body.appendChild(script);
  };

  renderEmbedly = () => {
    if (window.embedly) {
      // window.embedly();
    } else {
      this.getScript();
    }
  };

  render() {
    const { url } = this.props.data;
    return (
      <div lassName="md-block-atomic-embed">
        <div className="embedly-card-url-container">
          <a className="embedly-card-url embedly-card" href={url} data-card-controls="0">
            {url}
          </a>
        </div>
      </div>
    );
  }
}

export const AtomicSeparatorComponent = () => {
  return (
    <div className="md-block-atomic md-block-atomic-break">
      <hr className="text-node-separator" />
    </div>
  );
};

export const AtomicBlock = (props) => {
  const { blockProps, block, contentState } = props;
  const index = block.getEntityAt(0);
  let entitydata = null;
  let entityType = null;
  if (index !== null) {
    const entity = contentState.getEntity(block.getEntityAt(0));
    entitydata = entity.getData();
    entityType = entity.getType();
  }
  const data = block.getData();
  const type = data.get('type') || entityType;
  if (blockProps.components[type]) {
    const AtComponent = blockProps.components[type];
    return (
      <div className={`md-block-atomic-wrapper md-block-atomic-wrapper-${type}`}>
        <AtComponent data={entitydata} />
      </div>
    );
  }
  return null;
};