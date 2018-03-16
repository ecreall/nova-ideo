import React from 'react';
import { ImageSideButton } from 'medium-draft';
import { I18n } from 'react-redux-i18n';
import 'isomorphic-fetch';

class ImageButton extends ImageSideButton {
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