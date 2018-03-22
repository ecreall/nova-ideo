import React from 'react';
import { ImageSideButton, Block, addNewBlock } from 'medium-draft';
import { I18n } from 'react-redux-i18n';
import 'isomorphic-fetch';

class ImageButton extends ImageSideButton {
  onChange(e) {
    // e.preventDefault();
    const file = e.target.files[0];
    if (file.type.indexOf('image/') === 0) {
      // eslint-disable-next-line no-undef
      const src = URL.createObjectURL(file);
      this.props.setEditorState(
        addNewBlock(this.props.getEditorState(), Block.IMAGE, {
          src: src
        })
      );
    }
    this.props.addFile(file);
    this.props.close();
  }

  render() {
    return (
      <button className="md-sb-button md-sb-img-button" type="button" onClick={this.onClick} title={I18n.t('editor.addImage')}>
        <i className="mdi-set mdi-camera" />
        <input
          type="file"
          accept="image/*"
          ref={(input) => {
            this.input = input;
          }}
          onChange={this.onChange}
          style={{ display: 'none' }}
        />
      </button>
    );
  }
}

export default ImageButton;