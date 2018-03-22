import React from 'react';
import { Entity, EditorState, Modifier, SelectionState } from 'draft-js';
import { getCurrentBlock } from 'medium-draft/lib/model';
import Icon from 'material-ui/Icon';
import { I18n } from 'react-redux-i18n';
import classNames from 'classnames';

import { EMBED_SIZES, EMBED_POSITIONS, DEFAULT_EMBED_DATA } from './constants';

export function getEmbedDataFromNode(node, defaultData) {
  const data = node && node.dataset;
  const position = data && data.position;
  const size = data && data.size;
  return (
    defaultData || {
      position: position || DEFAULT_EMBED_DATA.position,
      size: size || DEFAULT_EMBED_DATA.size
    }
  );
}

export function extractDataFromMap(map) {
  return {
    position: map.get('position'),
    size: map.get('size')
  };
}

export function extractEmbedData(data, prefix = '', defaultData = null) {
  const position = data.position;
  const size = data.size;
  return (
    defaultData || {
      [`${prefix}position`]: position || DEFAULT_EMBED_DATA.position,
      [`${prefix}size`]: size || DEFAULT_EMBED_DATA.size
    }
  );
}

class BlockDataManager extends React.Component {
  constructor(props) {
    super(props);
    const data = props.data || {};
    this.state = {
      ...extractEmbedData(data),
      open: false
    };
    this.background = null;
  }

  componentDidMount() {
    document.addEventListener('mousedown', this.handleClickOutside);
  }

  componentWillUnmount() {
    document.removeEventListener('mousedown', this.handleClickOutside);
  }

  handleClickOutside = (event) => {
    if (this.background && !this.background.contains(event.target)) {
      this.closeMenu();
    }
  };

  focusBlock = () => {
    const { block, blockProps } = this.props;
    const { getEditorState, setEditorState } = blockProps;
    const key = block.getKey();
    const editorState = getEditorState();
    const currentblock = getCurrentBlock(editorState);
    if (currentblock.getKey() === key) {
      return;
    }
    const newSelection = new SelectionState({
      anchorKey: key,
      focusKey: key,
      anchorOffset: 0,
      focusOffset: 0
    });
    setEditorState(EditorState.forceSelection(editorState, newSelection));
  };

  updateData = (key, value) => {
    const { entity, contentState, selection, blockProps: { getEditorState, setEditorState } } = this.props;
    const data = { [key]: value };
    this.setState(data, () => {
      if (entity !== undefined) Entity.mergeData(entity, data);
      const editorState = getEditorState();
      setEditorState(EditorState.push(editorState, Modifier.mergeBlockData(contentState, selection, data), 'change-block-data'));
    });
  };

  onSizeMinus = () => {
    const { size } = this.state;
    const minSize = EMBED_SIZES.small;
    const newSize = size > minSize ? size - 1 : minSize;
    this.updateData('size', newSize);
  };

  onSizePlus = () => {
    const { size } = this.state;
    const maxSize = EMBED_SIZES.large;
    const newSize = size < maxSize ? size + 1 : maxSize;
    this.updateData('size', newSize);
  };

  onLeft = () => {
    this.updateData('position', EMBED_POSITIONS.left);
  };

  onRight = () => {
    this.updateData('position', EMBED_POSITIONS.right);
  };

  onCenter = () => {
    this.updateData('position', EMBED_POSITIONS.center);
  };

  openMenu = () => {
    this.setState({ open: true });
  };

  closeMenu = () => {
    this.setState({ open: false });
  };

  render() {
    const { className, children, readOnly } = this.props;
    const { position, size, open } = this.state;
    return (
      <div className={classNames(className, position, `size-${size}`)} onClick={this.focusBlock}>
        {children}
        {!readOnly &&
          <div
            ref={(background) => {
              this.background = background;
            }}
            className={classNames('md-block-with-data-background', { open: open })}
            onClick={this.openMenu}
            contentEditable="false"
          >
            <div className={classNames('md-block-with-data-menu', { 'md-editor-toolbar--isopen': open })}>
              <span
                className={classNames('md-RichEditor-styleButton', {
                  'md-RichEditor-activeButton': position === EMBED_POSITIONS.left
                })}
                onClick={this.onLeft}
              >
                <Icon className="icon mdi-set mdi-format-float-left" />
              </span>
              <span
                className={classNames('md-RichEditor-styleButton', {
                  'md-RichEditor-activeButton': position === EMBED_POSITIONS.center
                })}
                onClick={this.onCenter}
              >
                <Icon className="icon mdi-set mdi-format-float-center" />
              </span>
              <span
                className={classNames('md-RichEditor-styleButton', {
                  'md-RichEditor-activeButton': position === EMBED_POSITIONS.right
                })}
                onClick={this.onRight}
              >
                <Icon className="icon mdi-set mdi-format-float-right" />
              </span>

              <span
                className={classNames('md-RichEditor-styleButton', {
                  'md-RichEditor-disabledButton': size === EMBED_SIZES.small
                })}
                onClick={this.onSizeMinus}
              >
                <Icon className="icon mdi-set mdi-magnify-minus" />
              </span>
              <span
                className={classNames('md-RichEditor-styleButton', {
                  'md-RichEditor-disabledButton': size === EMBED_SIZES.large
                })}
                onClick={this.onSizePlus}
              >
                <Icon className="icon mdi-set mdi-magnify-plus" />
              </span>
            </div>
          </div>}
      </div>
    );
  }
}

export default BlockDataManager;