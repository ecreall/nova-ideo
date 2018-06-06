import React from 'react';
import {
  Editor,
  EditorState,
  Modifier,
  convertFromHTML,
  ContentState,
  SelectionState,
  getDefaultKeyBinding,
  KeyBindingUtil,
  convertFromRaw,
  convertToRaw
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
    let editorstate = props.value && typeof props.value === 'string' && this.resetEditor(props.value);
    editorstate = editorstate || (props.value && EditorState.createWithContent(convertFromRaw(props.value))) || props.value;
    this.state = { editorState: editorstate || EditorState.createEmpty() };
  }

  resetEditor = (text, focus) => {
    let editorState;
    const htmlText = text || emptyText;
    if (htmlText !== emptyText) {
      const blocksFromHTML = convertFromHTML(htmlText);
      const contentState = ContentState.createFromBlockArray(blocksFromHTML.contentBlocks, blocksFromHTML.entityMap);
      editorState = EditorState.createWithContent(contentState);
      if (focus) {
        editorState = this.endFocus(editorState);
      }
    } else {
      editorState = EditorState.createEmpty();
    }
    return editorState;
  };

  reset = (text) => {
    this.setState({ editorState: this.resetEditor(text, true) });
  };

  clear = (focus) => {
    this.setState({ editorState: this.resetEditor(emptyText) }, () => {
      if (focus) this.focus();
    });
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
    this.onChange(newEditorState);
  };

  getPlainText = () => {
    return this.state.editorState.getCurrentContent().getPlainText();
  };

  getHTMLText = () => {
    return convertToHTML(this.state.editorState.getCurrentContent());
  };

  onChange = (editorState) => {
    this.setState({ editorState: editorState }, () => {
      this.props.onChange(convertToRaw(this.state.editorState.getCurrentContent()));
    });
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