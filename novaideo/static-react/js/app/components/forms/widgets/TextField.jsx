/* eslint-disable react/no-array-index-key */
import React from 'react';
import ContentEditable from 'react-contenteditable';

class TextField extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      html: this.props.value || ''
    };
  }

  shouldComponentUpdate() {
    // TODO
    return false;
  }

  onChange = (event) => {
    this.props.onChange(event.target.value);
  };

  render() {
    const { name } = this.props;
    return (
      <ContentEditable
        style={{
          fontVariantLigatures: 'none',
          overflow: 'auto',
          maxHeight: '10rem',
          maxWidth: '100%',
          marginRight: 2,
          position: 'relative',
          boxSizing: 'border-box',
          cursor: 'text',
          outline: 0,
          textAlign: 'left',
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word',
          width: '100%'
        }}
        html={this.state.html} // innerHTML of the editable div
        disabled={false} // use true to disable edition
        onChange={this.onChange} // handle innerHTML change
        name={name}
        role="textbox"
        ariaMultiline="true"
        ariaAutocomplete="list"
        ariaExpanded="false"
        spellCheck="true"
        autoCorrect="off"
        autoComplete="off"
        contentEditable="true"
      />
    );
  }
}

export default TextField;