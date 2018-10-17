import React from 'react';

import EmojiPicker from './EmojiPicker';
import TextEditor from './Editor';

class TextBoxField extends React.Component {
  static defaultProps = {
    style: {},
    autoFocus: false,
    withEmoji: true
  };

  componentDidMount() {
    const { autoFocus, initRef, value } = this.props;
    if (autoFocus) this.editor.focus(value);
    if (initRef) initRef(this);
  }

  shouldComponentUpdate() {
    return false;
  }

  editor = null;

  clear = () => {
    if (this.editor) {
      this.editor.clear(true);
    }
  };

  onChange = (value) => {
    const { onChange } = this.props;
    if (this.editor) {
      onChange(value);
    }
  };

  onSelectEmoji = (emoji) => {
    // when the animation is complete
    setTimeout(() => {
      this.editor.insertText(emoji);
    }, 200);
  };

  getPlainText = () => {
    return this.editor.getPlainText();
  };

  getHTMLText = () => {
    return this.editor.getHTMLText();
  };

  render() {
    const {
      placeholder, value, style, withEmoji, onCtrlEnter, onEnter
    } = this.props;
    return [
      <TextEditor
        key="text-editor"
        ref={(editor) => {
          this.editor = editor;
        }}
        placeholder={placeholder}
        value={value}
        onChange={this.onChange}
        onCtrlEnter={onCtrlEnter}
        onEnter={onEnter}
      />,
      withEmoji ? <EmojiPicker key="emoji-picker" style={style || {}} onSelect={this.onSelectEmoji} /> : null
    ];
  }
}

export default TextBoxField;