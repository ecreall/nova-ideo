import React from 'react';
import { EditorState, Modifier, convertToRaw, SelectionState, convertFromRaw } from 'draft-js';
import { Editor, Block, createEditorState, addNewBlockAt, rendererFn, HANDLED, NOT_HANDLED } from 'medium-draft';
import { setImportOptions, htmlToStyle } from 'medium-draft/lib/importer';
import { setRenderOptions, styleToHTML } from 'medium-draft/lib/exporter';
import 'medium-draft/lib/index.css';
import filesize from 'filesize';

import {
  newBlockToHTML,
  newEntityToHTML,
  newHTMLtoBlock,
  newHtmlToEntity,
  handleBeforeInput,
  BLOCK_BUTTONS,
  INLINE_BUTTONS
} from './utils';
import { AtomicEmbedComponent, AtomicSeparatorComponent, AtomicBlock } from './blocks/Atomic';
import ImageBlock from './blocks/ImageBlock';
import SeparatorButton from './SeparatorButton';
import EmbedButton from './EmbedButton';
import ImageButton from './ImageButton';

export const emptyText = '<p class="md-block-unstyled"><br/></p>';

class MediumEditor extends React.Component {
  constructor(props) {
    super(props);

    this.importer = setImportOptions({
      htmlToStyle: htmlToStyle,
      htmlToEntity: newHtmlToEntity,
      htmlToBlock: newHTMLtoBlock
    });

    this.exporter = setRenderOptions({
      styleToHTML: styleToHTML,
      blockToHTML: newBlockToHTML,
      entityToHTML: newEntityToHTML
    });

    this.sideButtons = [
      {
        title: 'Image',
        component: (btnProps) => {
          return <ImageButton {...btnProps} addFile={this.addFile} />;
        }
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

    this.blockButtons = BLOCK_BUTTONS();

    this.inlineButtons = INLINE_BUTTONS();

    let editorstate = props.value && typeof props.value === 'string' && this.resetEditor(props.value);
    editorstate = editorstate || (props.value && EditorState.createWithContent(convertFromRaw(props.value))) || props.value;
    this.state = {
      editorState: editorstate || EditorState.createEmpty(),
      editorEnabled: !props.readOnly
    };

    this.editor = null;
    this.files = [];
  }

  componentDidMount() {
    const { autoFocus, initRef } = this.props;
    if (autoFocus) this.focus(true);
    if (initRef) initRef(this);
  }

  componentWillReceiveProps(nextProps) {
    const { readOnly, value } = this.props;
    if (readOnly && nextProps.value !== value) {
      let editorstate = nextProps.value && typeof nextProps.value === 'string' && this.resetEditor(nextProps.value);
      editorstate = editorstate || nextProps.value;
      this.setState({
        editorState: editorstate || EditorState.createEmpty()
      });
    }
  }

  addFile = (file) => {
    const fileData = file;
    fileData.id = `files-${file.name}`;

    // Tell file it's own extension
    fileData.extension = this.fileExtension(file);

    // Tell file it's own readable size
    fileData.sizeReadable = this.fileSizeReadable(file.size);

    // Add preview, either image or file extension
    if (file.type && this.mimeTypeLeft(file.type) === 'image') {
      fileData.preview = {
        type: 'image',
        url: window.URL.createObjectURL(file)
      };
    } else {
      fileData.preview = {
        type: 'file',
        url: window.URL.createObjectURL(file)
      };
    }
    this.files.push(fileData);
  };

  mimeTypeLeft = (mime) => {
    return mime.split('/')[0];
  };

  fileExtension = (file) => {
    const extensionSplit = file.name.split('.');
    if (extensionSplit.length > 1) {
      return extensionSplit[extensionSplit.length - 1];
    }
    return 'none';
  };

  fileSizeReadable = (size) => {
    return filesize(size);
  };

  getEditorState = () => {
    return this.state.editorState;
  };

  setEditorState = (editorState) => {
    this.setState({ editorState: editorState });
  };

  rendererFn = (setEditorState, getEditorState) => {
    const { readOnly } = this.props;
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
            setEditorState: setEditorState,
            getEditorState: getEditorState,
            components: atomicRenderers,
            readOnly: readOnly
          }
        };
      case Block.IMAGE:
        return {
          component: ImageBlock,
          editable: true,
          props: {
            setEditorState: setEditorState,
            getEditorState: getEditorState,
            readOnly: readOnly
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

  isEmpty = () => {
    return this.isEmptyText(this.getHTMLText());
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
    return this.exporter(this.state.editorState.getCurrentContent());
  };

  onChange = (editorState) => {
    const { onChange } = this.props;
    this.setState({ editorState: editorState }, () => {
      if (onChange) onChange(convertToRaw(this.state.editorState.getCurrentContent()));
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
    const { editorState, editorEnabled } = this.state;
    const { placeholder } = this.props;
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
        inlineButtons={this.inlineButtons}
        blockButtons={this.blockButtons}
        rendererFn={this.rendererFn}
      />
    );
  }
}

export default MediumEditor;