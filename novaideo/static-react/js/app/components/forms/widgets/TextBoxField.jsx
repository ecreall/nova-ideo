import React from 'react';

import EmojiPicker from './EmojiPicker';
import TextEditor from './Editor';

class TextBoxField extends React.Component {
  constructor(props) {
    super(props);
    this.editor = null;
  }

  componentDidMount() {
    this.editor.focus(this.props.value);
  }

  shouldComponentUpdate(nextProps) {
    if (!nextProps.value) {
      this.editor.clear();
    }
    return !nextProps.value;
  }

  onChange = (value) => {
    const isEmpty = this.editor.isEmptyText(value);
    const textValue = isEmpty ? '' : value;
    this.props.onChange(textValue);
  };

  onSelectEmoji = (emoji) => {
    this.editor.insertText(emoji);
  };

  render() {
    const { placeholder, value } = this.props;
    return [
      <TextEditor
        ref={(editor) => {
          this.editor = editor;
        }}
        placeholder={placeholder}
        value={value}
        onChange={this.onChange}
        onCtrlEnter={this.props.onCtrlEnter}
      />,
      <EmojiPicker onSelect={this.onSelectEmoji} />
    ];
  }
}

export default TextBoxField;