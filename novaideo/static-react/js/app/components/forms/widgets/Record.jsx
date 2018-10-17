/* eslint-disable react/no-array-index-key */
import React from 'react';
import { ReactMic } from 'react-mic';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import MicNoneIcon from '@material-ui/icons/MicNone';
import StopIcon from '@material-ui/icons/Stop';
import classNames from 'classnames';
import filesize from 'filesize';
import { I18n } from 'react-redux-i18n';

import StyledButton from '../../styledComponents/Button';
import Dialog from '../../common/Dialog';

const styles = (theme) => {
  return {
    container: {
      padding: '20px 25px',
      width: '100%',
      fontSize: 17,
      lineHeight: 1.5
    },
    titleContainer: {
      fontWeight: 900
    },
    soundWave: {
      width: 'calc(100% + 50px)',
      marginLeft: -25
    },
    button: {
      width: 40,
      height: 40,
      fontSize: 24,
      marginRight: 10,
      boxShadow: '0 1px 4px rgba(128, 128, 128, 0.5)'
    },
    tertiaryBtn: {
      backgroundColor: theme.palette.tertiary.color
    },
    control: {
      display: 'flex',
      justifyContent: 'center',
      marginTop: 10,
      marginBottom: 10
    },
    footer: {
      display: 'flex',
      justifyContent: 'flex-end',
      paddingTop: 5
    }
  };
};

export class DumbRecord extends React.Component {
  state = {
    record: false,
    open: false,
    loading: true,
    file: null
  };

  startRecording = () => {
    this.setState({
      record: true
    });
  };

  stopRecording = () => {
    this.setState({
      record: false,
      loading: true
    });
  };

  onStop = (recordedBlob) => {
    const file = recordedBlob.blob;
    file.name = 'filename';
    file.lastModifiedDate = new Date();
    file.id = 'files-record';
    file.extension = 'webm';
    file.sizeReadable = filesize(file.size);
    file.preview = {
      type: 'audio',
      url: recordedBlob.blobURL
    };
    this.setState({ file: file, loading: false });
  };

  close = () => {
    const { onChange } = this.props;
    const { file } = this.state;
    this.setState(
      {
        open: false
      },
      () => {
        if (file) onChange(file);
      }
    );
  };

  leave = () => {
    this.setState({
      open: false
    });
  };

  open = () => {
    this.setState({
      open: true
    });
  };

  render() {
    const { children, theme, classes } = this.props;
    const { open, record, file } = this.state;
    return [
      <div onClick={this.open}>{children}</div>,
      <Dialog
        directDisplay
        appBar={(
          <div className={classes.titleContainer}>
            <span className={classes.title}>{I18n.t('forms.record')}</span>
          </div>
        )}
        open={open}
        onClose={this.leave}
      >
        <div className={classes.container}>
          <ReactMic
            record={record}
            className={classes.soundWave}
            onStop={this.onStop}
            strokeColor={theme.palette.tertiary.color}
            backgroundColor={theme.palette.primary[500]}
          />
          <div className={classes.control}>
            <Button
              disabled={record}
              onClick={this.startRecording}
              variant="fab"
              color="primary"
              aria-label="add"
              className={classes.button}
            >
              <MicNoneIcon />
            </Button>
            <Button
              disabled={!record}
              onClick={this.stopRecording}
              variant="fab"
              color="secondary"
              aria-label="edit"
              className={classNames(classes.button, classes.tertiaryBtn)}
            >
              <StopIcon />
            </Button>
          </div>
          {file && (
            <audio controls style={{ width: '100%' }}>
              <source src={file.preview.url} type={file.type} />
            </audio>
          )}
          <div className={classes.footer}>
            <StyledButton
              disabled={!file}
              onClick={this.close}
              background={theme.palette.success[500]}
              className={classes.buttonFooter}
            >
              {I18n.t('forms.add')}
            </StyledButton>
          </div>
        </div>
      </Dialog>
    ];
  }
}

export default withStyles(styles, { withTheme: true })(DumbRecord);