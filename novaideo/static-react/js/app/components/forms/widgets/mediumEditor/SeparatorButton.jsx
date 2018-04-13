import React from 'react';
import { AtomicBlockUtils, Entity } from 'draft-js';
import { I18n } from 'react-redux-i18n';

class SeparatorButton extends React.PureComponent {
  onClick = () => {
    const entityKey = Entity.create('separator', 'IMMUTABLE', {});
    this.props.setEditorState(AtomicBlockUtils.insertAtomicBlock(this.props.getEditorState(), entityKey, '-'));
    this.props.close();
  };

  render() {
    return (
      <button
        className="md-sb-button md-sb-img-button"
        type="button"
        title={I18n.t('editor.addSeparator')}
        onClick={this.onClick}
      >
        <i className="mdi-set mdi-all-inclusive" />
      </button>
    );
  }
}

export default SeparatorButton;