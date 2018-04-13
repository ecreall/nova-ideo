import React from 'react';
import { withStyles } from 'material-ui/styles';
import { AtomicBlockUtils, Entity } from 'draft-js';
import { I18n } from 'react-redux-i18n';
import Input from 'material-ui/Input';

import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import { DEFAULT_EMBED_DATA } from './constants';

const styles = {
  button: {
    marginLeft: '5px !important'
  },
  root: {
    backgroundColor: 'white',
    border: '1px solid #a0a0a2',
    borderRadius: 4,
    boxShadow: 'inset 0 1px 1px rgba(0,0,0,.075)',
    alignItems: 'center',
    height: 35
  },
  input: {
    padding: '10px 10px 10px',
    fontSize: 15,
    '&::placeholder': {
      color: '#000',
      fontSize: 15,
      fontWeight: 400,
      opacity: '.375'
    }
  }
};

class EmbedButton extends React.Component {
  state = { url: '' };

  form = null;

  handleClickOpen = () => {
    this.form.open();
  };

  handleClose = () => {
    this.form.close();
    this.props.close();
  };

  addEmbedURL = (url) => {
    const entityKey = Entity.create('embed', 'MUTABLE', { url: url, type: 'embed', ...DEFAULT_EMBED_DATA });
    this.props.setEditorState(AtomicBlockUtils.insertAtomicBlock(this.props.getEditorState(), entityKey, 'E'));
  };

  handleSubmit = () => {
    const { url } = this.state;
    this.props.close();
    this.handleClose();
    if (url) this.addEmbedURL(url);
  };

  onUrlChange = (event) => {
    this.setState({ url: event.target.value });
  };

  render() {
    const { theme, classes } = this.props;
    const { url } = this.state;
    return [
      <button
        className="md-sb-button md-sb-img-button"
        type="button"
        title={I18n.t('editor.addEmbed')}
        onClick={this.handleClickOpen}
      >
        <i className="mdi-set mdi-code-tags" />
      </button>,
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        appBar={I18n.t('editor.addEmbedForm')}
        footer={[
          <CancelButton onClick={this.handleClose}>
            {I18n.t('forms.cancel')}
          </CancelButton>,
          <Button disabled={!url} onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.button}>
            {I18n.t('editor.addEmbedFormSubmission')}
          </Button>
        ]}
      >
        <Input
          fullWidth
          disableUnderline
          placeholder={I18n.t('editor.addEmbedFormPlaceholder')}
          onChange={this.onUrlChange}
          classes={{
            root: classes.root,
            input: classes.input
          }}
        />
      </Form>
    ];
  }
}

export default withStyles(styles, { withTheme: true })(EmbedButton);