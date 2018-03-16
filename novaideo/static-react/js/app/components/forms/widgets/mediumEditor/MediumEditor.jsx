import React from 'react';
import { EditorState, Modifier, convertToRaw, SelectionState } from 'draft-js';
import { convertToHTML } from 'draft-convert';
import { Editor, Block, createEditorState, addNewBlockAt, rendererFn, HANDLED, NOT_HANDLED } from 'medium-draft';
import { setImportOptions, htmlToStyle, htmlToEntity } from 'medium-draft/lib/importer';
import { setRenderOptions, styleToHTML } from 'medium-draft/lib/exporter';
import 'medium-draft/lib/index.css';

import {
  newBlockToHTML,
  newEntityToHTML,
  newHTMLtoBlock,
  handleBeforeInput,
  AtomicEmbedComponent,
  AtomicSeparatorComponent,
  AtomicBlock
} from './utils';
import SeparatorButton from './SeparatorButton';
import EmbedButton from './EmbedButton';
import ImageButton from './ImageButton';

export const emptyText = '<p></p>';

class MediumEditor extends React.Component {
  constructor(props) {
    super(props);
    this.importer = setImportOptions({
      htmlToStyle: htmlToStyle,
      htmlToEntity: htmlToEntity,
      htmlToBlock: newHTMLtoBlock
    });
    this.state = {
      editorState: this.resetEditor(props.value),
      editorEnabled: !props.readOnly
    };
    this.editor = null;
    this.sideButtons = [
      {
        title: 'Image',
        component: ImageButton
      },
      {
        title: 'Embed',
        component: EmbedButton
      },
      {
        title: 'Separator',
        component: SeparatorButton
      }
    ];
    this.exporter = setRenderOptions({
      styleToHTML: styleToHTML,
      blockToHTML: newBlockToHTML,
      entityToHTML: newEntityToHTML
    });
  }

  getEditorState = () => {
    return this.state.editorState;
  };

  rendererFn = (setEditorState, getEditorState) => {
    const atomicRenderers = {
      embed: AtomicEmbedComponent,
      separator: AtomicSeparatorComponent
    };
    const rFnOld = rendererFn(setEditorState, getEditorState);
    const rFnNew = (contentBlock) => {
      const type = contentBlock.getType();
      switch (type) {
      case Block.ATOMIC:
        return {
          component: AtomicBlock,
          editable: false,
          props: {
            components: atomicRenderers
          }
        };
      default:
        return rFnOld(contentBlock);
      }
    };
    return rFnNew;
  };

  handleDroppedFiles = (selection, files) => {
    const file = files[0];
    if (file.type.indexOf('image/') === 0) {
      // eslint-disable-next-line no-undef
      const src = URL.createObjectURL(file);
      this.onChange(
        addNewBlockAt(this.state.editorState, selection.getAnchorKey(), Block.IMAGE, {
          src: src
        })
      );
      return HANDLED;
    }
    return NOT_HANDLED;
  };

  handleReturn = () => {
    return NOT_HANDLED;
  };

  resetEditor = (text) => {
    let editorState;
    const htmlText = text || emptyText;
    if (htmlText !== emptyText) {
      editorState = createEditorState(convertToRaw(this.importer(htmlText)));
    } else {
      editorState = createEditorState();
    }
    return editorState;
  };

  reset = (text) => {
    this.setState({ editorState: this.resetEditor(text, true) });
  };

  clear = (focus) => {
    this.setState({ editorState: this.resetEditor(emptyText, focus) });
  };

  endFocus = (editorState) => {
    if (editorState) {
      const content = editorState.getCurrentContent();
      const blockMap = content.getBlockMap();
      const key = blockMap.last().getKey();
      const length = blockMap.last().getLength();
      const selection = new SelectionState({
        anchorKey: key,
        anchorOffset: length,
        focusKey: key,
        focusOffset: length
      });
      return EditorState.forceSelection(editorState, selection);
    }
    return editorState;
  };

  focus = (end) => {
    if (this.editor) {
      if (end) {
        this.setState({ editorState: this.endFocus(this.state.editorState) });
      } else {
        this.editor.focus();
      }
    }
  };

  isEmptyText = (text) => {
    return !text || text === emptyText;
  };

  insertText = (text) => {
    const editorState = this.state.editorState;
    const currentContent = editorState.getCurrentContent();
    const selection = editorState.getSelection();
    const textWithEntity = Modifier.insertText(currentContent, selection, text, null, null);
    let newEditorState = EditorState.push(editorState, textWithEntity, 'insert-characters');
    newEditorState = this.endFocus(newEditorState);
    const content = convertToHTML(newEditorState.getCurrentContent());
    this.props.onChange(content);
    this.setState({ editorState: newEditorState });
  };

  getPlainText = () => {
    return this.state.editorState.getCurrentContent().getPlainText();
  };

  onChange = (editorState) => {
    const { onChange } = this.props;
    if (onChange) {
      const content = this.exporter(editorState.getCurrentContent());
      onChange(content);
    }
    return this.setState({ editorState: editorState });
  };

  handleKeyCommand = (command) => {
    const { onCtrlEnter, onEnter } = this.props;
    if (onCtrlEnter && command === 'ctrl-enter') {
      onCtrlEnter();
      return 'handled';
    }
    if (onEnter && command === 'split-block') {
      onEnter();
      return 'handled';
    }
    return 'not-handled';
  };

  render() {
    const { editorState, editorEnabled, placeholder } = this.state;
    return (
      <Editor
        ref={(editor) => {
          this.editor = editor;
        }}
        editorState={editorState}
        onChange={this.onChange}
        editorEnabled={editorEnabled}
        handleDroppedFiles={this.handleDroppedFiles}
        handleKeyCommand={this.handleKeyCommand}
        placeholder={placeholder}
        beforeInput={handleBeforeInput}
        handleReturn={this.handleReturn}
        sideButtons={this.sideButtons}
        rendererFn={this.rendererFn}
      />
    );
  }
}

export default MediumEditor;