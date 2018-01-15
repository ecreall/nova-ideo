import React from 'react';
import {
  Editor,
  EditorState,
  Modifier,
  convertFromHTML,
  ContentState,
  SelectionState,
  getDefaultKeyBinding,
  KeyBindingUtil
} from 'draft-js';
import { convertToHTML } from 'draft-convert';

const { hasCommandModifier } = KeyBindingUtil;

export const emptyText = '<p></p>';

function keyBindingFn(e) {
  if ((e.ctrlKey || e.metaKey) && (e.keyCode === 13 || e.keyCode === 10) && hasCommandModifier(e)) {
    return 'ctrl-enter';
  }
  return getDefaultKeyBinding(e);
}

class TextEditor extends React.Component {
  constructor(props) {
    super(props);
    this.editor = null;
    this.state = { editorState: this.resetEditor(props.value) };
  }

  resetEditor = (text) => {
    let editorState;
    const htmlText = text || emptyText;
    const blocksFromHTML = convertFromHTML(htmlText);
    const contentState = ContentState.createFromBlockArray(blocksFromHTML);
    editorState = EditorState.createWithContent(contentState);
    editorState = this.endFocus(editorState);
    return editorState;
  };

  reset = (text) => {
    this.setState({ editorState: this.resetEditor(text) });
  };

  clear = () => {
    this.setState({ editorState: this.resetEditor(emptyText) });
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
    this.setState(
      {
        editorState: EditorState.push(editorState, textWithEntity, 'insert-characters')
      },
      () => {
        this.focus(true);
        const content = convertToHTML(this.state.editorState.getCurrentContent());
        this.props.onChange(content);
      }
    );
  };

  onChange = (editorState) => {
    const content = convertToHTML(editorState.getCurrentContent());
    this.props.onChange(content);
    return this.setState({ editorState: editorState });
  };

  handleKeyCommand = (command) => {
    const { onCtrlEnter } = this.props;
    if (onCtrlEnter && command === 'ctrl-enter') {
      onCtrlEnter();
      return 'handled';
    }
    return 'not-handled';
  };

  render() {
    return (
      <Editor
        ref={(editor) => {
          this.editor = editor;
        }}
        editorState={this.state.editorState}
        onChange={this.onChange}
        handleKeyCommand={this.handleKeyCommand}
        keyBindingFn={keyBindingFn}
      />
    );
  }
}

export default TextEditor;